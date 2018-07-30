import pyglet
import config
import time as t

from system.component import Component
from entities.shot import Shot
from entities.target import Target
from random import randint
from random import choice



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
pyglet.resource.path = ['assets']
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
window.level_text = pyglet.text.Label(f'LEVEL 1',
    font_name='Time New Roman',
    font_size=46,
    x=200, y=window.height - 100,
    anchor_x='center', anchor_y='center')

window.game_state = 'play'
window.last_target_time = 0
window.last_level_time = int(t.time())
window.level = 1
#############################################################


def draw():
    """
    Clears screen and renders our objects
    :return:
    """
    window.clear()
    if window.game_state == 'play':
        window.backgrounds[0].blit(0,0)

        map(lambda idx,i: i.set_id(idx),enumerate(target_objects))
        # draw all targets
        for target in sorted(target_objects, key=lambda obj: obj.z):
            if isinstance(target, Component):
                if target.draw() == -1:
                    del target_objects[target.id]

        # draw all shots fired
        for idx, shot in enumerate(shot_objects):
            if isinstance(shot, Component):
                if shot.draw() == -1:
                    del shot_objects[idx]

    elif window.game_state == 'end':
        window.center_text.draw()
        window.play_again_text.draw()

    window.score.draw()
    window.level_text.draw()



def update(time):
    """
    Updates our list of entity (shot and target) objects
    :param time:
    :return:
    """

    if int(t.time()) - window.last_level_time > 15:
        window.level += 1
        window.level_text.text = f'LEVEL {window.level}'
        window.last_level_time = int(t.time())

    if len(target_objects) < 15:
        if int(t.time()) - window.last_target_time > 1:
            for i in range((randint(1,window.level)%5)):
                if randint(0,10) < 4+window.level:
                    x = randint(50, config.window_width - 50)
                    y = randint(50, config.window_height - 50)
                    z = choice( [.50, .75, 1.0, 1.25, 1.50, 1.75, 2.0] )
                    print(f'z: {z}')
                    target_objects.append(Target(
                        name='andreas',
                        x=x, y=y,
                        speed=randint(0,window.level),
                        state='moving',
                        z=z
                    ))
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
                            score += target.speed+1
                            window.score.text=f'{score}'





# Did not get mouse_press to work in windows
@window.event
def on_mouse_release(x, y, button, modifiers):
    """
    On each mouse click, we create a new shot object
    """
    print('x: {}, y {}, button {}, modifiers {}'.format(x, y, button, modifiers))
    if window.game_state == 'play':
        name = 'miranda' if randint(0,1) == 0 else 'emil'
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
