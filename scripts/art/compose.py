#!/usr/bin/env python3
"""gen_art.py の原本から、ゲームが読む素材を組み立てる（API は呼ばない）。

  python3 scripts/art/compose.py --src <原本の dir> --font <ZenKurenaido-Regular.ttf>

出力は src/assets/{bg,senpai,images}。掲示板の文字は生成に任せると崩れるのでここで描く。
フォントは Zen Kurenaido（SIL OFL）。ビットマップに焼くだけで、フォント自体は repo にも配布物にも入れない。
"""
import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
OUT = Path("src/assets")
INK = (58, 54, 50)


def crop16x9(im):
    im = im.convert("RGB")
    top = (im.height - H) // 2
    return im.crop((0, top, W, top + H))


def dusk(im, s=0.62, gain=0.97):
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255
    out = a * (1 - s) + a * np.array([1.0, 0.70, 0.46], dtype=np.float32) * s
    return Image.fromarray((np.clip(out * gain, 0, 1) * 255).astype(np.uint8))


def font(path, size):
    return ImageFont.truetype(str(path), size)


def squiggles(d, x, y, w, n, gap=30, color=(120, 116, 110)):
    rng = np.random.default_rng(x * 7 + y)
    for i in range(n):
        lw = int(w * rng.uniform(0.6, 1.0))
        d.line([(x, y + i * gap), (x + lw, y + i * gap)], fill=color, width=3)


