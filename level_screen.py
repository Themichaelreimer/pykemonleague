from pytmx import *
from pytmx.util_pyglet import load_pyglet
import pyglet
from pyglet.gl import *
from pyglet.window import key

# TODO:
# Move all this crap into a Map Object and
# refocus what LevelScreen should be

class SafeSprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(SafeSprite, self).__init__(*args, **kwargs)
        gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        #gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        #gl.glTexParameteri(self._texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


class LevelScreen:

    def __init__(self, path, batch):
        self.name="level1"
        self.batch = batch
        #path = pyglet.resource.file("assets/tilesets/map1-2")
        self.tm = load_pyglet(path)

        self.width_in_tiles = self.tm.width
        self.height_in_tiles = self.tm.height
        self.tile_width = self.tm.tilewidth
        self.tile_height = self.tm.tileheight
        self.pixel_width = self.width_in_tiles * self.tm.tilewidth
        self.pixel_height = self.height_in_tiles * self.tm.tileheight

        # Map of tiles with properties that are active
        # ie, the top most non-empty non-decorative tile
        self.effective_map = {}
        self.sprites = []
        self.batches = []

        self.generate_sprites()

        self.x = 0
        self.y = 0

    def get_tile_at_position(self, x: int, y: int) -> dict:
        if x < 0 or x >= self.width_in_tiles:
            raise Exception("Queried Tile out of bounds")
        if y < 0 or y >= self.height_in_tiles:
            raise Exception("Queried Tile out of bounds")
        tid = self.effective_map[(x, y)]
        return self.tm.tile_properties[tid]

    def generate_sprites(self):
        tw = self.tm.tilewidth
        th = self.tm.tileheight
        mw = self.tm.width
        mh = self.tm.height

        for layer in self.tm.visible_layers:
            new_batch = pyglet.graphics.Batch()
            self.batches.append(new_batch)
            if isinstance(layer, TiledTileLayer):
                for tx, ty, img in layer.tiles():
                    adj_x = tx*tw
                    adj_y = self.pixel_height - (ty * th)

                    spr = SafeSprite(
                        img,
                        batch=new_batch,
                        x=adj_x,
                        y=adj_y
                    )

                    print(f"Sprite ({adj_x}, {adj_y})")
                    self.sprites.append(spr)
                    self.effective_map[(tx, ty)] = layer.data[tx][ty]
            elif isinstance(layer, TiledObjectGroup):
                pass
            elif isinstance(layer, TiledImageLayer):
                pass


    def update(self, keys: dict, dt: float):
        if keys[key.UP] and self.y < self.height_in_tiles - 1:
            self.y += 1
        elif keys[key.DOWN] and self.y > 0:
            self.y -= 1
        if keys[key.RIGHT] and self.x < self.width_in_tiles - 1:
            self.x += 1
        elif keys[key.LEFT] and self.x > 0:
            self.x -= 1

    def render(self):

        glLoadIdentity()
        #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        glTranslatef(self.x * self.tile_width*-1, self.pixel_height - self.y * self.tile_height, 0.0)
        for batch in self.batches:
            batch.draw()
