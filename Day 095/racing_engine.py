"""
Day 95: Custom 2D Racing Game
Physics Engine, Relative Kinematics, and Track Rendering
"""

import math
import random
import time
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class TrafficCar:
    x: float
    y: float
    speed: float  # Absolute speed (km/h)
    symbol: str = "🚘"
    width: float = 2.5
    height: float = 3.0


class RacingEngine:
    """
    2D Top-down arcade racing engine with multi-lane highway kinematics,
    dynamic traffic spawning, nitro boost mechanics, and collision detection.
    """

    def __init__(self, track_width: int = 36, track_height: int = 22):
        self.track_width = track_width
        self.track_height = track_height
        self.lane_centers = [7.0, 14.0, 21.0, 28.0]

        self.player_x = self.lane_centers[1]
        self.player_y = 3.0
        self.player_width = 2.5
        self.player_height = 3.0

        self.speed = 60.0         # Current speed in km/h
        self.min_speed = 30.0
        self.base_max_speed = 150.0
        self.nitro_gauge = 100.0   # 0 to 100%
        self.is_nitro_active = False

        self.distance = 0.0       # Meters traveled
        self.score = 0
        self.crashed = False
        self.road_offset = 0.0

        self.traffic: List[TrafficCar] = []

    def steer(self, direction: str):
        """Steers the car left or right within track boundaries."""
        if self.crashed:
            return
        delta = 2.5 if direction == "left" else (-2.5 if direction == "right" else 0.0)
        new_x = self.player_x - delta
        # Keep within asphalt road margins (lanes 4 to 31)
        if 4.0 <= new_x <= self.track_width - 5.0:
            self.player_x = new_x

    def accelerate(self, active: bool = True):
        """Accelerates the vehicle up to max speed."""
        if self.crashed:
            return
        top_speed = self.base_max_speed * (1.4 if self.is_nitro_active else 1.0)
        if active:
            self.speed = min(top_speed, self.speed + (6.0 if self.is_nitro_active else 3.0))
        else:
            # Engine drag / coasting deceleration
            self.speed = max(self.min_speed, self.speed - 1.5)

    def brake(self):
        """Applies vehicle brakes."""
        if self.crashed:
            return
        self.speed = max(self.min_speed, self.speed - 6.0)

    def trigger_nitro(self, activate: bool = True):
        """Activates nitrous oxide boost if gauge > 0."""
        if activate and self.nitro_gauge > 5.0 and not self.crashed:
            self.is_nitro_active = True
            self.nitro_gauge = max(0.0, self.nitro_gauge - 2.5)
        else:
            self.is_nitro_active = False
            # Slow passive nitro regeneration when cruising
            if not activate:
                self.nitro_gauge = min(100.0, self.nitro_gauge + 0.3)

    def spawn_traffic(self):
        """Spawns oncoming or slower competitor vehicles ahead on the road."""
        if len(self.traffic) < 4 and random.random() < 0.25:
            lane = random.choice(self.lane_centers)
            # Ensure no car already in immediate spawn zone
            if not any(abs(t.x - lane) < 3.0 and t.y > self.track_height - 6.0 for t in self.traffic):
                traffic_speed = random.uniform(40.0, 90.0)
                symbols = ["🚙", "🚕", "🚚", "🚗"]
                self.traffic.append(
                    TrafficCar(
                        x=lane,
                        y=float(self.track_height + 2),
                        speed=traffic_speed,
                        symbol=random.choice(symbols)
                    )
                )

    def update_traffic_and_collisions(self):
        """Calculates relative vehicle velocity vectors and checks AABB collisions."""
        dt = 0.1  # Fixed time delta per frame
        relative_mult = 0.08

        surviving_traffic: List[TrafficCar] = []
        for car in self.traffic:
            # Relative speed determines downward motion towards player
            rel_speed = (self.speed - car.speed) * relative_mult
            new_y = car.y - rel_speed

            # Swept Axis-Aligned Bounding Box (AABB) collision check
            x_overlap = abs(self.player_x - car.x) < (self.player_width + car.width) / 2.0
            car_y_min = min(car.y, new_y) - (car.height / 2.0)
            car_y_max = max(car.y, new_y) + (car.height / 2.0)
            player_y_min = self.player_y - (self.player_height / 2.0)
            player_y_max = self.player_y + (self.player_height / 2.0)

            y_overlap = (car_y_min <= player_y_max) and (car_y_max >= player_y_min)

            if x_overlap and y_overlap:
                self.crashed = True

            car.y = new_y

            # Keep car if still visible on track
            if car.y > -3.0:
                surviving_traffic.append(car)
            else:
                # Successfully overtook competitor
                self.score += int(car.speed)

        self.traffic = surviving_traffic

    def step(
        self,
        steer_dir: Optional[str] = None,
        accelerate: bool = False,
        brake: bool = False,
        nitro: bool = False
    ) -> Dict[str, Any]:
        """Advances the racing engine by 1 tick."""
        if self.crashed:
            return {"crashed": True, "score": self.score, "distance": self.distance}

        if steer_dir:
            self.steer(steer_dir)

        self.trigger_nitro(nitro)

        if brake:
            self.brake()
        else:
            self.accelerate(accelerate)

        # Update distance & score
        meters_this_tick = (self.speed * 1000.0 / 3600.0) * 0.1
        self.distance += meters_this_tick
        self.score += int(meters_this_tick * 0.5)

        # Track road marker animation
        self.road_offset = (self.road_offset + (self.speed * 0.02)) % 4.0

        self.spawn_traffic()
        self.update_traffic_and_collisions()

        return {
            "crashed": self.crashed,
            "speed": round(self.speed, 1),
            "distance_m": round(self.distance, 1),
            "nitro": round(self.nitro_gauge, 1),
            "score": self.score,
            "traffic_count": len(self.traffic)
        }

    def render_ascii_frame(self) -> str:
        """Renders the racing track as an ASCII matrix for terminal animation."""
        grid = [[" " for _ in range(self.track_width)] for _ in range(self.track_height)]

        # Render track borders and dashed road divider lines
        dashed = int(self.road_offset) % 2 == 0
        for y in range(self.track_height):
            # Left & Right grass/guard rails
            grid[y][3] = "║"
            grid[y][self.track_width - 4] = "║"

            # 3 dashed lane dividers
            for div_x in [10, 18, 25]:
                if (y + int(self.road_offset)) % 3 != 0:
                    grid[y][div_x] = "┆"

        # Render traffic cars
        for car in self.traffic:
            cx = int(round(car.x))
            cy = int(round(car.y))
            if 0 <= cy < self.track_height and 0 <= cx < self.track_width:
                grid[cy][cx] = "X"
                if cy > 0:
                    grid[cy - 1][cx] = "T"

        # Render player car
        px = int(round(self.player_x))
        py = int(round(self.player_y))
        if 0 <= py < self.track_height and 0 <= px < self.track_width:
            grid[py][px] = "▲"
            if py > 0:
                grid[py - 1][px] = "█"
                if px > 0:
                    grid[py - 1][px - 1] = "▌"
                if px < self.track_width - 1:
                    grid[py - 1][px + 1] = "▐"

        # Header status
        nitro_bar = "■" * int(self.nitro_gauge // 10) + "░" * (10 - int(self.nitro_gauge // 10))
        status = (
            f" SPEED: {int(self.speed):3d} KM/H | "
            f"NITRO: [{nitro_bar}] | "
            f"DIST: {int(self.distance):4d}M | "
            f"SCORE: {self.score:05d}"
        )

        lines = ["=" * self.track_width, status, "=" * self.track_width]
        for row in reversed(grid):
            lines.append("".join(row))
        lines.append("=" * self.track_width)

        if self.crashed:
            lines.append("💥💥 CRASH DETECTED! VEHICLE TOTALED! 💥💥")

        return "\n".join(lines)


def run_turtle_racer():
    """Launches interactive Desktop 2D Racing Game using Python Turtle."""
    import turtle

    screen = turtle.Screen()
    screen.title("Python 100 Days of Code: Turbo Grand Prix Racer")
    screen.bgcolor("#1a1a1a")
    screen.setup(width=500, height=650)
    screen.tracer(0)

    engine = RacingEngine(track_width=36, track_height=22)

    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.penup()

    screen.listen()
    screen.onkeypress(lambda: engine.steer("left"), "Left")
    screen.onkeypress(lambda: engine.steer("right"), "Right")
    screen.onkeypress(lambda: engine.accelerate(True), "Up")
    screen.onkeyrelease(lambda: engine.accelerate(False), "Up")
    screen.onkeypress(lambda: engine.brake(), "Down")
    screen.onkeypress(lambda: engine.trigger_nitro(True), "space")
    screen.onkeyrelease(lambda: engine.trigger_nitro(False), "space")

    print("[+] Turtle Racer active. Controls: Left/Right to Steer, Up to Accel, Space for Nitro!")

    for _ in range(400):
        if engine.crashed:
            drawer.goto(0, 0)
            drawer.color("red")
            drawer.write("💥 CRASHED! 💥", align="center", font=("Arial", 26, "bold"))
            screen.update()
            break

        engine.step()
        drawer.clear()

        # Draw HUD
        drawer.goto(-220, 280)
        drawer.color("white")
        drawer.write(
            f"SPEED: {int(engine.speed)} km/h | DIST: {int(engine.distance)}m | SCORE: {engine.score}",
            font=("Courier", 12, "bold")
        )

        # Draw Player
        px = (engine.player_x - 18) * 10
        py = (engine.player_y - 11) * 22
        drawer.goto(px, py)
        drawer.color("yellow" if engine.is_nitro_active else "cyan")
        drawer.write("🏎️", align="center", font=("Arial", 22, "normal"))

        # Draw Traffic
        for car in engine.traffic:
            cx = (car.x - 18) * 10
            cy = (car.y - 11) * 22
            drawer.goto(cx, cy)
            drawer.color("orange")
            drawer.write(car.symbol, align="center", font=("Arial", 20, "normal"))

        screen.update()
        time.sleep(0.04)

    turtle.bye()
