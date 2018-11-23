from time import sleep

from PyDMXControl.audio import player

player.play("tests/you-will-be-found.mp3")
sleep(5)
player.pause()
print("paused")
sleep(1)
player.unpause()

player.sleep_till_done()
print("done")
