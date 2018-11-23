from time import sleep

from PyDMXControl.audio import player

player.set_volume(0)
player.set_volume(1, 5000)
player.play("tests/you-will-be-found.mp3")
print("playing")
sleep(10)
player.pause()
print("paused")
sleep(3)
player.unpause()
print("unpaused")
player.sleep_till_done()
print("done")
