# --- scripts/ocr_infer.py (임시버전) ---
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
from pdf2image import convert_from_path
import easyocr

# 파일 상단에 추가


def _to_py(obj):
    if isinstance(obj, np.generic):  # np.int32, np.float32 등
        return obj.item()
    if isinstance(obj, np.ndarray):  # numpy array -> list
        return obj.tolist()
    return obj


DOC_DIR = Path("data/synth/docs")
OUT_DIR = Path("data/ocr")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run_ocr_on_images(images: List, reader: easyocr.Reader) -> Dict[str, Any]:
    pages = []
    for page_idx, img in enumerate(images, start=1):
        arr = np.array(img)
        items = reader.readtext(arr)  # [ [bbox, text, conf], ... ]
        boxes = []
        for b, t, c in items:
            # bbox는 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] 형태
            box_py = [[int(pt[0]), int(pt[1])] for pt in b]
            boxes.append({"text": str(t), "conf": float(c), "box": box_py})
        pages.append({"page": int(page_idx), "boxes": boxes})
    return {"pages": pages}


def main():
    reader = easyocr.Reader(["ko", "en"], gpu=False)
    for pdf in sorted(DOC_DIR.glob("*.pdf")):
        images = convert_from_path(str(pdf), dpi=200)
        out = run_ocr_on_images(images, reader)
        out["pdf_path"] = str(pdf)
        (OUT_DIR / (pdf.stem + ".json")).write_text(
            json.dumps(out, ensure_ascii=False, indent=2, default=_to_py),
            encoding="utf-8",
        )
        print("wrote", OUT_DIR / (pdf.stem + ".json"))


if __name__ == "__main__":
    main()
