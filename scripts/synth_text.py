from pathlib import Path
import json
import random

OUT = Path("data/synth/text.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)


def fake_rrn():
    front = "".join(str(random.randint(0, 9)) for _ in range(6))
    back = "".join(str(random.randint(0, 9)) for _ in range(7))
    return f"{front}-{back}"


samples = []
for i in range(1000):
    rrn = fake_rrn()
    txt = f"홍길동의 주민등록번호는 {rrn} 입니다."
    start = txt.find(rrn)
    spans = [{"type": "RRN", "start": start, "end": start + len(rrn), "value": rrn}]
    samples.append({"text": txt, "spans": spans})

with OUT.open("w", encoding="utf-8") as f:
    for s in samples:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

print("wrote", OUT, "lines:", len(samples))
