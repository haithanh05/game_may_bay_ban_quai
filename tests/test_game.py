from src.models import (
    Player,
    Bullet,
    Enemy,
    Star,
    PowerUp,
    ComboSystem,
    Shockwave,
    Particle,
    Asteroid,
    PvPMatch,
)


def test_player_hp_and_damage():
    player = Player(x=50, y=100)
    assert player.hp == 3
    player.take_damage(1)
    assert player.hp == 2


def test_player_4way_movement():
    player = Player(x=50, y=100, screen_width=160, screen_height=120)
    
    # Bay sang trái và sang phải
    player.move_left(speed=10)
    assert player.x == 40
    player.move_right(speed=20)
    assert player.x == 60

    # Bay lên và bay xuống
    player.move_up(speed=30)
    assert player.y == 70
    player.move_down(speed=15)
    assert player.y == 85

    # Kiểm tra giới hạn biên màn hình
    player.move_up(speed=200)
    assert player.y >= 14
    player.move_down(speed=200)
    assert player.y <= 110
    player.move_left(speed=200)
    assert player.x == 0
    player.move_right(speed=200)
    assert player.x == 160 - 8


def test_player_shield_absorption():
    player = Player(x=50, y=100)
    player.add_shield(2)
    assert player.shield == 2

    # Đòn đánh thứ nhất bị giáp cản hoàn toàn, HP không đổi
    hit = player.take_damage(1)
    assert hit is False
    assert player.hp == 3
    assert player.shield == 1

    # Đặt lại invulnerable_timer để nhận đòn tiếp theo
    player.invulnerable_timer = 0
    player.take_damage(1)
    assert player.shield == 0
    assert player.hp == 3

    # Hết giáp, đòn đánh kế tiếp sẽ trừ trực tiếp vào HP
    player.invulnerable_timer = 0
    hit = player.take_damage(1)
    assert hit is True
    assert player.hp == 2


def test_player_heal_and_bomb():
    player = Player(x=50, y=100)
    player.hp = 2
    player.heal(1)
    assert player.hp == 3
    player.heal(10)
    assert player.hp == player.max_hp

    # Kiểm tra sử dụng bom EMP
    assert player.bombs == 1
    assert player.use_bomb() is True
    assert player.bombs == 0
    assert player.use_bomb() is False
    player.add_bomb(2)
    assert player.bombs == 2


def test_heavy_enemy_properties():
    enemy = Enemy(x=50, y=10, enemy_type="heavy")
    assert enemy.hp == 2
    assert enemy.score_value == 20


def test_boss_enemy_properties_and_patrol():
    boss = Enemy(x=60, y=0, enemy_type="boss")
    assert boss.hp == 25
    assert boss.score_value == 150
    assert boss.enemy_type == "boss"

    boss.update()
    assert boss.y > 0

    boss.y = 16
    prev_x = boss.x
    boss.update()
    assert boss.x != prev_x


def test_fast_enemy_movement():
    fast = Enemy(x=50, y=10, enemy_type="fast")
    assert fast.speed > 1.5
    fast.update()
    assert fast.y > 10


def test_enemy_shooting():
    heavy = Enemy(x=50, y=20, enemy_type="heavy")
    heavy.shoot_timer = 1
    assert heavy.can_shoot() is True
    assert heavy.shoot_timer > 1


def test_starfield_wrap_around():
    star = Star(screen_width=160, screen_height=120)
    star.y = 120
    star.update(screen_height=120)
    assert star.y == 0


def test_powerup_movement():
    powerup = PowerUp(x=50, y=120)
    powerup.update()
    assert powerup.is_active is False


def test_powerup_kinds_and_colors():
    for kind in ["triple", "shield", "bomb", "heal", "rapid"]:
        pup = PowerUp(x=20, y=20, kind=kind)
        assert pup.kind == kind
        assert pup.color in [9, 10, 11, 12, 14]


def test_bullet_movement_and_bounds():
    # Đạn người chơi (bay lên)
    player_bullet = Bullet(x=50, y=50, vx=0, vy=-4.0, is_enemy=False, owner_id=1)
    player_bullet.update()
    assert player_bullet.y < 50
    assert player_bullet.owner_id == 1

    # Đạn P2 (bay xuống)
    p2_bullet = Bullet(x=50, y=50, vx=0, vy=4.5, is_enemy=False, owner_id=2)
    p2_bullet.update()
    assert p2_bullet.y > 50
    assert p2_bullet.owner_id == 2

    # Đạn địch (bay xuống)
    enemy_bullet = Bullet(x=50, y=50, vx=0, vy=3.0, is_enemy=True)
    enemy_bullet.update()
    assert enemy_bullet.y > 50

    # Văng khỏi màn hình
    out_bullet = Bullet(x=50, y=-6, vy=-4.0)
    out_bullet.update()
    assert out_bullet.is_active is False


