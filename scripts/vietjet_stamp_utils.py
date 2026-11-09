# -*- coding: utf-8 -*-
"""
vietjet_stamp_utils.py
Tạo con dấu đỏ (rubber stamp) và chữ ký mực xanh thực tế cho bộ hồ sơ Vietjet
tương thích hoàn hảo hệ thống Linux và font tiếng Việt.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def create_circular_stamp(outer_text, center_text, sub_center_text="", size=380):
    """
    Tạo con dấu tròn màu đỏ mô phỏng con dấu doanh nghiệp / ngân hàng
    """
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    red_color = (205, 28, 38, 230)
    center = size / 2.0
    radius = size / 2.0 - 15

    # Vòng tròn ngoài và trong
    draw.ellipse([15, 15, size - 15, size - 15], outline=red_color, width=5)
    draw.ellipse([26, 26, size - 26, size - 26], outline=red_color, width=2)

    font_curve = get_font(FONT_SANS_BOLD, 20)
    font_center = get_font(FONT_SERIF_BOLD, 22)
    font_sub = get_font(FONT_SANS_BOLD, 16)
    font_star = get_font(FONT_SERIF_BOLD, 26)

    # Uốn lượn ký tự cung tròn trên
    chars = list(outer_text)
    n_chars = len(chars)
    if n_chars > 0:
        total_angle = min(220, n_chars * 11)
        start_angle = -90 - total_angle / 2.0
        step_angle = total_angle / max(1, n_chars - 1)
        r_text = radius - 24

        for i, char in enumerate(chars):
            ang_deg = start_angle + i * step_angle
            ang_rad = math.radians(ang_deg)
            cx = center + r_text * math.cos(ang_rad)
            cy = center + r_text * math.sin(ang_rad)

            char_img = Image.new("RGBA", (44, 44), (255, 255, 255, 0))
            cdraw = ImageDraw.Draw(char_img)
            bbox = cdraw.textbbox((0, 0), char, font=font_curve)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            cdraw.text(((44 - w) / 2.0, (44 - h) / 2.0), char, font=font_curve, fill=red_color)

            rot_deg = -(ang_deg + 90)
            rotated_char = char_img.rotate(rot_deg, resample=Image.BICUBIC, expand=True)
            rw, rh = rotated_char.size
            img.paste(rotated_char, (int(cx - rw / 2.0), int(cy - rh / 2.0)), rotated_char)

    # Ngôi sao trung tâm
    star = "★"
    s_box = draw.textbbox((0, 0), star, font=font_star)
    sw = s_box[2] - s_box[0]
    draw.text((center - sw / 2.0, center - 65), star, font=font_star, fill=red_color)

    # Chữ ở tâm (Tên công ty)
    c_box = draw.textbbox((0, 0), center_text, font=font_center)
    cw = c_box[2] - c_box[0]
    draw.text((center - cw / 2.0, center - 16), center_text, font=font_center, fill=red_color)

    # Chữ phụ (Mã số thuế / chi nhánh)
    if sub_center_text:
        sub_box = draw.textbbox((0, 0), sub_center_text, font=font_sub)
        subw = sub_box[2] - sub_box[0]
        draw.text((center - subw / 2.0, center + 22), sub_center_text, font=font_sub, fill=red_color)

    # Vòng tròn bảo vệ tâm
    draw.ellipse([center - 95, center - 95, center + 95, center + 95], outline=red_color, width=1)

    return img


def create_signature_image(name="Nguyễn Thị Phương Thảo", seed=42, width=240, height=90):
    """
    Tạo chữ ký tay màu mực xanh bút bi thực tế
    """
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    blue_color = (0, 48, 145, 235)

    rng = random.Random(seed)
    # Tạo đường lượn chữ ký
    pts = [(20, 50)]
    for i in range(1, 10):
        x = 20 + i * 20 + rng.randint(-4, 4)
        y = 20 + (i % 2) * 35 + rng.randint(-6, 6)
        pts.append((x, y))
    pts.append((220, 65))
    pts.append((140, 75))
    pts.append((60, 72))
    pts.append((210, 68))

    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=blue_color, width=3)

    draw.line([(25, 78), (225, 74)], fill=blue_color, width=2)
    return img
