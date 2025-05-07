import math

class Vec:
    """
    Custom 2D vector class, used through-out project for 2d vector calculations e.g. velocity

    object stores only x and y component of Vector
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __truediv__(self, other):
        """
        Divides both components of the vector by the input value
        :param other: float | int
        :return: Vec
        """
        return Vec(self.x / other, self.y / other)

    def __floordiv__(self, other):
        """
        Does Floor division to both components of the Vector
        :param other: float | int
        :return: Vec
        """
        return Vec(self.x // other, self.y // other)

    def __mul__(self, other):
        """
        Does multiplication to both components of the Vector
        :param other: float | int
        :return: Vec
        """
        return Vec(self.x * other, self.y * other)

    def __sub__(self, other):
        """
        Subtracts another vector off itself and returns the new vector
        :param other: Vec
        :return: Vec
        """
        return Vec(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """
        Adds another vector to itself and returns the new vector
        :param other: Vec
        :return: Vec
        """
        return Vec(self.x + other.x, self.y + other.y)
    def __neg__(self):
        """
        Returns a negated version of itself
        :return: Vec
        """
        return Vec(-self.x,-self.y)

    def __getitem__(self,item):
        """
        Allows the vector to be treated like a list of 2 values [x,y]
        :param item:  int
        :return: float | int
        """
        if item == 0: return self.x
        elif item == 1: return self.y
    def __setitem__(self,key,value):
        """
        Allows the vector to be treated like a list of 2 values [x,y]
        :param key: int
        :param value: float | int
        :return: None
        """
        if key%2 == 0: self.x = value
        else: self.y = value

    def __str__(self):
        """
        function that allows the object to be turned into a string and output
        :return: str
        """
        return f'<Vector2: ({self.x}, {self.y})>'
    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        """
        Allows the object to be iterated through and unpacked same as a tuple
        :return: tuple
        """
        return iter((self.x, self.y))

    @staticmethod
    def make_from_angle(angle,magnitude=1):
        """

        :param angle: float (radians)
        :param magnitude: float | int
        :return: Vec
        """
        return Vec(math.cos(angle),math.sin(angle))*magnitude

    def tuple(self,force_int=False):
        """
        returns itself as a tuple
        :param force_int: bool
        :return: tuple
        """
        if force_int: return (int(self.x),int(self.y))
        else: return (self.x,self.y)

    def length(self):
        """
        returns the length of the vector
        :return: float
        """
        return ((self.x)**2+(self.y)**2)**0.5
    def angle(self):
        """
        returns the angle of the vector
        :return: float (radians)
        """
        return math.atan2(self.y,self.x)

    def normalize(self):
        """
        sets the length of the vector to 1, if length is 0 then vector does not change
        :return: None
        """
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
    def normalized(self):
        """
        returns a vector of length 1 and angle of current vector, if length is 0 then returns self
        :return: Vec
        """
        self.normalize()
        return self
    def copy(self):
        """
        returns an identicle copy of the vector
        :return: Vec
        """
        return Vec(self.x,self.y)
    def length_squared(self):
        """
        returns the length of the vector squared, used for vector length comparison as it saves using the sqrt operation
        :return: float
        """
        return (self.x)**2+(self.y)**2