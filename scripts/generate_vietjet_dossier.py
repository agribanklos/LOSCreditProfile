# -*- coding: utf-8 -*-
"""
generate_vietjet_dossier.py
Sinh trọn bộ hồ sơ tín dụng Vietjet (1400.001.23.DN.0102325399) gồm 35 file PDF:
- Ưu tiên đồng bộ 7 tài liệu gốc công khai (2024 - 2026) từ public_documents/
- Giả lập 28 tài liệu nghiệp vụ nội bộ ngân hàng đặc thù ngành hàng không với con dấu đỏ và chữ ký.
"""

import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFont

# Thư mục làm việc
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOC_DIR = os.path.join(BASE_DIR, "documents", "1400.001.23.DN.0102325399")
PUB_DIR = os.path.join(BASE_DIR, "public_documents")
TEMP_DIR = os.path.join(BASE_DIR, "temp_stamps")

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
FONT_SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_header_box(draw, left_text, right_text):
    font_bold = get_font(FONT_SERIF_BOLD, 22)
    font_reg = get_font(FONT_SERIF_REG, 20)
    font_italic = get_font(FONT_SERIF_ITALIC, 19)

    # Bên trái
    y = 80
    for i, line in enumerate(left_text):
        f = font_bold if i == 0 else font_italic
        draw.text((100, y), line, fill=(20, 20, 20), font=f)
        y += 30

    # Bên phải (Quốc hiệu tiêu ngữ)
    y = 80
    for i, line in enumerate(right_text):
        f = font_bold if i in (0, 1) else font_italic
        bbox = draw.textbbox((0, 0), line, font=f)
        w = bbox[2] - bbox[0]
        draw.text((1140 - w, y), line, fill=(20, 20, 20), font=f)
        y += 30

    # Đường kẻ gạch ngang tiêu ngữ
    draw.line([(850, 145), (1050, 145)], fill=(30, 30, 30), width=2)
    draw.line([(100, 215), (1140, 215)], fill=(180, 180, 180), width=1)
    return 240

def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
        words = para.split(" ")
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    return lines

