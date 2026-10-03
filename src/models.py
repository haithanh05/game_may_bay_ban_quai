import math
import random
from typing import Optional, List, Tuple
'''List: Danh sách động (mảng). Ví dụ: List[Drone] là danh sách chứa các đối tượng Drone.

Tuple: Bộ dữ liệu cố định vị trí. Ví dụ: Tuple[float, float, int, int] là bộ gồm đúng 4 giá trị theo thứ tự: 2 số thực và 2 số nguyên.

Optional: Giá trị có thể có hoặc bằng None (rỗng). Ví dụ: Optional[int] nghĩa là số nguyên hoặc None.

Giống nhau: Đều dùng để mô tả Danh sách động (List ≈ vector), Bộ nhóm giá trị (Tuple ≈ tuple), và Giá trị có thể rỗng (Optional ≈ optional).

Khác nhau cốt lõi:

Python (typing): Chỉ là gợi ý (Type Hint) cho người đọc và IDE. Viết sai kiểu chương trình vẫn chạy bình thường.

C++: Là quy tắc bắt buộc. Viết sai kiểu trình biên dịch sẽ báo lỗi ngay và không cho
'''
class Star:
    """Đại diện cho một ngôi sao trong nền vũ trụ nhiều lớp (Parallax Starfield)."""

    def __init__(self, screen_width: int = 160, screen_height: int = 120, layer: int = 1):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layer = layer
        self.x = random.randint(0, screen_width - 1)
        self.y = random.randint(0, screen_height - 1)
        self.twinkle = random.randint(0, 30)
        
        # Tốc độ và màu sắc phân tầng theo độ sâu không gian
        if layer == 1:
            self.speed = 0.8
            self.color = 5  # Xám đậm (ở xa)
            self.size = 1
        elif layer == 2:
            self.speed = 1.5
            self.color = 6  # Xám sáng (ở giữa)
            self.size = 1
        else:
            self.speed = 2.4
            self.color = 7  # Trắng sáng (ở gần)
            self.size = 1

    def update(self, screen_height: int = 120):
        self.y += self.speed
        self.twinkle = (self.twinkle + 1) % 40
        if self.y >= screen_height:
            self.y = 0
            self.x = random.randint(0, self.screen_width - 1)


class Particle:
    """Hiệu ứng hạt cho vụ nổ, tia lửa đạn, khói lửa động cơ và vệt tốc biến Dash."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: Optional[float] = None,
        vy: Optional[float] = None,
        color: Optional[int] = None,
        life: Optional[int] = None,
        is_flame: bool = False,
        size: int = 1,
    ):
        self.x = float(x)
        self.y = float(y)
        self.is_flame = is_flame
        self.size = size
        
        if is_flame:
            # Lửa phụt từ đuôi phi thuyền
            self.vx = random.uniform(-0.5, 0.5) if vx is None else vx
            self.vy = random.uniform(1.0, 2.2) if vy is None else vy
            self.life = random.randint(4, 7) if life is None else life
            self.color = random.choice([7, 10, 9]) if color is None else color
        else:
            # Hạt vụ nổ / tia sáng
            self.vx = random.uniform(-1.8, 1.8) if vx is None else vx
            self.vy = random.uniform(-1.8, 1.8) if vy is None else vy
            self.life = random.randint(6, 14) if life is None else life
            self.color = random.choice([7, 8, 9, 10]) if color is None else color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1


class Shockwave:
    """Sóng xung kích lan tỏa khi dùng bom EMP hoặc tiêu diệt Boss."""

    def __init__(self, x: float, y: float, max_radius: float = 60, color: int = 10):
        self.x = float(x)
        self.y = float(y)
        self.radius = 2.0
        self.max_radius = float(max_radius)
        self.color = color
        self.is_active = True

    def update(self, speed: float = 3.5):
        self.radius += speed
        if self.radius >= self.max_radius:
            self.is_active = False


class FloatingText:
    """Chữ hiệu ứng bay lên có bóng đổ (drop shadow) giúp siêu dễ đọc."""

    def __init__(self, text: str, x: int, y: int, color: int = 7, life: int = 26):
        self.text = text
        self.x = int(x)
        self.y = float(y)
        self.color = color
        self.life = life
        self.is_active = True

    def update(self):
        self.y -= 0.4
        self.life -= 1
        if self.life <= 0:
            self.is_active = False


class Drone:
    """Phi thuyền vệ tinh hỗ trợ (Orbital Companion Drone) bay hộ vệ quanh phi thuyền chính."""

    def __init__(self, angle: float = 0.0, radius: float = 14.0):
        self.angle = angle
        self.radius = radius
        self.x = 0.0
        self.y = 0.0
        self.shoot_timer = 20

    def update(self, center_x: float, center_y: float, speed: float = 0.08):
        self.angle += speed
        self.x = center_x + 4 + math.cos(self.angle) * self.radius
        self.y = center_y + 4 + math.sin(self.angle) * self.radius
        self.shoot_timer -= 1

    def can_shoot(self) -> bool:
        if self.shoot_timer <= 0:
            self.shoot_timer = 24
            return True
        return False


class HomingMissile:
    """Tên lửa tầm nhiệt tự động bám đuổi mục tiêu gần nhất."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0.0,
        vy: float = -2.5,
        owner_id: int = 1,
        damage: int = 2,
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.owner_id = owner_id
        self.damage = damage
        self.color = 8
        self.life = 90
        self.is_active = True

    def update(self, targets: list):
        # Tìm mục tiêu khả dụng gần nhất
        best_target = None
        best_dist = 99999.0
        for t in targets:
            if getattr(t, "is_active", True) and getattr(t, "hp", 0) > 0:
                d = math.hypot(t.x - self.x, t.y - self.y)
                if d < best_dist:
                    best_dist = d
                    best_target = t

        if best_target and best_dist > 2:
            dx = (best_target.x - self.x) / best_dist
            dy = (best_target.y - self.y) / best_dist
            turn_rate = 0.22
            self.vx = self.vx * (1 - turn_rate) + dx * 3.5 * turn_rate
            self.vy = self.vy * (1 - turn_rate) + dy * 3.5 * turn_rate

        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0 or self.x < -10 or self.x > 170 or self.y < -10 or self.y > 130:
            self.is_active = False


