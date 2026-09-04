#!/usr/bin/env python3
"""OGP 画像 og.png（1200×630）を生成する。

  python3 tools/make-og.py            # リポジトリ直下に og.png を書く

依存: Pillow と、macOS 標準のヒラギノ明朝 ProN。題や副題を変えたら実行し直す。
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
CANVAS, INK, BODY, MUTED = "#F5F3ED", "#26251E", "#4C4A42", "#827E74"
SAND, PEACH, DECO, SAND_INK = "#D9C68F", "#DDB49C", "#C8A98E", "#7A5C0E"
FONT = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"   # index 0 = W3, 2 = W6

def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=2 if bold else 0)

def tracked(draw, xy, text, f, fill, tracking=0):
    """字間を足しながら一文字ずつ描く（PIL に字送りの指定がないため）"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking
    return x

def main(out):
    im = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(im)

    # 右下: 段状のジッグラト（icons/icon.svg と同じ印）
    cx, base = 1010, 548
    for i, (w, col) in enumerate([(300, DECO), (220, PEACH), (140, SAND)]):
        y1 = base - 46 * i
        d.rectangle([cx - w // 2, y1 - 46, cx + w // 2, y1], fill=col)
    d.rectangle([cx - 12, base - 138 - 26, cx + 12, base - 138], fill=SAND_INK)

    # 上: 小見出し
    tracked(d, (96, 104), "古代オリエント博物館を楽しむための読み物", font(28), SAND_INK, tracking=6)
    d.rectangle([96, 150, 176, 152], fill=SAND_INK)

    # 題
    tracked(d, (92, 188), "古代オリエントを、", font(96, True), INK, tracking=2)
    tracked(d, (92, 300), "立体で読む。", font(96, True), INK, tracking=2)

    # 副題
    tracked(d, (96, 446), "時間・空間・文明・神・言語・建築", font(38), BODY, tracking=3)

    # 下: URL と細線
    d.rectangle([96, 548, 560, 549], fill="#D3CEC4")
    d.text((96, 566), "ancient-orient-guide.vercel.app", font=font(24), fill=MUTED)

    im.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out) // 1024, "KB")

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "og.png"))
