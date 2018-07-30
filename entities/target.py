import pyglet
from system.component import Component
import config
import random
import time as t

class Target(Component):

    def __init__(self, *args, **kwargs):
        """
        Creates a sprite uning a ball image.
        """
        super(Target, self).__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 5)
        self.name = kwargs.get('name', 'andreas')
        self.state = kwargs.get('state', 'moving')
        self.z = kwargs.get('z', 2.5)
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
        self.hold = 64
        self.opacity = 255

        self.sprite.update(scale = self.z)
        self.mul_z = 2.5 # placeholder / mutator for z

        self.prob_change_x = random.random()
        self.prob_change_y = random.random()
        self.last_change_x_time = int(t.time())
        self.last_change_y_time = int(t.time())
        self.id = 0

    def set_id(self,idx):
        self.id = idx


    def check_hit(self, x, y, z):
        self.min_x = self.x - self.anchor_x
        self.min_y = self.y - self.anchor_y
        self.max_x = self.x + self.anchor_x
        self.max_y = self.y + self.anchor_y
        if x > self.min_x and y > self.min_y and \
           x < self.max_x and y < self.max_y:
           if z < 1 * self.z and z > 0.2 * self.z:
               pyglet.media.load('assets\\hit.wav', streaming=False).play()
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
            self.z -= 0.03
            self.y -= 5
            if self.z < 0:
                self.z = 0
            self.opacity -= 4 if self.opacity > 0 else 0
            self.sprite.set_position(self.x, self.y)
            self.sprite.update(scale = self.z, rotation = int((self.y % 356)))
            self.sprite.opacity = self.opacity
            if self.hold <= 0:
                self.sprite.delete()
        elif self.state == 'moving':
            self.x  += (self.speed * self.x_direction)
            self.y  += (self.speed * self.y_direction)

            self.sprite.set_position(self.x, self.y)


            if int(t.time()) - self.last_change_x_time > 1:
                if random.random() <= self.prob_change_x:
                    self.x_direction *= -1
                self.last_change_x_time = int(t.time())

            if int(t.time()) - self.last_change_y_time > 1:
                if random.random() <= self.prob_change_y:
                    self.y_direction *= -1
                self.last_change_y_time = int(t.time())

            if self.x < self.anchor_x:
                print(f'set to {self.anchor_x}')
                self.x = self.anchor_x
                self.x_direction *= -1
            if (self.x + self.anchor_x) > (config.window_width):
                self.x = (config.window_width-self.anchor_x)
                self.x_direction *= -1

            if self.y < self.anchor_y:
                self.y = self.anchor_y
                self.y_direction *= -1
            if (self.y + self.anchor_y) > (config.window_height):
                self.y = (config.window_height-self.anchor_y)
                self.y_direction *= -1

            if self.x_direction == 1:
                self.sprite.update(rotation = 2*self.speed)
            elif self.x_direction == -1:
                self.sprite.update(rotation = -(2*self.speed))



    def draw(self):
        """
        Draw our ball sprite to screen
        :return:
        """
        try:
            self.sprite.draw()
        except:
            return -1
