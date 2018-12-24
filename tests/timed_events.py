from PyDMXControl import Colors
from PyDMXControl.audio import player
from PyDMXControl.controllers import Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.profiles.Eyourlife import Small_Flat_Par
from PyDMXControl.profiles.Stairville import LED_Par_36, LED_Par_10mm
from PyDMXControl.utils.timing import TimedEvents


def get_timed_events(controller: Controller) -> TimedEvents:
    events = TimedEvents(True)

    # Add audio

    def run_audio():
        player.play("you-will-be-found.mp3")
        player.sleep_till_done()

    events.add_run_callback(run_audio)

    # Define some events
    bpm = 87
    bpm_millis = (1 / bpm) * 60 * 1000

    def a0():
        controller.all_color(Colors.Black)
        controller.all_on()
        controller.all_color([0, 0, 15], 12000)

    def a12400():
        controller.all_on(2000)
        controller.get_fixtures_by_name("S1 Art Left")[0].color([50, 100, 255], 2000)
        controller.get_fixtures_by_name("S3 Art Right")[0].color([50, 100, 255], 2000)

    def a18900():
        controller.get_fixtures_by_name("F1 Desk Right")[0].color([160, 140, 255], 2000)
        controller.get_fixtures_by_name("F2 Desk Left")[0].color([160, 140, 255], 2000)

    def a45000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([0, 150, 255])
            fixture.color([0, 0, 255], 15000)

    def a69000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.White, 5000)

        for fixture in controller.get_fixtures_by_profile(Small_Flat_Par):
            fixture.color([0, 128, 255], 5000)

    def a93000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([0, 25, 255], 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.White, 5000)

        for fixture in controller.get_fixtures_by_profile(Small_Flat_Par):
            fixture.color(Colors.White, 5000)

    def a125000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 5000)

        for fixture in controller.get_fixtures_by_profile(Small_Flat_Par):
            fixture.color(Colors.Black, 5000)

    def a138000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.dim(0)
            fixture.dim(255, 15000)

        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), bpm_millis * 4, colors=[
            [50, 128, 255], Colors.Black, Colors.Black, Colors.Black])

    def a152000():
        controller.clear_all_effects()
        controller.all_color(Colors.Blue)
        controller.all_color([50, 100, 255], 2000)

    def a174000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 8000)

        for fixture in controller.get_fixtures_by_profile(Small_Flat_Par):
            fixture.color(Colors.Blue, 8000)

    def a216000():
        controller.all_color([100, 128, 255])

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

    def a248900():
        c = [100, 128, 255]
        controller.all_color(c)

        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), bpm_millis * 4, colors=[c, Colors.Blue, c, c])

    def a270000():
        controller.clear_all_effects()

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Blue, 5000)

    def a292300():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([128, 128, 255], 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

    def a334000():
        controller.get_fixtures_by_name("S1 Art Left")[0].color([50, 100, 255], 1000)
        controller.get_fixtures_by_name("S3 Art Right")[0].color([50, 100, 255], 1000)

    # Store events
    events.add_event(0, a0, name="Start")
    events.add_event(12400, a12400)
    events.add_event(16800, controller.all_color, Colors.Blue, 1000)
    events.add_event(18900, a18900)
    events.add_event(38000, controller.all_color, Colors.Blue, 1000)
    events.add_event(45000, a45000)
    events.add_event(69000, a69000)
    events.add_event(93000, a93000)
    events.add_event(125000, a125000)
    events.add_event(138000, a138000)
    events.add_event(152000, a152000)
    events.add_event(174000, a174000)
    events.add_event(216000, a216000)
    events.add_event(248900, a248900)
    events.add_event(270000, a270000)
    events.add_event(292300, a292300)
    events.add_event(303000, controller.all_color, Colors.White, 500)
    events.add_event(333200, controller.all_color, Colors.Blue, 800)
    events.add_event(334000, a334000)
    events.add_event(344000, controller.all_color, Colors.Blue, 1000)
    events.add_event(354000, controller.all_off, 500)

    return events
