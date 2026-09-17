"""
Day 94: Space Invaders 2D Arcade Game
Physics Engine, Fleet Vector Dynamics, and Collision Detection
"""

import math
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class Alien:
    x: float
    y: float
    row: int
    points: int
    alive: bool = True
    char: str = "👾"


@dataclass
class Laser:
    x: float
    y: float
    vy: float
    from_player: bool


@dataclass
class Bunker:
    x: float
    y: float
    width: float = 3.0
    height: float = 1.0
    health: int = 3


class SpaceInvadersEngine:
    """
    Core arcade physics engine for Space Invaders.
    Handles grid boundaries, vector motion, laser collisions, bunker degradation, and waves.
    """

    def __init__(self, width: int = 50, height: int = 24):
        self.width = width
        self.height = height
        self.player_x = width / 2.0
        self.player_y = 2.0
        self.player_lives = 3
        self.score = 0
        self.wave = 1
        self.game_over = False
        self.victory = False

        self.fleet_dx = 0.8
        self.fleet_dy = 1.0
        self.fleet_dir = 1.0
        self.aliens: List[Alien] = []
        self.lasers: List[Laser] = []
        self.bunkers: List[Bunker] = []
        self.ufo_x: Optional[float] = None

        self.spawn_fleet()
        self.spawn_bunkers()

    def spawn_fleet(self):
        """Spawns an organized grid of alien invaders."""
        self.aliens.clear()
        rows = 3
        cols = 8
        spacing_x = 4.0
        spacing_y = 2.0
        start_x = 6.0
        start_y = self.height - 4.0

        for r in range(rows):
            pts = 30 if r == 0 else (20 if r == 1 else 10)
            char = "🛸" if r == 0 else ("👾" if r == 1 else "👽")
            for c in range(cols):
                self.aliens.append(
                    Alien(
                        x=start_x + (c * spacing_x),
                        y=start_y - (r * spacing_y),
                        row=r,
                        points=pts,
                        char=char
                    )
                )

    def spawn_bunkers(self):
        """Spawns defensive bunkers between the player and alien fleet."""
        self.bunkers.clear()
        num_bunkers = 4
        spacing = self.width / (num_bunkers + 1)
        for i in range(num_bunkers):
            bx = (i + 1) * spacing
            self.bunkers.append(Bunker(x=bx, y=5.0, width=3.0, health=3))

    def fire_player_laser(self) -> bool:
        """Fires a laser beam from player cannon if limit not exceeded."""
        player_lasers = [l for l in self.lasers if l.from_player]
        if len(player_lasers) < 2 and not self.game_over:
            self.lasers.append(Laser(x=self.player_x, y=self.player_y + 1.0, vy=1.2, from_player=True))
            return True
        return False

    def alien_fire_bomb(self):
        """Selects a random front-line alien to drop an energy bomb."""
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens or self.game_over:
            return

        # Group by column and pick the bottom-most alien
        bottom_aliens: Dict[int, Alien] = {}
        for a in alive_aliens:
            col_key = int(round(a.x))
            if col_key not in bottom_aliens or a.y < bottom_aliens[col_key].y:
                bottom_aliens[col_key] = a

        shooter = random.choice(list(bottom_aliens.values()))
        self.lasers.append(Laser(x=shooter.x, y=shooter.y - 1.0, vy=-0.8, from_player=False))

    def update_fleet(self):
        """Updates fleet positions, handles wall bounces, and advances downwards."""
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            # Wave cleared!
            self.wave += 1
            self.fleet_dx = min(1.6, self.fleet_dx + 0.2)
            self.spawn_fleet()
            return

        # Determine if any alien hit boundary
        bounce = False
        for a in alive_aliens:
            next_x = a.x + (self.fleet_dx * self.fleet_dir)
            if next_x <= 2.0 or next_x >= self.width - 3.0:
                bounce = True
                break

        if bounce:
            self.fleet_dir *= -1.0
            for a in alive_aliens:
                a.y -= self.fleet_dy
                # Check if aliens have invaded the player ground
                if a.y <= self.player_y + 1.0:
                    self.game_over = True
        else:
            for a in alive_aliens:
                a.x += self.fleet_dx * self.fleet_dir

    def update_lasers(self):
        """Moves all lasers and handles AABB collision detection."""
        active_lasers: List[Laser] = []

        for laser in self.lasers:
            laser.y += laser.vy

            # Check screen bounds
            if laser.y <= 0 or laser.y >= self.height:
                continue

            hit = False

            if laser.from_player:
                # Check collision with aliens
                for alien in self.aliens:
                    if alien.alive and abs(laser.x - alien.x) <= 1.5 and abs(laser.y - alien.y) <= 1.0:
                        alien.alive = False
                        self.score += alien.points
                        hit = True
                        break

                if not hit:
                    # Check collision with bunkers
                    for bunker in self.bunkers:
                        if bunker.health > 0 and abs(laser.x - bunker.x) <= bunker.width / 2 and abs(laser.y - bunker.y) <= 1.0:
                            bunker.health -= 1
                            hit = True
                            break
            else:
                # Alien bomb hits player
                if abs(laser.x - self.player_x) <= 1.5 and abs(laser.y - self.player_y) <= 1.0:
                    self.player_lives -= 1
                    hit = True
                    if self.player_lives <= 0:
                        self.game_over = True

                if not hit:
                    # Alien bomb hits bunker
                    for bunker in self.bunkers:
                        if bunker.health > 0 and abs(laser.x - bunker.x) <= bunker.width / 2 and abs(laser.y - bunker.y) <= 1.0:
                            bunker.health -= 1
                            hit = True
                            break

            if not hit:
                active_lasers.append(laser)

        self.lasers = active_lasers

    def step(self, action: Optional[str] = None) -> Dict[str, Any]:
        """
        Advances the game state by one simulation step.
        action: 'left', 'right', 'fire', or None
        """
        if self.game_over:
            return {"game_over": True, "score": self.score, "lives": self.player_lives}

        if action == "left":
            self.player_x = max(2.0, self.player_x - 1.5)
        elif action == "right":
            self.player_x = min(self.width - 2.0, self.player_x + 1.5)
        elif action == "fire":
            self.fire_player_laser()

        self.update_fleet()
        self.update_lasers()

        # Random alien firing
        if random.random() < 0.12:
            self.alien_fire_bomb()

        return {
            "game_over": self.game_over,
            "score": self.score,
            "lives": self.player_lives,
            "wave": self.wave,
            "aliens_remaining": sum(1 for a in self.aliens if a.alive)
        }

    def render_ascii_frame(self) -> str:
        """Renders the game board as an ASCII matrix for terminal display."""
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Draw aliens
        for a in self.aliens:
            if a.alive:
                gx = int(round(a.x))
                gy = int(round(a.y))
                if 0 <= gy < self.height and 0 <= gx < self.width:
                    grid[gy][gx] = "M"

        # Draw bunkers
        for b in self.bunkers:
            if b.health > 0:
                bx = int(round(b.x))
                by = int(round(b.y))
                char = "#" if b.health == 3 else ("=" if b.health == 2 else "-")
                for offset in (-1, 0, 1):
                    if 0 <= by < self.height and 0 <= bx + offset < self.width:
                        grid[by][bx + offset] = char

        # Draw lasers
        for l in self.lasers:
            lx = int(round(l.x))
            ly = int(round(l.y))
            if 0 <= ly < self.height and 0 <= lx < self.width:
                grid[ly][lx] = "|" if l.from_player else "v"

        # Draw player
        px = int(round(self.player_x))
        py = int(round(self.player_y))
        if 0 <= py < self.height and 0 <= px < self.width:
            grid[py][px] = "A"
            if px > 0:
                grid[py][px - 1] = "/"
            if px < self.width - 1:
                grid[py][px + 1] = "\\"

        # Assemble string from top down
        lines = [f" SCORE: {self.score:05d}  |  LIVES: {'♥ ' * self.player_lives} |  WAVE: {self.wave}"]
        lines.append("=" * self.width)
        for row in reversed(grid):
            lines.append("".join(row))
        lines.append("=" * self.width)
        return "\n".join(lines)


