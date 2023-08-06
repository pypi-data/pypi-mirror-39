"""juc2.art"""

#LOVE = '<3'
#def load_art(category, name):
#    path = '{}/{}.txt'.format(category, name)
#    data = [i for i in open(path, 'rb').readlines() if not i.startswith(LOVE)]
#    #with open(path, 'rb') as f:
#    #    data = f.read()
#    return ''.join(data)


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

categories = ['Animals']

class Animals:

    class Aardvardk:
        

        def __init__(self, x=0, y=0, transparent=False):
            self.name = self.__class__.__name__
            self.x = x
            self.y = y
            self.transparent = transparent

        def display(self):
            from .ascii_art.animals import aardvark
            return aardvark()

            # return load_art('Animals', self.name)
    #        return r'''
    #       _.---._    /\\
    #    ./'       "--`\//
    #  ./              o \
    # /./\  )______   \__ \
    #./  / /\ \   | \ \  \ \
    #   / /  \ \  | |\ \  \7
    #    "     "    "  "
    #'''

#
# make an ascii art reader that is amazing.
# read in an ascii sheet with x, y coordinates
# then read them in here as objects like
# art.tools.Screwdriver()
#

#############
# unique shapes

#
# This little weird game engine could have style.
#

#
# reference the orginial source wherever possible
#

"""
juc2.figures.tools.screwdriver
Author: jgs
Source: https://asciiart.website/index.php?art=objects/tools
"""