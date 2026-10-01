from pathlib import Path

BASE = Path(__file__).resolve().parent


# ── 문서 처리 ──
DOC_PATH = BASE / "docs" / "busan_guide.pdf"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
# ── 임베딩 · 저장소 ──
EMBED_MODEL = "text-embedding-3-small"
INDEX_PATH = "faiss_index"
# ── 검색 ──
TOP_K = 5
MIN_SCORE = -0.01
SEARCH_TYPE = "similarity"
# ── 생성 ──
LLM_MODEL = "gpt-4o-mini"
TEMPERATURE = 0
PROMPT_VER = "v3"


# ── 메시지 ──
MSG_NO_DOC = "가이드에서 관련 내용을 찾지 못했습니다."
MSG_ERROR = "일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