def run_turtle_game():
    """Launches interactive Desktop Space Invaders using Python Turtle."""
    import turtle

    screen = turtle.Screen()
    screen.title("Python 100 Days of Code: Space Invaders")
    screen.bgcolor("black")
    screen.setup(width=600, height=650)
    screen.tracer(0)

    engine = SpaceInvadersEngine(width=50, height=24)

    # Drawer turtle
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.penup()

    def go_left():
        engine.step("left")

    def go_right():
        engine.step("right")

    def shoot():
        engine.fire_player_laser()

    screen.listen()
    screen.onkeypress(go_left, "Left")
    screen.onkeypress(go_right, "Right")
    screen.onkeypress(shoot, "space")

    print("[+] Space Invaders Turtle window open. Press Left/Right to move, Space to fire!")

    # Simple animation loop
    for _ in range(600):
        if engine.game_over:
            drawer.goto(0, 0)
            drawer.color("red")
            drawer.write("GAME OVER", align="center", font=("Arial", 28, "bold"))
            screen.update()
            break

        engine.step()
        drawer.clear()

        # Draw Score
        drawer.goto(-260, 280)
        drawer.color("white")
        drawer.write(f"SCORE: {engine.score:04d}   LIVES: {engine.player_lives}   WAVE: {engine.wave}", font=("Courier", 14, "normal"))

        # Draw Aliens
        for a in engine.aliens:
            if a.alive:
                sx = (a.x - 25) * 11
                sy = (a.y - 12) * 22
                drawer.goto(sx, sy)
                drawer.color("green" if a.row == 0 else "yellow")
                drawer.write("👾", align="center", font=("Arial", 16, "normal"))

        # Draw Lasers
        for l in engine.lasers:
            lx = (l.x - 25) * 11
            ly = (l.y - 12) * 22
            drawer.goto(lx, ly)
            drawer.color("cyan" if l.from_player else "red")
            drawer.write("|" if l.from_player else "v", align="center", font=("Courier", 14, "bold"))

        # Draw Player
        px = (engine.player_x - 25) * 11
        py = (engine.player_y - 12) * 22
        drawer.goto(px, py)
        drawer.color("cyan")
        drawer.write("🚀", align="center", font=("Arial", 18, "normal"))

        screen.update()
        time.sleep(0.04)

    turtle.bye()
