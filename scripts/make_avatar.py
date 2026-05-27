"""자기소개 페이지용 프로필 아바타를 코드로 생성한다.

대화 맥락(바이브코딩 중인 개발자)을 반영해 헤드폰 + 안경 + 후드티 차림의
플랫 디자인 아바타를 다크모드 배경 위에 그린다. AI 이미지 생성 없이 Pillow
도형만으로 그리므로 재현 가능하다.

실행: python3 scripts/make_avatar.py  ->  assets/profile.png
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

RES = 1024          # supersampling 해상도 (최종은 512로 축소)
OUT = 512
CX = RES // 2

# 팔레트
BG_TOP = (42, 45, 74)
BG_BOT = (18, 20, 38)
SKIN = (242, 200, 165)
SKIN_SHADE = (226, 178, 142)
HAIR = (44, 44, 54)
HOODIE = (61, 90, 128)
HOODIE_DARK = (45, 67, 96)
RED = (255, 75, 75)        # Streamlit 레드 (헤드폰 포인트)
RED_DARK = (196, 52, 52)
FRAME = (28, 30, 38)


def gradient_circle():
    """세로 그라데이션을 원형으로 마스킹한 배경."""
    grad = Image.new("RGB", (1, RES))
    for y in range(RES):
        t = y / RES
        grad.putpixel(
            (0, y),
            tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)),
        )
    grad = grad.resize((RES, RES)).convert("RGBA")

    # 머리 뒤 은은한 레드 글로우
    glow = Image.new("RGBA", (RES, RES), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((CX - 320, 120, CX + 320, 760), fill=(*RED, 28))
    grad = Image.alpha_composite(grad, glow)
    return grad


def draw_character(img):
    d = ImageDraw.Draw(img)

    # 후드(머리 뒤) + 어깨
    d.rounded_rectangle((CX - 320, 800, CX + 320, RES + 60), radius=160,
                        fill=HOODIE_DARK)
    d.rounded_rectangle((CX - 300, 840, CX + 300, RES + 60), radius=150,
                        fill=HOODIE)
    # 후드 끈 (레드)
    d.line((CX - 40, 870, CX - 40, 980), fill=RED, width=14)
    d.line((CX + 40, 870, CX + 40, 980), fill=RED, width=14)
    d.ellipse((CX - 50, 975, CX - 30, 1000), fill=RED)
    d.ellipse((CX + 30, 975, CX + 50, 1000), fill=RED)

    # 목
    d.rounded_rectangle((CX - 45, 600, CX + 45, 730), radius=30, fill=SKIN_SHADE)

    # 귀
    d.ellipse((CX - 192, 410, CX - 120, 500), fill=SKIN)
    d.ellipse((CX + 120, 410, CX + 192, 500), fill=SKIN)

    # 머리카락(뒤) → 얼굴(앞) 순서로 그려 헤어라인 표현
    d.ellipse((CX - 192, 210, CX + 192, 600), fill=HAIR)
    d.ellipse((CX - 178, 250, CX + 178, 630), fill=SKIN)

    # 안경
    lens_y0, lens_y1 = 408, 478
    d.rounded_rectangle((CX - 148, lens_y0, CX - 40, lens_y1), radius=20,
                        fill=(150, 200, 210, 60), outline=FRAME, width=11)
    d.rounded_rectangle((CX + 40, lens_y0, CX + 148, lens_y1), radius=20,
                        fill=(150, 200, 210, 60), outline=FRAME, width=11)
    d.line((CX - 40, lens_y0 + 14, CX + 40, lens_y0 + 14), fill=FRAME, width=11)
    d.line((CX - 148, lens_y0 + 16, CX - 178, lens_y0 + 6), fill=FRAME, width=10)
    d.line((CX + 148, lens_y0 + 16, CX + 178, lens_y0 + 6), fill=FRAME, width=10)

    # 눈썹
    d.line((CX - 140, 392, CX - 56, 386), fill=HAIR, width=12)
    d.line((CX + 56, 386, CX + 140, 392), fill=HAIR, width=12)

    # 눈
    d.ellipse((CX - 104, 432, CX - 80, 456), fill=(40, 40, 48))
    d.ellipse((CX + 80, 432, CX + 104, 456), fill=(40, 40, 48))

    # 코
    d.line((CX, 480, CX - 14, 520), fill=SKIN_SHADE, width=9)
    d.line((CX - 14, 520, CX + 10, 522), fill=SKIN_SHADE, width=9)

    # 입 (살짝 미소)
    d.arc((CX - 46, 522, CX + 46, 582), start=20, end=160, fill=(150, 90, 80),
          width=10)

    # 헤드폰: 밴드 + 이어컵 (레드 포인트)
    d.arc((CX - 215, 200, CX + 215, 640), start=183, end=357, fill=FRAME,
          width=46)
    d.arc((CX - 215, 200, CX + 215, 640), start=185, end=355, fill=RED,
          width=30)
    for sx in (-1, 1):
        ex = CX + sx * 156
        d.rounded_rectangle((ex - 52, 400, ex + 52, 520), radius=34, fill=RED)
        d.rounded_rectangle((ex - 30, 424, ex + 30, 496), radius=22,
                            fill=RED_DARK)


def main():
    img = gradient_circle()
    draw_character(img)

    # 원형 클리핑
    mask = Image.new("L", (RES, RES), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, RES - 1, RES - 1), fill=255)
    r, g, b, a = img.split()
    img.putalpha(ImageChops.multiply(a, mask))

    img = img.resize((OUT, OUT), Image.LANCZOS)

    out = Path(__file__).resolve().parent.parent / "assets" / "profile.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
