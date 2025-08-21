from __future__ import annotations

import random
import string
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT_DIR = Path("data/synth/docs")
LBL_DIR = Path("data/synth/labels")
OUT_DIR.mkdir(parents=True, exist_ok=True)
LBL_DIR.mkdir(parents=True, exist_ok=True)


def rand_digits(n: int) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(n))


def fake_rrn() -> str:
    # 한국 주민번호 형식 흉내(가짜)
    return f"{rand_digits(6)}-{rand_digits(7)}"


def fake_card() -> str:
    # 16자리 카드번호 대시 포함
    parts = [rand_digits(4) for _ in range(4)]
    return "-".join(parts)


def fake_phone() -> str:
    return f"010-{rand_digits(4)}-{rand_digits(4)}"


def fake_email() -> str:
    user = "".join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(["example.com", "mail.com", "test.kr"])
    return f"{user}@{domain}"


@dataclass
class Field:
    key: str
    value: str


def make_doc(doc_id: int) -> Dict[str, Any]:
    pdf_path = OUT_DIR / f"doc_{doc_id:04d}.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    # 내용 (간단한 거래/신원 양식 느낌)
    fields: List[Field] = [
        Field("이름", random.choice(["김철수", "박영희", "이민수", "장서윤"])),
        Field("주민등록번호", fake_rrn()),
        Field("전화번호", fake_phone()),
        Field("이메일", fake_email()),
        Field("카드번호", fake_card()),
        Field("결제금액", f"{random.randint(12000, 490000):,}원"),
        Field("거래일시", f"2025-08-{random.randint(1,28):02d} 14:{random.randint(10,59):02d}"),
        Field("주문번호", f"ORD-{rand_digits(10)}"),
    ]

    y = height - 80
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "거래 명세서 / 개인정보 포함 예시 (합성)")
    y -= 30
    c.setFont("Helvetica", 12)

    gt: List[Dict[str, Any]] = []
    for f in fields:
        line = f"{f.key}: {f.value}"
        c.drawString(60, y, line)
        # 대략적 bbox (단순히 텍스트 시작 x,y와 폭 추정)
        gt.append(
            {
                "key": f.key,
                "value": f.value,
                "y": y,
                "x": 60,
                "w_est": 8 * len(line),  # 대충 1글자 8px로 가정
                "h_est": 16,
                "page": 1,
                "type": f.key,
            }
        )
        y -= 22

    c.showPage()
    c.save()

    # 라벨 JSON 저장 (텍스트/타입/대략적 위치)
    label = {
        "doc_id": f"doc_{doc_id:04d}",
        "pdf_path": str(pdf_path),
        "fields": gt,
    }
    (LBL_DIR / f"doc_{doc_id:04d}.json").write_text(
        __import__("json").dumps(label, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return label


def main(n_docs: int = 20) -> None:
    random.seed(42)
    for i in range(n_docs):
        make_doc(i)
    print(f"wrote {n_docs} PDFs into {OUT_DIR}")


if __name__ == "__main__":
    main()
