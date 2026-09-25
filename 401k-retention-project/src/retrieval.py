"""BM25 retrieval over synthetic plan documents."""

import re
from pathlib import Path

from rank_bm25 import BM25Okapi

HEADING_RE = re.compile(r"^[A-Z0-9 ()&/,.'%$-]{4,}$")
TOKEN_RE = re.compile(r"[a-z0-9]+")
MIN_SCORE = 1.0

STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "do", "does", "for", "from", "how", "i", "in", "into", "is", "it",
    "me", "my", "of", "on", "or", "our", "the", "this", "to", "was",
    "we", "what", "when", "where", "which", "who", "will", "with",
    "you", "your",
})


def _normalize(token):
    """Crude singularization so IRA matches IRAs, rollovers matches rollover."""
    if len(token) > 3 and token.endswith("s"):
        return token[:-1]
    return token


def _tokenize(text):
    return [
        _normalize(token)
        for token in TOKEN_RE.findall(text.lower())
        if token not in STOPWORDS
    ]


def _chunk_document(doc_id, text):
    """Split one SPD into section chunks with stable IDs."""
    chunks = []
    heading = None
    body_lines = []

    def flush():
        content = "\n".join(body_lines).strip()
        if heading is None and not content:
            return
        if heading is None or heading == "SUMMARY PLAN DESCRIPTION":
            return
        title = heading
        chunks.append({
            "chunk_id": doc_id + "-%03d" % (len(chunks) + 1),
            "doc_id": doc_id,
            "heading": title,
            "text": (title + "\n" + content).strip(),
        })

    for line in text.splitlines():
        stripped = line.strip()
        if stripped and HEADING_RE.match(stripped):
            flush()
            heading = stripped
            body_lines = []
        elif stripped:
            body_lines.append(stripped)
    flush()
    return chunks


class SpdRetriever:
    """BM25 search over the chunked SPD documents."""

    def __init__(self, data_dir="data/spd"):
        self.chunks = []
        for path in sorted(Path(data_dir).glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            self.chunks.extend(_chunk_document(path.stem, text))
        if not self.chunks:
            raise FileNotFoundError("No SPD chunks loaded from " + data_dir)
        self._bm25 = BM25Okapi([_tokenize(c["text"]) for c in self.chunks])

    def retrieve(self, query, k=3):
        """Return top-k chunks (with scores); empty means nothing matched."""
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(
            zip(scores, self.chunks), key=lambda pair: pair[0], reverse=True
        )
        results = []
        for score, chunk in ranked[:k]:
            if score < MIN_SCORE:
                continue
            results.append({**chunk, "score": round(float(score), 3)})
        return results