class Player:
    """Tàu chiến đấu của người chơi với bộ kỹ năng: Dash lướt né đòn, Mega Laser, Drone vệ tinh và Bom EMP."""

    def __init__(
        self,
        x: int,
        y: int,
        screen_width: int = 160,
        screen_height: int = 120,
        owner_id: int = 1,
        facing: int = 1,
        min_y: Optional[int] = None,
        max_y: Optional[int] = None,
    ):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.owner_id = owner_id
        self.facing = facing  # 1: hướng lên (P1), -1: hướng xuống (P2 đối kháng)
        self.min_y = min_y
        self.max_y = max_y

        self.width = 8
        self.height = 8
        
        self.score = 0
        self.hp = 3
        self.max_hp = 5
        self.shield = 0  # Giáp năng lượng bảo vệ
        self.bombs = 1   # Bom EMP hủy diệt
        self.max_bombs = 3
        
        # Bộ đếm hiệu lực vật phẩm
        self.triple_shot_timer = 0
        self.rapid_fire_timer = 0
        self.invulnerable_timer = 0
        self.rounds_won = 0

        # KỸ NĂNG 1: Tốc biến / Lướt né đòn (Phase Dash)
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.dash_vx = 0.0
        self.dash_vy = 0.0
        self.afterimages: List[Tuple[float, float, int, int]] = []  # [(x, y, facing, life)]

        # KỸ NĂNG 2: Siêu pháo hủy diệt Mega Beam
        self.mega_energy = 100
        self.max_mega_energy = 100
        self.mega_beam_timer = 0

        # KỸ NĂNG 3: Vệ tinh hộ vệ không gian (Orbiters)
        self.drones: List[Drone] = []
        self.drone_timer = 0

        # KỸ NĂNG 4 & BUFF: Nam châm, Ngưng đọng thời gian, Tên lửa
        self.magnet_timer = 0
        self.freeze_timer = 0
        self.missile_timer = 0

    def move_left(self, speed: int = 2):
        self.x = max(0, self.x - speed)

    def move_right(self, speed: int = 2):
        self.x = min(self.screen_width - 8, self.x + speed)

    def move_up(self, speed: int = 2):
        floor_y = self.min_y if self.min_y is not None else 14
        self.y = max(floor_y, self.y - speed)

    def move_down(self, speed: int = 2):
        ceil_y = self.max_y if self.max_y is not None else (self.screen_height - 10)
        self.y = min(ceil_y, self.y + speed)

    def trigger_dash(self, dx: float = 0.0, dy: float = 0.0) -> bool:
        """Kích hoạt kỹ năng Dash: Lướt nhanh tức thì và nhận trạng thái né đòn bất tử."""
        if self.dash_cooldown <= 0:
            self.dash_cooldown = 45  # 1.5 giây hồi chiêu
            self.dash_timer = 6     # Lướt 6 frames
            if dx == 0.0 and dy == 0.0:
                dy = -1.0 if self.facing == 1 else 1.0
            length = math.hypot(dx, dy)
            if length > 0:
                self.dash_vx = (dx / length) * 4.8
                self.dash_vy = (dy / length) * 4.8
            else:
                self.dash_vx = 0.0
                self.dash_vy = -4.8 if self.facing == 1 else 4.8

            self.invulnerable_timer = max(self.invulnerable_timer, 14)
            return True
        return False

    def trigger_mega_beam(self) -> bool:
        """Kích hoạt kỹ năng Mega Laser hủy diệt toàn bộ kẻ địch trên một đường thẳng."""
        if self.mega_energy >= 100 and self.mega_beam_timer <= 0:
            self.mega_energy = 0
            self.mega_beam_timer = 24  # Duy trì tia sáng trong 24 frames
            return True
        return False

    def add_drone(self):
        """Bổ sung một vệ tinh bay xung quanh phi thuyền."""
        current_count = len(self.drones)
        if current_count < 2:
            new_angle = (current_count * math.pi)
            self.drones.append(Drone(angle=new_angle, radius=14.0))
        self.drone_timer = 320  # Hiệu lực khoảng 10 giây

    def update_skills(self):
        """Cập nhật hồi chiêu, lướt và ảnh ảo của phi thuyền."""
        # Cập nhật Dash
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if self.dash_timer > 0:
            self.x += int(self.dash_vx)
            self.y += int(self.dash_vy)
            # Ràng buộc biên
            floor_y = self.min_y if self.min_y is not None else 14
            ceil_y = self.max_y if self.max_y is not None else (self.screen_height - 10)
            self.x = max(0, min(self.screen_width - 8, self.x))
            self.y = max(floor_y, min(ceil_y, self.y))
            # Lưu lại ảnh ảo Dash (Afterimage)
            self.afterimages.append((float(self.x), float(self.y), self.facing, 6))
            self.dash_timer -= 1

        # Cập nhật ảnh ảo
        updated_afterimages = []
        for ax, ay, afacing, alife in self.afterimages:
            if alife > 1:
                updated_afterimages.append((ax, ay, afacing, alife - 1))
        self.afterimages = updated_afterimages

        # Cập nhật năng lượng Mega Beam (tự hồi dần chậm)
        if self.mega_energy < 100 and self.mega_beam_timer <= 0:
            if random.random() < 0.25:
                self.mega_energy = min(100, self.mega_energy + 1)

        if self.mega_beam_timer > 0:
            self.mega_beam_timer -= 1

        # Cập nhật vệ tinh Drone
        if self.drone_timer > 0:
            self.drone_timer -= 1
            for drone in self.drones:
                drone.update(self.x, self.y)
        else:
            self.drones.clear()

        # Cập nhật các hiệu ứng khác
        if self.magnet_timer > 0:
            self.magnet_timer -= 1
        if self.freeze_timer > 0:
            self.freeze_timer -= 1
        if self.missile_timer > 0:
            self.missile_timer -= 1

        # Cập nhật thời gian bất tử và búp đạn (sửa triệt để lỗi tàng hình và bất tử vô tận)
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= 1
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1

    def add_score(self, points: int):
        if points > 0:
            self.score += points
            # Hồi 3 năng lượng Mega Beam mỗi khi có điểm
            self.mega_energy = min(100, self.mega_energy + 3)

    def take_damage(self, damage: int = 1) -> bool:
        if self.invulnerable_timer > 0:
            return False

        if self.shield > 0:
            self.shield = max(0, self.shield - damage)
            self.invulnerable_timer = 20
            return False

        self.hp = max(0, self.hp - damage)
        self.invulnerable_timer = 30
        return True

    def heal(self, amount: int = 1):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_shield(self, amount: int = 1):
        self.shield = min(3, self.shield + amount)

    def add_bomb(self, amount: int = 1):
        self.bombs = min(self.max_bombs, self.bombs + amount)

    def use_bomb(self) -> bool:
        if self.bombs > 0:
            self.bombs -= 1
            return True
        return False


