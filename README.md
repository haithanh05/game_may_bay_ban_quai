# 🚀 Space Defender 8-Bit

> **Đồ án thực hành môn học Python**
> **Ngôn ngữ**: Python 3.10+ | **Engine**: Pyxel (Retro Game Engine)

---

## 📌 1. Mục tiêu dự án
Xây dựng một game 2D phong cách Retro 8-bit nhẹ nhàng, tối ưu hiệu năng, áp dụng tư duy lập trình hướng đối tượng (OOP), quản lý mã nguồn bằng Git và viết Unit Test tự động.

---

## 🛠️ 2. Hướng dẫn Cài đặt & Chạy ứng dụng

### Yêu cầu
- Python >= 3.10

### Các bước thực hiện
1. **Tạo môi trường ảo**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy Game (Demo)**:
   ```bash
   python -m src.main
   ```

4. **Chạy Kiểm thử (Unit Test)**:
   ```bash
   pytest
   ```

---

## 🎮 3. Mô tả Input & Output

| Thành phần | Loại dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Input** | Bàn phím | Phím `A`/`D` hoặc `Mũi tên Trái`/`Phải` để di chuyển.<br>Phím `SPACE` để bắn đạn. |
| **Output** | Cửa sổ Đồ họa | Màn hình 160x120 Pixel @ 30 FPS.<br>Hiển thị điểm số (`SCORE`), vị trí người chơi và đạn thời gian thực. |

---

## 📅 4. Kế hoạch triển khai (Lộ trình MVP)
- **Tuần 1 (Bản MVP)**: Dựng cấu trúc thư mục, khởi tạo Pyxel window, cài đặt nhân vật di chuyển và di chuyển đạn.
- **Tuần 2 (Hoàn thiện logic & Test)**: Viết bài kiểm thử `pytest`, tối ưu hóa việc xóa đối tượng khỏi bộ nhớ.
- **Tuần 3 (Đóng gói & Báo cáo)**: Chuẩn hóa code theo chuẩn PEP8, hoàn thiện `README.md`, đưa mã nguồn lên GitHub.

---

## ⚖️ 5. Trích dẫn & Bản quyền
- Game Engine: Sử dụng thư viện mã nguồn mở [Pyxel](https://github.com/kitao/pyxel) (MIT License).
- Mã nguồn toàn bộ dự án do nhóm tự phát triển, tuân thủ quy định đạo đức lập trình.
