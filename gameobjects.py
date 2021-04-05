import pyglet
from pyglet.gl import *
from transform import *


class Cursor:

    def __init__(self):
        self.transform = Transform()
        self.sprite = pyglet.resource.image("assets/sprites/cursor.png")

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