class Bullet:
    """Đạn của người chơi hoặc của kẻ địch."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0.0,
        vy: float = -4.0,
        is_enemy: bool = False,
        color: int = 10,
        damage: int = 1,
        owner_id: int = 1,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.is_enemy = is_enemy
        self.color = color
        self.damage = damage
        self.owner_id = owner_id
        self.is_active = True

    def update(self, speed: int = 4, max_x: int = 250, max_y: int = 180):
        self.x += self.vx
        if self.is_enemy:
            self.y += abs(self.vy if self.vy != -4.0 else 2.5)
        else:
            self.y += self.vy if self.vy != -4.0 else -speed

        if self.y < -5 or self.y > max_y or self.x < -5 or self.x > max_x:
            self.is_active = False


class Enemy:
    """Kẻ địch ngoài hành tinh với nhiều chủng loại (Trinh sát, Tuần dương, Cảm tử, Boss)."""

    def __init__(self, x: int, y: int, enemy_type: str = "normal"):
        self.x = float(x)
        self.y = float(y)
        self.enemy_type = enemy_type
        self.shoot_timer = random.randint(40, 90)
        self.boss_dir = 1
        self.frame_offset = random.randint(0, 100)
        self.is_active = True

        if enemy_type == "heavy":
            self.hp = 2
            self.max_hp = 2
            self.speed = 0.8
            self.color = 9
            self.score_value = 20
            self.width = 10
            self.height = 8
        elif enemy_type == "fast":
            self.hp = 1
            self.max_hp = 1
            self.speed = 1.9
            self.color = 14
            self.score_value = 15
            self.width = 7
            self.height = 7
        elif enemy_type == "boss":
            self.hp = 25
            self.max_hp = 25
            self.speed = 0.4
            self.color = 8
            self.score_value = 150
            self.width = 24
            self.height = 14
            self.shoot_timer = 30
        else:  # normal scout
            self.hp = 1
            self.max_hp = 1
            self.speed = 1.3
            self.color = 8
            self.score_value = 10
            self.width = 8
            self.height = 8

    def update(self, speed_factor: float = 1.0, max_w: int = 240, max_h: int = 170):
        actual_speed = self.speed * speed_factor
        if self.enemy_type == "boss":
            if self.y < 16:
                self.y += actual_speed
            else:
                self.x += self.boss_dir * 0.9 * speed_factor
                if self.x <= 6:
                    self.boss_dir = 1
                elif self.x >= max_w - self.width - 6:
                    self.boss_dir = -1
        elif self.enemy_type == "fast":
            self.y += actual_speed
            self.x += math.sin((self.y + self.frame_offset) * 0.12) * 1.2 * speed_factor
            self.x = max(2, min(max_w - 10, self.x))
            if self.y > max_h:
                self.is_active = False
        else:
            self.y += actual_speed
            if self.y > max_h:
                self.is_active = False

    def can_shoot(self) -> bool:
        if self.enemy_type in ("heavy", "boss"):
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = 50 if self.enemy_type == "heavy" else 35
                return True
        return False


class Asteroid:
    """Thiên thạch vũ trụ trôi nổi làm chướng ngại vật hoặc nguồn nhặt vật phẩm."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0.0,
        vy: float = 0.6,
        size: int = 2,
        hp: int = 3,
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.size = size
        self.hp = hp
        self.max_hp = hp
        self.width = 10 if size == 2 else 6
        self.height = 10 if size == 2 else 6
        self.color = 5
        self.is_active = True

    def update(self, max_x: int = 255, max_y: int = 180):
        self.x += self.vx
        self.y += self.vy
        if self.y > max_y or self.y < -20 or self.x < -20 or self.x > max_x:
            self.is_active = False

    def take_damage(self, damage: int = 1) -> bool:
        self.hp -= damage
        if self.hp <= 0:
            self.is_active = False
            return True
        return False


