# 🚀 Space Defender 8-Bit - Ultimate Edition

> **Đồ án thực hành môn học Python**  
> **Ngôn ngữ**: Python 3.10+ | **Engine**: Pyxel (Retro Game Engine)

---

## 📌 1. Mục tiêu dự án
**Space Defender 8-Bit - Ultimate Edition** là tựa game bắn tàu vũ trụ 2D kinh điển mang đậm phong cách Arcade thập niên 80-90. Dự án được thiết kế theo kiến trúc **Lập trình Hướng đối tượng (OOP)** chuẩn mực, phân tách độc lập giữa tầng mô hình logic (`models.py`) và tầng đồ họa điều khiển (`main.py`), hỗ trợ đầy đủ Menu tương tác bằng Tiếng Việt, **bản đồ mở rộng độ phân giải cao `240 x 160` (Widescreen Retro Arcade)** (mở rộng 100% diện tích so với bản gốc 160x120), hệ thống 4 Màn chơi Chiến dịch, và chế độ **Đối kháng 2 người chơi (PvP Solo)** trên cùng bàn phím với 3 Đấu Trường kịch tính.

---

## 🌟 2. Các tính năng & Chế độ chơi nổi bật

### 📜 Menu Arcade hoàn toàn bằng Tiếng Việt
Giao diện khởi động trực quan với khung viền đôi, chữ có viền bóng đen (drop shadow) siêu dễ đọc:
- `1. CHIEN DICH (1 NGUOI CHOI)`: Vượt qua 4 Màn chơi không kích ngoài hành tinh và đại chiến Trùm cuối.
- `2. DOI KHANG (2 NGUOI SOLO)`: Đấu trường không gian cho 2 người chơi solo đối đầu trực tiếp trên cùng một bàn phím.
- `3. HUONG DAN CHOI`: Bảng hướng dẫn chi tiết toàn bộ phím bấm và ý nghĩa 10 loại vật phẩm.

---

### 🗺️ Hệ thống 4 Màn chơi Chiến dịch (Campaign Stages)
1. **Màn 1: Vành Đai Thiên Thạch (Asteroid Belt)**: Khởi đầu khám phá không gian ngoại ô, quái trinh sát và tuần dương hạm cơ bản (Mục tiêu: 180 điểm).
2. **Màn 2: Tinh Vân Đỏ (Crimson Nebula)**: Bầu trời nhuộm đỏ rực, tiêm kích cảm tử Kamikaze xuất hiện dồn dập với quỹ đạo lượn sóng zic-zac (Mục tiêu: 400 điểm).
3. **Màn 3: Hang Ổ Trùm Dreadnought (Dreadnought Fortress)**: Sấm chớp vũ trụ nhấp nháy, còi báo động khẩn cấp và Trạm chiến hạm Trùm cuối Void Dreadnought xuất hiện với mưa đạn 3 hướng (Mục tiêu: 750 điểm).
4. **Màn 4: Không Gian Vô Tận (Endless Chaos)**: Chế độ sinh tồn bất tận với tốc độ cao, điểm số nhân đôi và độ khó tăng tiến liên tục để thử thách kỷ lục.

---

### ⚔️ Chế độ Đối kháng 2 người Solo (PvP Dogfight) & 3 Đấu Trường Mở Rộng
- **Người chơi 1 (P1 - Blue Falcon)**: Bay tự do khắp bản đồ (`min_y = 16`, `max_y = 150`), hướng mũi tàu lên trên.
- **Người chơi 2 (P2 - Crimson Viper)**: Bay tự do khắp bản đồ (`min_y = 14`, `max_y = 148`), hướng mũi tàu chúc xuống dưới.
- **Tính năng Xả đạn liên tục (Autofire on Hold)**: Đè nút `SPACE` (P1) hoặc `ENTER` (P2) để tự động xả đạn liên tục cực mượt, không cần phải nhấp từng lần gây mỏi tay.
- **Phím kỹ năng P1 mới (Cực thuận tay)**:
  - Phím `R`: Siêu Pháo Mega Beam hủy diệt (hoặc `E`)
  - Phím `T`: Bom Nova EMP quét sạch đạn (hoặc `B`, `F`)
  - Phím `SHIFT` hoặc `C`: Dash lướt né đòn bất tử
  - Phím `SPACE`: Đè phím để xả đạn liên tục
  - Phím `W, A, S, D`: Bay 4 hướng
