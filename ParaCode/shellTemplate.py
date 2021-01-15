for file in *.peach; do
    rm "$file"
done


import sys

import os

import basic
import config
#import installDependencies

from colorama import init
from colorama import Fore as coloramaFore
from colorama import Back as coloramaBack
from colorama import Style as coloramaStyle
from colored import fore as Fore
from colored import back as Back
from colored import fg as Fg
from colored import bg as Bg
from colored import attr as Attr

import time

returned = config.returned

used = 0
executed = 0
canSubmit = True
debug = config.debug

# -- Configuration (Settings) -- #

user_color = "white"
user_style = "none"
console_color = "white"
console_style = "none"

pointer = "ParaCode Shell >>>"
pointer_color = "green"
pointer_style = "none"

error_color = "red"
error_style = "none"


while True:
    if used == 0:
        # print('ParaCode Shell Launched Successfully!')
        # print("")
        # print("")
        # print("")
        if __name__ == "__main__":
            os.system('')
            init()
            args = sys.argv
            if len(args) == 2:
                print(pointer_color + pointer_style + pointer + console_color + console_style + " " + args[1])
                time.sleep(1.25)
                basic.run('<stdin>', 'RUN("' + str(os.path.join(sys._MEIPASS, "shellTemplate.para")).replace('\\', '/').replace("'", '"') + '")')
        used = 1