"""
Day 93: Automate Google Chrome Dinosaur Game
Computer Vision, Pixel Analysis, and Autonomous Jump Trigger Engine
"""

import time
from typing import Tuple, Optional, Callable, Dict, Any
from PIL import Image, ImageDraw, ImageGrab
import pyautogui

# Disable PyAutoGUI fail-safe pause for high-frequency game loop responsiveness
pyautogui.PAUSE = 0.001


class DinoBot:
    """
    Autonomous bot that monitors the screen for obstacles (cacti & pterodactyls)
    and executes frame-perfect jump/duck keystrokes.
    """

    def __init__(
        self,
        scan_box: Tuple[int, int, int, int] = (460, 380, 550, 435),
        pixel_threshold: int = 15,
        jump_cooldown: float = 0.25,
        action_callback: Optional[Callable[[str], None]] = None
    ):
        """
        scan_box: (x1, y1, x2, y2) absolute screen coordinates or relative ROI
        pixel_threshold: minimum number of dark/light obstacle pixels to trigger jump
        jump_cooldown: cooldown period in seconds to prevent spamming jumps mid-air
        action_callback: optional custom callback function for simulating keystrokes
        """
        self.scan_box = scan_box
        self.pixel_threshold = pixel_threshold
        self.jump_cooldown = jump_cooldown
        self.last_jump_time = 0.0
        self.action_callback = action_callback
        self.is_running = False

    def is_night_mode(self, image: Image.Image) -> bool:
        """Determines if the game is in inverted dark/night mode."""
        gray = image.convert("L")
        # Sample corner pixels of the screen/box to detect background color
        pixels = list(gray.getdata())
        avg_lum = sum(pixels[:50]) / 50 if pixels else 255
        return avg_lum < 128

    def detect_obstacle(
        self,
        frame: Image.Image,
        box: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """
        Analyzes the Region of Interest (ROI) for obstacle pixel clusters.
        Supports automatic Day (dark on light) and Night (light on dark) detection.
        """
        scan_area = box or self.scan_box
        cropped = frame.crop(scan_area).convert("L")
        night = self.is_night_mode(cropped)

        # Count obstacle pixels
        obstacle_pixels = 0
        for pixel in cropped.getdata():
            if night:
                if pixel > 140:  # Bright pixel in night mode
                    obstacle_pixels += 1
            else:
                if pixel < 110:  # Dark pixel in day mode
                    obstacle_pixels += 1

            if obstacle_pixels >= self.pixel_threshold:
                return True

        return False

    def jump(self) -> bool:
        """Executes a spacebar jump if cooldown has elapsed."""
        now = time.time()
        if now - self.last_jump_time >= self.jump_cooldown:
            if self.action_callback:
                self.action_callback("jump")
            else:
                pyautogui.press("space")
            self.last_jump_time = now
            return True
        return False

    def duck(self, duration: float = 0.2) -> bool:
        """Executes a down-arrow duck for flying pterodactyls."""
        if self.action_callback:
            self.action_callback("duck")
        else:
            pyautogui.keyDown("down")
            time.sleep(duration)
            pyautogui.keyUp("down")
        return True

    def run_live_loop(self, duration_sec: int = 15) -> int:
        """Runs the live screen monitoring loop against an active Chrome window."""
        print(f"\n[+] Bot starting in 3 seconds... Switch to Chrome window (chrome://dino)!")
        for i in range(3, 0, -1):
            print(f"    Starting in {i}...")
            time.sleep(1)
        print("  [✓] BOT ENGAGED! Press Ctrl+C in terminal to halt.\n")

        # Initial jump to start the game
        self.jump()
        start_time = time.time()
        jump_count = 0

        try:
            while time.time() - start_time < duration_sec:
                screen = ImageGrab.grab()
                if self.detect_obstacle(screen):
                    if self.jump():
                        jump_count += 1
                        print(f"  [JUMP] Obstacle detected! Jump #{jump_count}")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\n  [!] Bot loop halted by user.")

        print(f"\n  [✓] Run completed. Total jumps triggered: {jump_count}")
        return jump_count


class SyntheticGameSimulator:
    """
    In-memory physics & obstacle simulator for the Chrome Dinosaur game.
    Enables deterministic automated testing and headless visualization.
    """

    def __init__(self, width: int = 600, height: int = 200):
        self.width = width
        self.height = height
        self.ground_y = 150
        self.dino_x = 50
        self.dino_y = self.ground_y
        self.dino_vy = 0.0
        self.gravity = 1.2
        self.jump_velocity = -14.0
        self.obstacles = []  # List of dicts: {"x": int, "w": int, "h": int}
        self.speed = 8.0
        self.score = 0
        self.night_mode = False

    def reset(self):
        self.dino_y = self.ground_y
        self.dino_vy = 0.0
        self.obstacles = []
        self.score = 0

    def spawn_obstacle(self, x: Optional[int] = None, width: int = 15, height: int = 35):
        spawn_x = x if x is not None else self.width + 20
        self.obstacles.append({"x": spawn_x, "w": width, "h": height})

    def jump(self):
        if self.dino_y >= self.ground_y:
            self.dino_vy = self.jump_velocity

    def step(self) -> Dict[str, Any]:
        """Advances game physics by 1 tick."""
        self.score += 1

        # Dino physics
        self.dino_y += self.dino_vy
        if self.dino_y < self.ground_y:
            self.dino_vy += self.gravity
        else:
            self.dino_y = self.ground_y
            self.dino_vy = 0.0

        # Move obstacles
        collision = False
        remaining_obstacles = []
        for obs in self.obstacles:
            obs["x"] -= self.speed
            # Check collision with dino
            dino_box = (self.dino_x, self.dino_y - 40, self.dino_x + 35, self.dino_y)
            obs_box = (obs["x"], self.ground_y - obs["h"], obs["x"] + obs["w"], self.ground_y)

            if (
                dino_box[0] < obs_box[2] and
                dino_box[2] > obs_box[0] and
                dino_box[1] < obs_box[3] and
                dino_box[3] > obs_box[1]
            ):
                collision = True

            if obs["x"] + obs["w"] > 0:
                remaining_obstacles.append(obs)

        self.obstacles = remaining_obstacles

        return {
            "score": self.score,
            "collision": collision,
            "dino_y": self.dino_y,
            "obstacle_count": len(self.obstacles)
        }

    def render_frame(self) -> Image.Image:
        """Renders the current game state as a PIL Image."""
        bg_color = (30, 30, 30) if self.night_mode else (255, 255, 255)
        fg_color = (230, 230, 230) if self.night_mode else (40, 40, 40)

        img = Image.new("RGB", (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)

        # Ground line
        draw.line([(0, self.ground_y), (self.width, self.ground_y)], fill=fg_color, width=2)

        # Dino
        dino_top = self.dino_y - 40
        draw.rectangle([self.dino_x, dino_top, self.dino_x + 35, self.dino_y], fill=fg_color)

        # Obstacles
        for obs in self.obstacles:
            obs_top = self.ground_y - obs["h"]
            draw.rectangle([obs["x"], obs_top, obs["x"] + obs["w"], self.ground_y], fill=fg_color)

        return img
