import random

class Star:
    def __init__(self, screen_width=160, screen_height=120):
        self.x = random.randint(0, screen_width - 1)
        self.y = random.randint(0, screen_height - 1)
        self.speed = random.choice([1, 2, 3])
        self.color = 5 if self.speed == 1 else (6 if self.speed == 2 else 7)

    def update(self, screen_height=120):
        self.y += self.speed
        if self.y >= screen_height:
            self.y = 0
            self.x = random.randint(0, 159)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        self.life = random.randint(5, 12)
        self.color = random.choice([8, 9, 10])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1


class Player:
    def __init__(self, x: int, y: int, screen_width: int = 160):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.score = 0
        self.hp = 3
        self.triple_shot_timer = 0

    def move_left(self, speed: int = 2):
        self.x = max(0, self.x - speed)

    def move_right(self, speed: int = 2):
        self.x = min(self.screen_width - 8, self.x + speed)

    def add_score(self, points: int):
        if points > 0:
            self.score += points

    def take_damage(self, damage: int = 1):
        self.hp = max(0, self.hp - damage)


class Bullet:
    def __init__(self, x: int, y: int, vx: float = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.is_active = True

    def update(self, speed: int = 4):
        self.x += self.vx
        self.y -= speed
        if self.y < 0 or self.x < 0 or self.x > 160:
            self.is_active = False


class Enemy:
    def __init__(self, x: int, y: int, enemy_type: str = "normal"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        if enemy_type == "heavy":
            self.hp = 2
            self.speed = 0.8
            self.color = 9
            self.score_value = 20
        else:
            self.hp = 1
            self.speed = 1.3
            self.color = 8
            self.score_value = 10
        self.is_active = True

    def update(self):
        self.y += self.speed
        if self.y > 120:
            self.is_active = False


class PowerUp:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_active = True

    def update(self):
        self.y += 1
        if self.y > 120:
            self.is_active = False