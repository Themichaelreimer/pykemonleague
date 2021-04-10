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


FPS = 120.0
game_window = pyglet.window.Window(800, 600)
font = pyglet.resource.add_font("assets/fonts/karmatic-arcade.ttf")
batch = Batch()
keys = key.KeyStateHandler()
game_window.push_handlers(keys)
screens = []

# Enables transparency on pngs
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
# Doesn't follow camera... Maybe use seperate batch?
#test_label = pyglet.text.Label("Test string", x=100, y=100)


@game_window.event
def on_draw():
    game_window.clear()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

    # TODO: Mark screens as being partially transparent
    if len(screens) > 0:
        cur_screen = screens[-1]
        cur_screen.render()

    
def update(dt: float):
    if len(screens) > 0:
        cur_screen = screens[-1]
        cur_screen.update(keys, dt)


def push_screen(screen):
    screens.append(screen)


def pop_screen():
    return screens.pop()


if __name__ == "__main__":
    screens.append(LevelScreen("assets/tilesets/map1-2.tmx", batch))
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()