- **Phím kỹ năng P2 công thái học (Thuận tay phải)**:
  - Phím `1` (hoặc `Numpad 1`): Bom Nova EMP
  - Phím `2` (hoặc `Numpad 2`): Siêu Pháo Mega Beam
  - Phím `0` (hoặc `Numpad 0`): Dash lướt né đòn
  - Phím `ENTER` (hoặc `K`, `RSHIFT`): Đè phím để xả đạn liên tục
  - Cụm phím `Mũi tên`: Bay 4 hướng
- **Chọn Đấu Trường (Bấm phím TAB)**:
  1. *Không Gian Mở*: Đấu trường rộng 240px có **2 Trạm Năng Lượng Không Gian (Cosmic Relics)** tại hai sườn (x=40, x=200). Phi thuyền bay gần trạm sẽ được sạc nhanh năng lượng Mega Beam!
  2. *Bão Thiên Thạch Chiến Thuật*: 5 khối thiên thạch lơ lửng cản đạn. Bắn vỡ thiên thạch có 60% tỉ lệ rơi vật phẩm tiếp tế hấp dẫn.
  3. *Bão Năng Lượng & Lưới Điện Plasma*: Tiếp tế rơi dồn dập, đồng thời vạch ngăn cách giữa sân định kỳ kích hoạt bão sét plasma cực mạnh giật điện phi thuyền dám vượt ranh giới.
- **Hiệu ứng Đối kháng Đỉnh cao**:
  - *Triệt tiêu đạn (Laser Clash)*: Đạn P1 và P2 bắn đối đầu sẽ va chạm và nổ tung thành chùm hoa lửa rực sáng.
  - *Cảnh báo nguy kịch (Low HP Alarm)*: Khi phi thuyền còn 1 HP, động cơ bốc khói đen và tóe tia lửa điện báo động.
- **Sửa triệt để lỗi tàng hình & bất tử**: Bộ đếm bất tử `invulnerable_timer` được cập nhật tự động mỗi khung hình trong `update_skills()`, đảm bảo phi thuyền chớp nháy đúng nhịp và trở lại bình thường, không bao giờ bị tàng hình hay bất tử vĩnh viễn.
- **Sửa triệt để lỗi nhặt đồ**: Cả P1 và P2 đều có thể bay tự do qua vạch giữa sân toàn bản đồ, bán kính nhặt đồ mở rộng 10 pixel cực nhạy.
- **Thể thức Chạm 2 (Best of 3 Rounds)**: Ai thắng 2 hiệp trước sẽ đoạt cúp vô địch chung cuộc.

---

### 🎨 Đồ Họa Nâng Cấp & Cơ Chế Phi Thuyền Biến Hình (Visual Evolution)
- **Phi thuyền biến đổi diện mạo theo Vật phẩm (Visual Morphs)**:
  - 🟡 **Khi nhặt Đạn 3 tia (Triple Shot)**: Thân tàu mở rộng thêm 2 bệ cánh gắn pháo laser phụ hai bên sườn có điểm sáng nòng pháo.
  - 🟣 **Khi nhặt Bắn nhanh (Rapid Laser)**: Mũi tàu vươn dài cặp nòng súng plasma kép siêu tốc màu hồng tím sáng rực.
  - ⚪ **Khi tích đầy năng lượng Mega Beam**: Lõi năng lượng trung tâm buồng lái phát sáng xung nhịp vàng trắng lấp lánh báo hiệu sẵn sàng khai hỏa.
  - 🔵 **Khi có Khiên năng lượng (Shield)**: Xuất hiện quả cầu khiên từ trường chuyển động xoay quanh tàu với các nút năng lượng vệ tinh.
  - 🔮 **Khi nhặt Vệ tinh (Drone)**: Triệu hồi các tiểu phi thuyền hộ vệ mini bay lượn bảo vệ xung quanh.
- **Hiệu ứng đạn bắn & cháy nổ nâng cấp**:
  - Tia đạn Laser được trang bị **lõi năng lượng trắng sáng chói (White Energy Core)** viền màu rực rỡ chuẩn phong cách Arcade.
  - Chớp sáng nòng súng (Muzzle Flash) khi khai hỏa.
  - Cột Siêu Pháo Mega Beam rộng 8 pixel rung lắc dữ dội kèm lõi trắng xuyên phá toàn bộ màn hình.
  - Tên lửa tầm nhiệt để lại vệt khói và chấn động màn hình (Screen Shake) chân thực.

---