def paste_sheet(board, sheet, x, y, angle):
    """紙を少し傾けて、影つきで貼る。"""
    rot = sheet.rotate(angle, expand=True, resample=Image.BICUBIC)
    alpha = rot.getchannel("A")
    sh = Image.new("RGBA", (rot.width + 40, rot.height + 40), (0, 0, 0, 0))
    sh.paste((30, 20, 10, 110), (20, 20), alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    board.alpha_composite(sh, (x - 14, y - 12))
    board.alpha_composite(rot, (x, y))
    return rot.size


def pin(board, x, y, color=(186, 62, 52)):
    S = 4
    im = Image.new("RGBA", (40 * S, 40 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([(14 * S, 15 * S), (30 * S, 31 * S)], fill=(20, 15, 10, 90))
    d.ellipse([(10 * S, 10 * S), (26 * S, 26 * S)], fill=color + (255,))
    d.ellipse([(13 * S, 12 * S), (18 * S, 17 * S)], fill=(255, 235, 225, 210))
    board.alpha_composite(im.resize((40, 40), Image.LANCZOS), (x - 18, y - 18))


def hole(board, x, y):
    d = ImageDraw.Draw(board)
    d.ellipse([(x - 4, y - 4), (x + 4, y + 4)], fill=(92, 62, 34, 255))
    d.arc([(x - 6, y - 6), (x + 6, y + 6)], 200, 40, fill=(224, 190, 140, 255), width=2)


def paperize(im, amount=0.016):
    """紙の絵だけ平板に見えるので、ごく薄いむらを掛けて背景の水彩に寄せる。"""
    a = np.asarray(im.convert("RGB"), dtype=np.float32)
    rng = np.random.default_rng(a.shape[0] * a.shape[1])
    n = Image.fromarray((rng.random(a.shape[:2]) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    n = (np.asarray(n, dtype=np.float32) - 127.5) / 6
    out = np.clip(a * (1 + amount * n[..., None]), 0, 255).astype(np.uint8)
    res = Image.fromarray(out).convert("RGBA")
    res.putalpha(im.getchannel("A"))
    return res


def notice(f, title, tint, w=270, h=330, photo=False):
    im = Image.new("RGBA", (w, h), tint + (255,))
    d = ImageDraw.Draw(im)
    d.text((22, 24), title, font=font(f, 24), fill=INK)
    if photo:
        d.rectangle([(26, 70), (w - 26, 230)], fill=(150, 170, 176))
        d.polygon([(26, 230), (110, 140), (170, 200), (210, 160), (w - 26, 230)], fill=(102, 122, 118))
        squiggles(d, 26, 256, w - 52, 2)
    else:
        squiggles(d, 24, 84, w - 48, int((h - 110) / 30))
    return paperize(im)


def sign_paper(f, title, color):
    """本文のとおり: 同じ字・同じ幅の下線・下線の上は空き・いちばん下に小さく締切。"""
    pw, ph = 372, 526
    im = Image.new("RGBA", (pw, ph), color + (255,))
    d = ImageDraw.Draw(im)
    tf = font(f, 46)
    tw = d.textlength(title, font=tf)
    d.text(((pw - tw) / 2, 74), title, font=tf, fill=INK)
    d.line([(46, 322), (pw - 46, 322)], fill=INK, width=4)
    sf = font(f, 25)
    s = "締切 二月七日 十七時"
    d.text(((pw - d.textlength(s, font=sf)) / 2, ph - 62), s, font=sf, fill=INK)
    return paperize(im)


def pencil(board, x, y, length=150):
    """鉛筆と紐。紐は紙のあいだの画鋲から、どちらの紙にも届く長さで下がる。"""
    S = 3
    im = Image.new("RGBA", (120 * S, (length + 280) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = 60 * S
    d.line([(cx, 0), (cx + 2 * S, 90 * S), (cx + 3 * S, 240 * S)], fill=(238, 232, 218, 255), width=3 * S)
    top, bot = 240 * S, (240 + length) * S
    w = 8 * S
    d.rectangle([(cx + 3 * S - w, top), (cx + 3 * S + w, bot)], fill=(64, 92, 78, 255))
    d.rectangle([(cx + 3 * S - w // 3, top), (cx + 3 * S + w // 3, bot)], fill=(82, 112, 96, 255))
    d.polygon([(cx + 3 * S - w, bot), (cx + 3 * S + w, bot), (cx + 3 * S, bot + 26 * S)], fill=(226, 196, 150, 255))
    d.polygon([(cx + 3 * S - w // 3, bot + 17 * S), (cx + 3 * S + w // 3, bot + 17 * S), (cx + 3 * S, bot + 26 * S)], fill=(50, 46, 44, 255))
    im = im.resize((120, length + 280), Image.LANCZOS).rotate(-1.5, resample=Image.BICUBIC, expand=False)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.paste((30, 20, 10, 90), (0, 0), im.getchannel("A"))
    board.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (x - 60 + 7, y + 7))
    board.alpha_composite(im, (x - 60, y))


LX, RX, PY = 716, 1210, 112  # 左右の紙の位置
PINX = (LX + 372 + RX) // 2


def make_board(base, f, mode, notices=True):
    """mode: two（二枚・白）／write_end（右の紙だけ・日焼け）／read_end（左の紙だけ・日焼け）"""
    b = base.convert("RGBA")
    spring = mode != "two"
    if spring:
        items = [("新入生歓迎", (246, 222, 222), False), ("部活動紹介", (222, 238, 222), False), ("吹奏楽部", (222, 232, 246), False)]
    else:
        items = [("生徒会のお知らせ", (246, 244, 236), False), ("インフルエンザ注意", (246, 240, 212), False), ("写真コンクール", (246, 244, 236), True)]
    spots = [(104, 118, -1.2), (396, 150, 0.8), (214, 472, 0.6)]
    for (t, c, ph), (x, y, a) in zip(items if notices else [], spots):
        paste_sheet(b, notice(f, t, c, photo=ph), x, y, a)
        pin(b, x + 135, y + 16, (64, 96, 150))
    white, aged = (250, 249, 244), (238, 226, 192)
    left = ("部誌に書く人", LX, 0.5)
    right = ("読書会で読む人", RX, -0.6)
    def paper(item, color):
        t, x, a = item
        paste_sheet(b, sign_paper(f, t, color), x, PY, a)
        pin(b, x + 34, PY + 22); pin(b, x + 338, PY + 22)
    def gone(item):
        _, x, _ = item
        ghost = Image.new("RGBA", (372, 526), (255, 236, 200, 26))
        b.alpha_composite(ghost, (x, PY))
        hole(b, x + 34, PY + 22); hole(b, x + 338, PY + 22)
    if mode == "two":
        paper(left, white); paper(right, white)
    elif mode == "write_end":
        gone(left); paper(right, aged)
    else:
        gone(right); paper(left, aged)
    pencil(b, PINX, PY + 6)
    pin(b, PINX, PY + 6, (64, 96, 150))
    return b.convert("RGB")


def perspective_coeffs(dst, src):
    A = []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    return np.linalg.solve(np.array(A, dtype=float), np.array(src, dtype=float).reshape(8)).tolist()


def hallway(src):
    """廊下の絵の掲示板は空なので、遠目の紙を透視で貼る（文字は読めない大きさ）。"""
    im = crop16x9(src).convert("RGBA")
    fw, fh = 800, 600
    flat = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    d = ImageDraw.Draw(flat)
    for (x, y, w, h, c) in [(40, 60, 150, 210, (240, 238, 230)), (215, 90, 150, 210, (240, 232, 205)), (120, 320, 150, 210, (236, 236, 228)), (470, 110, 130, 184, (250, 249, 244)), (635, 110, 130, 184, (250, 249, 244))]:
        d.rectangle([(x + 4, y + 4), (x + w + 4, y + h + 4)], fill=(60, 40, 20, 90))
        d.rectangle([(x, y), (x + w, y + h)], fill=c + (255,))
    quad = [(726, 272), (856, 360), (856, 574), (726, 596)]  # 絵の中の掲示板の内側（crop 後の座標）
    c = perspective_coeffs(quad, [(0, 0), (fw, 0), (fw, fh), (0, fh)])
    warped = flat.transform((W, H), Image.PERSPECTIVE, c, Image.BICUBIC)
    im.alpha_composite(warped)
    return im.convert("RGB")


def best_shift(base, other, box, r=14):
    x0, y0, x1, y1 = box
    a = np.asarray(base.convert("L").crop(box), dtype=np.float32)
    o = np.asarray(other.convert("L"), dtype=np.float32)
    best, arg = 1e18, (0, 0)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            e = np.abs(a - o[y0 + dy:y1 + dy, x0 + dx:x1 + dx]).mean()
            if e < best:
                best, arg = e, (dx, dy)
    return arg


def cutout(im):
    """市松もどきの白い背景を、縁から繋がっている所だけ透過にする（白いシャツは輪郭の内側なので残る）。"""
    a = np.asarray(im.convert("RGB"), dtype=np.int16)
    white = (a.min(axis=2) > 232) & ((a.max(axis=2) - a.min(axis=2)) < 16)
    h, w = white.shape
    seen = np.zeros_like(white)
    # 髪の後れ毛に囲まれた白も背景。顔（白目・眼鏡の光）と襟は外す
    sx = w / 1024
    pocket = np.zeros_like(white)
    pocket[:int(470 * sx), :int(375 * sx)] = True
    pocket[:int(470 * sx), int(640 * sx):] = True
    pocket[:int(170 * sx), :] = True
    pocket[int(400 * sx):int(470 * sx), :int(440 * sx)] = True
    seen |= white & pocket
    q = deque((int(y), int(x)) for y, x in zip(*np.nonzero(seen)))
    for x in range(w):
        for y in (0, h - 1):
            if white[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and white[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    mask = Image.fromarray(((~seen) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))
    m = np.asarray(mask, dtype=np.float32) / 255
    alpha = np.clip((m - 0.62) / 0.38, 0, 1)
    out = im.convert("RGBA")
    out.putalpha(Image.fromarray((alpha * 255).astype(np.uint8)))
    return out


def sprite(base, face):
    """頭だけ表情の絵から取り、胸から下は土台のまま（表情を変えても体が動かない）。"""
    if face is base:
        return cutout(base)
    dx, dy = best_shift(base, face, (300, 60, 720, 430))
    shifted = Image.new("RGB", base.size, (255, 255, 255))
    shifted.paste(face, (-dx, -dy))
    ramp = np.zeros((base.height, base.width), dtype=np.float32)
    ramp[:440, :] = 1
    ramp[440:490, :] = np.linspace(1, 0, 50)[:, None]
    A, B = np.asarray(shifted, dtype=np.float32), np.asarray(base, dtype=np.float32)
    mixed = A * ramp[..., None] + B * (1 - ramp[..., None])
    print("  shift", dx, dy)
    return cutout(Image.fromarray(mixed.astype(np.uint8)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); ap.add_argument("--font", required=True)
    a = ap.parse_args(); src = Path(a.src); f = Path(a.font)
    for d in ("bg", "senpai", "images"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    load = lambda n: Image.open(src / f"{n}.png").convert("RGB")
    save = lambda im, p: im.save(OUT / p, quality=90, subsampling=0)
    hall = hallway(load("bg_hallway")); club = crop16x9(load("bg_clubroom")); base = crop16x9(load("board_base"))
    save(hall, "bg/hallway.jpg"); save(dusk(hall), "bg/hallway_dusk.jpg")
    save(club, "bg/clubroom.jpg"); save(dusk(club, 0.5), "bg/clubroom_dusk.jpg")
    save(crop16x9(load("bg_bedroom")), "bg/bedroom.jpg")
    two = make_board(base, f, "two")
    save(two, "bg/board_two.jpg"); save(dusk(two), "bg/board_two_dusk.jpg")
    save(make_board(base, f, "write_end"), "bg/board_write_end.jpg")
    save(make_board(base, f, "read_end"), "bg/board_read_end.jpg")
    menu = dusk(make_board(base, f, "two", notices=False)).convert("RGBA")  # メニューの枠と重なるので貼り紙は外す
    d = ImageDraw.Draw(menu)
    d.text((112, 150), "二枚の紙", font=font(f, 120), fill=(46, 34, 26, 255))  # 題は仮
    save(menu.convert("RGB"), "images/main-menu.jpg")
    # アプリのアイコン（favicon と PWA は npm run icon がここから作る）
    two.crop((880, 80, 1520, 720)).resize((1024, 1024), Image.LANCZOS).save("public/icon.png")
    b = load("senpai_base")
    for name, face in (("neutral", b), ("smile", load("senpai_smile")), ("concern", load("senpai_concern")), ("grin", load("senpai_grin"))):
        print(name)
        sprite(b, face).resize((696, 1044), Image.LANCZOS).save(OUT / f"senpai/{name}.png", optimize=True)


if __name__ == "__main__":
    main()