class PowerUp:
    """Vật phẩm hỗ trợ mở rộng phong phú (10 loại vật phẩm hấp dẫn)."""

    KINDS = [
        "triple",   # Đạn 3 tia
        "shield",   # Giáp năng lượng
        "bomb",     # +1 Bom Nova
        "heal",     # Hồi sinh lực
        "rapid",    # Bắn nhanh
        "mega",     # Sạc đầy Mega Beam
        "drone",    # Vệ tinh hộ vệ
        "magnet",   # Nam châm hút vật phẩm
        "freeze",   # Đóng băng thời gian
        "missile",  # Tên lửa tầm nhiệt
    ]

    def __init__(self, x: int, y: int, kind: str = "triple"):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.is_active = True
        self.width = 7
        self.height = 7

        color_map = {
            "triple": 10,   # Vàng
            "shield": 12,   # Xanh ngọc
            "bomb": 9,      # Cam
            "heal": 11,     # Xanh lá
            "rapid": 14,    # Hồng
            "mega": 7,      # Trắng sáng
            "drone": 13,    # Tím nhạt
            "magnet": 10,   # Vàng kim
            "freeze": 6,    # Băng lam
            "missile": 8,   # Đỏ
        }
        self.color = color_map.get(kind, 10)

    def update(self, target_x: Optional[float] = None, target_y: Optional[float] = None, max_y: int = 120):
        if target_x is not None and target_y is not None:
            # Hiệu ứng nam châm hút về phía phi thuyền
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 2:
                self.x += (dx / dist) * 2.8
                self.y += (dy / dist) * 2.8
        else:
            self.y += 1

        if self.y > max_y or self.y < -10 or self.x < -10 or self.x > 220:
            self.is_active = False