def create_scanned_page(header_left, header_right, title, sections, table_data=None, footer_type="bank"):
    # Kích thước A4 ở 150 DPI: 1240 x 1754
    width, height = 1240, 1754
    # Màu giấy thực tế (hơi ngà nhẹ #fbfcf9)
    img = Image.new("RGBA", (width, height), (252, 252, 250, 255))
    draw = ImageDraw.Draw(img)

    # Nhiễu hạt scan nhẹ
    rng = random.Random(42)
    pixels = img.load()
    for _ in range(3500):
        rx = rng.randint(0, width - 1)
        ry = rng.randint(0, height - 1)
        gray = rng.randint(235, 248)
        pixels[rx, ry] = (gray, gray, gray, 255)

    y = draw_header_box(draw, header_left, header_right)

    # Tiêu đề tài liệu
    font_title = get_font(FONT_SERIF_BOLD, 28)
    title_box = draw.textbbox((0, 0), title, font=font_title)
    tw = title_box[2] - title_box[0]
    draw.text(((width - tw) / 2.0, y + 20), title, fill=(15, 15, 15), font=font_title)
    y += 85

    # Nội dung văn bản
    font_sec_title = get_font(FONT_SERIF_BOLD, 22)
    font_body = get_font(FONT_SERIF_REG, 20)

    for sec_title, sec_body in sections:
        if sec_title:
            draw.text((100, y), sec_title, fill=(10, 40, 90), font=font_sec_title)
            y += 34
        if sec_body:
            wrapped = wrap_text(sec_body, font_body, 1040, draw)
            for line in wrapped:
                if y > 1400:
                    break
                draw.text((100, y), line, fill=(30, 30, 30), font=font_body)
                y += 30
            y += 12

    # Bảng số liệu nếu có
    if table_data and y < 1300:
        headers, rows = table_data
        col_w = 1040 // len(headers)
        # Vẽ header bảng
        draw.rectangle([100, y, 1140, y + 36], fill=(235, 240, 248), outline=(150, 170, 200), width=1)
        for c_idx, h_text in enumerate(headers):
            draw.text((110 + c_idx * col_w, y + 6), h_text, fill=(10, 20, 60), font=font_sec_title)
        y += 36
        for r_idx, row in enumerate(rows):
            if y > 1350:
                break
            bg = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 253)
            draw.rectangle([100, y, 1140, y + 34], fill=bg, outline=(200, 210, 225), width=1)
            for c_idx, cell in enumerate(row):
                draw.text((110 + c_idx * col_w, y + 6), str(cell), fill=(20, 20, 20), font=font_body)
            y += 34
        y += 20

    # Chân trang (Ký tên, đóng dấu)
    y_footer = 1450
    if footer_type == "vjc":
        # Đại diện Vietjet ký
        draw.text((180, y_footer), "KẾ TOÁN TRƯỞNG / CFO", fill=(20, 20, 20), font=font_sec_title)
        draw.text((170, y_footer + 180), "Hồ Ngọc Yến Phương", fill=(10, 10, 10), font=font_sec_title)

        draw.text((800, y_footer), "TỔNG GIÁM ĐỐC / CHỦ TỊCH", fill=(20, 20, 20), font=font_sec_title)
        draw.text((790, y_footer + 180), "Đinh Việt Phương", fill=(10, 10, 10), font=font_sec_title)

        # Chèn chữ ký
        sig_cfo = Image.open(os.path.join(TEMP_DIR, "sig_hnyp.png")).convert("RGBA")
        img.paste(sig_cfo, (170, y_footer + 40), sig_cfo)

        sig_ceo = Image.open(os.path.join(TEMP_DIR, "sig_dvp.png")).convert("RGBA")
        img.paste(sig_ceo, (790, y_footer + 40), sig_ceo)

        # Đóng dấu Vietjet
        stamp = Image.open(os.path.join(TEMP_DIR, "stamp_vjc.png")).convert("RGBA")
        stamp = stamp.resize((260, 260))
        img.paste(stamp, (750, y_footer + 30), stamp)

    elif footer_type == "bank_sgd":
        # Chi nhánh Sở Giao dịch ký
        draw.text((150, y_footer), "TRƯỞNG PHÒNG KHDN LỚN", fill=(20, 20, 20), font=font_sec_title)
        draw.text((170, y_footer + 180), "Nguyễn Hữu Minh", fill=(10, 10, 10), font=font_sec_title)

        draw.text((800, y_footer), "GIÁM ĐỐC CHI NHÁNH SỞ GIAO DỊCH", fill=(20, 20, 20), font=font_sec_title)
        draw.text((820, y_footer + 180), "Trần Đức Vinh", fill=(10, 10, 10), font=font_sec_title)

        sig1 = Image.open(os.path.join(TEMP_DIR, "sig_hnyp.png")).convert("RGBA")
        img.paste(sig1, (160, y_footer + 40), sig1)

        sig2 = Image.open(os.path.join(TEMP_DIR, "sig_tdv.png")).convert("RGBA")
        img.paste(sig2, (810, y_footer + 40), sig2)

        stamp = Image.open(os.path.join(TEMP_DIR, "stamp_agri_sgd.png")).convert("RGBA")
        stamp = stamp.resize((260, 260))
        img.paste(stamp, (770, y_footer + 30), stamp)

    elif footer_type == "ttpd":
        # Trung tâm Phê duyệt Miền Bắc ký
        draw.text((150, y_footer), "CHUYÊN VIÊN THẨM ĐỊNH LẠI", fill=(20, 20, 20), font=font_sec_title)
        draw.text((170, y_footer + 180), "Lê Văn Hùng", fill=(10, 10, 10), font=font_sec_title)

        draw.text((760, y_footer), "GIÁM ĐỐC TTPD TÍN DỤNG MIỀN BẮC", fill=(20, 20, 20), font=font_sec_title)
        draw.text((800, y_footer + 180), "Vũ Thị Thanh Bình", fill=(10, 10, 10), font=font_sec_title)

        sig1 = Image.open(os.path.join(TEMP_DIR, "sig_ntpt.png")).convert("RGBA")
        img.paste(sig1, (160, y_footer + 40), sig1)

        sig2 = Image.open(os.path.join(TEMP_DIR, "sig_vtb.png")).convert("RGBA")
        img.paste(sig2, (800, y_footer + 40), sig2)

        stamp = Image.open(os.path.join(TEMP_DIR, "stamp_agri_ttpd_mb.png")).convert("RGBA")
        stamp = stamp.resize((260, 260))
        img.paste(stamp, (760, y_footer + 30), stamp)

    elif footer_type == "caav":
        # Cục Hàng không Việt Nam ký
        draw.text((150, y_footer), "TRƯỞNG PHÒNG TIÊU CHUẨN AN TOÀN BAY", fill=(20, 20, 20), font=font_sec_title)
        draw.text((170, y_footer + 180), "Đào Văn Tuấn", fill=(10, 10, 10), font=font_sec_title)

        draw.text((790, y_footer), "CỤC TRƯỞNG CỤC HÀNG KHÔNG", fill=(20, 20, 20), font=font_sec_title)
        draw.text((820, y_footer + 180), "Đinh Việt Thắng", fill=(10, 10, 10), font=font_sec_title)

        sig = Image.open(os.path.join(TEMP_DIR, "sig_dvp.png")).convert("RGBA")
        img.paste(sig, (810, y_footer + 40), sig)

        stamp = Image.open(os.path.join(TEMP_DIR, "stamp_caav.png")).convert("RGBA")
        stamp = stamp.resize((260, 260))
        img.paste(stamp, (770, y_footer + 30), stamp)

    return img.convert("RGB")


def setup_directories():
    categories = [
        "A_Ho_So_Phap_Ly",
        "B_Ho_So_Kinh_Te",
        "C_Ho_So_Vay_Von",
        "D_Ho_So_Tai_San_Bao_Dam",
        "E_Ho_So_Chi_Nhanh_Lap",
        "F_Ho_So_TTPD_Lap",
        "G_Thong_Bao_Thu_Cong_Tac",
        "H_Ho_So_Giai_Ngan",
        "I_Ho_So_Quan_Ly_No"
    ]
    for cat in categories:
        os.makedirs(os.path.join(DOC_DIR, cat), exist_ok=True)
    print("Directories initialized successfully.")


