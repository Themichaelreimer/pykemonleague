from typing import Tuple

import pyglet
import pyglet.gl as gl
from transform import *

class Cursor:

    def __init__(self):
        self.transform = Transform()
        self.sprite = pyglet.resource.image("assets/sprites/cursor.png")

    def get_cursor_pos(self) -> Tuple[int,int]:
        return self.x(), self.y()

    def move(self, dx, dy):
        self.transform.move(dx, dy)

    def update(self, dt):
        self.transform.update(dt)

    def render(self):
        p = self.transform.render_position
        gl.glPushMatrix()
        self.transform.render()  # Actually just applies the transform matrix
        self.sprite.blit(0, 0, 0)
        gl.glPopMatrix()

    def x(self):
        return self.transform.position.x

    def y(self):
        return self.transform.position.y

    def is_moving(self):
        return self.transform.is_moving()

