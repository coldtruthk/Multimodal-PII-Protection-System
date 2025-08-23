from pathlib import Path
import json
from typing import List, Dict, Any
import sys

# 프로젝트 루트에서 실행되지 않을 때를 대비해 루트 추가
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pii.rules import detect, apply_mask  # noqa: E402

OCR_DIR = Path("data/ocr")
OUT_DIR = Path("data/pii")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def concat_text(pages: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for p in pages or []:
        for box in p.get("boxes", []) or []:
            txt = (box.get("text") or "").strip()
            if txt:
                lines.append(txt)
    return "\n".join(lines)


def main() -> None:
    files = sorted(OCR_DIR.glob("*.json"))
    if not files:
        print("[pii] no OCR json files found under data/ocr")
    for jf in files:
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
            text = concat_text(data.get("pages", []))
            spans = detect(text)
            masked = apply_mask(text, spans)
            out = {
                "pdf_path": data.get("pdf_path"),
                "text": text,
                "spans": spans,
                "masked": masked,
            }
            (OUT_DIR / jf.name).write_text(
                json.dumps(out, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print("[pii] wrote", OUT_DIR / jf.name, "spans:", len(spans))
        except Exception as e:
            # 에러가 있어도 전체 파이프라인이 멈추지 않게 로그만 남기고 다음 파일로
            print(f"[pii][ERROR] {jf}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