def test_combo_system():
    combo = ComboSystem(combo_duration=50)
    assert combo.get_multiplier() == 1

    for _ in range(3):
        mult = combo.add_hit()
    assert mult == 2

    for _ in range(3):
        mult = combo.add_hit()
    assert mult == 3

    for _ in range(4):
        mult = combo.add_hit()
    assert mult == 4

    combo.combo_timer = 1
    combo.update()
    assert combo.combo_count == 0
    assert combo.get_multiplier() == 1


def test_shockwave_and_particles():
    wave = Shockwave(x=50, y=50, max_radius=20)
    assert wave.radius < 10
    wave.update(speed=25)
    assert wave.is_active is False

    flame = Particle(x=50, y=50, is_flame=True)
    assert flame.life > 0
    flame.update()
    assert flame.life < 7


def test_pvp_player_facing_and_boundaries():
    # P1 (nửa dưới)
    p1 = Player(x=76, y=98, owner_id=1, facing=1, min_y=64, max_y=110)
    assert p1.facing == 1
    assert p1.owner_id == 1
    p1.move_up(speed=100)
    assert p1.y == 64  # Bị chặn ở vạch giữa sân
    p1.move_down(speed=100)
    assert p1.y == 110

    # P2 (nửa trên)
    p2 = Player(x=76, y=18, owner_id=2, facing=-1, min_y=14, max_y=56)
    assert p2.facing == -1
    assert p2.owner_id == 2
    p2.move_down(speed=100)
    assert p2.y == 56  # Bị chặn ở vạch giữa sân
    p2.move_up(speed=100)
    assert p2.y == 14


def test_pvp_match_flow():
    match = PvPMatch(target_wins=2)
    assert match.p1_wins == 0
    assert match.p2_wins == 0
    assert match.winner is None

    # Hiệp 1: P1 thắng
    winner = match.record_round_win(1)
    assert winner is None
    assert match.p1_wins == 1
    assert match.current_round == 2

    # Hiệp 2: P2 gỡ hòa
    winner = match.record_round_win(2)
    assert winner is None
    assert match.p2_wins == 1
    assert match.current_round == 3

    # Hiệp 3: P1 kết liễu trận đấu
    winner = match.record_round_win(1)
    assert winner == 1
    assert match.winner == 1

    # Đặt lại trận đấu
    match.reset_match()
    assert match.p1_wins == 0
    assert match.p2_wins == 0
    assert match.current_round == 1
    assert match.winner is None


def test_asteroid_mechanics():
    ast = Asteroid(x=30, y=50, vx=0.5, vy=0.2, size=2, hp=3)
    assert ast.hp == 3
    assert ast.is_active is True

    ast.update()
    assert ast.x == 30.5
    assert ast.y == 50.2

    # Bị bắn trúng 1 hit
    destroyed = ast.take_damage(1)
    assert destroyed is False
    assert ast.hp == 2
    assert ast.is_active is True

    # Bị bắn thêm 2 hit nổ tung
    destroyed = ast.take_damage(2)
    assert destroyed is True
    assert ast.is_active is False


def test_stage_manager_progression():
    from src.models import StageManager
    sm = StageManager()
    assert sm.current_stage == 1
    assert "MAN 1" in sm.get_stage_name()

    # Chưa đủ điểm qua màn
    assert sm.check_progression(score=100) is False
    assert sm.current_stage == 1

    # Đạt 180 điểm -> qua Màn 2
    assert sm.check_progression(score=180) is True
    assert sm.current_stage == 2
    assert "MAN 2" in sm.get_stage_name()

    # Đạt 400 điểm -> qua Màn 3
    assert sm.check_progression(score=400) is True
    assert sm.current_stage == 3
    assert "MAN 3" in sm.get_stage_name()


def test_pvp_arenas():
    match = PvPMatch(arena_id=0)
    assert "KHONG GIAN MO" in match.get_arena_name()
    match.arena_id = 1
    assert "BAO THIEN THACH" in match.get_arena_name()
    match.arena_id = 2
    assert "BAO NANG LUONG" in match.get_arena_name()


def test_player_dash_and_skills():
    player = Player(x=50, y=50)
    assert player.dash_cooldown == 0
    # Kích hoạt Dash
    assert player.trigger_dash(dx=1.0, dy=0.0) is True
    assert player.dash_cooldown > 0
    assert player.dash_timer > 0
    # Không thể Dash liên tục khi đang hồi chiêu
    assert player.trigger_dash(dx=1.0, dy=0.0) is False

    # Thử nghiệm Mega Beam
    assert player.mega_energy == 100
    assert player.trigger_mega_beam() is True
    assert player.mega_energy == 0
    assert player.mega_beam_timer > 0

    # Thử nghiệm Drone hộ vệ
    assert len(player.drones) == 0
    player.add_drone()
    assert len(player.drones) == 1
    assert player.drone_timer > 0