from pyglet.window import key

from transform import *
from camera import Camera
from gameobjects import Cursor
from map import Map


class LevelScreen:

    def __init__(self, map_path, batch, screen_settings):
        self.batch = batch
        self.map = Map(map_path)
        self.camera = Camera.get_camera()  # Should already be initialized to this map's data
        self.cursor = Cursor()
        self.cursor.transform.scale = 0.5
        self.event_stack = [] # For things like dialog
        self.map_objects = {}
        self.screen_settings = screen_settings

        self.width, self.height = self.map.get_bounds()

        self.camera = Camera(
            x=0,
            y=0,
            width_in_tiles=self.width,
            height_in_tiles=self.height,
            screen_settings = self.screen_settings
        )

    def update(self, keys, dt):
        x, y = self.cursor.get_cursor_pos()

        if not self.cursor.is_moving():
            dx = 0
            dy = 0

            if keys[key.UP]:
                dy = 1
            elif keys[key.DOWN]:
                dy = -1
            if keys[key.RIGHT]:
                dx = 1
            elif keys[key.LEFT]:
                dx = -1

            nx = x + dx
            ny = y + dy
            if (nx, ny) in self.map:
                self.cursor.move(dx, dy)
                self.camera.move(dx, dy) 

        self.camera.update(dt)
        self.cursor.update(dt)

        if keys[key.X]:
            print(f"{self.map.get_tile_at_position(x,y)=}")

    def get_object_at_position(self, x: int, y: int):
        if (x, y) in self.map_objects:
            return self.map_objects[(x, y)]

    def in_rendering_range(self, x, y):
        left = self.camera.transform.x
        right = left + self.camera.width_in_tiles
        bottom = self.camera.transform.y
        top = bottom + self.camera.height_in_tiles
        return left <= x <= right and bottom <= y <= top

    def render(self):
        self.camera.render()
        self.map.render()
        self.cursor.render()

