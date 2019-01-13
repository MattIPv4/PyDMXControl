from PyDMXControl.design._screen import Screen
from PyDMXControl.design.parts._Pipe import Pipe

screen = Screen()
screen.add_part(Pipe(200, 10, 20, 0))
screen.add_part(Pipe(200, 10, 40, 0))
screen.add_part(Pipe(200, 10, 60, 0))
screen.run()
