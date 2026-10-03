import random
import pyxel
from src.models import Player, Bullet, Enemy, Star, Particle, PowerUp


class SpaceDefenderApp:
    def __init__(self):
        pyxel.init(160, 120, title="Space Defender 8-Bit - Ultimate Edition")
        
        # Cấu hình âm thanh chuẩn Pyxel 2.x
        pyxel.sounds[0].set("a3 a2", "p", "7", "s", 5)   # Tiếng bắn đạn
        pyxel.sounds[1].set("c2 c1", "n", "7", "f", 10)  # Tiếng nổ
        pyxel.sounds[2].set("g3 c4", "t", "7", "n", 10)  # Tiếng ăn Power-up (ĐÃ SỬA)
        
        self.stars = [Star() for _ in range(30)]
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player = Player(x=76, y=100)
        self.bullets = []
        self.enemies = []
        self.particles = []
        self.powerups = []
        self.game_over = False

    def create_explosion(self, x, y):
        for _ in range(12):
            self.particles.append(Particle(x + 4, y + 4))

    def update(self):
        # Cập nhật nền sao vũ trụ
        for star in self.stars:
            star.update()

        # Cập nhật hạt nổ
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.life > 0]

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Cập nhật thời gian Power-up
        if self.player.triple_shot_timer > 0:
            self.player.triple_shot_timer -= 1

        # Điều khiển di chuyển
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.move_left()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.move_right()

        # Bắn đạn (Đạn đơn hoặc Đạn 3 tia)
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.player.triple_shot_timer > 0:
                self.bullets.append(Bullet(self.player.x + 3, self.player.y, vx=0))
                self.bullets.append(Bullet(self.player.x, self.player.y, vx=-0.8))
                self.bullets.append(Bullet(self.player.x + 6, self.player.y, vx=0.8))
            else:
                self.bullets.append(Bullet(self.player.x + 3, self.player.y, vx=0))
            pyxel.play(0, 0)

        # Sinh kẻ thù (Tốc độ tăng dần theo điểm số)
        spawn_rate = max(12, 30 - (self.player.score // 50))
        if pyxel.frame_count % spawn_rate == 0:
            enemy_x = random.randint(0, 152)
            enemy_type = "heavy" if random.random() < 0.3 else "normal"
            self.enemies.append(Enemy(enemy_x, 0, enemy_type=enemy_type))

        # Cập nhật vị trí
        for bullet in self.bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update()
        for powerup in self.powerups:
            powerup.update()

        # Va chạm: Đạn - Kẻ thù
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.is_active and enemy.is_active:
                    if (bullet.x < enemy.x + 8 and bullet.x + 2 > enemy.x and
                        bullet.y < enemy.y + 8 and bullet.y + 4 > enemy.y):
                        bullet.is_active = False
                        enemy.hp -= 1
                        if enemy.hp <= 0:
                            enemy.is_active = False
                            self.player.add_score(enemy.score_value)
                            self.create_explosion(enemy.x, enemy.y)
                            pyxel.play(1, 1)

                            # Tỷ lệ 15% rơi Power-up
                            if random.random() < 0.15:
                                self.powerups.append(PowerUp(enemy.x, enemy.y))

        # Va chạm: Người chơi - Power-up
        for powerup in self.powerups:
            if powerup.is_active:
                if (self.player.x < powerup.x + 6 and self.player.x + 8 > powerup.x and
                    self.player.y < powerup.y + 6 and self.player.y + 8 > powerup.y):
                    powerup.is_active = False
                    self.player.triple_shot_timer = 180  # 6 giây đạn 3 tia
                    pyxel.play(2, 2)

        # Va chạm: Người chơi - Kẻ thù
        for enemy in self.enemies:
            if enemy.is_active:
                if (self.player.x < enemy.x + 8 and self.player.x + 8 > enemy.x and
                    self.player.y < enemy.y + 8 and self.player.y + 8 > enemy.y):
                    enemy.is_active = False
                    self.create_explosion(enemy.x, enemy.y)
                    self.player.take_damage(1)
                    pyxel.play(1, 1)
                    if self.player.hp <= 0:
                        self.game_over = True

        # Lọc đối tượng
        self.bullets = [b for b in self.bullets if b.is_active]
        self.enemies = [e for e in self.enemies if e.is_active]
        self.powerups = [p for p in self.powerups if p.is_active]

    def draw(self):
        pyxel.cls(0)

        # Vẽ nền sao
        for star in self.stars:
            pyxel.pset(star.x, star.y, star.color)

        # Vẽ hạt nổ
        for particle in self.particles:
            pyxel.pset(int(particle.x), int(particle.y), particle.color)

        if self.game_over:
            pyxel.text(60, 45, "GAME OVER", 8)
            pyxel.text(45, 60, f"FINAL SCORE: {self.player.score}", 7)
            pyxel.text(35, 75, "PRESS 'R' TO RESTART", 10)
            return

        # UI: Score & HP
        pyxel.text(4, 4, f"SCORE:{self.player.score}", 7)
        hp_text = "HP:" + "O" * self.player.hp
        pyxel.text(125, 4, hp_text, 8)

        # Báo hiệu Power-up
        if self.player.triple_shot_timer > 0:
            pyxel.text(4, 14, "TRIPLE SHOT!", 10)

        # Vẽ Người chơi (Xanh da trời)
        pyxel.rect(self.player.x, self.player.y, 8, 8, 11)

        # Vẽ Đạn (Vàng)
        for bullet in self.bullets:
            pyxel.rect(int(bullet.x), int(bullet.y), 2, 4, 10)

        # Vẽ Kẻ thù (Đỏ / Cam)
        for enemy in self.enemies:
            pyxel.rect(enemy.x, enemy.y, 8, 8, enemy.color)

        # Vẽ Power-up (Tím)
        for powerup in self.powerups:
            pyxel.rect(powerup.x, powerup.y, 6, 6, 12)


if __name__ == "__main__":
    SpaceDefenderApp()