"""juc2.art.animals"""

aardvardk = r'''
       _.---._    /\\
    ./'       "--`\//
  ./              o \
 /./\  )______   \__ \
./  / /\ \   | \ \  \ \
   / /  \ \  | |\ \  \7
    "     "    "  "
'''

bunny = r'''
        /\ /|
       |||| |
        \ | \
    _ _ /  @ @
  /    \   =>X<=
/|      |   /
\|     /__| |
  \_____\ \__\
'''

boar = r'''
          _,-""""-..__
     |`,-'_. `  ` ``  `--'""".
     ;  ,'  | ``  ` `  ` ```  `.
   ,-'   ..-' ` ` `` `  `` `  ` |==.
 ,'    ^    `  `    `` `  ` `.  ;   \
`}_,-^-   _ .  ` \ `  ` __ `   ;    #
   `"---"' `-`. ` \---""`.`.  `;
              \\` ;       ; `. `,
               ||`;      / / | |
              //_;`    ,_;' ,_;"
'''

cat = r'''
\    /\
 )  ( ')
(  /  )
 \(__)|
'''

cow = r'''
(___)
(o o)_____/
 @@ `     \
  \ ____, /
  //    //
 ^^    ^^
'''

deer = r'''
      ""\/  \/""
        "\__/"
         (oo)
-. ______-LJ
 ,'        |
 |.____..  /
 \\      /A\
  |A     |//
'''

dog = r'''
          .-._
         {_}^ )o
{\________//~`
 (         )
 /||~~~~~||\
|_\\_    \\_\_
"' ""'    ""'"'
'''

elephant = r'''
         /  \~~~/  \
   ,----(     ..    )
  /      \__     __/
 /|         (\  |(
^ \   /___\  /\ |
   |__|   |__|-"
'''

elephant_large = r'''
             ___.-~"~-._   __....__
           .'    `    \ ~"~        ``-.
          /` _      )  `\              `\
         /`  a)    /     |               `\
        :`        /      |                 \
   <`-._|`  .-.  (      /   .            `;\\
    `-. `--'_.'-.;\___/'   .      .       | \\
 _     /:--`     |        /     /        .'  \\
("\   /`/        |       '     '         /    :`;
`\'\_/`/         .\     /`~`=-.:        /     ``
  `._.'          /`\    |      `\      /(
                /  /\   |        `Y   /  \
               J  /  Y  |         |  /`\  \
              /  |   |  |         |  |  |  |
             "---"  /___|        /___|  /__|
                    '"""         '"""  '"""
'''

elephant_small = r'''
  .----.-.
 /    ( o \
'|  __ ` ||
 |||  ||| -'
'''

frog = r'''
  oO)-.
 /__  _\
 \  \(  |
  \__|\ {
  '  '--'
'''

gorilla = r'''
      ."`".
  .-./ _=_ \.-.
 {  (,(oYo),) }}
 {{ |   "   |} }
 { { \(---)/  }}
 {{  }'-=-'{ } }
 { { }._:_.{  }}
 {{  } -:- { } }
 {_{ }`===`{  _}
((((\)     (/))))
'''

horse = r'''
                   ;;
                 ,;;'\
      __       ,;;' ' \
    /'  '\'~~'~' \ /'\.)
 ,;(      )    /  |
,;' \    /-.,,(   )
     ) /|      ) /|
     ||(_\     ||(_\
     (_\       (_\
'''

horse = r'''
                   ;;
                 ,;;'\
      __       ,;;' ' \
    /'  '\'~~'~' \ /'\.)
 ,;(      )    /  |
,;' \    /-.,,(   )
     ) /|      ) /|
     ||(_\     ||(_\
     (_\       (_\
'''

lamb = r'''
                 _,._
             __.'   _)
            <_,)'.-"a\
              /' (    \
  _.-----..,-'   (`"--^
 //              |
(|   `;      ,   |
  \   ;.----/  ,/
   ) // /   | |\ \
   \ \\`\   | |/ /
    \ \\ \  | |\/
     `" `"  `"` 
'''

lion = r'''
             o00000000o
            o0/\0000/\0o
           o00\c "" J/00o
 o.       0000/ b  d \000
 `00.     0000    _  |000
  `00     `0000(=_Y_=)00'
  //       ;0000`\7/000'
 ((       /  `0000000'
  \\    .'          |
   \\  /       \  | |
    \\/         ) | |
     \         /_ | |__
     (___________)))))))
                 ```````
'''

lobster = r'''
                         ,.---.   
               ,,,,     /    _ `.
                \\\\   /      \  )
                 |||| /\/``-.__\/
                 ::::/\/_
 {{`-.__.-'(`(^^(^^^(^ 9 `.========='
{{{{{{ { ( ( (  (   (-----:=
 {{.-'~~'-.(,(,,(,,,(__6_.'=========.
                 ::::\/\ 
                 |||| \/\  ,-'/\
                ////   \ `` _/  )
               ```     \  `   /
                         `---''
'''

pig = r'''
                  (\__
              (\   `\__
(`, .------.,-'     b  |
 `-/            ',__,-"` 
  |   `;      ,  |
   \   ;.----/ ,/
    ) // /  ( ( \
    \ \`.`\  \ \ \
     `-` `"   `-`"
'''

seahorse = r'''
   .``-,_
  /o)''..`.
_.`._,,,:_;:
'.` /--/--/
    |-':--|
    |'-"--|
    \--;'-;
     '._;--\
     _  \._|
    ;,'_/'/
    '.__.'
'''

snail = r'''
    ______
   /  ___ \
  |  / ,.\ |O    O
  | |  \d/ | \__/
  |__\_____/-(..)
_/_____________/
'''

whale = r'''
     .-'
'--./ /     _.---.
'-,  (__..-`       \
   \          .     |
    `,.__.   ,__.--/
      '._/_.'___.-`
'''


class _Meta:
    def __init__(self, x=0, y=0, transparent=False):
        self.x = x
        self.y = y
        self.transparent = transparent
    
    def display(self):
        return self.figure


class Animals:

    class Aardvardk(_Meta):
        author = 'VK'
        figure = aardvardk

    class Bunny(_Meta):
        author = 'unknown'
        figure = bunny

    class Boar(_Meta):
        author = 'jrei'
        figure = boar

    class Cat(_Meta):
        author = 'jgs'
        figure = cat

    class Cow(_Meta):
        author = 'jgs'
        figure = cow

    class Deer(_Meta):
        author = 'vir'
        figure = deer

    class Dog(_Meta):
        author = 'jgs'
        figure = deer

    class Elephant(_Meta):
        author = 'hjw'
        figure = elephant

    class ElephantLarge(_Meta):
        author = 'jgs'
        figure = elephant_large

    class ElephantSmall(_Meta):
        author = 'unknown'
        figure = elephant_small

    class Frog(_Meta):
        author = 'Dov Sherman'
        figure = frog

    class Gorilla(_Meta):
        author = 'jgs'
        figure = gorilla

    class Horse(_Meta):
        author = 'unknown'
        figure = horse

    class Lamb(_Meta):
        author = 'jgs'
        figure = lamb

    class Lion(_Meta):
        author = 'jgs'
        figure = lion

    class Lobster(_Meta):
        author = 'jgs'
        figure = lobster

    class Pig(_Meta):
        author = 'jgs'
        figure = pig

    class Seahorse(_Meta):
        author = 'fsr'
        figure = seahorse

    class Snail(_Meta):
        author = 'dwb'
        figure = snail

    class Whale(_Meta):
        author = 'unknown'
        figure = whale
