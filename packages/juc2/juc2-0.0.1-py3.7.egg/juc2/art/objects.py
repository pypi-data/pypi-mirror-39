"""juc2.art.objects"""

anchor = r'''
             (_)
              |
         ()---|---()
              |
              |
       __     |     __
      |\     /^\     /|
        '..-'   '-..'
          `-._ _.-`
'''

axe = r'''
  ,  /\  .
 //`-||-'\\
(| -=||=- |)
 \\,-||-.//
  `  ||  '
     ||
     ||
     ||
     ||
     ||
     ()
'''

balloon = r'''
     ,-""""-.
   ,'      _ `.
  /       )_)  \
 :              :
 \              /
  \            /
   `.        ,'
     `.    ,'
       `.,'
        /\`.   ,-._
            `-'    
'''

bomb_small = r'''
     ,--.!,
  __/   -*-
,d08b.  '|`
0088MM
`9MMP'
'''

bomb_large = r'''
             . . .
              \|/
            `--+--'
              /|\
             ' | '
               |
               |
           ,--'#`--.
           |#######|
        _.-'#######`-._
     ,-'###############`-.
   ,'#####################`,
  /#########################\
 |###########################|
|#############################|
|#############################|
|#############################|
|#############################|
 |###########################|
  \#########################/
   `.#####################,'
     `._###############_,'
        `--..#####..--'
'''

bone = r'''
 .-.               .-.
(   `-._________.-'   )
 >=     _______     =<
(   ,-'`       `'-,   )
 `-'               `-'
'''

book = r'''
      _.--._  _.--._
,-=.-":;:;:;\':;:;:;"-._
\\\:;:;:;:;:;\:;:;:;:;:;\
 \\\:;:;:;:;:;\:;:;:;:;:;\
  \\\:;:;:;:;:;\:;:;:;:;:;\
   \\\:;:;:;:;:;\:;::;:;:;:\
    \\\;:;::;:;:;\:;:;:;::;:\
     \\\;;:;:_:--:\:_:--:_;:;\
      \\\_.-"      :      "-._\
       \`_..--""--.;.--""--.._=>
'''

bucket = r'''
        ___
     .-'   `-.
    /         \
   /   _____   \
  /.-'"     "`-.\
 d(             )b
  |`-.._____..-'|
  |             |
  |             |
  |             |
  |             |
  |             |
  |             |
  |             |
  \             /
   `-.._____..-'
'''

camera = r'''
       ____
  _[]_/____\__n_
 |_____.--.__()_|
 |LI  //# \\    |
 |    \\__//    |
 |     '--'     |
 '--------------'
'''

candle = r'''
        )
       (_)
      .-'-.
      |   |
      |   |
      |   |
      |   |
    __|   |__   .-.
 .-'  |   |  `-:   :
:     `---'     :-'
 `-._       _.-'
     '""""""
'''

cigarette = r'''
              )
             (
 _ ___________ )
[_[___________#
'''

clock = r'''
  _______
 /  12   \
|    |    |
|9   |   3|
|     \   |
|         |
 \___6___/
'''

diamond = r'''
  .     '     ,
    _________
 _ /_|_____|_\ _
   '. \   / .'
     '.\ /.'
       '.'
'''

feather = r'''
             _______  ____________
        ,,/\/    /  \/  //  /  /   \
=\\\\\\\============================-
        ``\ \  \\   \    \   /\  \ /
           ----- ------------  ---
'''

gun = r'''
  _  __________=__
   \\@([____]_____()
  _/\|-[____]
 /     /(( )
/____|'----'
\____/
'''

light_bulb = r'''
  ..---..
 /       \
|         |
:         ;
 \  \~/  /
  `, Y ,'
   |_|_|
   |===|
   |===|
    \_/
'''

wine_bottle = r'''
    __
   [__]
   |  |
   |  |
   |  |
   |  |
   |  |
  /`-. \
 /-._|  \
|        |
|`-...   |
|'` . |  |
|`,'- |  |
|`-...|  |
|        |
 `-....-'
'''

wine_glass = r'''
 ,----.
(      ) 
|`----'|
\      /
 `.  ,'
   ||     
 ,-||-.
(  ''  )
 `----'
'''


class _Meta:
    def __init__(self, x=0, y=0, transparent=False):
        self.x = x
        self.y = y
        self.transparent = transparent
    
    def display(self):
        return self.figure


class Objects:

    class Anchor(_Meta):
        author = 'jgs'
        figure = anchor

    class Axe(_Meta):
        author = 'hjm'
        figure = axe
    
    class Balloon(_Meta):
        author = 'hjm'
        figure = balloon

    class BombSmall(_Meta):
        author = 'hjm'
        figure = bomb_small
    
    class BombLarge(_Meta):
        author = 'unknown'
        figure = bomb_large

    class Bone(_Meta):
        author = 'jgs'
        figure = bone

    class Book(_Meta):
        author = 'shimrod'
        figure = book

    class Bucket(_Meta):
        author = 'VK'
        figure = bucket
    
    class Camera(_Meta):
        author = 'jgs'
        figure = camera

    class Candle(_Meta):
        author = 'jgs'
        figure = candle
    
    class Cigarette(_Meta):
        author = 'jgs'
        figure = cigarette
    
    class Clock(_Meta):
        author = 'unknown'
        figure = clock
    
    class Diamond(_Meta):
        author = 'unknown'
        figure = diamond

    class Feather(_Meta):
        author = 'unknown'
        figure = feather
    
    class Gun(_Meta):
        author = 'unknown'
        figure = gun
    
    class LightBulb(_Meta):
        author = 'Peter Punk'
        figure = light_bulb

    class WineBottle(_Meta):
        author = 'jrei'
        figure = wine_bottle
    
    class WineGlass(_Meta):
        author = 'jrei'
        figure = wine_glass
