import pyglet
import config
import time as t

from system.component import Component
from entities.shot import Shot
from entities.target import Target
from random import randint



shot_objects = []
target_objects = []

#############################################################
# Initialize window

# Get screen resolution and init fullscreen
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
window = pyglet.window.Window(fullscreen=True,
                                height=screen.height,
                              width=screen.width)
pyglet.resource.path = [config.resource_path]
pyglet.resource.reindex()
window.backgrounds = [
    pyglet.resource.image('sannabadet.jpg')
]
for image in window.backgrounds:
    image.width = screen.width
    image.height = screen.height
window.set_mouse_cursor(
    window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
)

window.score = pyglet.text.Label(f'0',
    font_name='Time New Roman',
    font_size=36,
    x=window.width/2, y=window.height - 64,
    anchor_x='center', anchor_y='center')
window.center_text = pyglet.text.Label(f'GAME OVER',
    font_name='Time New Roman',
    font_size=46,
    x=window.width/2, y=window.height/2,
    anchor_x='center', anchor_y='center')
window.play_again_text = pyglet.text.Label(f'tryck höger musknapp för att spela igen',
    font_name='Time New Roman',
    font_size=12,
    x=window.width/2, y=window.height/2 + 40,
    anchor_x='center', anchor_y='center')

window.game_state = 'play'
window.last_target_time = 0
#############################################################


def draw():
    """
    Clears screen and renders our objects
    :return:
    """
    window.clear()
    if window.game_state == 'play':
        window.backgrounds[0].blit(0,0)

        # draw all shots fired
        for idx, target in enumerate(target_objects):
            if isinstance(target, Component):
                if target.draw() == -1:
                    del target_objects[idx]

        # draw all targets
        for idx, shot in enumerate(shot_objects):
            if isinstance(shot, Component):
                if shot.draw() == -1:
                    del shot_objects[idx]
    elif window.game_state == 'end':
        window.center_text.draw()
        window.play_again_text.draw()

    window.score.draw()



def update(time):
    """
    Updates our list of entity (shot and target) objects
    :param time:
    :return:
    """

    if len(target_objects) < 10:
        if int(t.time()) - window.last_target_time > 1:
            for i in range(randint(1,3)):
                x = randint(50, config.window_width - 50)
                y = randint(50, config.window_height - 50)
                target_objects.append(Target(name='andreas', x=x, y=y, speed=randint(0,6), state='moving'))
            window.last_target_time = int(t.time())
    elif window.game_state == 'play':
        window.game_state = 'end'
        del shot_objects[:]


    if window.game_state == 'play':
        for target in target_objects:
            if isinstance(target, Component):
                if target.hold <= 0:
                    try:
                        del target_objects[tidx]
                    except:
                        None
                else:
                    target.update()
        #print(f'{pyglet.our_score}')
        for bidx, shot in enumerate(shot_objects):
            if isinstance(shot, Component):
                shot.update()
                for tidx, target in enumerate(target_objects):
                    if isinstance(target, Component):
                        if target.check_hit(shot.x, shot.y, shot.z) == True:
                            try:
                                del shot_objects[bidx]
                            except:
                                None
                            score = int(window.score.text)
                            score += target.speed
                            window.score.text=f'{score}'





# Did not get mouse_press to work in windows
@window.event
def on_mouse_release(x, y, button, modifiers):
    """
    On each mouse click, we create a new shot object
    """
    print('x: {}, y {}, button {}, modifiers {}'.format(x, y, button, modifiers))
    if window.game_state == 'play':
        name = 'miranda' if len(shot_objects) % 2 == 0 else 'emil'
        shot_objects.append(Shot(name=name, x=x, y=y, speed=randint(-2,3)))
    elif window.game_state == 'end' and button == 4:
        window.score.text=f'0'
        del target_objects[:]
        window.game_state = 'play'


def main():
    """
    This is the main method. This contains an embedded method.
    :return:
    """

    @window.event
    def on_draw():
        draw()
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
main()