### 🚀 Bộ Kỹ Năng Tác Chiến Hiện Đại (Skills)
- **Kỹ năng 1 - Dash Lướt Né Đòn (Phase Dash)**: Lướt nhanh tức thời theo hướng chỉ định, để lại chuỗi bóng mờ (Afterimages) và nhận trạng thái bất tử né đạn trong 14 frames.
- **Kỹ năng 2 - Siêu Pháo Mega Beam (Hyper Laser)**: Tích tụ 100% năng lượng để xả chùm tia laser cực đại xuyên thấu mọi chướng ngại vật trên đường thẳng.
- **Kỹ năng 3 - Bom Nova EMP**: Sóng chấn động diện rộng quét sạch mọi viên đạn đối thủ và gây sát thương nặng.
- **Kỹ năng 4 - Vệ Tinh Hộ Vệ (Orbiters)**: Triệu hồi các phi thuyền vệ tinh mini bay xoay quanh yểm trợ hỏa lực.

---

### 🛡️ Kho 10 Loại Vật Phẩm Nâng Cấp (Power-ups)
1. 🟡 **Triple Shot (`3`)**: Bắn chùm 3 tia đạn góc rộng.
2. 🔵 **Energy Shield (`S`)**: Giáp năng lượng chống đỡ đòn đánh trực tiếp.
3. 🟠 **Nova EMP Bomb (`B`)**: Bổ sung +1 Bom EMP hủy diệt.
4. 🟢 **Repair Kit (`+`)**: Hồi phục 1 điểm sinh lực (HP).
5. 🟣 **Rapid Laser (`R`)**: Kích hoạt bắn liên thanh đạn kép tốc độ cao.
6. ⚪ **Mega Crystal (`M`)**: Nạp đầy ngay 100% năng lượng Siêu Pháo Mega Beam.
7. 🔮 **Orbital Drone (`D`)**: Triệu hồi vệ tinh bay xoay quanh hộ vệ.
8. 🧲 **Gravity Magnet (`U`)**: Nam châm hút toàn bộ vật phẩm và điểm thưởng về phía tàu.
9. ❄️ **Chrono Freeze (`F`)**: Đóng băng/làm chậm 60% tốc độ kẻ địch trong 5 giây.
10. 🚀 **Homing Missiles (`T`)**: Bắn ra cặp tên lửa tầm nhiệt tự động truy lùng mục tiêu.

---

## 🕹️ 3. Bảng điều khiển chi tiết (Controls)

### 📌 Chế độ Chiến dịch (1 Người chơi)
| Thao tác | Phím bấm | Chi tiết |
| :--- | :--- | :--- |
| **Bay 4 hướng** | `W, A, S, D` hoặc `Mũi tên` | Lên, Xuống, Trái, Phải tự do |
| **Bắn Laser** | `SPACE` | **Đè phím để xả đạn liên tục** (không cần nhấp từng lần) |
| **Dash Né đòn** | `SHIFT` hoặc `C` | Lướt nhanh tức thời và né đạn bất tử |
| **Mega Beam** | `R` hoặc `E` | Bắn chùm tia năng lượng hủy diệt |
| **Bom Nova EMP** | `T` hoặc `B` / `F` | Quét sạch đạn và diệt quái diện rộng |
| **Tạm dừng / Menu** | `P`: Tạm dừng | `M` hoặc `ESC`: Về Menu chính |
| **Chơi lại** | `R` | Chơi lại ngay khi Game Over |

### ⚔️ Chế độ Đối kháng (2 Người Solo)
| Thao tác | Người chơi 1 (P1 - Xanh ngọc) | Người chơi 2 (P2 - Đỏ cam) |
| :--- | :--- | :--- |
| **Bay 4 hướng** | `W, A, S, D` | Cụm phím `Mũi tên` (`Lên, Xuống, Trái, Phải`) |
| **Bắn Laser** | `SPACE` (**Đè để xả đạn liên tục**) | `ENTER` hoặc `K` hoặc `RSHIFT` (**Đè để xả đạn liên tục**) |
| **Dash Né đòn** | `SHIFT` hoặc `C` | Phím `0` hoặc `Numpad 0` hoặc `RCTRL` |
| **Mega Beam** | `R` hoặc `E` | Phím `2` hoặc `Numpad 2` |
| **Bom Nova EMP** | `T` hoặc `B` / `F` | Phím `1` hoặc `Numpad 1` |
| **Đổi Đấu Trường**| `TAB`: Chuyển đổi 3 Đấu trường | `TAB`: Chuyển đổi 3 Đấu trường |
| **Tạm dừng / Menu**| `P`: Tạm dừng hiệp đấu | `M` hoặc `ESC`: Về Menu chính |

---

## 🛠️ 4. Hướng dẫn Cài đặt & Trải nghiệm

### Yêu cầu hệ thống
- **Python**: Phiên bản >= 3.10

