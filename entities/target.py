import pyglet
from system.component import Component
import config

class Target(Component):

    def __init__(self, *args, **kwargs):
        """
        Creates a sprite uning a ball image.
        """
        super(Target, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 5)
        self.name = kwargs.get('name', 'andreas')
        self.state = kwargs.get('state', 'moving')
        pyglet.media.load('assets\\pappa1.wav', streaming=False).play()
        self.images = {
            'andreas' : [
                pyglet.image.load('assets\\andreas.png'),
                pyglet.image.load('assets\\andreas2.png'),
                ]
        }

        for image in self.images[self.name]:
            image.anchor_x = int( image.width / 2 )
            image.anchor_y = int( image.height / 2 )

        self.image = self.images[self.name][0]
        self.width = self.image.width
        self.height = self.image.height
        self.anchor_x = self.image.anchor_x
        self.anchor_y = self.image.anchor_y
        self.sprite = pyglet.sprite.Sprite(self.image, self.x, self.y)

        self.min_x = self.x - self.anchor_x
        self.min_y = self.x - self.anchor_y
        self.max_x = self.y + self.anchor_x
        self.max_y = self.y + self.anchor_y

        self.x_direction = 1
        self.y_direction = 1
        self.z = 2.5
        self.hold = 64



    def check_hit(self, x, y, z):
        self.min_x = self.x - self.anchor_x
        self.min_y = self.y - self.anchor_y
        self.max_x = self.x + self.anchor_x
        self.max_y = self.y + self.anchor_y
        if x > self.min_x and y > self.min_y and \
           x < self.max_x and y < self.max_y:
           if z < 1 and z > 0.2:
               pyglet.media.load('assets\\CAN.WAV', streaming=False).play()
               self.sprite = pyglet.sprite.Sprite(self.images[self.name][1], self.x, self.y)
               self.state = 'shot'
               return True
        return False

    def update(self):
        """
        Increments x and y value and updates positionself.
        Also ensures that the ball does not leave the screen area by changing its axis x_direction
        :return:
        """

        # Two states, either target is shot or its moving
        if self.state == 'shot':
            self.hold -= 1
            self.z -= 0.008
            self.y -= 5
            if self.z < 0:
                self.z = 0
            opacity = int(255 * (self.z/2.5))
            self.sprite.set_position(self.x, self.y)
            self.sprite.update(scale = self.z-1.8, rotation = int(360 * self.z * 2))
            self.sprite.opacity = opacity
            if self.hold <= 0:
                self.sprite.delete()
        elif self.state == 'moving':
            self.x  += (self.speed * self.x_direction)
            self.y  += (self.speed * self.y_direction)

            self.sprite.set_position(self.x, self.y)

            if self.x < self.anchor_x or (self.x + self.anchor_x) > (config.window_width):
                self.x_direction *= -1

            if self.y < self.anchor_y or (self.y + self.anchor_y) > (config.window_height):
                self.y_direction *= -1



    def draw(self):
        """
        Draw our ball sprite to screen
        :return:
        """
        try:
            self.sprite.draw()
        except:
            return -1
