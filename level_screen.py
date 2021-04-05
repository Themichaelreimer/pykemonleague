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

    def update(self, keys, dt):
        if keys[key.UP]:
            self.cursor.move(0, 1)
            self.camera.move(0, 1)
        elif keys[key.DOWN]:
            self.cursor.move(0, -1)
            self.camera.move(0, -1)
        if keys[key.RIGHT]:
            self.camera.move(1, 0)
        elif keys[key.LEFT]:
            self.camera.move(-1, 0)

        self.camera.update(dt)
        self.cursor.update(dt)

    def render(self):
        self.camera.render()
        self.map.render()
        self.cursor.render()