def link_public_documents():
    mapping = {
        os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A11_01.pdf"): os.path.join(PUB_DIR, "VJC_Thong_Bao_Thay_Doi_DKDN_2026.pdf"),
        os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A12_01.pdf"): os.path.join(PUB_DIR, "VJC_Nghi_Quyet_Bien_Ban_DHDCD_2026.pdf"),
        os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A18_01.pdf"): os.path.join(PUB_DIR, "VJC_Bao_Cao_Tinh_Hinh_Quan_Tri_Cong_Ty_2024.pdf"),
        os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A19_01.pdf"): os.path.join(PUB_DIR, "VJC_Bao_Cao_Tinh_Hinh_Quan_Tri_Cong_Ty_2025.pdf"),
        os.path.join(DOC_DIR, "B_Ho_So_Kinh_Te", "140000123DN0102325399_B1_01.pdf"): os.path.join(PUB_DIR, "VJC_Bao_Cao_Tai_Chinh_Hop_Nhat_Kiem_Toan_2024.pdf"),
        os.path.join(DOC_DIR, "B_Ho_So_Kinh_Te", "140000123DN0102325399_B1_02.pdf"): os.path.join(PUB_DIR, "VJC_Bao_Cao_Thuong_Nien_2025.pdf"),
        os.path.join(DOC_DIR, "B_Ho_So_Kinh_Te", "140000123DN0102325399_B2_01.pdf"): os.path.join(PUB_DIR, "VJC_Bao_Cao_Tai_Chinh_Hop_Nhat_Kiem_Toan_2025.pdf"),
        os.path.join(DOC_DIR, "C_Ho_So_Vay_Von", "140000123DN0102325399_CI12_01.pdf"): os.path.join(PUB_DIR, "VJC_Nghi_Quyet_Bien_Ban_DHDCD_2026.pdf"),
    }
    for dest, src in mapping.items():
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            print(f"Copied public doc -> {os.path.basename(dest)} ({os.path.getsize(dest)/1024/1024:.2f} MB)")
        else:
            print(f"WARNING: Public file not found: {src}")


