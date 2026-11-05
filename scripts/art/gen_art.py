#!/usr/bin/env python3
"""仮絵を OpenAI の画像 API で作る（P3）。生成物の原本は --out に置く（repo には載せない）。

  python3 scripts/art/gen_art.py --out <dir> [key ...]     # key 無しは全部。原本があれば作らない
  python3 scripts/art/gen_art.py --out <dir> --face        # 表情 3 つ（senpai_base から顔だけ edits）

鍵は環境変数 OPENAI_API_KEY。1 本目は生成の絵のまま出して、作品ページに開示する。
"""
import argparse, base64, concurrent.futures as cf, json, os, sys, urllib.request, uuid
from pathlib import Path

MODEL = os.environ.get("ERABU_ART_MODEL", "gpt-image-2")
BG_STYLE = (
    "Hand-drawn Japanese visual novel background art. Soft watercolor wash over delicate clean pencil lines, "
    "muted warm palette of ivory, pale wood and faded teal, quiet melancholic slice-of-life mood, natural perspective. "
    "The main subject sits in the upper two thirds of the frame. No people. "
    "Absolutely no text, no letters, no numbers, no writing, no signage, no logo, no watermark."
)
SP_STYLE = (
    "Character sprite for a wholesome all-ages Japanese visual novel. Soft watercolor anime style with clean pencil line art, "
    "muted natural colors matching a quiet slice-of-life story. Fully transparent background, no floor, no cast shadow. "
    "No text, no logo, no watermark."
)
ASSETS = {
    "bg_hallway": ("1920x1088", "An empty Japanese high school corridor on a quiet winter afternoon. Long polished floor receding into the distance, "
        "large windows along the right wall letting in pale winter light, classroom sliding doors along the left wall. "
        "On the left wall in the middle distance hangs a large cork bulletin board. Camera at eye level. " + BG_STYLE),
    "bg_clubroom": ("1920x1088", "A small Japanese high school literature club room that used to be a book storage room. One window with winter afternoon light. "
        "Two rows of grey steel shelves filled with thin bound magazines with faded spines and plain notebooks. "
        "Five mismatched chairs around a worn wooden table, an electric kettle and two ceramic mugs on the table, one small old electric heater on the floor. "
        "Cozy and dusty. " + BG_STYLE),
    "bg_bedroom": ("1920x1088", "A small Japanese teenager's bedroom late at night. A desk by a curtained window, a laptop with a softly glowing blank white screen, "
        "a small desk lamp, stacks of paperback books on the shelf and floor, a single bed at the edge of the frame. "
        "Deep blue shadows with warm lamplight. " + BG_STYLE),
    "board_base": ("1920x1088", "Straight-on frontal close-up of a cork bulletin board on a school corridor wall, filling the whole frame, soft side light, "
        "worn wooden frame visible at the very top and bottom edges. The cork surface is completely empty, a few loose pushpin holes. "
        "No paper on it. " + BG_STYLE.replace("The main subject sits in the upper two thirds of the frame. ", "")),
    "senpai_base": ("1024x1536", "An original character: a third-year Japanese high school student, the president of a small literature club. "
        "Ordinary slim build. Chin-length dark hair in a neat bob with a few loose strands, thin round glasses, calm intelligent eyes, "
        "relaxed neutral expression with mouth closed. Modest school uniform: dark navy blazer over a grey cardigan, white shirt buttoned to the top, "
        "simple ribbon tie, long pleated skirt below the knees. Standing relaxed, facing the viewer at a slight angle, both arms lowered, "
        "holding a worn paperback in one hand at her side. Framing from mid-thigh up, centered, head close to the top of the image with a small margin. " + SP_STYLE),
}
FACES = {
    "senpai_smile": "A warm gentle smile with soft eyes, mouth lightly curved.",
    "senpai_concern": "A troubled, quietly sad expression: eyebrows slightly raised at the inner ends, eyes looking a little down, mouth a small closed line.",
    "senpai_grin": "A teasing, mischievous smirk: one corner of the mouth raised, eyes narrowed with amusement.",
}


def api(req):
    with urllib.request.urlopen(req, timeout=290) as r:
        return json.load(r)


def save(res, out):
    Path(out).write_bytes(base64.b64decode(res["data"][0]["b64_json"]))
    u = res.get("usage", {})
    print(f"{Path(out).name} OK usage={u.get('input_tokens')}/{u.get('output_tokens')}", flush=True)


def generate(key, size, prompt, out):
    body = {"model": MODEL, "prompt": prompt, "size": size, "quality": "medium", "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"})
    save(api(req), out)


def edit(prompt, base, out):
    boundary = uuid.uuid4().hex
    parts = []
    for k, v in {"model": MODEL, "prompt": prompt, "size": "1024x1536", "quality": "medium", "n": "1"}.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="image[]"; filename="base.png"\r\nContent-Type: image/png\r\n\r\n'.encode() + Path(base).read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts),
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    save(api(req), out)


def run(jobs):
    bad = 0
    with cf.ThreadPoolExecutor(5) as ex:
        for name, fut in [(n, ex.submit(f, *a)) for n, f, a in jobs]:
            try:
                fut.result()
            except urllib.error.HTTPError as e:
                print(name, "HTTP", e.code, e.read()[:300].decode(errors="replace"), flush=True); bad += 1
            except Exception as e:
                print(name, "ERR", repr(e)[:300], flush=True); bad += 1
    return bad


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--face", action="store_true"); ap.add_argument("keys", nargs="*")
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    jobs = []
    if a.face:
        for k, expr in FACES.items():
            p = out / f"{k}.png"
            if not p.exists():
                jobs.append((k, edit, (f"Keep this exact same character, same art style, same hair, same glasses, same clothes, same pose, same framing, same position in the image, same transparent background. Change only the facial expression: {expr}", out / "senpai_base.png", p)))
    else:
        for k in a.keys or ASSETS:
            p = out / f"{k}.png"
            if not p.exists():
                size, prompt = ASSETS[k]
                jobs.append((k, generate, (k, size, prompt, p)))
    print("jobs", [j[0] for j in jobs], "model", MODEL, flush=True)
    sys.exit(1 if run(jobs) else 0)


if __name__ == "__main__":
    main()
