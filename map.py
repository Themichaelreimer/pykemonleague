from pytmx import *
from pytmx.util_pyglet import load_pyglet

import pyglet
from pyglet.gl import glTexParameteri, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE

from camera import Camera

# TODO:
# Move all this crap into a Map Object and
# refocus what LevelScreen should be


class SafeSprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(SafeSprite, self).__init__(*args, **kwargs)
        glTexParameteri(self._texture.target, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(self._texture.target, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        #gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        #gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


class Map:

    def __init__(self, path):
        self.name = "level1"
        self.tm = load_pyglet(path)

        self.width_in_tiles = self.tm.width
        self.height_in_tiles = self.tm.height
        self.tile_width = self.tm.tilewidth
        self.tile_height = self.tm.tileheight
        self.pixel_width = self.width_in_tiles * self.tm.tilewidth
        self.pixel_height = self.height_in_tiles * self.tm.tileheight
        self.x = 0
        self.y = 0

        # Map of tiles with properties that are active
        # ie, the top most non-empty non-decorative tile
        self.effective_map = {}
        self.map_objects = {}
        self.sprites = []
        self.batches = []

        self.generate_sprites()
        self.camera = Camera(
            x=self.x,
            y=self.y,
            tile_width=self.tile_width,
            tile_height=self.tile_height,
            width_in_tiles=self.width_in_tiles,
            height_in_tiles=self.height_in_tiles
        )

    def get_tile_at_position(self, x: int, y: int) -> dict:
        if x < 0 or x >= self.width_in_tiles:
            raise Exception("Queried Tile out of bounds")
        if y < 0 or y >= self.height_in_tiles:
            raise Exception("Queried Tile out of bounds")
        tid = self.effective_map[(x, y)]
        return self.tm.tile_properties[tid]

    def get_object_at_position(self, x: int, y: int):
        if (x, y) in self.map_objects:
            return self.map_objects[(x, y)]

    def generate_sprites(self):
        tw = self.tm.tilewidth
        th = self.tm.tileheight

        for layer in self.tm.visible_layers:
            new_batch = pyglet.graphics.Batch()
            self.batches.append(new_batch)
            if isinstance(layer, TiledTileLayer):
                for tx, ty, img in layer.tiles():
                    adj_x = tx*tw
                    adj_y = self.pixel_height - ((ty+1) * th)

                    spr = SafeSprite(
                        img,
                        batch=new_batch,
                        x=adj_x,
                        y=adj_y
                    )

                    self.sprites.append(spr)
                    self.effective_map[(tx, ty)] = layer.data[tx][ty]
            elif isinstance(layer, TiledObjectGroup):
                pass
            elif isinstance(layer, TiledImageLayer):
                pass

    def update(self, keys: dict, dt: float):
        pass

    def render(self):
        #self.camera.render()
        for batch in self.batches:
            batch.draw()