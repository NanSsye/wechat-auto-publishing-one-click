#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

BAD_SOURCES = {'local_generated_cover', 'ai_generated', 'text_card'}

def fit_cover(img):
    target = (900, 383)
    src = img.convert('RGB')
    sw, sh = src.size
    tw, th = target
    src_ratio = sw / sh
    target_ratio = tw / th
    if src_ratio > target_ratio:
        new_h = sh
        new_w = int(sh * target_ratio)
        left = (sw - new_w) // 2
        box = (left, 0, left + new_w, sh)
    else:
        new_w = sw
        new_h = int(sw / target_ratio)
        top = (sh - new_h) // 2
        box = (0, top, sw, top + new_h)
    return src.crop(box).resize(target, Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--fallback', required=False)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    picks = [args.input] + ([args.fallback] if args.fallback else [])
    chosen = None
    for p in picks:
        if p and Path(p).exists() and Path(p).stat().st_size > 0:
            chosen = p
            break
    if not chosen:
        raise SystemExit('no real source image found for cover')
    out = fit_cover(Image.open(chosen))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output, format='PNG')
    print(args.output)

if __name__ == '__main__':
    main()