class ComboSystem:
    """Hệ thống chuỗi tiêu diệt liên hoàn nhân bội số điểm thưởng (x1 -> x4)."""

    def __init__(self, combo_duration: int = 70):
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_duration = combo_duration
        self.max_combo = 0

    def add_hit(self) -> int:
        self.combo_count += 1
        self.combo_timer = self.combo_duration
        if self.combo_count > self.max_combo:
            self.max_combo = self.combo_count
        return self.get_multiplier()

    def get_multiplier(self) -> int:
        if self.combo_count >= 10:
            return 4
        elif self.combo_count >= 6:
            return 3
        elif self.combo_count >= 3:
            return 2
        return 1

    def update(self):
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo_count = 0


class PvPMatch:
    """Quản lý luật chơi, hiệp đấu, điểm số và đấu trường trong Chế độ Đối kháng 2 người solo."""

    ARENA_NAMES = ["KHONG GIAN MO", "BAO THIEN THACH", "BAO NANG LUONG"]

    def __init__(self, target_wins: int = 2, arena_id: int = 0):
        self.target_wins = target_wins
        self.arena_id = arena_id
        self.p1_wins = 0
        self.p2_wins = 0
        self.current_round = 1
        self.winner = None

    def record_round_win(self, winner_id: int) -> Optional[int]:
        if winner_id == 1:
            self.p1_wins += 1
        elif winner_id == 2:
            self.p2_wins += 1

        self.current_round += 1
        if self.p1_wins >= self.target_wins:
            self.winner = 1
            return 1
        elif self.p2_wins >= self.target_wins:
            self.winner = 2
            return 2
        return None

    def reset_match(self):
        self.p1_wins = 0
        self.p2_wins = 0
        self.current_round = 1
        self.winner = None

    def get_arena_name(self) -> str:
        return self.ARENA_NAMES[self.arena_id % len(self.ARENA_NAMES)]


class StageManager:
    """Quản lý các màn chơi, bối cảnh vũ trụ và điều kiện thăng cấp trong Chế độ Chiến dịch."""

    STAGE_INFO = {
        1: {
            "name": "MAN 1: VANH DAI THIEN THACH",
            "subtitle": "Khai pha khong gian ngoai o",
            "target_score": 180,
            "star_color_offset": 0,
        },
        2: {
            "name": "MAN 2: TINH VAN DO",
            "subtitle": "Ham doi cam tu dot kich",
            "target_score": 400,
            "star_color_offset": 1,
        },
        3: {
            "name": "MAN 3: HANG O TRUM DREADNOUGHT",
            "subtitle": "Dai chien Chien ham Trum cuoi",
            "target_score": 750,
            "star_color_offset": 2,
        },
        4: {
            "name": "MAN 4: KHONG GIAN VO TAN",
            "subtitle": "Sinh ton dinh cao & San diem",
            "target_score": 999999,
            "star_color_offset": 3,
        },
    }

    def __init__(self):
        self.current_stage = 1
        self.stage_transition_timer = 0

    def check_progression(self, score: int) -> bool:
        info = self.STAGE_INFO.get(self.current_stage)
        if info and score >= info["target_score"] and self.current_stage < 4:
            self.current_stage += 1
            self.stage_transition_timer = 70
            return True
        return False

    def get_stage_name(self) -> str:
        return self.STAGE_INFO.get(self.current_stage, {}).get("name", f"MAN {self.current_stage}")