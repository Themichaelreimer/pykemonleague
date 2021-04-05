from pyglet.window import key

from transform import *
from camera import Camera
from gameobjects import Cursor
from map import Map


class LevelScreen:

    def __init__(self, map_path, batch):
        self.batch = batch
        self.map = Map(map_path)
        self.camera = Camera.get_camera()  # Should already be initialized to this map's data
        self.cursor = Cursor()
        self.cursor.transform.scale = 0.5
        self.event_stack = [] # For things like dialog

        self.width, self.height = self.map.get_bounds()

    def update(self, keys, dt):
        x, y = self.cursor.get_cursor_pos()
        if keys[key.UP] and y < self.height-1:
            self.cursor.move(0, 1)
            self.camera.move(0, 1)
        elif keys[key.DOWN] and y > 0:
            self.cursor.move(0, -1)
            self.camera.move(0, -1)
        if keys[key.RIGHT] and x < self.width-1:
            self.cursor.move(1, 0)
            self.camera.move(1, 0)
        elif keys[key.LEFT] and x > 0:
            self.cursor.move(-1, 0)
            self.camera.move(-1, 0)

        self.camera.update(dt)
        self.cursor.update(dt)

    def render(self):
        self.camera.render()
        self.map.render()
        self.cursor.render()

