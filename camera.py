from transform import *
from pyglet.gl import glTranslatef


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
                 ):
        self.transform = Transform()
        self.transform.setPos(x, y)

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.width_in_tiles = width_in_tiles
        self.height_in_tiles = height_in_tiles

        self.camera_width = 0
        self.camera_height = 0

        Camera.this = self

    def move(self, dx: int, dy: int):
        # TODO: Factor in camera width to force position such that the viewport is entirely inside the map
        tpos = self.transform.position + Vector2(dx, dy)
        if 0 <= tpos.x < self.width_in_tiles and 0 <= tpos.y < self.height_in_tiles:
            self.transform.move(dx, dy)

    def get_pixel_width(self):
        return self.tile_width * self.width_in_tiles

    def get_pixel_height(self):
        return self.tile_height * self.height_in_tiles

    def update(self, dt: float):
        self.transform.update(dt)

    def render(self):
        position = self.transform.render_position
        glTranslatef(
            position.x * self.tile_width * -1,
            position.y * self.tile_height * -1,
            0
        )