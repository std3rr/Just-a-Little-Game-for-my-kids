import pyglet
from system.component import Component
import config

class Shot(Component):

    def __init__(self, *args, **kwargs):
        """
        Creates a sprite uning a ball image.
        """
        super(Shot, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 5)
        self.name = kwargs.get('name', 'miranda')
        pyglet.media.load(f'assets\\{self.name}_shot.wav', streaming=False).play()
        self.images = {
            'miranda' : [
                pyglet.image.load('assets\\miranda.png')
                ],
            'emil' : [
                pyglet.image.load('assets\\emil.png')
            ]
        }

        self.image = self.images[self.name][0]

        self.width = self.image.width
        self.height = self.image.height
        #self.anchor_x = self.ball_image.anchor_x = int(self.width/2)
        #self.anchor_y = self.ball_image.anchor_y = int(self.height/2)
        self.anchor_x = self.image.anchor_x = int(  self.width / 2 )
        self.anchor_y = self.image.anchor_y = int( self.height / 2 )
        self.sprite = pyglet.sprite.Sprite(self.image, self.x, self.y)
        self.min_x = self.x - self.anchor_x
        self.min_y = self.x - self.anchor_y
        self.max_x = self.y + self.anchor_x
        self.max_y = self.y + self.anchor_y

        self.z = 2.5


    def update(self):
        """
        Increments x and y value and updates positionself.
        Also ensures that the ball does not leave the screen area by changing its axis x_direction
        :return:
        """

        # gravitation? :)
        self.y -= 2
        self.z -= 0.08
        self.sprite.set_position(self.x, self.y)

        self.sprite.update(scale = self.z) #, rotation = int(360 * self.z/8))
        #self.ball_sprite.opacity = int(255 * (self.z))

        if self.z <= 0:
            self.sprite.delete()


    def draw(self):
        """
        Draw our ball sprite to screen
        :return:
        """
        try:
            self.sprite.draw()
        except:
            return -1
