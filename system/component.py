import abc
# abs let us create abstract classes that can only be derived,
# not instatiated.

class Component(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        """
        Constructs Component object given passed kwargs.
        :param active Defines if the object has to update
        :param render Defines if the object has to render
        :param x Defines the x location of the object
        :param y Defines the y location of the object
        :param width Defines the width of the object
        :param height Defines the height of the object
        """

        # Basic stuff
        self.activate = kwargs.get('activate', True)
        self.render = kwargs.get('render', True)
        self.debug = kwargs.get('debug', False)
        self.x = kwargs.get('x', 0.0)
        self.y = kwargs.get('y', 0.0)
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)

        @abc.abstractmethod
        def update_self(self):
            pass

        @abc.abstractmethod
        def draw_self(self):
            pass

        
