#!/usr/bin/env python3
"""Mini 3D Sandbox (Ursina)

Windows quick start:
1) py -m pip install ursina
2) py sandbox_game_3d.py

Controls:
- WASD: move
- Mouse: look around
- Left click: place block
- Right click: remove block
- 1~5: select block type
- ESC: release mouse
"""

from ursina import Button, Ursina, color, destroy, held_keys, mouse, scene, window
from ursina.prefabs.first_person_controller import FirstPersonController

BLOCK_COLORS = {
    1: color.lime,
    2: color.brown,
    3: color.gray,
    4: color.azure,
    5: color.yellow,
}

selected_block = 1


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), block_type=1):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube",
            color=BLOCK_COLORS.get(block_type, color.white),
            highlight_color=color.white33,
            scale=1,
        )
        self.block_type = block_type

    def input(self, key):
        global selected_block
        if self.hovered:
            if key == "left mouse down":
                Voxel(position=self.position + mouse.normal, block_type=selected_block)
            elif key == "right mouse down":
                destroy(self)


def build_world(size=16):
    for z in range(size):
        for x in range(size):
            # base ground layer
            Voxel(position=(x, 0, z), block_type=1)
            # tiny height variation for a less flat look
            if (x + z) % 7 == 0:
                Voxel(position=(x, 1, z), block_type=2)


def update():
    global selected_block
    if held_keys["1"]:
        selected_block = 1
    if held_keys["2"]:
        selected_block = 2
    if held_keys["3"]:
        selected_block = 3
    if held_keys["4"]:
        selected_block = 4
    if held_keys["5"]:
        selected_block = 5


def main() -> None:
    app = Ursina()
    window.title = "Mini 3D Sandbox (Codex Demo)"
    window.borderless = False
    window.exit_button.visible = False
    window.fps_counter.enabled = True

    build_world(size=20)

    player = FirstPersonController()
    player.cursor.visible = True
    player.gravity = 0.5
    player.position = (10, 3, 10)
    player.speed = 5

    app.run()


if __name__ == "__main__":
    main()
