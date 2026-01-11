"""
Notes:
- Action space: Discrete(4) -> 0=UP,1=DOWN,2=LEFT,3=RIGHT
- Observation: (H_blocks, W_blocks) uint8 grid: 0=empty,1=snake,2=food
- Rendering is optional (render_mode='human' will open a Pygame window).
"""

import random
import sys
try:
    import numpy as np
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        f"Missing dependency 'numpy'.\nInstall it for the Python interpreter at: {sys.executable}\nExample: {sys.executable} -m pip install numpy\nOr select a Python interpreter in your editor that already has numpy installed."
    ) from e
from typing import Tuple, Optional

try:
    from gym import Env
    from gym.spaces import Discrete, Box
except Exception:
    # Minimal fallback if gym is not installed
    class Env:
        pass

    class Discrete:
        def __init__(self, n):
            self.n = n

    class Box:
        def __init__(self, low, high, shape, dtype):
            self.low = low
            self.high = high
            self.shape = shape
            self.dtype = dtype

from snake import Snake
from food import Food


class SnakeEnv(Env):
    ACTIONS = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}

    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
        block_size: int = 20,
        max_steps: Optional[int] = 1000,
        render_mode: Optional[str] = None,
        seed: Optional[int] = None,
    ):
        self.width = width
        self.height = height
        self.block = block_size
        self.grid_w = width // block_size
        self.grid_h = height // block_size

        self.action_space = Discrete(4)
        self.observation_space = Box(0, 2, shape=(self.grid_h, self.grid_w), dtype=np.uint8)

        self.max_steps = max_steps
        self.render_mode = render_mode

        self._rng = random.Random()
        if seed is not None:
            self.seed(seed)

        # Game objects (created on reset)
        self.snake: Optional[Snake] = None
        self.food: Optional[Food] = None

        self.steps = 0

        # Optional rendering resources
        self._screen = None
        if self.render_mode == "human":
            import pygame
            from screen import Screen

            pygame.init()
            self._screen = Screen(width, height)

    def seed(self, seed=None):
        self._rng.seed(seed)

    def reset(self, seed: Optional[int] = None, options: dict = None):
        if seed is not None:
            self.seed(seed)

        # Create Snake and Food without rendering
        # We pass a minimal dummy screen that only provides width/height attributes for logic
        class _DummyScreen:
            def __init__(self, w, h):
                self.width = w
                self.height = h

        dummy = _DummyScreen(self.width, self.height)
        self.snake = Snake(dummy, block_size=self.block)
        self.food = Food(dummy, block_size=self.block)

        # Ensure food doesn't spawn on the snake
        while self.food.position in self.snake.positions:
            self.food.position = self.food.spawn()

        self.steps = 0
        obs = self._get_obs()
        return obs

    def _get_obs(self) -> np.ndarray:
        grid = np.zeros((self.grid_h, self.grid_w), dtype=np.uint8)

        # mark snake
        for x, y in self.snake.positions:
            gx = x // self.block
            gy = y // self.block
            if 0 <= gx < self.grid_w and 0 <= gy < self.grid_h:
                grid[gy, gx] = 1

        # mark food
        fx, fy = self.food.position
        grid[fy // self.block, fx // self.block] = 2

        return grid

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, dict]:
        assert action in (0, 1, 2, 3), "Action must be an int in [0,3]"
        direction = self.ACTIONS[action]
        self.snake.change_direction(direction)

        self.snake.move()
        self.steps += 1

        reward = -0.001  # small time penalty
        done = False
        info = {}

        # Food eaten
        if self.snake.get_head() == self.food.position:
            self.snake.grow = True
            reward += 1.0
            # respawn food not on snake
            self.food.position = self.food.spawn()
            attempts = 0
            while self.food.position in self.snake.positions:
                self.food.position = self.food.spawn()
                attempts += 1
                if attempts > 1000:
                    break

        # Collisions
        if self.snake.check_self_collision() or self.snake.check_wall_collision():
            reward -= 1.0
            done = True

        # Max steps
        if self.max_steps is not None and self.steps >= self.max_steps:
            done = True
            info["TimeLimit.truncated"] = True

        obs = self._get_obs()
        return obs, float(reward), done, info

    def render(self, mode: str = "human"):
        if mode == "human":
            if self._screen is None:
                import pygame
                from screen import Screen

                pygame.init()
                self._screen = Screen(self.width, self.height)

            # draw
            self._screen.clear()
            # snake draw uses pygame
            # we temporarily attach the actual screen to objects for drawing
            self.snake.screen = self._screen
            self.food.screen = self._screen
            self.snake.draw()
            self.food.draw()
            self._screen.update()
        elif mode == "rgb_array":
            import pygame
            # Create an off-screen surface and draw to it
            surface = pygame.Surface((self.width, self.height))
            # draw background
            surface.fill((0, 0, 0))

            # draw snake
            for x, y in self.snake.positions:
                pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(x, y, self.block, self.block))

            # draw food
            fx, fy = self.food.position
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(fx, fy, self.block, self.block))

            arr = np.transpose(pygame.surfarray.array3d(surface), (1, 0, 2))
            return arr
        else:
            raise ValueError("Unsupported render mode: " + str(mode))

    def close(self):
        if self._screen is not None:
            import pygame
            pygame.quit()
            self._screen = None


if __name__ == "__main__":
    env = SnakeEnv(render_mode=None)
    obs = env.reset()
    for _ in range(10):
        action = random.randint(0, 3)
        obs, r, done, info = env.step(action)
        if done:
            print("Done", r, info)
            break
    print("Obs shape:", obs.shape)