### Các bước thực hiện
1. **Khởi tạo và kích hoạt môi trường ảo**:
   ```bash
   python -m venv venv
   # Trên Windows:
   .\venv\Scripts\activate
   # Trên macOS/Linux:
   source venv/bin/activate
   ```

2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Khởi chạy trò chơi**:
   ```bash
   python -m src.main
   ```

4. **Chạy kiểm thử tự động (Unit Test)**:
   ```bash
   pytest -v
   ```

---

## 🏛️ 5. Cấu trúc Thư mục & Thiết kế OOP

```text
PhamNguyenHaiThanh_2125110144/
│
├── src/
│   ├── __init__.py
│   ├── main.py          # Pyxel App Loop, Menu Tiếng Việt, 4 Màn chơi, 3 Arenas PvP, HUD có bóng đổ
│   └── models.py        # Mô hình OOP: Player, Drone, HomingMissile, Enemy, Asteroid, StageManager, PvPMatch...
│
├── tests/
│   ├── __init__.py
│   └── test_game.py     # 20 bài kiểm thử tự động toàn diện với Pytest
│
├── requirements.txt     # pyxel==2.2.8, pytest==8.0.0
└── README.md            # Tài liệu hướng dẫn sử dụng và báo cáo đồ án
```

---

## 🧪 6. Kết quả Kiểm thử (Unit Testing)

Bộ kiểm thử bao gồm **20 unit test** độc lập với giao diện, chạy trong 0.05 giây:
- ✅ `test_player_hp_and_damage`: Kiểm tra sinh lực và trừ máu khi nhận sát thương.
- ✅ `test_player_4way_movement`: Kiểm tra bay 4 hướng và giới hạn biên màn hình.
- ✅ `test_player_shield_absorption`: Kiểm tra giáp năng lượng bảo vệ không mất máu.
- ✅ `test_player_heal_and_bomb`: Kiểm tra hồi máu và sử dụng bom Nova EMP.
- ✅ `test_heavy_enemy_properties`: Kiểm tra chỉ số tàu tuần dương hạng nặng.
- ✅ `test_boss_enemy_properties_and_patrol`: Kiểm tra tạo hình, chỉ số và cơ chế tuần tra ngang của Trùm.
- ✅ `test_fast_enemy_movement`: Kiểm tra chuyển động sóng sin zic-zac của tiêm kích cảm tử.
- ✅ `test_enemy_shooting`: Kiểm tra bộ đếm bắn đạn phản công của địch.
- ✅ `test_starfield_wrap_around`: Kiểm tra vòng lặp vô tận của nền sao Parallax.
- ✅ `test_powerup_movement`: Kiểm tra chuyển động rơi và tự hủy khi ra ngoài biên của vật phẩm.
- ✅ `test_powerup_kinds_and_colors`: Kiểm tra đủ các loại vật phẩm nâng cấp và mã màu hiển thị.
- ✅ `test_bullet_movement_and_bounds`: Kiểm tra hướng bay đạn ta/địch/P2 và giải phóng bộ nhớ.
- ✅ `test_combo_system`: Kiểm tra bậc nhân thưởng chuỗi combo (x1, x2, x3, x4) và đếm lùi thời gian.
- ✅ `test_shockwave_and_particles`: Kiểm tra bán kính lan tỏa của sóng xung kích và hạt phản lực.
- ✅ `test_pvp_player_facing_and_boundaries`: Kiểm tra hướng quay và giới hạn nửa sân của P1 và P2 trong PvP.
- ✅ `test_pvp_match_flow`: Kiểm tra luật thi đấu chạm 2 (Best of 3), chuyển hiệp và xác định nhà vô địch.
- ✅ `test_asteroid_mechanics`: Kiểm tra chuyển động và nhận sát thương vỡ vụn của thiên thạch.
- ✅ `test_stage_manager_progression`: Kiểm tra tiến trình chuyển 4 Màn chơi theo điểm số.
- ✅ `test_pvp_arenas`: Kiểm tra chuyển đổi và tên 3 Đấu trường trong chế độ đối kháng.
- ✅ `test_player_dash_and_skills`: Kiểm tra kỹ năng Dash né đòn, Mega Beam và Drone vệ tinh.

---

## ⚖️ 7. Bản quyền & Đạo đức lập trình
- **Engine**: Sử dụng nền tảng đồ họa mã nguồn mở [Pyxel Engine](https://github.com/kitao/pyxel) (MIT License).
- Toàn bộ mã nguồn, thuật toán đối kháng 2 người, hệ thống màn chơi và tài liệu do sinh viên tự nghiên cứu phát triển, tuân thủ quy chuẩn đạo đức học thuật.
