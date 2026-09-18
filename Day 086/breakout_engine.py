"""
Day 86: Breakout Arcade Game Engine & Collision Physics
2D vector kinematics, brick matrix collision, dynamic paddle deflection, and game state loop.
"""

from typing import List, Tuple, Optional


class Brick:
    def __init__(self, x: float, y: float, width: float = 60, height: float = 20, points: int = 10, color: str = "red"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = points
        self.color = color
        self.is_destroyed = False

    def check_collision(self, ball_x: float, ball_y: float, ball_r: float = 8.0) -> bool:
        if self.is_destroyed:
            return False
        # Axis-aligned bounding box (AABB) collision
        collides = (
            ball_x + ball_r >= self.x - self.width / 2 and
            ball_x - ball_r <= self.x + self.width / 2 and
            ball_y + ball_r >= self.y - self.height / 2 and
            ball_y - ball_r <= self.y + self.height / 2
        )
        if collides:
            self.is_destroyed = True
            return True
        return False


class Paddle:
    def __init__(self, x: float = 0, y: float = -240, width: float = 100, height: float = 15, speed: float = 30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_left(self, arena_half_w: float = 300):
        self.x = max(-arena_half_w + self.width / 2, self.x - self.speed)

    def move_right(self, arena_half_w: float = 300):
        self.x = min(arena_half_w - self.width / 2, self.x + self.speed)


class Ball:
    def __init__(self, x: float = 0, y: float = -200, dx: float = 5.0, dy: float = 5.0, radius: float = 8.0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def bounce_x(self):
        self.dx = -self.dx

    def bounce_y(self):
        self.dy = -self.dy

    def reset(self, x: float = 0, y: float = -200, dx: float = 5.0, dy: float = 5.0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


class BreakoutGame:
    def __init__(self, width: int = 600, height: int = 600):
        self.width = width
        self.height = height
        self.half_w = width / 2
        self.half_h = height / 2

        self.paddle = Paddle(x=0, y=-240)
        self.ball = Ball(x=0, y=-200, dx=4.0, dy=5.0)
        self.score = 0
        self.lives = 3
        self.is_game_over = False
        self.has_won = False

        self.bricks: List[Brick] = []
        self.build_bricks()

    def build_bricks(self):
        """Builds classic 4-layer brick wall."""
        self.bricks = []
        colors_and_points = [
            ("red", 70, 200),
            ("orange", 50, 175),
            ("green", 30, 150),
            ("yellow", 10, 125)
        ]
        brick_w = 64
        brick_h = 18

        for color, pts, y_pos in colors_and_points:
            for col in range(-4, 5):  # 9 bricks per row
                x_pos = col * (brick_w + 4)
                self.bricks.append(Brick(x=x_pos, y=y_pos, width=brick_w, height=brick_h, points=pts, color=color))

    def step(self) -> dict:
        """Executes one physics tick."""
        if self.is_game_over or self.has_won:
            return {"score": self.score, "lives": self.lives, "game_over": self.is_game_over, "won": self.has_won}

        self.ball.update()

        # 1. Wall Collisions
        if self.ball.x + self.ball.radius >= self.half_w:
            self.ball.x = self.half_w - self.ball.radius
            self.ball.bounce_x()
        elif self.ball.x - self.ball.radius <= -self.half_w:
            self.ball.x = -self.half_w + self.ball.radius
            self.ball.bounce_x()

        if self.ball.y + self.ball.radius >= self.half_h:
            self.ball.y = self.half_h - self.ball.radius
            self.ball.bounce_y()

        # 2. Bottom Boundary (Life Lost)
        if self.ball.y - self.ball.radius <= -self.half_h:
            self.lives -= 1
            if self.lives <= 0:
                self.is_game_over = True
            else:
                self.ball.reset(x=self.paddle.x, y=-200, dx=4.0, dy=5.0)

        # 3. Paddle Collision with dynamic angle deflection
        if (
            self.ball.dy < 0 and
            self.ball.y - self.ball.radius <= self.paddle.y + self.paddle.height / 2 and
            self.ball.y + self.ball.radius >= self.paddle.y - self.paddle.height / 2 and
            self.paddle.x - self.paddle.width / 2 <= self.ball.x <= self.paddle.x + self.paddle.width / 2
        ):
            # Dynamic bounce: distance from center alters horizontal angle
            offset = (self.ball.x - self.paddle.x) / (self.paddle.width / 2)
            self.ball.dx = offset * 6.0
            self.ball.bounce_y()

        # 4. Brick Collisions
        for brick in self.bricks:
            if brick.check_collision(self.ball.x, self.ball.y, self.ball.radius):
                self.ball.bounce_y()
                self.score += brick.points
                break  # Hit one brick per tick

        # 5. Victory check
        active_bricks = [b for b in self.bricks if not b.is_destroyed]
        if not active_bricks:
            self.has_won = True

        return {
            "score": self.score,
            "lives": self.lives,
            "remaining_bricks": len(active_bricks),
            "game_over": self.is_game_over,
            "won": self.has_won
        }

    def render_ascii_frame(self) -> str:
        """Renders compact ASCII snapshot of the active game board."""
        rows = 15
        cols = 35
        grid = [[" "] * cols for _ in range(rows)]

        # Map bricks
        for b in self.bricks:
            if not b.is_destroyed:
                gx = int((b.x + self.half_w) / self.width * cols)
                gy = int((self.half_h - b.y) / self.height * rows)
                if 0 <= gy < rows and 0 <= gx < cols:
                    grid[gy][gx] = "█"

        # Map paddle
        py = int((self.half_h - self.paddle.y) / self.height * rows)
        px = int((self.paddle.x + self.half_w) / self.width * cols)
        for dx in range(-2, 3):
            if 0 <= py < rows and 0 <= px + dx < cols:
                grid[py][px + dx] = "="

        # Map ball
        by = int((self.half_h - self.ball.y) / self.height * rows)
        bx = int((self.ball.x + self.half_w) / self.width * cols)
        if 0 <= by < rows and 0 <= bx < cols:
            grid[by][bx] = "O"

        border = "+" + "-" * cols + "+"
        lines = [border]
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append(border)
        lines.append(f" Score: {self.score:<6} Lives: {'❤️ ' * self.lives}")
        return "\n".join(lines)
