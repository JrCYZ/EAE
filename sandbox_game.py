#!/usr/bin/env python3
"""Mini Sandbox Game (Tkinter)

Controls:
- WASD: move player
- Left click: place block
- Right click: remove block
- Mouse wheel / Q,E: select block type
- R: regenerate world
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass

TILE_SIZE = 24
GRID_W = 28
GRID_H = 18
HUD_HEIGHT = 56

BLOCK_TYPES = [
    ("grass", "#5FA44A"),
    ("dirt", "#8B5A2B"),
    ("stone", "#7D7D7D"),
    ("water", "#3E7FD1"),
    ("sand", "#D9C17A"),
]


@dataclass
class Player:
    x: int = GRID_W // 2
    y: int = GRID_H // 2


class SandboxGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Mini Sandbox (Codex Demo)")
        width = GRID_W * TILE_SIZE
        height = GRID_H * TILE_SIZE + HUD_HEIGHT
        self.canvas = tk.Canvas(root, width=width, height=height, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()

        self.player = Player()
        self.selected = 0
        self.map_data = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
        self._generate_world()

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.root.bind("<Key>", self.on_key)

        self.draw()

    def _generate_world(self) -> None:
        for y in range(GRID_H):
            for x in range(GRID_W):
                noise = random.random()
                if noise < 0.08:
                    self.map_data[y][x] = 3  # water
                elif noise < 0.18:
                    self.map_data[y][x] = 4  # sand
                elif noise < 0.45:
                    self.map_data[y][x] = 2  # stone
                elif noise < 0.72:
                    self.map_data[y][x] = 1  # dirt
                else:
                    self.map_data[y][x] = 0  # grass

    def draw(self) -> None:
        self.canvas.delete("all")
        for y in range(GRID_H):
            for x in range(GRID_W):
                block_id = self.map_data[y][x]
                _, color = BLOCK_TYPES[block_id]
                x1 = x * TILE_SIZE
                y1 = y * TILE_SIZE
                x2 = x1 + TILE_SIZE
                y2 = y1 + TILE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")

        self._draw_player()
        self._draw_hud()

    def _draw_player(self) -> None:
        x1 = self.player.x * TILE_SIZE + 4
        y1 = self.player.y * TILE_SIZE + 4
        x2 = x1 + TILE_SIZE - 8
        y2 = y1 + TILE_SIZE - 8
        self.canvas.create_oval(x1, y1, x2, y2, fill="#FF6363", outline="#ffffff", width=2)

    def _draw_hud(self) -> None:
        top = GRID_H * TILE_SIZE
        self.canvas.create_rectangle(0, top, GRID_W * TILE_SIZE, top + HUD_HEIGHT, fill="#111", outline="#333")
        text = "WASD移动 | 左键放置 | 右键删除 | Q/E或滚轮切换方块 | R重置"
        self.canvas.create_text(12, top + 14, anchor="w", text=text, fill="#DDD", font=("Consolas", 10))

        for i, (name, color) in enumerate(BLOCK_TYPES):
            x = 12 + i * 104
            y = top + 28
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, outline="#555")
            label = f"{i+1}. {name}"
            if i == self.selected:
                label += "  <"
            self.canvas.create_text(x + 26, y + 10, anchor="w", text=label, fill="#fff", font=("Consolas", 10))

    def on_left_click(self, event: tk.Event) -> None:
        gx, gy = self._to_grid(event.x, event.y)
        if self._valid(gx, gy):
            self.map_data[gy][gx] = self.selected
            self.draw()

    def on_right_click(self, event: tk.Event) -> None:
        gx, gy = self._to_grid(event.x, event.y)
        if self._valid(gx, gy):
            self.map_data[gy][gx] = 0
            self.draw()

    def on_mouse_wheel(self, event: tk.Event) -> None:
        if event.delta > 0:
            self.selected = (self.selected - 1) % len(BLOCK_TYPES)
        else:
            self.selected = (self.selected + 1) % len(BLOCK_TYPES)
        self.draw()

    def on_key(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        if key == "a":
            self.player.x = max(0, self.player.x - 1)
        elif key == "d":
            self.player.x = min(GRID_W - 1, self.player.x + 1)
        elif key == "w":
            self.player.y = max(0, self.player.y - 1)
        elif key == "s":
            self.player.y = min(GRID_H - 1, self.player.y + 1)
        elif key == "q":
            self.selected = (self.selected - 1) % len(BLOCK_TYPES)
        elif key == "e":
            self.selected = (self.selected + 1) % len(BLOCK_TYPES)
        elif key == "r":
            self._generate_world()
        else:
            return
        self.draw()

    def _to_grid(self, x: int, y: int) -> tuple[int, int]:
        return x // TILE_SIZE, y // TILE_SIZE

    @staticmethod
    def _valid(gx: int, gy: int) -> bool:
        return 0 <= gx < GRID_W and 0 <= gy < GRID_H


def main() -> None:
    root = tk.Tk()
    game = SandboxGame(root)
    game.draw()
    root.mainloop()


if __name__ == "__main__":
    main()
