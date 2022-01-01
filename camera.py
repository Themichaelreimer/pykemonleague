from transform import *
from pyglet.gl import glTranslatef
from math import ceil

class Camera:

    this = None

    @staticmethod
    def get_camera():
        if Camera.this is not None:
            return Camera.this

    def __init__(self,
                 x=0,
                 y=0,
                 tile_width=16,
                 tile_height=16,
                 width_in_tiles=1,
                 height_in_tiles=1,
                 screen_settings=None
                 ):

        assert(screen_settings is not None, "Screen settings must be defined")

        self.transform = Transform()
        self.transform.setPos(x, y)

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.width_in_tiles = width_in_tiles
        self.height_in_tiles = height_in_tiles
        self.screen_settings = screen_settings

        Camera.this = self

    def move(self, dx: int, dy: int):
        new_x = self.transform.position.x + dx
        new_y = self.transform.position.y + dy

        max_x = self.width_in_tiles - self.screen_settings['tile_width'] + 1
        max_y = self.height_in_tiles - self.screen_settings['tile_height'] + 1

        #breakpoint()
        if not (0 <= new_x < max_x):
            return

        if not (0 <= new_y < max_y):
            return

        self.transform.move(dx, dy)

    def get_pixel_width(self):
        return self.tile_width * self.screen_settings['tile_width']

    def get_pixel_height(self):
        return self.tile_height * self.screen_settings['tile_height']

    def is_moving(self) -> bool:
        return self.transform.is_moving()

    def update(self, dt: float):
        self.transform.update(dt)

    def render(self):
        position = self.transform.render_position
        glTranslatef(
            position.x * self.tile_width * -1,
            position.y * self.tile_height * -1,
            0
        )
