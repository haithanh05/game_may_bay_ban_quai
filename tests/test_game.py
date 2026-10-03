from src.models import Player, Bullet, Enemy, Star, PowerUp


def test_player_hp_and_damage():
    player = Player(x=50, y=100)
    assert player.hp == 3
    player.take_damage(1)
    assert player.hp == 2


def test_heavy_enemy_properties():
    enemy = Enemy(x=50, y=10, enemy_type="heavy")
    assert enemy.hp == 2
    assert enemy.score_value == 20


def test_starfield_wrap_around():
    star = Star(screen_width=160, screen_height=120)
    star.y = 120
    star.update(screen_height=120)
    assert star.y == 0


def test_powerup_movement():
    powerup = PowerUp(x=50, y=120)
    powerup.update()
    assert powerup.is_active is False