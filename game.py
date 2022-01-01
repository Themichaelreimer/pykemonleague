import pyglet
from pyglet.window import key
from pyglet.graphics import Batch
from level_screen import LevelScreen
from pyglet.gl import *

class TestInputScreen:

    def __init__(self, batch):
        self.name = "TestScreen"
        self.st = "Test"
        self.batch = batch
        self.label = None
        self.make_label(self.st)

    def make_label(self, s: str):
        self.label = pyglet.text.Label(s, font_size=36, x=400, y=300,batch=self.batch)

    def update(self, keys: dict, dt: float):
        keys_str = [str(k) for k in keys if keys[k]]
        new_st = " ".join(keys_str)

        self.st = new_st
        self.make_label(new_st)

    def render(self):
        if self.label:
            self.label.draw()

window_config = {
    
}

screen_settings = {
    'sx':1,  # x scale relative to default size
    'sy':1,  # y scale ^^
    'tile_width': 30, # width of screen in tiles
    'tile_height': 20,  # height of screen in tiles
    'tile_size': 32, # size of tiles in pixels
    'width': 32 * 30,  # width in pixels
    'height': 32 * 20, # height in pixels
}

FPS = 60.0
game_window = pyglet.window.Window(
    screen_settings['width'],
    screen_settings['height'],
    config = window_config,
    resizable=True
)

font = pyglet.resource.add_font("assets/fonts/karmatic-arcade.ttf")
batch = Batch()
keys = key.KeyStateHandler()
game_window.push_handlers(keys)
screens = []

# Enables transparency on pngs
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Doesn't follow camera... Maybe use seperate batch?
# test_label = pyglet.text.Label("Test string", x=100, y=100)


@game_window.event
def on_draw():
    game_window.clear()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    # Scale to screen dimensions. The 2.0 scales the 16x16 tiles -> 32x32
    glScalef(2.0 * screen_settings['sx'], 2.0 * screen_settings['sy'], 1.0)

    # TODO: Mark screens as being partially transparent
    if len(screens) > 0:
        cur_screen = screens[-1]
        cur_screen.render()

@game_window.event
def on_resize(width, height):
    default_w = screen_settings['width']
    default_h = screen_settings['height']
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glScalef(width/default_w, height/default_h, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    sx = width/default_w
    sy = height/default_h
    screen_settings['sx'] = sx
    screen_settings['sy'] = sy

    
def update(dt: float):
    if len(screens) > 0:
        cur_screen = screens[-1]
        cur_screen.update(keys, dt)


def push_screen(screen):
    screens.append(screen)


def pop_screen():
    return screens.pop()


if __name__ == "__main__":
    screens.append(LevelScreen("assets/tilemaps/lv1.tmx", batch, screen_settings))
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()
