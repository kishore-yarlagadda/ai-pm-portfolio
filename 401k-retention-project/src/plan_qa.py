"""Retrieval-grounded plan-document Q&A with citations and escalation."""

import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from llm_client import LLMClient
from retrieval import SpdRetriever

ADVICE_BAIT = (
    "should i", "what should", "recommend", "advice",
    "best option", "worth it",
)


class CitedAnswer(BaseModel):
    """The only shape the LLM may return for plan questions."""

    answer: str
    chunk_ids: List[str]
    escalate: bool


class PlanDocQA:
    """Answer plan-document questions from retrieved SPD sections."""

    def __init__(self, retriever=None, llm_client=None):
        self.retriever = retriever or SpdRetriever()
        self.llm_client = llm_client or LLMClient()

    def answer(self, question: str) -> Dict[str, Any]:
        text = question.lower()
        if any(trigger in text for trigger in ADVICE_BAIT):
            return self._escalate("Advice request, not a document question.")
        chunks = self.retriever.retrieve(question)
        if not chunks:
            return self._escalate("No matching plan-document section.")
        drafted = None
        if self.llm_client.is_live_available:
            drafted = self._draft_with_llm(question, chunks)
        if drafted is None or not self._citations_valid(drafted, chunks):
            return self._deterministic_answer(chunks)
        cited = ", ".join("[%s]" % cid for cid in drafted.chunk_ids)
        return {
            "action": "ANSWER_PLAN_QUESTION",
            "reason": "Answered from plan documents with citations.",
            "message": drafted.answer + "\n\nSource: " + cited,
            "citations": drafted.chunk_ids,
            "is_active": True,
        }

    def _draft_with_llm(self, question, chunks) -> Optional[CitedAnswer]:
        context_block = "\n\n".join(
            "[%s]\n%s" % (c["chunk_id"], c["text"]) for c in chunks
        )
        system_prompt = (
            "You answer 401(k) plan questions using only the supplied "
            "plan-document excerpts. Reply with JSON only: "
            '{"answer": str, "chunk_ids": [str], "escalate": bool}. '
            "Cite every factual claim with its chunk ID in brackets, for "
            "example [harbor-manufacturing-spd-006]. If the excerpts do not "
            "answer the question, set escalate to true and leave answer "
            "empty. Never give investment, tax, or legal advice."
        )
        try:
            raw = self.llm_client.generate_response(
                system_prompt=system_prompt,
                user_message="Excerpts:\n" + context_block + "\n\nQuestion: " + question,
            )
            return CitedAnswer(**json.loads(raw))
        except Exception:
            return None

    @staticmethod
    def _citations_valid(drafted: CitedAnswer, chunks) -> bool:
        if drafted.escalate or not drafted.chunk_ids:
            return False
        valid_ids = {c["chunk_id"] for c in chunks}
        return all(cid in valid_ids for cid in drafted.chunk_ids) and any(
            cid in drafted.answer for cid in drafted.chunk_ids
        )

    @staticmethod
    def _deterministic_answer(chunks) -> Dict[str, Any]:
        top = chunks[0]
        message = (
            "From the plan documents, section "
            + top["heading"]
            + " ["
            + top["chunk_id"]
            + "]:\n\n"
            + top["text"]
            + "\n\nSource: ["
            + top["chunk_id"]
            + "]"
        )
        extra = [c["chunk_id"] for c in chunks[1:]]
        if extra:
            message += "\n\nAlso relevant: " + ", ".join(
                "[%s]" % cid for cid in extra
            )
        return {
            "action": "ANSWER_PLAN_QUESTION",
            "reason": "Deterministic extractive answer with citation.",
            "message": message,
            "citations": [c["chunk_id"] for c in chunks],
            "is_active": True,
        }

    @staticmethod
    def _escalate(reason: str) -> Dict[str, Any]:
        return {
            "action": "ESCALATE_PLAN_QUESTION",
            "reason": reason,
            "message": (
                "I could not verify an answer in the plan documents, so "
                "I am routing this to a retirement specialist instead of "
                "guessing. No transaction has been executed."
            ),
            "is_active": False,
            "human_review_required": True,
        }
