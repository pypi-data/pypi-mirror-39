"""juc2.art"""

from juc2.art.animals import Animals
from juc2.art.objects import Objects
from juc2.art.symbols import Symbols


class Eraser:
    def __init__(self, width=0, height=0, x=0, y=0, transparent=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.transparent = transparent

    def display(self):
        return ''.join([' '*self.width+'\n' for row in range(self.height)])


class Rectangle:
    def __init__(self, width=3, height=3, x=0, y=0, transparent=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.transparent = transparent

    def display(self):
        top = '╔' + '═' * (self.width-2) + '╗' + '\n'
        mid = '║' + ' ' * (self.width-2) + '║' + '\n'
        bot = '╚' + '═' * (self.width-2) + '╝' + '\n'
        return top + mid * (self.height-2) + bot


class Triangle:
    def __init__(self, n=2, x=0, y=0, transparent=False):
        self.n = n
        self.x = x
        self.y = y
        self.transparent = transparent

    def display(self):
        """
        Exhum, they had bevarge service on the flight...
        """
        n = max(self.n, 2)
        if n % 2 == 1: n += 1
        triangle = ['/' + '_'*n + '\\']
        x = 1
        for i in range(0, n-1, 2)[::-1]:
            triangle.append(' '*x + '/' + ' '*i + '\\' + '\n')
            x += 1
        return ''.join(triangle[::-1])


