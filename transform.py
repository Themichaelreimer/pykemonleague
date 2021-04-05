from math import sqrt
from typing import Union
from pyglet.gl import *


class Transform:

    VELOCITY_FLOOR = 0.01
    MIN_SPEED = 8

    def __init__(self):
        self.render_position = Vector2()  # Position to draw at; will move towards self.position automatically every frame
        self.position = Vector2()  # Theoretical position
        self.scale = 1
        self.rotation = 0

    def update(self, dt):

        dv = self.render_position - self.position
        dist2 = dv.length2()
        if dist2 < self.VELOCITY_FLOOR:
            self.render_position = self.position.copy()
        else:
            velocity = (dist2/2)
            if velocity < self.MIN_SPEED:
                velocity = self.MIN_SPEED
            dp = velocity * dt

            # Move render_position towards position by dp units
            self.render_position = self.render_position - dv*dp

    def move(self, dx:int, dy:int):
        self.setPos(self.position.x+dx, self.position.y+dy)

    def setPos(self, x: int, y: int, immediate=False):
        self.position = Vector2(x, y)
        if immediate:
            self.render_position = Vector2(x, y)

    def render(self):
        """ This doesn't really render exactly, it just performs a translation and scale. Not necessary for camera"""
        inv_scale = 1/self.scale
        gl.glScalef(self.scale, self.scale, 1)
        gl.glTranslatef(self.render_position.x * 16 * inv_scale, self.render_position.y * inv_scale * 16, 0)

    def is_moving(self):
        return not self.render_position == self.position


class Vector2:

    def __init__(self, x: Union[int, float] = 0, y: Union[int, float] = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Vector2(x=self.x-other.x, y=self.y-other.y)

    def __mul__(self, other):
        # TODO: Make this right
        dx = other * self.x
        dy = other * self.y
        return Vector2(dx, dy)

    def __str__(self):
        return f"({self.x},{self.y})"

    def copy(self):
        return Vector2(self.x, self.y)

    def length(self):
        return sqrt(self.length2())

    def length2(self):
        return self.x**2 + self.y**2

    def normal(self):
        if self.x == self.y == 0:
            return Vector2()  # I'm defining ||(0,0)|| = (0,0) just because
        dist = self.length()
        return Vector2(x=self.x/dist, y=self.y/dist)
