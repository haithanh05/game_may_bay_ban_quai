import math
import random
import pyxel
from src.models import (
    Player,
    Bullet,
    Enemy,
    Star,
    Particle,
    PowerUp,
    Shockwave,
    FloatingText,
    ComboSystem,
    Asteroid,
    PvPMatch,
    Drone,
    HomingMissile,
    StageManager,
)


def draw_text_shadow(x: int, y: int, text: str, col: int, shadow_col: int = 0):
    """Vẽ chữ có bóng đen đổ viền giúp chữ luôn siêu sắc nét và dễ đọc trên mọi nền."""
    pyxel.text(x + 1, y + 1, text, shadow_col)
    pyxel.text(x, y, text, col)


def draw_badge(x: int, y: int, text: str, text_col: int, bg_col: int = 0, border_col: int = 1):
    """Vẽ huy hiệu trạng thái bo viền nổi bật."""
    w = len(text) * 4 + 4
    pyxel.rect(x, y - 1, w, 8, bg_col)
    pyxel.rectb(x, y - 1, w, 8, border_col)
    draw_text_shadow(x + 2, y, text, text_col, 0)


class SpaceDefenderApp:
    def __init__(self):
        # Mở rộng bản đồ lên 240 x 160 pixel chuẩn Widescreen Retro Arcade cực kỳ rộng rãi
        pyxel.init(240, 160, title="Space Defender 8-Bit - Ultimate Edition", fps=30)

        # Cấu hình 8 kênh âm thanh chất lượng chuẩn Retro Arcade
        pyxel.sounds[0].set("a3 a2", "p", "7", "s", 4)             # Laser P1
        pyxel.sounds[1].set("c2 c1", "n", "7", "f", 8)             # Vụ nổ
        pyxel.sounds[2].set("c3 e3 g3 c4", "t", "7777", "nnnn", 5)   # Nhặt Power-up
        pyxel.sounds[3].set("f2 c2", "s", "77", "ff", 6)           # Bị trúng đòn
        pyxel.sounds[4].set("c2 g1 c1 f0", "n", "7765", "ffff", 8)   # Bom EMP / Mega Beam
        pyxel.sounds[5].set("g2 d2", "p", "66", "ss", 6)           # Đạn P2 / Địch
        pyxel.sounds[6].set("e3 a3", "p", "66", "nn", 4)           # Combo / Dash
        pyxel.sounds[7].set("f2 a2 d3", "s", "666", "fff", 4)      # Phóng tên lửa Homing

        # Nền sao 3 tầng Parallax trải rộng 240x160
        self.stars = (
            [Star(screen_width=240, screen_height=160, layer=1) for _ in range(28)]
            + [Star(screen_width=240, screen_height=160, layer=2) for _ in range(22)]
            + [Star(screen_width=240, screen_height=160, layer=3) for _ in range(18)]
        )

        self.state = "menu"
        self.prev_state = "campaign"
        self.menu_cursor = 0

        self.high_score = 0
        self.screen_shake = 0
        self.boss_warning_timer = 0
        self.next_boss_score = 450

        self.stage_mgr = StageManager()
        self.pvp_match = PvPMatch(target_wins=2, arena_id=0)
        self.pvp_round_timer = 0
        self.pvp_round_winner = 0
        self.pvp_hazard_timer = 0

        self.reset_campaign()
        self.reset_pvp_round()

        pyxel.run(self.update, self.draw)

    # ========================== RESET & KHỞI TẠO ==========================

    def reset_campaign(self):
        self.player = Player(x=116, y=130, screen_width=240, screen_height=160)
        self.bullets = []
        self.missiles = []
        self.enemies = []
        self.asteroids = []
        self.particles = []
        self.powerups = []
        self.shockwaves = []
        self.floating_texts = []
        self.combo_sys = ComboSystem()
        self.stage_mgr = StageManager()
        self.boss_active = False
        self.boss_warning_timer = 0
        self.screen_shake = 0
        self.game_over = False

    def reset_pvp_round(self):
        # Người chơi 1 & 2 được tự do bay khắp toàn bộ bản đồ 240x160
        self.p1 = Player(
            x=116,
            y=135,
            screen_width=240,
            screen_height=160,
            owner_id=1,
            facing=1,
            min_y=16,   # Bay lên tự do tới sát đỉnh để nhặt vật phẩm
            max_y=150,
        )
        self.p1.hp = 4
        self.p1.shield = 1
        self.p1.bombs = 1

        self.p2 = Player(
            x=116,
            y=24,
            screen_width=240,
            screen_height=160,
            owner_id=2,
            facing=-1,
            min_y=14,
            max_y=148,  # Bay xuống tự do tới sát đáy
        )
        self.p2.hp = 4
        self.p2.shield = 1
        self.p2.bombs = 1

        self.pvp_bullets = []
        self.pvp_missiles = []
        self.pvp_powerups = []
        self.pvp_hazard_timer = 0

        # Thiên thạch theo Đấu trường mở rộng
        if self.pvp_match.arena_id == 1:
            self.pvp_asteroids = [
                Asteroid(x=35, y=55, vx=0.6, vy=0, size=2, hp=3),
                Asteroid(x=195, y=68, vx=-0.5, vy=0, size=2, hp=3),
                Asteroid(x=85, y=80, vx=0.4, vy=0, size=1, hp=2),
                Asteroid(x=150, y=94, vx=-0.4, vy=0, size=1, hp=2),
                Asteroid(x=60, y=108, vx=0.5, vy=0, size=2, hp=3),
            ]
        elif self.pvp_match.arena_id == 2:
            self.pvp_asteroids = [
                Asteroid(x=115, y=80, vx=0.3, vy=0, size=1, hp=2),
            ]
        else:
            self.pvp_asteroids = [
                Asteroid(x=50, y=78, vx=0.4, vy=0, size=2, hp=3),
                Asteroid(x=185, y=82, vx=-0.4, vy=0, size=1, hp=2),
            ]

        self.particles = []
        self.shockwaves = []
        self.floating_texts = []
        self.screen_shake = 0
        self.pvp_round_winner = 0

    def create_explosion(self, x: float, y: float, count: int = 14, is_boss: bool = False):
        total = count * 2 if is_boss else count
        for _ in range(total):
            self.particles.append(Particle(x + 4, y + 4))
        if is_boss:
            self.shockwaves.append(Shockwave(x + 12, y + 7, max_radius=65, color=10))
            self.screen_shake = max(self.screen_shake, 10)
        else:
            self.screen_shake = max(self.screen_shake, 4)

    # ========================== CHẾ ĐỘ CHIẾN DỊCH ==========================

    def trigger_campaign_bomb(self):
        if not self.player.use_bomb():
            return

        self.screen_shake = 12
        pyxel.play(2, 4)
        self.shockwaves.append(Shockwave(self.player.x + 4, self.player.y + 4, max_radius=110, color=7))
        self.shockwaves.append(Shockwave(self.player.x + 4, self.player.y + 4, max_radius=75, color=10))
        self.floating_texts.append(FloatingText("BOM NOVA EMP!", 60, 75, color=10, life=30))

        for bullet in self.bullets:
            if bullet.is_enemy:
                bullet.is_active = False
                for _ in range(3):
                    self.particles.append(Particle(bullet.x, bullet.y, color=10, life=8))

        for enemy in self.enemies:
            if enemy.is_active:
                enemy.hp -= 10
                self.create_explosion(enemy.x, enemy.y, count=8)
                if enemy.hp <= 0:
                    enemy.is_active = False
                    mult = self.combo_sys.add_hit()
                    gained = enemy.score_value * mult
                    self.player.add_score(gained)
                    self.floating_texts.append(FloatingText(f"+{gained}", int(enemy.x), int(enemy.y), color=10))
                    if enemy.enemy_type == "boss":
                        self.boss_active = False
                        self.next_boss_score = self.player.score + 350

    def trigger_campaign_mega_beam(self):
        if not self.player.trigger_mega_beam():
            return

        self.screen_shake = 10
        pyxel.play(2, 4)
        self.floating_texts.append(FloatingText("MEGA LASER!", int(self.player.x) - 10, int(self.player.y) - 8, color=7))
        bx1 = self.player.x - 3
        bx2 = self.player.x + 11
        for enemy in self.enemies:
            if enemy.is_active and (bx1 < enemy.x + getattr(enemy, "width", 8) and bx2 > enemy.x):
                enemy.hp -= 8
                self.create_explosion(enemy.x, enemy.y, count=6)
                if enemy.hp <= 0:
                    enemy.is_active = False
                    mult = self.combo_sys.add_hit()
                    gained = enemy.score_value * mult
                    self.player.add_score(gained)
                    self.floating_texts.append(FloatingText(f"+{gained}", int(enemy.x), int(enemy.y), color=10))
                    if enemy.enemy_type == "boss":
                        self.boss_active = False
                        self.next_boss_score = self.player.score + 350

        for ast in self.asteroids:
            if ast.is_active and (bx1 < ast.x + ast.width and bx2 > ast.x):
                if ast.take_damage(8):
                    self.create_explosion(ast.x, ast.y, count=8)

    def spawn_campaign_enemies(self):
        if self.boss_active or self.boss_warning_timer > 0:
            return

        if self.stage_mgr.current_stage >= 3 and self.player.score >= self.next_boss_score and not self.boss_active:
            self.boss_warning_timer = 60
            pyxel.play(3, 5)
            return

        base_rate = max(8, 25 - self.stage_mgr.current_stage * 3 - (self.player.score // 80))
        if pyxel.frame_count % base_rate == 0:
            enemy_x = random.randint(8, 224)
            rand_val = random.random()
            if self.stage_mgr.current_stage == 1:
                enemy_type = "heavy" if rand_val < 0.2 else "normal"
            elif self.stage_mgr.current_stage == 2:
                enemy_type = "fast" if rand_val < 0.45 else ("heavy" if rand_val < 0.7 else "normal")
            else:
                enemy_type = "fast" if rand_val < 0.4 else ("heavy" if rand_val < 0.75 else "normal")

            self.enemies.append(Enemy(enemy_x, -8, enemy_type=enemy_type))

        ast_rate = 90 if self.stage_mgr.current_stage in (1, 4) else 140
        if pyxel.frame_count % ast_rate == 0 and len(self.asteroids) < 4:
            ax = random.randint(10, 220)
            self.asteroids.append(Asteroid(ax, -12, vx=random.uniform(-0.3, 0.3), vy=0.7))

    def update_campaign(self):
        if self.stage_mgr.check_progression(self.player.score):
            self.screen_shake = 8
            pyxel.play(2, 6)
            self.shockwaves.append(Shockwave(120, 80, max_radius=100, color=10))

        if self.stage_mgr.stage_transition_timer > 0:
            self.stage_mgr.stage_transition_timer -= 1

        # Điều khiển P1
        dx, dy = 0.0, 0.0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.move_left()
            dx -= 1.0
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.move_right()
            dx += 1.0
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.player.move_up()
            dy -= 1.0
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.player.move_down()
            dy += 1.0

        # KỸ NĂNG P1: SHIFT / C cho Dash né đòn
        if pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.KEY_C):
            if self.player.trigger_dash(dx, dy):
                pyxel.play(2, 6)
                self.floating_texts.append(FloatingText("TOC BIEN!", int(self.player.x) - 4, int(self.player.y), color=11))

        # KỸ NĂNG P1: Phím R cho Mega Beam
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.KEY_E):
            self.trigger_campaign_mega_beam()

        # KỸ NĂNG P1: Phím T cho Bom Nova EMP
        if pyxel.btnp(pyxel.KEY_T) or pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.KEY_F) or pyxel.btnp(pyxel.KEY_X):
            self.trigger_campaign_bomb()

        # Lửa phản lực đuôi
        is_boosting = pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)
        if pyxel.frame_count % (1 if is_boosting else 2) == 0:
            flame_vy = random.uniform(1.8, 3.2) if is_boosting else random.uniform(0.8, 1.8)
            self.particles.append(Particle(self.player.x + 2, self.player.y + 9, vy=flame_vy, is_flame=True))
            self.particles.append(Particle(self.player.x + 5, self.player.y + 9, vy=flame_vy, is_flame=True))

        # ĐÈ PHÍM SPACE ĐỂ BẮN LIÊN TỤC (Tự động xả đạn không cần bấm từng lần)
        can_shoot = False
        if self.player.rapid_fire_timer > 0:
            if pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count % 3 == 0:
                can_shoot = True
        else:
            if (pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count % 6 == 0) or pyxel.btnp(pyxel.KEY_SPACE):
                can_shoot = True

        if can_shoot:
            px, py = self.player.x, self.player.y
            if self.player.triple_shot_timer > 0:
                # Bắn 3 tia laser mở rộng
                self.bullets.append(Bullet(px + 3, py, vx=0, vy=-4.8, color=10))
                self.bullets.append(Bullet(px - 2, py + 2, vx=-1.4, vy=-4.2, color=10))
                self.bullets.append(Bullet(px + 8, py + 2, vx=1.4, vy=-4.2, color=10))
            elif self.player.rapid_fire_timer > 0:
                # Bắn đạn kép siêu tốc
                self.bullets.append(Bullet(px + 1, py, vx=0, vy=-5.8, color=14))
                self.bullets.append(Bullet(px + 5, py, vx=0, vy=-5.8, color=14))
            else:
                self.bullets.append(Bullet(px + 3, py, vx=0, vy=-4.8, color=10))
            # Chớp sáng nòng pháo (Muzzle flash)
            self.particles.append(Particle(px + 3, py - 2, vx=0, vy=-0.5, color=7, life=2))
            pyxel.play(0, 0)

        for drone in self.player.drones:
            if drone.can_shoot():
                self.bullets.append(Bullet(drone.x + 1, drone.y, vx=0, vy=-4.2, color=13))

        if self.player.missile_timer > 0 and pyxel.frame_count % 30 == 0:
            self.missiles.append(HomingMissile(self.player.x - 2, self.player.y, vx=-1.0, vy=-2.0, owner_id=1))
            self.missiles.append(HomingMissile(self.player.x + 10, self.player.y, vx=1.0, vy=-2.0, owner_id=1))
            pyxel.play(2, 7)

        # Cập nhật kỹ năng người chơi (tự động giảm thời gian bất tử, triệt tiêu lỗi tàng hình)
        self.player.update_skills()
        self.combo_sys.update()

        if self.boss_warning_timer > 0:
            self.boss_warning_timer -= 1
            if self.boss_warning_timer == 0:
                self.boss_active = True
                self.enemies.append(Enemy(88, -14, enemy_type="boss"))

        self.spawn_campaign_enemies()

        for bullet in self.bullets:
            bullet.update()
        for mis in self.missiles:
            mis.update(self.enemies)

        speed_factor = 0.4 if self.player.freeze_timer > 0 else 1.0
        for enemy in self.enemies:
            enemy.update(speed_factor=speed_factor)
        for ast in self.asteroids:
            ast.update()

        mag_x = self.player.x if self.player.magnet_timer > 0 else None
        mag_y = self.player.y if self.player.magnet_timer > 0 else None
        for powerup in self.powerups:
            powerup.update(target_x=mag_x, target_y=mag_y, max_y=150)

        for enemy in self.enemies:
            if enemy.is_active and enemy.can_shoot():
                if enemy.enemy_type == "heavy":
                    self.bullets.append(Bullet(enemy.x + 4, enemy.y + 8, vx=0, vy=2.6, is_enemy=True, color=9))
                    pyxel.play(3, 5)
                elif enemy.enemy_type == "boss":
                    self.bullets.append(Bullet(enemy.x + 4, enemy.y + 12, vx=-1.0, vy=2.2, is_enemy=True, color=8))
                    self.bullets.append(Bullet(enemy.x + 12, enemy.y + 13, vx=0.0, vy=2.8, is_enemy=True, color=8))
                    self.bullets.append(Bullet(enemy.x + 20, enemy.y + 12, vx=1.0, vy=2.2, is_enemy=True, color=8))
                    pyxel.play(3, 5)

        for bullet in self.bullets:
            if not bullet.is_active or bullet.is_enemy:
                continue
            for enemy in self.enemies:
                if not enemy.is_active:
                    continue
                ew = getattr(enemy, "width", 8)
                eh = getattr(enemy, "height", 8)
                if (
                    bullet.x < enemy.x + ew
                    and bullet.x + 2 > enemy.x
                    and bullet.y < enemy.y + eh
                    and bullet.y + 4 > enemy.y
                ):
                    bullet.is_active = False
                    enemy.hp -= bullet.damage
                    for _ in range(3):
                        self.particles.append(Particle(bullet.x, bullet.y, color=10, life=6))

                    if enemy.hp <= 0:
                        self.destroy_enemy(enemy)

        for mis in self.missiles:
            if not mis.is_active or mis.owner_id != 1:
                continue
            for enemy in self.enemies:
                if not enemy.is_active:
                    continue
                if (
                    mis.x < enemy.x + getattr(enemy, "width", 8)
                    and mis.x + 3 > enemy.x
                    and mis.y < enemy.y + getattr(enemy, "height", 8)
                    and mis.y + 3 > enemy.y
                ):
                    mis.is_active = False
                    enemy.hp -= mis.damage
                    self.create_explosion(mis.x, mis.y, count=6)
                    if enemy.hp <= 0:
                        self.destroy_enemy(enemy)

        for bullet in self.bullets:
            if not bullet.is_active or bullet.is_enemy:
                continue
            for ast in self.asteroids:
                if not ast.is_active:
                    continue
                if (
                    bullet.x < ast.x + ast.width
                    and bullet.x + 2 > ast.x
                    and bullet.y < ast.y + ast.height
                    and bullet.y + 4 > ast.y
                ):
                    bullet.is_active = False
                    if ast.take_damage(1):
                        self.create_explosion(ast.x, ast.y, count=8)
                        pyxel.play(1, 1)
                        self.player.add_score(5)
                        if random.random() < 0.35:
                            self.powerups.append(PowerUp(ast.x + 2, ast.y + 2, kind=random.choice(PowerUp.KINDS)))

        for powerup in self.powerups:
            if not powerup.is_active:
                continue
            if (
                abs((self.player.x + 4) - (powerup.x + 3.5)) < 10
                and abs((self.player.y + 4) - (powerup.y + 3.5)) < 10
            ):
                powerup.is_active = False
                pyxel.play(2, 2)
                self.apply_campaign_powerup(powerup.kind, powerup.x, powerup.y)

        for bullet in self.bullets:
            if not bullet.is_active or not bullet.is_enemy:
                continue
            if (
                self.player.x < bullet.x + 3
                and self.player.x + 8 > bullet.x
                and self.player.y < bullet.y + 3
                and self.player.y + 8 > bullet.y
            ):
                bullet.is_active = False
                hit = self.player.take_damage(1)
                self.screen_shake = 6
                if hit:
                    self.create_explosion(self.player.x, self.player.y, count=6)
                    pyxel.play(1, 3)
                else:
                    self.floating_texts.append(FloatingText("GIAP DA DO!", self.player.x - 6, self.player.y, color=12))
                    pyxel.play(2, 2)

                if self.player.hp <= 0:
                    self.game_over = True
                    self.state = "gameover"
                    pyxel.play(1, 1)

        for enemy in self.enemies:
            if not enemy.is_active:
                continue
            ew = getattr(enemy, "width", 8)
            eh = getattr(enemy, "height", 8)
            if (
                self.player.x < enemy.x + ew
                and self.player.x + 8 > enemy.x
                and self.player.y < enemy.y + eh
                and self.player.y + 8 > enemy.y
            ):
                if enemy.enemy_type != "boss":
                    enemy.is_active = False
                    self.create_explosion(enemy.x, enemy.y, count=10)

                hit = self.player.take_damage(1)
                self.screen_shake = 8
                if hit:
                    pyxel.play(1, 3)
                else:
                    self.floating_texts.append(FloatingText("GIAP DA DO!", self.player.x - 6, self.player.y, color=12))
                    pyxel.play(2, 2)

                if self.player.hp <= 0:
                    self.game_over = True
                    self.state = "gameover"
                    pyxel.play(1, 1)

        self.bullets = [b for b in self.bullets if b.is_active]
        self.missiles = [m for m in self.missiles if m.is_active]
        self.enemies = [e for e in self.enemies if e.is_active]
        self.asteroids = [a for a in self.asteroids if a.is_active]
        self.powerups = [p for p in self.powerups if p.is_active]

        if self.player.score > self.high_score:
            self.high_score = self.player.score

    def destroy_enemy(self, enemy: Enemy):
        enemy.is_active = False
        is_boss = enemy.enemy_type == "boss"
        self.create_explosion(enemy.x, enemy.y, count=12, is_boss=is_boss)
        pyxel.play(1, 1)

        mult = self.combo_sys.add_hit()
        if mult > 1:
            pyxel.play(2, 6)
            self.floating_texts.append(FloatingText(f"LIEN HOAN x{mult}!", 80, 30, color=10))

        gained = enemy.score_value * mult
        self.player.add_score(gained)
        self.floating_texts.append(FloatingText(f"+{gained}", int(enemy.x), int(enemy.y), color=7))

        if is_boss:
            self.boss_active = False
            self.next_boss_score = self.player.score + 350
            self.floating_texts.append(FloatingText("TRUM DA BI TIEU DIET!", 50, 60, color=10, life=40))
            self.powerups.append(PowerUp(enemy.x + 4, enemy.y + 6, kind="shield"))
            self.powerups.append(PowerUp(enemy.x + 14, enemy.y + 6, kind="mega"))
        else:
            if random.random() < 0.28:
                kind = random.choice(PowerUp.KINDS)
                self.powerups.append(PowerUp(enemy.x + 2, enemy.y + 2, kind=kind))

    def apply_campaign_powerup(self, kind: str, x: float, y: float):
        ix, iy = int(x), int(y)
        if kind == "triple":
            self.player.triple_shot_timer = 200
            self.floating_texts.append(FloatingText("DAN 3 TIA!", ix, iy, color=10))
        elif kind == "shield":
            self.player.add_shield(1)
            self.floating_texts.append(FloatingText("GIAP NANG LUONG!", ix, iy, color=12))
        elif kind == "bomb":
            self.player.add_bomb(1)
            self.floating_texts.append(FloatingText("+1 BOM EMP!", ix, iy, color=9))
        elif kind == "heal":
            self.player.heal(1)
            self.floating_texts.append(FloatingText("+1 HOI MAU!", ix, iy, color=11))
        elif kind == "rapid":
            self.player.rapid_fire_timer = 180
            self.floating_texts.append(FloatingText("BAN NHANH!", ix, iy, color=14))
        elif kind == "mega":
            self.player.mega_energy = 100
            self.floating_texts.append(FloatingText("MEGA LASER SAN SANG!", ix - 10, iy, color=7))
        elif kind == "drone":
            self.player.add_drone()
            self.floating_texts.append(FloatingText("+VE TINH HO VE!", ix - 5, iy, color=13))
        elif kind == "magnet":
            self.player.magnet_timer = 240
            self.floating_texts.append(FloatingText("NAM CHAM HUT!", ix, iy, color=10))
        elif kind == "freeze":
            self.player.freeze_timer = 150
            self.floating_texts.append(FloatingText("DONG BANG THOI GIAN!", ix - 10, iy, color=6))
        elif kind == "missile":
            self.player.missile_timer = 200
            self.floating_texts.append(FloatingText("TEN LUA TAM NHIET!", ix - 10, iy, color=8))

    # ========================== CHẾ ĐỘ ĐỐI KHÁNG 2 NGƯỜI (PVP) ==========================

    def trigger_pvp_bomb(self, player: Player, target_player: Player):
        if not player.use_bomb():
            return

        self.screen_shake = 10
        pyxel.play(2, 4)
        self.shockwaves.append(Shockwave(player.x + 4, player.y + 4, max_radius=85, color=10 if player.owner_id == 1 else 9))
        self.floating_texts.append(FloatingText(f"P{player.owner_id} BOM EMP!", int(player.x) - 10, int(player.y), color=10))

        for bullet in self.pvp_bullets:
            if bullet.owner_id != player.owner_id:
                bullet.is_active = False
                self.particles.append(Particle(bullet.x, bullet.y, color=10, life=6))

        dist = math.hypot(player.x - target_player.x, player.y - target_player.y)
        if dist < 70:
            hit = target_player.take_damage(1)
            if hit:
                self.create_explosion(target_player.x, target_player.y, count=6)
                pyxel.play(1, 3)

    def update_pvp(self):
        if pyxel.btnp(pyxel.KEY_TAB):
            self.pvp_match.arena_id = (self.pvp_match.arena_id + 1) % len(PvPMatch.ARENA_NAMES)
            self.floating_texts.append(FloatingText(f"DAU TRUONG: {self.pvp_match.get_arena_name()}", 45, 75, color=10))

        # 1. NGƯỜI CHƠI 1: W, A, S, D, SPACE, R (Mega Beam), T (Bom Nova EMP), SHIFT/C (Dash)
        dx1, dy1 = 0.0, 0.0
        if pyxel.btn(pyxel.KEY_A):
            self.p1.move_left()
            dx1 -= 1.0
        if pyxel.btn(pyxel.KEY_D):
            self.p1.move_right()
            dx1 += 1.0
        if pyxel.btn(pyxel.KEY_W):
            self.p1.move_up()
            dy1 -= 1.0
        if pyxel.btn(pyxel.KEY_S):
            self.p1.move_down()
            dy1 += 1.0

        if pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.KEY_C):
            if self.p1.trigger_dash(dx1, dy1):
                pyxel.play(2, 6)
                self.floating_texts.append(FloatingText("P1 DASH!", int(self.p1.x) - 4, int(self.p1.y), color=11))

        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.KEY_E):
            if self.p1.trigger_mega_beam():
                pyxel.play(2, 4)
                self.screen_shake = 8
                self.floating_texts.append(FloatingText("P1 MEGA BEAM!", int(self.p1.x) - 8, int(self.p1.y), color=7))
                if abs(self.p1.x - self.p2.x) < 12:
                    self.p2.take_damage(2)

        if pyxel.btnp(pyxel.KEY_T) or pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.KEY_F):
            self.trigger_pvp_bomb(self.p1, self.p2)

        if pyxel.frame_count % 2 == 0:
            self.particles.append(Particle(self.p1.x + 2, self.p1.y + 9, vy=1.4, is_flame=True))
            self.particles.append(Particle(self.p1.x + 5, self.p1.y + 9, vy=1.4, is_flame=True))

        # ĐÈ PHÍM SPACE ĐỂ P1 XẢ ĐẠN LIÊN TỤC (Tự động xả đạn không cần bấm từng lần)
        can_shoot_p1 = False
        if self.p1.rapid_fire_timer > 0:
            if pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count % 3 == 0:
                can_shoot_p1 = True
        else:
            if (pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count % 6 == 0) or pyxel.btnp(pyxel.KEY_SPACE):
                can_shoot_p1 = True

        if can_shoot_p1:
            px, py = self.p1.x, self.p1.y
            if self.p1.triple_shot_timer > 0:
                self.pvp_bullets.append(Bullet(px + 3, py, vx=0, vy=-4.8, owner_id=1, color=10))
                self.pvp_bullets.append(Bullet(px - 2, py + 2, vx=-1.4, vy=-4.2, owner_id=1, color=10))
                self.pvp_bullets.append(Bullet(px + 8, py + 2, vx=1.4, vy=-4.2, owner_id=1, color=10))
            elif self.p1.rapid_fire_timer > 0:
                self.pvp_bullets.append(Bullet(px + 1, py, vx=0, vy=-5.8, owner_id=1, color=11))
                self.pvp_bullets.append(Bullet(px + 5, py, vx=0, vy=-5.8, owner_id=1, color=11))
            else:
                self.pvp_bullets.append(Bullet(px + 3, py, vx=0, vy=-4.8, owner_id=1, color=10))
            self.particles.append(Particle(px + 3, py - 2, vx=0, vy=-0.5, color=7, life=2))
            pyxel.play(0, 0)

        # 2. NGƯỜI CHƠI 2: MŨI TÊN, ENTER/K, PHÍM 1 (Bom EMP), PHÍM 2 (Mega Beam), PHÍM 0 (Dash)
        dx2, dy2 = 0.0, 0.0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.p2.move_left()
            dx2 -= 1.0
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.p2.move_right()
            dx2 += 1.0
        if pyxel.btn(pyxel.KEY_UP):
            self.p2.move_up()
            dy2 -= 1.0
        if pyxel.btn(pyxel.KEY_DOWN):
            self.p2.move_down()
            dy2 += 1.0

        # P2 Dash: Phím 0 / Numpad 0 / RCTRL
        if pyxel.btnp(pyxel.KEY_0) or pyxel.btnp(pyxel.KEY_KP_0) or pyxel.btnp(pyxel.KEY_RCTRL):
            if self.p2.trigger_dash(dx2, dy2):
                pyxel.play(2, 6)
                self.floating_texts.append(FloatingText("P2 DASH!", int(self.p2.x) - 4, int(self.p2.y), color=14))

        # P2 Mega Beam: Phím 2 / Numpad 2
        if pyxel.btnp(pyxel.KEY_2) or pyxel.btnp(pyxel.KEY_KP_2):
            if self.p2.trigger_mega_beam():
                pyxel.play(2, 4)
                self.screen_shake = 8
                self.floating_texts.append(FloatingText("P2 MEGA BEAM!", int(self.p2.x) - 8, int(self.p2.y), color=7))
                if abs(self.p1.x - self.p2.x) < 14:
                    self.p1.take_damage(2)

        # P2 Bom EMP: Phím 1 / Numpad 1
        if pyxel.btnp(pyxel.KEY_1) or pyxel.btnp(pyxel.KEY_KP_1):
            self.trigger_pvp_bomb(self.p2, self.p1)

        if pyxel.frame_count % 2 == 0:
            self.particles.append(Particle(self.p2.x + 2, self.p2.y, vy=-1.4, is_flame=True))
            self.particles.append(Particle(self.p2.x + 5, self.p2.y, vy=-1.4, is_flame=True))

        # ĐÈ PHÍM ENTER ĐỂ P2 XẢ ĐẠN LIÊN TỤC (Tự động xả đạn không cần bấm từng lần)
        p2_shoot_btn = (
            pyxel.btn(pyxel.KEY_RETURN)
            or pyxel.btn(pyxel.KEY_KP_ENTER)
            or pyxel.btn(pyxel.KEY_K)
            or pyxel.btn(pyxel.KEY_RSHIFT)
        )
        p2_shoot_btnp = (
            pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.KEY_KP_ENTER)
            or pyxel.btnp(pyxel.KEY_K)
            or pyxel.btnp(pyxel.KEY_RSHIFT)
        )

        can_shoot_p2 = False
        if self.p2.rapid_fire_timer > 0:
            if p2_shoot_btn and pyxel.frame_count % 3 == 0:
                can_shoot_p2 = True
        else:
            if (p2_shoot_btn and pyxel.frame_count % 6 == 0) or p2_shoot_btnp:
                can_shoot_p2 = True

        if can_shoot_p2:
            px, py = self.p2.x, self.p2.y
            if self.p2.triple_shot_timer > 0:
                self.pvp_bullets.append(Bullet(px + 3, py + 8, vx=0, vy=4.8, owner_id=2, color=9))
                self.pvp_bullets.append(Bullet(px - 2, py + 6, vx=-1.4, vy=4.2, owner_id=2, color=9))
                self.pvp_bullets.append(Bullet(px + 8, py + 6, vx=1.4, vy=4.2, owner_id=2, color=9))
            elif self.p2.rapid_fire_timer > 0:
                self.pvp_bullets.append(Bullet(px + 1, py + 8, vx=0, vy=5.8, owner_id=2, color=14))
                self.pvp_bullets.append(Bullet(px + 5, py + 8, vx=0, vy=5.8, owner_id=2, color=14))
            else:
                self.pvp_bullets.append(Bullet(px + 3, py + 8, vx=0, vy=4.8, owner_id=2, color=9))
            self.particles.append(Particle(px + 3, py + 10, vx=0, vy=0.5, color=7, life=2))
            pyxel.play(3, 5)

        # Cập nhật kỹ năng P1 & P2 (tự động đếm lùi invulnerable_timer, xóa hoàn toàn lỗi tàng hình)
        self.p1.update_skills()
        self.p2.update_skills()

        # CƠ CHẾ ĐẶC BIỆT CỦA CÁC ĐẤU TRƯỜNG PVP MỞ RỘNG
        if self.pvp_match.arena_id == 0:
            # ĐẤU TRƯỜNG 1: KHÔNG GIAN MỞ - 2 Cột năng lượng vũ trụ tại x=40 và x=200 nạp Mega Beam khi tiếp cận
            for pylon_x in (40, 200):
                if math.hypot((self.p1.x + 4) - pylon_x, (self.p1.y + 4) - 80) < 22:
                    if pyxel.frame_count % 3 == 0:
                        self.p1.mega_energy = min(100, self.p1.mega_energy + 1)
                        self.particles.append(Particle(pylon_x + random.randint(-4, 4), 80 + random.randint(-4, 4), color=11, life=4))
                if math.hypot((self.p2.x + 4) - pylon_x, (self.p2.y + 4) - 80) < 22:
                    if pyxel.frame_count % 3 == 0:
                        self.p2.mega_energy = min(100, self.p2.mega_energy + 1)
                        self.particles.append(Particle(pylon_x + random.randint(-4, 4), 80 + random.randint(-4, 4), color=14, life=4))

        elif self.pvp_match.arena_id == 2:
            # ĐẤU TRƯỜNG 3: BÃO NĂNG LƯỢNG & LƯỚI ĐIỆN PLASMA NGUY HIỂM Ở GIỮA SÂN
            self.pvp_hazard_timer = (self.pvp_hazard_timer + 1) % 180
            if self.pvp_hazard_timer < 35:
                # Bão plasma đang quét qua vạch giữa (y=76..84)
                if 76 <= self.p1.y <= 84:
                    if self.p1.take_damage(1):
                        self.create_explosion(self.p1.x, self.p1.y, count=8)
                        pyxel.play(1, 3)
                        self.floating_texts.append(FloatingText("P1 BI GIAT DIEN!", int(self.p1.x) - 10, int(self.p1.y), color=9))
                    self.screen_shake = 5
                if 76 <= self.p2.y <= 84:
                    if self.p2.take_damage(1):
                        self.create_explosion(self.p2.x, self.p2.y, count=8)
                        pyxel.play(1, 3)
                        self.floating_texts.append(FloatingText("P2 BI GIAT DIEN!", int(self.p2.x) - 10, int(self.p2.y), color=9))
                    self.screen_shake = 5

        for drone in self.p1.drones:
            if drone.can_shoot():
                self.pvp_bullets.append(Bullet(drone.x + 1, drone.y, vx=0, vy=-4.2, owner_id=1, color=13))
        for drone in self.p2.drones:
            if drone.can_shoot():
                self.pvp_bullets.append(Bullet(drone.x + 1, drone.y + 4, vx=0, vy=4.2, owner_id=2, color=13))

        if self.p1.missile_timer > 0 and pyxel.frame_count % 35 == 0:
            self.pvp_missiles.append(HomingMissile(self.p1.x + 4, self.p1.y, vx=0, vy=-2.0, owner_id=1))
        if self.p2.missile_timer > 0 and pyxel.frame_count % 35 == 0:
            self.pvp_missiles.append(HomingMissile(self.p2.x + 4, self.p2.y + 8, vx=0, vy=2.0, owner_id=2))

        for bullet in self.pvp_bullets:
            bullet.update(max_x=245, max_y=165)
        for mis in self.pvp_missiles:
            target = [self.p2] if mis.owner_id == 1 else [self.p1]
            mis.update(target)

        for ast in self.pvp_asteroids:
            ast.update(max_x=255, max_y=180)
            if ast.x <= 4 or ast.x >= 226:
                ast.vx = -ast.vx

        # Tiếp tế rơi ở khu vực chiến trường mở rộng 240x160
        drop_rate = 75 if self.pvp_match.arena_id == 2 else 115
        if pyxel.frame_count % drop_rate == 0 and len(self.pvp_powerups) < 4:
            kind = random.choice(PowerUp.KINDS)
            px = random.randint(25, 215)
            py = random.randint(50, 110)
            self.pvp_powerups.append(PowerUp(px, py, kind=kind))

        # Va chạm đạn P1 - P2 triệt tiêu lẫn nhau (Laser Clash bùng nổ hoa lửa)
        for b1 in self.pvp_bullets:
            if not b1.is_active or b1.owner_id != 1:
                continue
            for b2 in self.pvp_bullets:
                if not b2.is_active or b2.owner_id != 2:
                    continue
                if abs(b1.x - b2.x) < 5 and abs(b1.y - b2.y) < 6:
                    b1.is_active = False
                    b2.is_active = False
                    for _ in range(4):
                        self.particles.append(Particle((b1.x + b2.x) / 2, (b1.y + b2.y) / 2, color=7, life=6))
                    pyxel.play(3, 5)

        for bullet in self.pvp_bullets:
            if not bullet.is_active:
                continue
            for ast in self.pvp_asteroids:
                if not ast.is_active:
                    continue
                if (
                    bullet.x < ast.x + ast.width
                    and bullet.x + 2 > ast.x
                    and bullet.y < ast.y + ast.height
                    and bullet.y + 4 > ast.y
                ):
                    bullet.is_active = False
                    if ast.take_damage(1):
                        self.create_explosion(ast.x, ast.y, count=10)
                        pyxel.play(1, 1)
                        # 60% tỉ lệ nổ thiên thạch rơi vật phẩm tiếp tế hấp dẫn
                        if random.random() < 0.60:
                            drop_kind = random.choice(["shield", "triple", "bomb", "heal", "rapid", "mega"])
                            self.pvp_powerups.append(PowerUp(int(ast.x), int(ast.y), kind=drop_kind))

        # Đạn P1 trúng P2
        for bullet in self.pvp_bullets:
            if not bullet.is_active or bullet.owner_id != 1:
                continue
            if (
                bullet.x < self.p2.x + 8
                and bullet.x + 2 > self.p2.x
                and bullet.y < self.p2.y + 8
                and bullet.y + 4 > self.p2.y
            ):
                bullet.is_active = False
                hit = self.p2.take_damage(1)
                self.screen_shake = 6
                if hit:
                    self.create_explosion(self.p2.x, self.p2.y, count=6)
                    pyxel.play(1, 3)
                else:
                    self.floating_texts.append(FloatingText("P2 DO GIAP!", int(self.p2.x) - 4, int(self.p2.y) + 8, color=12))
                    pyxel.play(2, 2)

        # Đạn P2 trúng P1
        for bullet in self.pvp_bullets:
            if not bullet.is_active or bullet.owner_id != 2:
                continue
            if (
                bullet.x < self.p1.x + 8
                and bullet.x + 2 > self.p1.x
                and bullet.y < self.p1.y + 8
                and bullet.y + 4 > self.p1.y
            ):
                bullet.is_active = False
                hit = self.p1.take_damage(1)
                self.screen_shake = 6
                if hit:
                    self.create_explosion(self.p1.x, self.p1.y, count=6)
                    pyxel.play(1, 3)
                else:
                    self.floating_texts.append(FloatingText("P1 DO GIAP!", int(self.p1.x) - 4, int(self.p1.y) - 6, color=12))
                    pyxel.play(2, 2)

        # Nhặt vật phẩm trong PvP: Hitbox 10px rộng mở, cả P1 và P2 nhặt siêu mượt mà
        for pup in self.pvp_powerups:
            if not pup.is_active:
                continue
            if (
                abs((self.p1.x + 4) - (pup.x + 3.5)) < 10
                and abs((self.p1.y + 4) - (pup.y + 3.5)) < 10
            ):
                pup.is_active = False
                pyxel.play(2, 2)
                self.apply_pvp_powerup(self.p1, pup.kind)

            if (
                abs((self.p2.x + 4) - (pup.x + 3.5)) < 10
                and abs((self.p2.y + 4) - (pup.y + 3.5)) < 10
            ):
                pup.is_active = False
                pyxel.play(2, 2)
                self.apply_pvp_powerup(self.p2, pup.kind)

        # Kết thúc hiệp đấu
        if self.p1.hp <= 0:
            self.create_explosion(self.p1.x, self.p1.y, count=20)
            pyxel.play(1, 1)
            self.pvp_round_winner = 2
            match_winner = self.pvp_match.record_round_win(2)
            pyxel.play(2, 6)
            self.state = "pvp_match_end" if match_winner else "pvp_round_end"
            self.pvp_round_timer = 90

        elif self.p2.hp <= 0:
            self.create_explosion(self.p2.x, self.p2.y, count=20)
            pyxel.play(1, 1)
            self.pvp_round_winner = 1
            match_winner = self.pvp_match.record_round_win(1)
            pyxel.play(2, 6)
            self.state = "pvp_match_end" if match_winner else "pvp_round_end"
            self.pvp_round_timer = 90

        self.pvp_bullets = [b for b in self.pvp_bullets if b.is_active]
        self.pvp_missiles = [m for m in self.pvp_missiles if m.is_active]
        self.pvp_powerups = [p for p in self.pvp_powerups if p.is_active]
        self.pvp_asteroids = [a for a in self.pvp_asteroids if a.is_active]

    def apply_pvp_powerup(self, player: Player, kind: str):
        pid = f"P{player.owner_id}"
        ix, iy = int(player.x), int(player.y)
        if kind == "triple":
            player.triple_shot_timer = 180
            self.floating_texts.append(FloatingText(f"{pid}: DAN 3 TIA!", ix, iy, color=10))
        elif kind == "shield":
            player.add_shield(1)
            self.floating_texts.append(FloatingText(f"{pid}: +1 GIAP!", ix, iy, color=12))
        elif kind == "bomb":
            player.add_bomb(1)
            self.floating_texts.append(FloatingText(f"{pid}: +1 BOM!", ix, iy, color=9))
        elif kind == "heal":
            player.heal(1)
            self.floating_texts.append(FloatingText(f"{pid}: +1 MAU!", ix, iy, color=11))
        elif kind == "rapid":
            player.rapid_fire_timer = 160
            self.floating_texts.append(FloatingText(f"{pid}: BAN NHANH!", ix, iy, color=14))
        elif kind == "mega":
            player.mega_energy = 100
            self.floating_texts.append(FloatingText(f"{pid}: MEGA BEAM!", ix, iy, color=7))
        elif kind == "drone":
            player.add_drone()
            self.floating_texts.append(FloatingText(f"{pid}: +VE TINH!", ix, iy, color=13))
        elif kind == "missile":
            player.missile_timer = 180
            self.floating_texts.append(FloatingText(f"{pid}: TEN LUA!", ix, iy, color=8))

    # ========================== VÒNG LẶP UPDATE ==========================

    def update(self):
        for star in self.stars:
            star.update(screen_height=160)

        if self.screen_shake > 0:
            self.screen_shake -= 1

        for pt in self.particles:
            pt.update()
        for wave in self.shockwaves:
            wave.update()
        for ftext in self.floating_texts:
            ftext.update()
        self.particles = [pt for pt in self.particles if pt.life > 0]
        self.shockwaves = [w for w in self.shockwaves if w.is_active]
        self.floating_texts = [t for t in self.floating_texts if t.is_active]

        if pyxel.btnp(pyxel.KEY_P) and self.state in ("campaign", "pvp", "paused"):
            if self.state == "paused":
                self.state = self.prev_state
            else:
                self.prev_state = self.state
                self.state = "paused"
            return

        if (pyxel.btnp(pyxel.KEY_M) or pyxel.btnp(pyxel.KEY_ESCAPE)) and self.state in ("paused", "help", "gameover", "pvp_match_end"):
            self.state = "menu"
            return

        if self.state == "menu":
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
                self.menu_cursor = (self.menu_cursor - 1) % 3
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                self.menu_cursor = (self.menu_cursor + 1) % 3

            if pyxel.btnp(pyxel.KEY_1):
                self.menu_cursor = 0
            if pyxel.btnp(pyxel.KEY_2):
                self.menu_cursor = 1
            if pyxel.btnp(pyxel.KEY_3):
                self.menu_cursor = 2

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                if self.menu_cursor == 0:
                    self.reset_campaign()
                    self.state = "campaign"
                elif self.menu_cursor == 1:
                    self.pvp_match.reset_match()
                    self.reset_pvp_round()
                    self.state = "pvp"
                elif self.menu_cursor == 2:
                    self.state = "help"
            return

        if self.state == "help":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.state = "menu"
            return

        if self.state == "paused":
            return

        if self.state == "campaign":
            self.update_campaign()
            return

        if self.state == "gameover":
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_campaign()
                self.state = "campaign"
            return

        if self.state == "pvp":
            self.update_pvp()
            return

        if self.state == "pvp_round_end":
            self.pvp_round_timer -= 1
            if self.pvp_round_timer <= 0 or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_pvp_round()
                self.state = "pvp"
            return

        if self.state == "pvp_match_end":
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_R):
                self.pvp_match.reset_match()
                self.reset_pvp_round()
                self.state = "pvp"
            return

    # ========================== PHẦN ĐỒ HỌA & HIỂN THỊ ==========================

    def draw_player_ship(self, player: Player):
        """Vẽ phi thuyền với đồ họa pixel chất lượng cao và tự động biến đổi diện mạo theo Power-up."""
        x = int(player.x)
        y = int(player.y)

        # Vẽ bóng mờ tốc biến Dash
        for ax, ay, afacing, alife in player.afterimages:
            ghost_col = 5 if alife < 3 else (12 if player.owner_id == 1 else 14)
            pyxel.rectb(int(ax), int(ay), 8, 8, ghost_col)

        # Chớp nháy nhẹ khi bất tử (chỉ chớp nháy ngắn, tuyệt đối không bị tàng hình vô tận)
        if player.invulnerable_timer > 0 and (player.invulnerable_timer // 2) % 2 == 1:
            return

        is_p2 = player.owner_id == 2 and player.facing == -1

        if not is_p2:
            # ================= P1: BLUE FALCON (HƯỚNG LÊN) =================
            # 1. Thân chính và cánh
            pyxel.rect(x + 3, y + 1, 2, 7, 11)   # Thân xanh ngọc
            pyxel.rect(x + 2, y + 4, 4, 3, 1)    # Khung thân xanh navy
            pyxel.rect(x, y + 6, 8, 2, 1)        # Sải cánh ngang
            pyxel.pset(x + 4, y, 7)              # Mũi nhọn trắng
            pyxel.pset(x + 3, y + 2, 7)          # Kính buồng lái lấp lánh (Specular glint)
            pyxel.pset(x + 4, y + 2, 12)
            pyxel.pset(x, y + 5, 10)             # Nòng pháo laser
            pyxel.pset(x + 7, y + 5, 10)
            pyxel.pset(x + 2, y + 7, 9)          # Động cơ đáy
            pyxel.pset(x + 5, y + 7, 9)

            # BIẾN HÌNH KHI CÓ TRIPLE SHOT: Mọc thêm 2 bệ súng ngoài sải cánh màu vàng
            if player.triple_shot_timer > 0:
                pyxel.rect(x - 2, y + 4, 2, 4, 10)
                pyxel.rect(x + 8, y + 4, 2, 4, 10)
                pyxel.pset(x - 2, y + 3, 7)
                pyxel.pset(x + 9, y + 3, 7)

            # BIẾN HÌNH KHI CÓ RAPID LASER: Mũi tàu nạp súng plasma kép màu hồng tím
            if player.rapid_fire_timer > 0:
                pyxel.rect(x + 2, y - 1, 1, 3, 14)
                pyxel.rect(x + 5, y - 1, 1, 3, 14)
                pyxel.pset(x + 2, y - 1, 7)
                pyxel.pset(x + 5, y - 1, 7)

            # BIẾN HÌNH KHI CÓ MEGA BEAM: Lõi năng lượng ở tâm thân tàu phát sáng trắng vàng rực rỡ
            if player.mega_energy >= 100 or player.mega_beam_timer > 0:
                core_pulse = 7 if (pyxel.frame_count // 3) % 2 == 0 else 10
                pyxel.rect(x + 3, y + 4, 2, 2, core_pulse)

        else:
            # ================= P2: CRIMSON VIPER (HƯỚNG XUỐNG) =================
            pyxel.rect(x + 3, y, 2, 7, 8)        # Thân đỏ
            pyxel.rect(x + 2, y + 1, 4, 3, 2)    # Khung thân tím
            pyxel.rect(x, y, 8, 2, 2)            # Sải cánh trên
            pyxel.pset(x + 4, y + 7, 7)          # Mũi nhọn trắng
            pyxel.pset(x + 3, y + 5, 10)         # Kính buồng lái vàng
            pyxel.pset(x + 4, y + 5, 7)
            pyxel.pset(x, y + 2, 9)              # Nòng pháo
            pyxel.pset(x + 7, y + 2, 9)
            pyxel.pset(x + 2, y, 14)             # Động cơ đỉnh
            pyxel.pset(x + 5, y, 14)

            # P2 BIẾN HÌNH TRIPLE SHOT
            if player.triple_shot_timer > 0:
                pyxel.rect(x - 2, y, 2, 4, 9)
                pyxel.rect(x + 8, y, 2, 4, 9)
                pyxel.pset(x - 2, y + 4, 7)
                pyxel.pset(x + 9, y + 4, 7)

            # P2 BIẾN HÌNH RAPID LASER
            if player.rapid_fire_timer > 0:
                pyxel.rect(x + 2, y + 6, 1, 3, 14)
                pyxel.rect(x + 5, y + 6, 1, 3, 14)

            # P2 BIẾN HÌNH MEGA BEAM
            if player.mega_energy >= 100 or player.mega_beam_timer > 0:
                core_pulse = 7 if (pyxel.frame_count // 3) % 2 == 0 else 14
                pyxel.rect(x + 3, y + 2, 2, 2, core_pulse)

        # Cảnh báo bốc khói khi HP thấp (chỉ còn 1 HP)
        if player.hp == 1 and pyxel.frame_count % 3 == 0:
            smoke_col = 5 if pyxel.frame_count % 6 == 0 else 8
            self.particles.append(Particle(x + 4, y + 4, vy=random.uniform(-0.5, 0.5), color=smoke_col, life=8))

        # Vòng khiên năng lượng bảo vệ
        if player.shield > 0:
            pulse = (pyxel.frame_count % 3)
            col = 12 if player.owner_id == 1 else 14
            pyxel.circb(x + 4, y + 4, 8 + pulse, col)
            angle = (pyxel.frame_count * 0.2)
            sx = int(x + 4 + math.cos(angle) * 8)
            sy = int(y + 4 + math.sin(angle) * 8)
            pyxel.pset(sx, sy, 7)

        # Vệ tinh Drone xoay quanh
        for drone in player.drones:
            dx, dy = int(drone.x), int(drone.y)
            pyxel.rect(dx, dy, 3, 3, 13)
            pyxel.pset(dx + 1, dy + 1, 7)

        # Cột Siêu Pháo Mega Beam hủy diệt (rộng 8 pixel, lõi trắng sáng chói)
        if player.mega_beam_timer > 0:
            beam_x = x
            bw = 8
            beam_col = 10 if (pyxel.frame_count % 2 == 0) else 12
            if not is_p2:
                # Bắn lên chạm đỉnh
                pyxel.rect(beam_x, 0, bw, y, beam_col)
                pyxel.rect(beam_x + 2, 0, bw - 4, y, 7)
            else:
                # Bắn xuống chạm đáy
                pyxel.rect(beam_x, y + 8, bw, 160 - (y + 8), 14 if (pyxel.frame_count % 2 == 0) else 7)
                pyxel.rect(beam_x + 2, y + 8, bw - 4, 160 - (y + 8), 7)

    def draw_asteroid(self, ast: Asteroid):
        x, y = int(ast.x), int(ast.y)
        w, h = ast.width, ast.height
        pyxel.rect(x + 1, y, w - 2, h, 5)
        pyxel.rect(x, y + 1, w, h - 2, 5)
        pyxel.pset(x + 2, y + 2, 6)
        pyxel.pset(x + w - 3, y + 3, 4)
        pyxel.pset(x + 3, y + h - 3, 4)

    def draw_enemy(self, enemy: Enemy):
        x, y = int(enemy.x), int(enemy.y)
        if enemy.enemy_type == "boss":
            # Trùm chiến hạm khổng lồ
            pyxel.rect(x + 6, y, 12, 12, 5)
            pyxel.rect(x + 2, y + 3, 20, 7, 1)
            pyxel.rect(x, y + 6, 24, 4, 2)
            core_col = 8 if (enemy.hp <= 8 and (pyxel.frame_count // 3) % 2 == 0) else 10
            pyxel.rect(x + 10, y + 4, 4, 4, core_col)
            pyxel.pset(x + 11, y + 5, 7)
            pyxel.rect(x + 2, y + 10, 2, 3, 9)
            pyxel.rect(x + 20, y + 10, 2, 3, 9)
        elif enemy.enemy_type == "heavy":
            pyxel.rect(x + 2, y, 6, 7, 9)
            pyxel.rect(x, y + 2, 10, 4, 4)
            pyxel.pset(x + 4, y + 3, 10)
            pyxel.pset(x + 5, y + 3, 10)
            pyxel.pset(x + 1, y + 6, 8)
            pyxel.pset(x + 8, y + 6, 8)
            hp_w = max(0, int((enemy.hp / enemy.max_hp) * 8))
            pyxel.rect(x + 1, y - 2, 8, 1, 0)
            pyxel.rect(x + 1, y - 2, hp_w, 1, 11)
        elif enemy.enemy_type == "fast":
            pyxel.tri(x + 3, y + 6, x, y, x + 6, y, 14)
            pyxel.pset(x + 3, y + 2, 10)
            pyxel.pset(x + 3, y + 6, 7)
        else:
            pyxel.rect(x + 2, y + 1, 4, 6, 8)
            pyxel.rect(x, y + 2, 8, 2, 9)
            pyxel.pset(x + 3, y + 3, 7)
            pyxel.pset(x + 4, y + 3, 10)

    def draw_powerup(self, powerup: PowerUp):
        x, y = int(powerup.x), int(powerup.y)
        pyxel.rect(x, y, 7, 7, 0)
        pyxel.rectb(x, y, 7, 7, powerup.color)
        pyxel.pset(x + 1, y + 1, 7)
        labels = {
            "triple": "3",
            "shield": "S",
            "bomb": "B",
            "heal": "+",
            "rapid": "R",
            "mega": "M",
            "drone": "D",
            "magnet": "U",
            "freeze": "F",
            "missile": "T",
        }
        pyxel.text(x + 2, y + 1, labels.get(powerup.kind, "?"), powerup.color)

    # ========================== GIAO DIỆN MÀN HÌNH ==========================

    def draw_menu(self):
        pyxel.camera(0, 0)
        pyxel.rect(28, 12, 184, 136, 0)
        pyxel.rectb(28, 12, 184, 136, 1)
        pyxel.rectb(30, 14, 180, 132, 5)

        draw_text_shadow(72, 22, "SPACE DEFENDER", 10, 0)
        draw_text_shadow(60, 34, "--- 8-BIT ULTIMATE ---", 12, 0)

        options = [
            ("1. CHIEN DICH (1 NGUOI)", "4 Man choi & Trum cuoi"),
            ("2. DOI KHANG (2 NGUOI)", "Solo PvP tren ban phim"),
            ("3. HUONG DAN CHOI", "Phim bam & cac ky nang"),
        ]

        for i, (opt, sub) in enumerate(options):
            oy = 52 + i * 24
            is_selected = self.menu_cursor == i

            bg = 1 if is_selected else 0
            border = 10 if is_selected else 5
            pyxel.rect(42, oy - 2, 156, 18, bg)
            pyxel.rectb(42, oy - 2, 156, 18, border)

            if is_selected:
                cursor_char = ">" if (pyxel.frame_count // 10) % 2 == 0 else " "
                draw_text_shadow(46, oy + 1, cursor_char, 10, 0)
                draw_text_shadow(54, oy + 1, opt, 10, 0)
                draw_text_shadow(54, oy + 9, sub, 7, 0)
            else:
                draw_text_shadow(54, oy + 1, opt, 7, 0)
                draw_text_shadow(54, oy + 9, sub, 6, 0)

        draw_text_shadow(62, 132, "W/S: CHON  |  SPACE: VAO GAME", 7, 0)

    def draw_help(self):
        pyxel.camera(0, 0)
        pyxel.rect(12, 6, 216, 148, 0)
        pyxel.rectb(12, 6, 216, 148, 1)

        draw_text_shadow(70, 10, "HUONG DAN & KY NANG MOI", 10, 0)
        pyxel.line(16, 20, 224, 20, 1)

        draw_text_shadow(18, 24, "[NGUOI CHOI 1 - XANH NGOC]", 11, 0)
        draw_text_shadow(22, 34, "W,A,S,D : Bay 4 huong     | DE SPACE: Xa dan lien tuc", 7, 0)
        draw_text_shadow(22, 44, "PHIM R  : MEGA BEAM phao  | PHIM T  : BOM NOVA EMP", 10, 0)
        draw_text_shadow(22, 54, "SHIFT/C : DASH ne don bat tu", 9, 0)

        draw_text_shadow(18, 66, "[NGUOI CHOI 2 - DO CAM SOLO]", 14, 0)
        draw_text_shadow(22, 76, "MUI TEN : Bay 4 huong     | DE ENTER: Xa dan lien tuc", 7, 0)
        draw_text_shadow(22, 86, "PHIM 2  : MEGA BEAM phao  | PHIM 1  : BOM NOVA EMP", 10, 0)
        draw_text_shadow(22, 96, "PHIM 0  : DASH ne don     | TAB     : DOI DAU TRUONG", 9, 0)

        draw_text_shadow(18, 110, "[10 VAT PHAM]: 3:Dan3  S:Giap  B:Bom  +:Mau  R:Nhanh", 12, 0)
        draw_text_shadow(18, 120, "               M:Beam  D:Drone  U:Hut  F:Freeze  T:Rocket", 12, 0)

        draw_text_shadow(54, 138, "NHAN [SPACE] HOAC [ESC] VE MENU", 7, 0)

    def draw_campaign_hud(self):
        pyxel.rect(0, 0, 240, 14, 0)
        pyxel.line(0, 14, 240, 14, 1)

        draw_badge(3, 3, f"M{self.stage_mgr.current_stage}", 10, 0, 10)
        draw_badge(25, 3, f"SC:{self.player.score:05d}", 7, 0, 1)
        draw_badge(80, 3, f"HI:{self.high_score:05d}", 6, 0, 1)

        draw_badge(135, 3, f"HP:{self.player.hp}", 8 if self.player.hp > 1 else 9, 0, 8)
        if self.player.shield > 0:
            draw_badge(175, 3, f"S:{self.player.shield}", 12, 0, 12)
        draw_badge(205, 3, f"B:{self.player.bombs}", 9, 0, 9)

        # Thanh kỹ năng dưới
        dash_ready = self.player.dash_cooldown == 0
        draw_text_shadow(3, 149, "[DASH:SHIFT]" if dash_ready else f"DASH:{self.player.dash_cooldown//10}", 11 if dash_ready else 5, 0)

        beam_ready = self.player.mega_energy >= 100
        draw_text_shadow(75, 149, "[BEAM:R]" if beam_ready else f"BEAM:{self.player.mega_energy}%", 10 if beam_ready else 6, 0)

        draw_text_shadow(130, 149, "[BOM:T]", 9 if self.player.bombs > 0 else 5, 0)

        if self.player.triple_shot_timer > 0:
            draw_badge(175, 148, "DAN 3 TIA", 10, 0, 10)
        elif self.player.rapid_fire_timer > 0:
            draw_badge(175, 148, "BAN NHANH", 14, 0, 14)
        elif self.player.freeze_timer > 0:
            draw_badge(175, 148, "DONG BANG", 6, 0, 6)
        elif self.player.magnet_timer > 0:
            draw_badge(175, 148, "NAM CHAM", 10, 0, 10)

        if self.combo_sys.combo_count >= 2:
            mult = self.combo_sys.get_multiplier()
            draw_badge(175, 16, f"x{mult} LIEN HOAN!", 10 if mult > 2 else 7, 0, 10)

        # Banner chuyển Màn chơi
        if self.stage_mgr.stage_transition_timer > 0:
            pyxel.rect(50, 68, 140, 24, 0)
            pyxel.rectb(50, 68, 140, 24, 10)
            draw_text_shadow(60, 72, self.stage_mgr.get_stage_name(), 10, 0)
            draw_text_shadow(64, 81, StageManager.STAGE_INFO[self.stage_mgr.current_stage]["subtitle"], 7, 0)

        # Thanh máu Boss
        for enemy in self.enemies:
            if enemy.enemy_type == "boss" and enemy.is_active:
                pyxel.rect(55, 26, 130, 5, 0)
                pyxel.rectb(55, 26, 130, 5, 8)
                ratio = max(0.0, enemy.hp / enemy.max_hp)
                bar_w = int(ratio * 128)
                pyxel.rect(56, 27, bar_w, 3, 8 if ratio < 0.3 else 10)
                draw_text_shadow(72, 19, "TRUM: VOID DREADNOUGHT", 8, 0)
                break

    def draw_pvp_hud(self):
        # Dải ngăn cách giữa sân tại y=80
        pyxel.line(0, 80, 240, 80, 1)
        for i in range(0, 240, 8):
            pyxel.pset(i, 80, 5)

        # Hiển thị đặc trưng của Đấu trường
        if self.pvp_match.arena_id == 0:
            # 2 Trạm năng lượng tiếp đạn tại x=40 và x=200
            for px in (40, 200):
                r_col = 11 if (pyxel.frame_count // 6) % 2 == 0 else 10
                pyxel.circb(px, 80, 6, r_col)
                pyxel.circ(px, 80, 2, 7)
                draw_text_shadow(px - 14, 88, "[TRAM N/L]", 6, 0)
        elif self.pvp_match.arena_id == 2:
            # Lưới điện bão plasma nguy hiểm
            if 145 <= self.pvp_hazard_timer < 180:
                warn_col = 9 if (pyxel.frame_count // 3) % 2 == 0 else 10
                pyxel.line(0, 80, 240, 80, warn_col)
                if (pyxel.frame_count // 4) % 2 == 0:
                    draw_text_shadow(80, 72, "! CANH BAO: BAO PLASMA !", warn_col, 0)
            elif self.pvp_hazard_timer < 35:
                for lx in range(0, 240, 6):
                    py_off = random.randint(-2, 2)
                    pyxel.line(lx, 80 + py_off, lx + 6, 80 - py_off, 7 if random.random() < 0.5 else 10)
                draw_text_shadow(84, 72, "! NGUY HIEM: BAO PLASMA !", 10, 0)

        # Tỷ số hiệp giữa đỉnh
        p1_stars = "O" * self.pvp_match.p1_wins + "-" * (self.pvp_match.target_wins - self.pvp_match.p1_wins)
        p2_stars = "O" * self.pvp_match.p2_wins + "-" * (self.pvp_match.target_wins - self.pvp_match.p2_wins)
        pyxel.rect(86, 1, 68, 10, 0)
        pyxel.rectb(86, 1, 68, 10, 10)
        draw_text_shadow(90, 3, f"P1:{p1_stars}  VS  P2:{p2_stars}", 10, 0)

        draw_badge(2, 2, self.pvp_match.get_arena_name(), 6, 0, 1)

        # Thông số P2
        draw_badge(184, 2, f"P2 MAU:{self.p2.hp}", 8 if self.p2.hp > 1 else 9, 0, 8)
        if self.p2.shield > 0:
            draw_badge(184, 11, f"GIAP:{self.p2.shield}", 14, 0, 14)
        draw_text_shadow(148, 21, "[1]BOM [2]BEAM [0]DASH", 6, 0)

        # Thông số P1
        draw_badge(2, 148, f"P1 MAU:{self.p1.hp}", 11 if self.p1.hp > 1 else 9, 0, 11)
        if self.p1.shield > 0:
            draw_badge(52, 148, f"GIAP:{self.p1.shield}", 12, 0, 12)
        draw_badge(96, 148, f"BOM:{self.p1.bombs}", 9, 0, 9)
        draw_text_shadow(145, 148, "[R]BEAM [T]BOM [TAB]MAP", 5, 0)

    def draw(self):
        ox = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        oy = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        pyxel.camera(-ox, -oy)

        pyxel.cls(0)

        color_offset = 0
        if self.state == "campaign":
            color_offset = StageManager.STAGE_INFO.get(self.stage_mgr.current_stage, {}).get("star_color_offset", 0)

        for star in self.stars:
            col = star.color
            if color_offset == 1 and col == 5:
                col = 2  # Tinh vân đỏ tím
            elif color_offset == 2 and col == 5:
                col = 4  # Tinh vân đen tối
            pyxel.pset(star.x, star.y, col)

        for wave in self.shockwaves:
            pyxel.circb(int(wave.x), int(wave.y), int(wave.radius), wave.color)

        for pt in self.particles:
            pyxel.pset(int(pt.x), int(pt.y), pt.color)

        if self.state == "menu":
            self.draw_menu()
            return

        if self.state == "help":
            self.draw_help()
            return

        # CHIẾN DỊCH
        if self.state in ("campaign", "gameover") or (self.state == "paused" and self.prev_state == "campaign"):
            for bullet in self.bullets:
                bx, by = int(bullet.x), int(bullet.y)
                if bullet.is_enemy:
                    pyxel.circ(bx + 1, by + 1, 1, bullet.color)
                    pyxel.pset(bx + 1, by + 1, 7)
                else:
                    # Tia đạn laser có lõi sáng trắng cực đẹp
                    pyxel.rect(bx, by, 2, 5, bullet.color)
                    pyxel.line(bx, by, bx, by + 3, 7)

            for mis in self.missiles:
                pyxel.rect(int(mis.x), int(mis.y), 2, 3, 8)
                pyxel.pset(int(mis.x), int(mis.y), 7)

            for ast in self.asteroids:
                self.draw_asteroid(ast)

            for powerup in self.powerups:
                self.draw_powerup(powerup)

            for enemy in self.enemies:
                self.draw_enemy(enemy)

            if self.player.hp > 0:
                self.draw_player_ship(self.player)

            for ftext in self.floating_texts:
                draw_text_shadow(ftext.x, int(ftext.y), ftext.text, ftext.color, 0)

            if self.boss_warning_timer > 0 and (self.boss_warning_timer // 6) % 2 == 0:
                pyxel.rect(60, 60, 120, 16, 8)
                pyxel.rectb(60, 60, 120, 16, 7)
                draw_text_shadow(65, 65, "! BAO DONG: TRUM DREADNOUGHT !", 7, 0)

            pyxel.camera(0, 0)
            self.draw_campaign_hud()

            if self.state == "gameover":
                pyxel.rect(60, 48, 120, 64, 0)
                pyxel.rectb(60, 48, 120, 64, 8)
                draw_text_shadow(80, 54, "KET THUC TRO CHOI", 8, 0)
                draw_text_shadow(70, 66, f"TONG DIEM : {self.player.score}", 7, 0)
                draw_text_shadow(70, 76, f"DIEM KYLUC: {self.high_score}", 10, 0)
                draw_text_shadow(70, 86, f"CHUOI MAX : x{self.combo_sys.max_combo}", 11, 0)
                draw_text_shadow(66, 98, "R:CHOI LAI  |  M:MENU", 7, 0)

        # ĐỐI KHÁNG (PVP)
        if self.state in ("pvp", "pvp_round_end", "pvp_match_end") or (self.state == "paused" and self.prev_state == "pvp"):
            for bullet in self.pvp_bullets:
                bx, by = int(bullet.x), int(bullet.y)
                pyxel.rect(bx, by, 2, 5, bullet.color)
                pyxel.line(bx, by, bx, by + 3, 7)

            for mis in self.pvp_missiles:
                pyxel.rect(int(mis.x), int(mis.y), 2, 3, 8)

            for ast in self.pvp_asteroids:
                self.draw_asteroid(ast)

            for pup in self.pvp_powerups:
                self.draw_powerup(pup)

            if self.p1.hp > 0:
                self.draw_player_ship(self.p1)
            if self.p2.hp > 0:
                self.draw_player_ship(self.p2)

            for ftext in self.floating_texts:
                draw_text_shadow(ftext.x, int(ftext.y), ftext.text, ftext.color, 0)

            pyxel.camera(0, 0)
            self.draw_pvp_hud()

            if self.state == "pvp_round_end":
                pyxel.rect(50, 56, 140, 42, 0)
                pyxel.rectb(50, 56, 140, 42, 10)
                draw_text_shadow(54, 62, f"NGUOI CHOI {self.pvp_round_winner} THANG HIEP NAY!", 10, 0)
                draw_text_shadow(58, 73, "CHUAN BI HIEP TIEP THEO...", 7, 0)
                if (pyxel.frame_count // 10) % 2 == 0:
                    draw_text_shadow(62, 84, "NHAN [SPACE] DE VAO NGAY", 6, 0)

            if self.state == "pvp_match_end":
                pyxel.rect(48, 48, 144, 56, 0)
                pyxel.rectb(48, 48, 144, 56, 10)
                draw_text_shadow(60, 54, "CHUC MUNG NHA VO DICH!", 10, 0)
                draw_text_shadow(54, 66, f"NGUOI CHOI {self.pvp_match.winner} CHIEN THANG!", 11, 0)
                draw_text_shadow(64, 77, f"TI SO: {self.pvp_match.p1_wins} - {self.pvp_match.p2_wins}", 7, 0)
                draw_text_shadow(56, 89, "SPACE:TAI DAU | M:VE MENU", 6, 0)

        # TẠM DỪNG
        if self.state == "paused":
            pyxel.camera(0, 0)
            pyxel.rect(70, 62, 100, 28, 0)
            pyxel.rectb(70, 62, 100, 28, 10)
            draw_text_shadow(100, 67, "TAM DUNG", 10, 0)
            draw_text_shadow(78, 77, "P: TIEP TUC  |  M: MENU", 7, 0)


if __name__ == "__main__":
    SpaceDefenderApp()