def generate_all_simulated_docs():
    docs_to_generate = [
        # Nhóm A
        (
            os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A14_01.pdf"),
            ["BỘ GIAO THÔNG VẬN TẢI", "CỤC HÀNG KHÔNG VIỆT NAM", "Số: 08/AOC-CAAV/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 10 tháng 01 năm 2026"],
            "GIẤY CHỨNG NHẬN NGƯỜI KHAI THÁC TÀU BAY (AOC)",
            [
                ("I. THÔNG TIN NGƯỜI KHAI THÁC:", "Tên tổ chức: CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET (VIETJET AIR)\nĐịa chỉ trụ sở: 302/3 Phố Kim Mã, Ba Đình, Hà Nội.\nMã số doanh nghiệp: 0102325399.\nCăn cứ Luật Hàng không dân dụng Việt Nam và các Nghị định của Chính phủ."),
                ("II. NĂNG ĐỊNH VÀ PHẠM VI KHAI THÁC ĐƯỢC PHÊ DUYỆT:", "1. Loại tàu bay khai thác: Airbus A320, A321-200, A321neo (CFM LEAP-1A) và Airbus A330-300 (Rolls-Royce Trent 700).\n2. Phạm vi khai thác: Vận chuyển hành khách, hàng hóa thương mại quốc nội và mạng bay quốc tế khu vực Châu Á - Thái Bình Dương, Australia, Châu Âu.\n3. Thời hạn hiệu lực: Đến ngày 31 tháng 12 năm 2028.")
            ],
            None,
            "caav"
        ),
        (
            os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A15_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 15/QĐ-VJC.HĐQT/2022"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 04 năm 2022"],
            "QUYẾT ĐỊNH BỔ NHIỆM TỔNG GIÁM ĐỐC",
            [
                ("HỘI ĐỒNG QUẢN TRỊ CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET", "Căn cứ Luật Doanh nghiệp năm 2020 và Điều lệ Công ty Cổ phần Hàng không Vietjet;\nCăn cứ Nghị quyết Đại hội đồng Cổ đông thường niên;"),
                ("QUYẾT ĐỊNH:", "Điều 1: Bổ nhiệm Ông Đinh Việt Phương giữ chức vụ Tổng Giám đốc Công ty Cổ phần Hàng không Vietjet nhiệm kỳ 2022 - 2027.\nĐiều 2: Ông Đinh Việt Phương là Người đại diện theo pháp luật của Công ty, có toàn quyền chỉ đạo điều hành hoạt động sản xuất kinh doanh, ký kết các Hợp đồng kinh tế, Hợp đồng tín dụng với các Ngân hàng và tổ chức tài chính.\nĐiều 3: Quyết định có hiệu lực thi hành kể từ ngày ký.")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A16_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 18/QĐ-VJC.HĐQT/2022"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 18 tháng 04 năm 2022"],
            "QUYẾT ĐỊNH BỔ NHIỆM PHÓ TỔNG GIÁM ĐỐC KIÊM CFO",
            [
                ("HỘI ĐỒNG QUẢN TRỊ CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET", "Căn cứ Điều lệ tổ chức và hoạt động của Vietjet Air;\nXét năng lực và kinh nghiệm quản trị tài chính hàng không quốc tế;"),
                ("QUYẾT ĐỊNH:", "Điều 1: Bổ nhiệm Bà Hồ Ngọc Yến Phương giữ chức vụ Phó Tổng Giám đốc kiêm Giám đốc Tài chính (CFO).\nĐiều 2: Bà Hồ Ngọc Yến Phương đại diện Công ty thực hiện việc đàm phán, hoàn thiện hồ sơ cấp tín dụng, ký kết các chứng từ giải ngân và kiểm soát tài chính với Ngân hàng Nông nghiệp và PTNT Việt Nam (Agribank).")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "A_Ho_So_Phap_Ly", "140000123DN0102325399_A21_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 21/CV-VJC.PL/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 26 tháng 04 năm 2026"],
            "BẢN SAO Y CCCD BAN LÃNH ĐẠO VIETJET AIR",
            [
                ("THÔNG TIN NGƯỜI ĐẠI DIỆN PHÁP LUẬT VÀ QUẢN TRỊ:", "1. Bà Nguyễn Thị Phương Thảo - Chức vụ: Chủ tịch HĐQT Vietjet Air\n   Số CCCD: 001170000888 cấp ngày 20/05/2021 tại Cục Cảnh sát QLHC về TTXH.\n2. Ông Đinh Việt Phương - Chức vụ: Tổng Giám đốc kiêm Đại diện theo PL\n   Số CCCD: 001069001999 cấp ngày 15/06/2021 tại Cục Cảnh sát QLHC về TTXH.\n3. Bà Hồ Ngọc Yến Phương - Chức vụ: Phó Tổng Giám đốc kiêm Giám đốc Tài chính\n   Số CCCD: 079169002345 cấp ngày 10/08/2021 tại Cục Cảnh sát QLHC về TTXH.")
            ],
            None,
            "vjc"
        ),

        # Nhóm B
        (
            os.path.join(DOC_DIR, "B_Ho_So_Kinh_Te", "140000123DN0102325399_B3_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 45/BC-VJC.TC/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 04 năm 2026"],
            "BÁO CÁO NHANH HOẠT ĐỘNG KHAI THÁC BAY QUÝ 1/2026",
            [
                ("1. CHỈ TIÊU VẬN TẢI VÀ ĐỘI TÀU BAY:", "• Số lượng chuyến bay thực hiện: 38.500 chuyến bay (tăng 18,2% cùng kỳ).\n• Lượng hành khách vận chuyển: 7,2 triệu lượt khách.\n• Hệ số sử dụng ghế bình quân: 87,5%.\n• Tổng số tàu bay đang khai thác: 105 tàu bay (dòng A321 và A330)."),
                ("2. DOANH THU VÀ LỢI NHUẬN ƯỚC TÍNH QUÝ 1/2026:", "• Doanh thu thuần hợp nhất: 21.450 tỷ VNĐ.\n• Trong đó doanh thu phụ trợ & hàng hóa: 8.920 tỷ VNĐ (chiếm 41,6%).\n• Lợi nhuận trước thuế: 820 tỷ VNĐ.")
            ],
            (
                ["Chỉ tiêu", "Q1/2025", "Q1/2026", "Tăng trưởng"],
                [
                    ["Số chuyến bay", "32.500", "38.500", "+18,5%"],
                    ["Khách vận chuyển (triệu)", "6,1", "7,2", "+18,0%"],
                    ["Doanh thu (tỷ VNĐ)", "17.800", "21.450", "+20,5%"],
                    ["Lợi nhuận TT (tỷ VNĐ)", "580", "820", "+41,4%"]
                ]
            ),
            "vjc"
        ),

        # Nhóm C
        (
            os.path.join(DOC_DIR, "C_Ho_So_Vay_Von", "140000123DN0102325399_CI11_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 26/2026/VJC-PA"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 26 tháng 04 năm 2026"],
            "PHƯƠNG ÁN SỬ DỤNG VỐN VAY HẠN MỨC 2026 - 2027",
            [
                ("I. NHU CẦU VỐN LƯU ĐỘNG KINH DOANH:", "Căn cứ kế hoạch bay năm 2026 với 145.000 chuyến bay, Vietjet dự kiến tiêu thụ khoảng 1,1 triệu tấn nhiên liệu bay Jet A1.\nTổng chi phí nhiên liệu ước tính: 28.500 tỷ VNĐ.\nChi phí bảo dưỡng động cơ định kỳ và phụ tùng thay thế: 6.200 tỷ VNĐ."),
                ("II. ĐỀ NGHỊ CẤP HẠN MỨC TÍN DỤNG TẠI AGRIBANK:", "1. Hạn mức tín dụng đề xuất: 2.500.000.000.000 VNĐ (Hai nghìn năm trăm tỷ đồng).\n2. Mục đích: Thanh toán tiền mua nhiên liệu Jet A1 (cho Skypec, Petrolimex Aviation) và thanh toán chi phí bảo dưỡng kỹ thuật hàng không.\n3. Thời hạn hạn mức: 12 tháng. Thời hạn từng khế ước: tối đa 06 tháng.\n4. Nguồn trả nợ: Dòng tiền doanh thu bán vé chuyển về Agribank Chi nhánh Sở Giao dịch.")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "C_Ho_So_Vay_Von", "140000123DN0102325399_CI13_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 99/HĐNT-SKYPEC/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 05 tháng 01 năm 2026"],
            "HỢP ĐỒNG NGUYÊN TẮC CUNG ỨNG XĂNG DẦU JET A1",
            [
                ("CÁC BÊN THAM GIA KÝ KẾT:", "Bên A (Bên mua): CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET\nBên B (Bên bán): CÔNG TY TNHH MTV NHIÊN LIỆU HÀNG KHÔNG VIỆT NAM (SKYPEC)"),
                ("NỘI DUNG CHÍNH:", "1. Đối tượng: Tra nạp nhiên liệu hàng không Jet A1 tại các sân bay Nội Bài, Tân Sơn Nhất, Đà Nẵng, Cam Ranh, Phú Quốc...\n2. Sản lượng dự kiến: 650.000 tấn/năm. Đơn giá theo công bố Platt's Singapore cộng phụ phí tra nạp.\n3. Phương thức thanh toán: Chuyển khoản ngân hàng hoặc phát hành Thư tín dụng (L/C) thông qua Agribank Chi nhánh Sở Giao dịch.")
            ],
            None,
            "vjc"
        ),

        # Nhóm D (Tài sản bảo đảm)
        (
            os.path.join(DOC_DIR, "D_Ho_So_Tai_San_Bao_Dam", "140000123DN0102325399_D1_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 1400-HĐTC/2026/VJC"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 02 tháng 05 năm 2026"],
            "HỢP ĐỒNG THẾ CHẤP QUYỀN ĐÒI NỢ DOANH THU VÉ MÁY BAY",
            [
                ("CĂN CỨ VÀ NỘI DUNG THẾ CHẤP:", "Bên thế chấp: CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET\nBên nhận thế chấp: NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VIỆT NAM - CHI NHÁNH SỞ GIAO DỊCH"),
                ("TÀI SẢN THẾ CHẤP:", "• Toàn bộ quyền đòi nợ và nguồn thu phát sinh từ kênh bán vé máy bay thông qua Hệ thống thanh toán thanh toán đại lý (BSP Vietnam - IATA) và các đại lý cấp 1.\n• Giá trị định giá tài sản bảo đảm: 2.200.000.000.000 VNĐ.\n• Vietjet cam kết ủy quyền cho Agribank toàn quyền trích nợ tự động trên tài khoản chuyên thu để thu hồi nợ vay.")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "D_Ho_So_Tai_San_Bao_Dam", "140000123DN0102325399_D3_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "THẨM ĐỊNH GIÁ VIỆT NAM", "Số: 89/CT-TĐG/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 28 tháng 04 năm 2026"],
            "CHỨNG THƯ THẨM ĐỊNH GIÁ ĐỘNG CƠ TÀU BAY CFM LEAP-1A",
            [
                ("1. TÀI SẢN YÊU CẦU THẨM ĐỊNH:", "• Tên tài sản: 02 Động cơ máy bay phản lực CFM International LEAP-1A26 (Serial: 598124 & 598125), lắp ráp phục vụ dự phòng đội tàu bay A321neo.\n• Chủ sở hữu: Công ty Cổ phần Hàng không Vietjet (không có tranh chấp)."),
                ("2. KẾT QUẢ THẨM ĐỊNH GIÁ:", "• Phương pháp thẩm định: Phương pháp so sánh thị trường quốc tế kết hợp chi phí thay thế khấu hao.\n• Giá trị thẩm định: 1.450.000.000.000 VNĐ (Một nghìn bốn trăm năm mươi tỷ đồng - tương đương ~58,2 triệu USD).")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "D_Ho_So_Tai_San_Bao_Dam", "140000123DN0102325399_D5_01.pdf"),
            ["BẢO HIỂM HÀNG KHÔNG", "LIÊN DANH BẢO VIỆT - PVI", "Số: 12/HD-BHHK/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 10 tháng 01 năm 2026"],
            "HỢP ĐỒNG BẢO HIỂM THÂN VỎ VÀ PHỤ TÙNG TÀU BAY",
            [
                ("1. ĐỐI TƯỢNG BẢO HIỂM:", "Toàn bộ thân vỏ đội tàu bay Vietjet (105 chiếc) và các động cơ dự phòng LEAP-1A, Trent 700 được bảo hiểm rủi ro bay, rủi ro mặt đất và rủi ro kỹ thuật toàn diện."),
                ("2. CHUYỂN QUYỀN THỤ HƯỞNG BẢO HIỂM:", "Bên bảo hiểm xác nhận Agribank Chi nhánh Sở Giao dịch là Người thụ hưởng quyền lợi bảo hiểm đầu tiên đối với 02 động cơ LEAP-1A cầm cố thế chấp bảo đảm khoản vay hạn mức 2.500 tỷ VNĐ.")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "D_Ho_So_Tai_San_Bao_Dam", "140000123DN0102325399_D6_01.pdf"),
            ["BỘ GIAO THÔNG VẬN TẢI", "CỤC HÀNG KHÔNG VIỆT NAM", "Số: 45/GCN-ĐKBD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 04 tháng 05 năm 2026"],
            "GIẤY CHỨNG NHẬN ĐĂNG KÝ BIỆN PHÁP BẢO ĐẢM TÀU BAY",
            [
                ("NỘI DUNG ĐĂNG KÝ GIAO DỊCH BẢO ĐẢM:", "Cục Hàng không Việt Nam chứng nhận đã đăng ký thế chấp tàu bay/động cơ máy bay:\n• Bên bảo đảm: CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET\n• Bên nhận bảo đảm: AGRIBANK - CHI NHÁNH SỞ GIAO DỊCH\n• Tài sản thế chấp: 02 Động cơ CFM LEAP-1A26 (Số hiệu: 598124, 598125).\n• Đã ghi vào Sổ bạ đăng bạ Quốc gia theo quy định.")
            ],
            None,
            "caav"
        ),

        # Nhóm E (Chi nhánh lập)
        (
            os.path.join(DOC_DIR, "E_Ho_So_Chi_Nhanh_Lap", "140000123DN0102325399_E11_01.pdf"),
            ["NGÂN HÀNG NHÀ NƯỚC VIỆT NAM", "TRUNG TÂM THÔNG TIN TÍN DỤNG (CIC)", "Mã tra cứu: CIC-VJC-20260426"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 26 tháng 04 năm 2026"],
            "BÁO CÁO THÔNG TIN QUAN HỆ TÍN DỤNG DOANH NGHIỆP CIC",
            [
                ("1. THÔNG TIN KHÁCH HÀNG:", "• Tên: CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET | MST: 0102325399\n• Điểm tín dụng CIC: Hạng 1 (Rủi ro cực thấp).\n• Nhóm nợ hiện tại: Nhóm 1 (Nợ đủ tiêu chuẩn). Lịch sử 5 năm không có nợ quá hạn từ nhóm 2 trở lên."),
                ("2. QUAN HỆ TÍN DỤNG TẠI CÁC TCTD:", "• Dư nợ ngắn hạn: 23.400 tỷ VNĐ tại 8 NHTM lớn.\n• Tài sản bảo đảm đăng ký tại Trung tâm giao dịch: 38.500 tỷ VNĐ (Tỷ lệ bảo đảm 164%).\n• Tình hình thanh toán gốc và lãi: Đúng hạn 100%.")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "E_Ho_So_Chi_Nhanh_Lap", "140000123DN0102325399_E2_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "PHÒNG QUẢN LÝ RỦI RO", "Số: 94/XHTD-2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 27 tháng 04 năm 2026"],
            "KẾT QUẢ CHẤM ĐIỂM XẾP HẠNG TÍN DỤNG NỘI BỘ",
            [
                ("KẾT QUẢ CHẤM ĐIỂM THEO HỆ THỐNG XHTD NỘI BỘ AGRIBANK:", "• Nhóm chỉ tiêu tài chính: 56.5 / 60 điểm (Thanh khoản cao, dòng tiền OCF thặng dư 6.120 tỷ).\n• Nhóm chỉ tiêu phi tài chính: 37.7 / 40 điểm (Thương hiệu dẫn đầu thị phần, đội bay hiện đại).\n• Tổng điểm xếp hạng: 94.2 / 100 điểm.\n• HẠNG TÍN DỤNG: AA+ (Khách hàng đặc biệt ưu tiên cấp tín dụng).")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "E_Ho_So_Chi_Nhanh_Lap", "140000123DN0102325399_E3_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "HỘI ĐỒNG TÍN DỤNG", "Số: 32/BB-HĐTD.SGD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 28 tháng 04 năm 2026"],
            "BIÊN BẢN HỌP HỘI ĐỒNG TÍN DỤNG CHI NHÁNH",
            [
                ("HỘI ĐỒNG TÍN DỤNG THỐNG NHẤT 100% NỘI DUNG:", "1. Nhất trí đề xuất cấp hạn mức tín dụng 2.500 tỷ VNĐ cho Công ty Cổ phần Hàng không Vietjet.\n2. Do mức cấp tín dụng vượt thẩm quyền phán quyết của Chi nhánh loại 1 (>500 tỷ VNĐ), Hội đồng quyết nghị lập Tờ trình trình Ban Tổng Giám đốc và Trung tâm Phê duyệt Tín dụng Miền Bắc xem xét phê duyệt theo thẩm quyền.")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "E_Ho_So_Chi_Nhanh_Lap", "140000123DN0102325399_E4_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "BAN GIÁM ĐỐC", "Số: 15/TTr-NHNo.SGD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 29 tháng 04 năm 2026"],
            "TỜ TRÌNH ĐỀ NGHỊ CẤP HẠN MỨC TÍN DỤNG VƯỢT THẨM QUYỀN",
            [
                ("Kính gửi: TRUNG TÂM PHÊ DUYỆT TÍN DỤNG MIỀN BẮC - AGRIBANK", "1. Khách hàng đề nghị: CÔNG TY CỔ PHẦN HÀNG KHÔNG VIETJET (MST: 0102325399).\n2. Hạn mức đề xuất: 2.500.000.000.000 VNĐ.\n3. Mục đích vay: Tài trợ chi phí mua xăng dầu Jet A1 và thuê động cơ tàu bay.\n4. Biện pháp bảo đảm: Thế chấp quyền đòi nợ đại lý vé BSP (2.200 tỷ) và 02 động cơ LEAP-1A (1.450 tỷ), tổng giá trị TSBĐ 3.650 tỷ VNĐ (bảo đảm 146%).\nChi nhánh Sở Giao dịch kính trình TTPD Miền Bắc thẩm định lại và phê duyệt.")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "E_Ho_So_Chi_Nhanh_Lap", "140000123DN0102325399_E5_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "TỔ KIỂM TRA THỰC TẾ", "Số: 22/BC-KT/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 25 tháng 04 năm 2026"],
            "BÁO CÁO KIỂM TRA THỰC TẾ CƠ SỞ HOẠT ĐỘNG VIETJET",
            [
                ("KẾT QUẢ KIỂM TRA HIỆN TRƯỜNG:", "1. Trung tâm Điều hành bay (OCC) tại Sân bay Nội Bài và Tân Sơn Nhất: Đang vận hành liên tục 24/7, tỷ lệ đúng giờ (OTP) đạt 86,5%.\n2. Kiểm tra kho phụ tùng và động cơ LEAP-1A: Lưu giữ đúng quy chuẩn an toàn hàng không ICAO, đầy đủ tài liệu bảo dưỡng từ nhà sản xuất CFM International.\n3. Tình hình kinh doanh thực tế diễn ra sôi động, dòng tiền bán vé ghi nhận ổn định.")
            ],
            None,
            "bank_sgd"
        ),

        # Nhóm F (TTPD lập)
        (
            os.path.join(DOC_DIR, "F_Ho_So_TTPD_Lap", "140000123DN0102325399_F1_01.pdf"),
            ["AGRIBANK - TTPD MIỀN BẮC", "PHÒNG THẨM ĐỊNH LẠI", "Mã HS: 1400.001.23.DN.0102325399"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 05 tháng 05 năm 2026"],
            "BÁO CÁO THẨM ĐỊNH LẠI ĐỘC LẬP TÍN DỤNG",
            [
                ("1. ĐÁNH GIÁ NĂNG LỰC TÀI CHÍNH VÀ HOẠT ĐỘNG:", "Doanh nghiệp phục hồi mạnh mẽ sau Covid, doanh thu 2024-2025 tăng trưởng bình quân trên 25%/năm, đạt 78.600 tỷ VNĐ năm 2025. Lợi nhuận trước thuế dương bền vững 2.450 tỷ VNĐ. Đòn bẩy tài chính an toàn trong ngành hàng không."),
                ("2. KẾT LUẬN THẨM ĐỊNH LẠI:", "Nhất trí với đề xuất của Chi nhánh Sở Giao dịch. Chấp thuận cấp HMTD 2.500 tỷ VNĐ với điều kiện kiểm soát chặt dòng tiền bán vé máy bay qua Agribank.")
            ],
            None,
            "ttpd"
        ),
        (
            os.path.join(DOC_DIR, "F_Ho_So_TTPD_Lap", "140000123DN0102325399_F2_01.pdf"),
            ["AGRIBANK - TTPD MIỀN BẮC", "TỔ PHÁP CHẾ & TUÂN THỦ", "Số: 48/PC-TTPD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 06 tháng 05 năm 2026"],
            "Ý KIẾN PHÁP CHẾ VỀ HỒ SƠ TÍN DỤNG VIETJET AIR",
            [
                ("Ý KIẾN THẨM TRA PHÁP LÝ:", "1. Hồ sơ pháp nhân Vietjet đầy đủ, người đại diện theo pháp luật có đủ thẩm quyền ký kết.\n2. Biện pháp bảo đảm bằng Động cơ tàu bay và Quyền đòi nợ đại lý phù hợp quy định Bộ luật Dân sự và Luật Hàng không Dân dụng Việt Nam. Đã hoàn tất thủ tục đăng bạ tại CAAV.")
            ],
            None,
            "ttpd"
        ),
        (
            os.path.join(DOC_DIR, "F_Ho_So_TTPD_Lap", "140000123DN0102325399_F3_01.pdf"),
            ["NGÂN HÀNG NÔNG NGHIỆP VÀ PTNT VN", "HỘI ĐỒNG TÍN DỤNG TRỤ SỞ CHÍNH", "Số: 72/BB-HĐTD.TSC/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 08 tháng 05 năm 2026"],
            "BIÊN BẢN HỌP PHÊ DUYỆT CẤP HẠN MỨC TÍN DỤNG",
            [
                ("HỘI ĐỒNG TÍN DỤNG TSC QUYẾT NGHỊ:", "Thông qua việc cấp tín dụng hạn mức 2.500.000.000.000 VNĐ cho Công ty Cổ phần Hàng không Vietjet. Giao Chi nhánh Sở Giao dịch quản lý giải ngân và thu hồi nợ nghiêm ngặt.")
            ],
            None,
            "ttpd"
        ),
        (
            os.path.join(DOC_DIR, "F_Ho_So_TTPD_Lap", "140000123DN0102325399_F4_01.pdf"),
            ["AGRIBANK - TTPD MIỀN BẮC", "BAN GIÁM ĐỐC", "Số: 88/TB-TTPD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 10 tháng 05 năm 2026"],
            "THÔNG BÁO PHÊ DUYỆT CHÍNH THỨC CẤP TÍN DỤNG",
            [
                ("Kính gửi: AGRIBANK CHI NHÁNH SỞ GIAO DỊCH", "Trung tâm Phê duyệt Tín dụng Miền Bắc thông báo phê duyệt hồ sơ vay vốn của Công ty Cổ phần Hàng không Vietjet:\n• Hạn mức: 2.500.000.000.000 VNĐ.\n• Thời hạn hạn mức: 12 tháng.\n• Lãi suất: Thả nổi theo chính sách khách hàng doanh nghiệp lớn của Agribank.")
            ],
            None,
            "ttpd"
        ),

        # Nhóm G
        (
            os.path.join(DOC_DIR, "G_Thong_Bao_Thu_Cong_Tac", "140000123DN0102325399_G1_01.pdf"),
            ["AGRIBANK - TTPD MIỀN BẮC", "PHÒNG THẨM ĐỊNH", "Số: 35/CV-TTPD/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 03 tháng 05 năm 2026"],
            "CÔNG VĂN YÊU CẦU LÀM RÕ CƠ CẤU DOANH THU PHỤ TRỢ",
            [
                ("YÊU CẦU GIẢI TRÌNH:", "Đề nghị Vietjet làm rõ tỷ trọng doanh thu phụ trợ và kế hoạch mở rộng các đường bay quốc tế đường dài đi Úc và Ấn Độ trong năm 2026.")
            ],
            None,
            "ttpd"
        ),
        (
            os.path.join(DOC_DIR, "G_Thong_Bao_Thu_Cong_Tac", "140000123DN0102325399_G2_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 55/CV-VJC.TC/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 04 tháng 05 năm 2026"],
            "CÔNG VĂN GIẢI TRÌNH BỔ SUNG CỦA VIETJET AIR",
            [
                ("Kính gửi: TTPD MIỀN BẮC & CHI NHÁNH SỞ GIAO DỊCH", "Vietjet giải trình: Doanh thu phụ trợ năm 2025 đạt trên 40% nhờ các gói hành lý, chọn chỗ, bán hàng miễn thuế trên máy bay và bảo hiểm du lịch. Mạng bay Úc và Ấn Độ đạt hiệu suất ghế trên 88%, mang lại dòng ngoại tệ dồi dào.")
            ],
            None,
            "vjc"
        ),

        # Nhóm H (Giải ngân)
        (
            os.path.join(DOC_DIR, "H_Ho_So_Giai_Ngan", "140000123DN0102325399_H1_01.pdf"),
            ["CÔNG TY CỔ PHẦN", "HÀNG KHÔNG VIETJET", "Số: 01/2026/GN-VJC"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 05 năm 2026"],
            "GIẤY ĐỀ NGHỊ RÚT VỐN KIÊM KHẾ ƯỚC NHẬN NỢ ĐỢT 1",
            [
                ("ĐỀ NGHỊ RÚT VỐN VAY:", "Căn cứ Hợp đồng tín dụng hạn mức số 1400-HĐTD/2026/VJC ngày 12/05/2026;\nVietjet đề nghị rút vốn Đợt 1 số tiền: 500.000.000.000 VNĐ (Năm trăm tỷ đồng).\nMục đích: Thanh toán tiền mua nhiên liệu bay Jet A1 cho Skypec theo Hóa đơn VAT số 0012589.")
            ],
            None,
            "vjc"
        ),
        (
            os.path.join(DOC_DIR, "H_Ho_So_Giai_Ngan", "140000123DN0102325399_H2_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "PHÒNG KHDN LỚN", "Số: 78/BC-KSGN/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 05 năm 2026"],
            "BÁO CÁO KIỂM SOÁT ĐIỀU KIỆN GIẢI NGÂN ĐỢT 1",
            [
                ("KẾT QUẢ KIỂM SOÁT:", "• Hợp đồng mua bán và hóa đơn VAT tra nạp nhiên liệu Jet A1 đầy đủ, hợp lệ.\n• Đã hoàn tất ký phụ lục thế chấp và kiểm tra không có nợ quá hạn.\n• Đủ điều kiện giải ngân 500 tỷ VNĐ chuyển thẳng cho bên thụ hưởng Skypec.")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "H_Ho_So_Giai_Ngan", "140000123DN0102325399_H3_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "PHÒNG KẾ TOÁN VÀ THANH TOÁN", "Số: 1505/UNC-2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 05 năm 2026"],
            "LỆNH CHUYỂN TIỀN THANH TOÁN NHIÊN LIỆU JET A1",
            [
                ("NỘI DUNG THANH TOÁN:", "Trích nợ tài khoản vay giải ngân của Vietjet: 500.000.000.000 VNĐ.\nChuyển có vào tài khoản của Công ty Skypec tại Agribank Chi nhánh Sở Giao dịch.\nLý do: Thanh toán tiền nhiên liệu máy bay Jet A1 đợt 1 tháng 05/2026.")
            ],
            None,
            "bank_sgd"
        ),

        # Nhóm I (Quản lý nợ)
        (
            os.path.join(DOC_DIR, "I_Ho_So_Quan_Ly_No", "140000123DN0102325399_I1_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "TỔ KIỂM TRA SAU VAY", "Số: 34/BB-KTSV/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 15 tháng 06 năm 2026"],
            "BIÊN BẢN KIỂM TRA SỬ DỤNG VỐN SAU GIẢI NGÂN",
            [
                ("KẾT QUẢ KIỂM TRA ĐỊNH KỲ 30 NGÀY:", "Khoản vay 500 tỷ được sử dụng đúng mục đích 100% thanh toán cho đối tác cung cấp xăng dầu Skypec. Toàn bộ các chuyến bay được nạp nhiên liệu đầy đủ và đúng lịch bay. Doanh thu bán vé thu về Agribank SGD trong tháng đạt 3.850 tỷ VNĐ, đủ điều kiện trả nợ gốc lãi.")
            ],
            None,
            "bank_sgd"
        ),
        (
            os.path.join(DOC_DIR, "I_Ho_So_Quan_Ly_No", "140000123DN0102325399_I3_01.pdf"),
            ["AGRIBANK - SỞ GIAO DỊCH", "PHÒNG QUẢN LÝ RỦI RO", "Số: 89/BC-GS-Q3/2026"],
            ["CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc", "Hà Nội, ngày 30 tháng 09 năm 2026"],
            "BÁO CÁO GIÁM SÁT ĐỊNH KỲ CHẤT LƯỢNG TÍN DỤNG",
            [
                ("ĐÁNH GIÁ CHẤT LƯỢNG KHOẢN VAY:", "Khách hàng duy trì xếp hạng tín dụng AA+. Không phát sinh bất kỳ khoản nợ quá hạn nào. TSBĐ được kiểm tra định kỳ vẫn nguyên vẹn giá trị. Duy trì đánh giá khoản nợ Nhóm 1 đủ tiêu chuẩn.")
            ],
            None,
            "bank_sgd"
        ),
    ]

    for path, hl, hr, title, secs, tbl, f_type in docs_to_generate:
        print(f"Generating simulated PDF -> {os.path.basename(path)} ...")
        page = create_scanned_page(hl, hr, title, secs, tbl, f_type)
        page.save(path, "PDF", resolution=150.0)
    print("All 28 simulated internal bank documents generated successfully!")

if __name__ == "__main__":
    setup_directories()
    link_public_documents()
    generate_all_simulated_docs()
