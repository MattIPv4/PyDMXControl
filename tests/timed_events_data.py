from PyDMXControl import Colors
from PyDMXControl.audio import player
from PyDMXControl.controllers import Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.profiles.Stairville import LED_Par_36, LED_Par_10mm
from PyDMXControl.profiles.funGeneration import LED_Pot_12_RGBW
from PyDMXControl.utils.timing import TimedEvents


def you_will_be_found(controller: Controller) -> TimedEvents:
    events = TimedEvents(True)

    # Add audio

    def run_audio():
        player.play("you-will-be-found.mp3")
        player.sleep_till_done()

    def stop_audio():
        player.stop()

    events.add_run_callback(run_audio)
    events.add_stop_callback(stop_audio)

    # Define some events
    bpm = 87
    bpm_millis = (1 / bpm) * 60 * 1000

    def a0():
        controller.all_off()
        controller.clear_all_effects()
        controller.all_color(Colors.Black)
        controller.all_on()
        controller.all_color([0, 0, 15], 12000)

    def a12400():
        controller.all_on(2000)
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([50, 100, 255], 2000)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([50, 100, 255], 2000)

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

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([0, 128, 255], 5000)

    def a93000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([0, 25, 255], 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.White, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.White, 5000)

    def a125000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
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

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
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
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([50, 100, 255], 1000)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([50, 100, 255], 1000)

    # Store events
    events.add_event(0, a0, name="Start (dim blue)")
    events.add_event(12400, a12400, name="Evan first")
    events.add_event(16800, controller.all_color, Colors.Blue, 1000)
    events.add_event(18900, a18900, name="Evan second")
    events.add_event(38000, controller.all_color, Colors.Blue, 1000)
    events.add_event(45000, a45000, name="Evan third")
    events.add_event(69000, a69000, name="'And OoooOh'")
    events.add_event(93000, a93000, name="'You will be found' boost")
    events.add_event(125000, a125000, name="Into social dark")
    events.add_event(138000, a138000, name="Social chase")
    events.add_event(152000, a152000, name="Out of social")
    events.add_event(174000, a174000, name="News voices")
    events.add_event(216000, a216000, name="Last 'Thank you, Evan Hansen'")
    events.add_event(248900, a248900)
    events.add_event(270000, a270000, name="End chase, 'you are not alone'")
    events.add_event(292300, a292300, name="End of 'you are not alone'")
    events.add_event(303000, controller.all_color, Colors.White, 500, name="'You will be found' boost")
    events.add_event(333200, controller.all_color, Colors.Blue, 800, name="Blue")
    events.add_event(334000, a334000, name="Evan spot")
    events.add_event(344000, controller.all_color, Colors.Blue, 1000)
    events.add_event(354000, controller.all_off, 500, name="End (blackout)")

    return events


def into_the_unknown(controller: Controller) -> TimedEvents:
    events = TimedEvents(True)

    # Add audio

    def run_audio():
        player.play("into-the-unknown.mp3")
        player.sleep_till_done()

    def stop_audio():
        player.stop()

    events.add_run_callback(run_audio)
    events.add_stop_callback(stop_audio)

    # BPM
    bpm = 145
    bpm_millis = (1 / bpm) * 60 * 1000

    # Define some events
    not_flood = controller.get_fixtures_by_profile(LED_Par_36) + controller.get_fixtures_by_profile(LED_Pot_12_RGBW)

    def a0():
        controller.all_off()
        controller.clear_all_effects()
        controller.all_color(Colors.Black)
        controller.all_on()

    def a500():
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([60, 60, 255], 2500)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([60, 60, 255], 2500)

    def a9000():
        controller.get_fixtures_by_name("S1 Art")[0].color([60, 60, 255], 2500)
        controller.get_fixtures_by_name("S2 Board")[0].color([60, 60, 255], 2500)

    def a16500():
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([40, 20, 255], 2500)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([40, 20, 255], 2500)

    def a23500():
        controller.get_fixtures_by_name("S1 Art")[0].color([40, 20, 255], 2500)
        controller.get_fixtures_by_name("S2 Board")[0].color([40, 20, 255], 2500)

    def a27000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.mix(Colors.Warm, Colors.Black, 0.4), 500)

    def a28000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([40, 20, 255, 128], 5000)

    def a39500():
        controller.get_fixtures_by_name("S1 Art")[0].color([255, 20, 100], 1500)
        controller.get_fixtures_by_name("S2 Board")[0].color(Colors.Warm, 2500)
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([255, 20, 100], 1500)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color(Colors.Warm, 2500)

    def a55000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.mix(Colors.Warm, Colors.Black, 0.1), 1000)

    def a58500():
        Chase.group_apply(
            not_flood,
            bpm_millis * 6 * 3, colors=[
                Colors.Warm, [255, 20, 100], [255, 20, 100],
                [255, 20, 100], [255, 20, 100], [255, 20, 100]
            ])

    def a68000():
        controller.clear_all_effects()

        controller.get_fixtures_by_name("S1 Art")[0].color(Colors.Warm, 1500)
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color(Colors.Warm, 1500)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color(Colors.Warm, 1500)

        controller.get_fixtures_by_name("S2 Board")[0].color([255, 20, 100], 1500)
        controller.get_fixtures_by_name("F1 Desk Right")[0].color([255, 20, 100], 1500)
        controller.get_fixtures_by_name("F2 Desk Left")[0].color([255, 20, 100], 1500)

    def a69500():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Warm, 7500)

    def a77000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Black, 8000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([60, 60, 255], 8000)

    def a86750():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([40, 50, 255], 500)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([40, 50, 255], 500)

    def a101000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([40, 50, 255], 500)

    def a108000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Black, 2500)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Black, 24000)

    def a132000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 2000)

    def a134000():
        controller.get_fixtures_by_name("S1 Art")[0].color([100, 100, 255], 1500)

    def a135500():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.mix([130, 130, 255], Colors.Black, .5), 1000)

    def a136500():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 500)

    def a137000():
        controller.get_fixtures_by_name("S2 Board")[0].color([30, 70, 255], 1000)

    def a138000():
        controller.get_fixtures_by_name("S2 Board")[0].color(Colors.Black, 250)

    def a139000():
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([30, 70, 255], 1000)

    def a140000():
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color(Colors.Black, 250)

    def a141000():
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([30, 70, 255], 1000)

    def a142000():
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color(Colors.Black, 250)

    def a143000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([30, 70, 255], 500)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([30, 70, 255], 10000)

    def a145000():
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([30, 70, 255], 1000)

    def a146000():
        controller.get_fixtures_by_name("S2 Board")[0].color([30, 70, 255], 1000)

    def a147000():
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([30, 70, 255], 1000)

    def a148000():
        controller.get_fixtures_by_name("S1 Art")[0].color([30, 70, 255], 1000)

    def a153000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([30, 70, 255], 2500)

    def a156000():
        for fixture in controller.get_all_fixtures():
            fixture.color(Colors.Black, 500)

    def a156500():
        Chase.group_apply(not_flood, 3500, colors=[
            [30, 70, 255], Colors.Black, Colors.Black,
            Colors.Black, Colors.Black, Colors.Black
        ])

    def a160000():
        controller.clear_all_effects()
        for fixture in controller.get_all_fixtures():
            fixture.color(Colors.Black, 1500)

    def a163000():
        controller.get_fixtures_by_name("S2 Board")[0].color([30, 70, 255], 500)

    def a164000():
        controller.get_fixtures_by_name("S2 Board")[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color([30, 70, 255], 500)

    def a165000():
        controller.get_fixtures_by_name("S4 Shelf Left")[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name("S1 Art")[0].color([30, 70, 255], 500)
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color([30, 70, 255], 500)

    def a166000():
        controller.get_fixtures_by_name("S1 Art")[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name("S3 Shelf Right")[0].color(Colors.Black, 1500)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([30, 70, 255, 128], 500)

    def a167000():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Black, 1500)

    def a168000():
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), 1000,
                          colors=[[30, 70, 255], Colors.Black, Colors.Black, Colors.Black])

    def a169000():
        controller.clear_all_effects()
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), 1000,
                          colors=[[70, 30, 255], Colors.Black, Colors.Black, Colors.Black])

    def a170000():
        controller.clear_all_effects()
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), 3000,
                          colors=[[70, 30, 255], Colors.Black, Colors.Black, Colors.Black])

    def a176000():
        controller.clear_all_effects()
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), 2000,
                          colors=[[30, 70, 255], [30, 70, 255], Colors.Black, Colors.Black])

    def a178000():
        controller.clear_all_effects()
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([70, 30, 255], 500)

    def a180000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([30, 70, 255], 500)

    def a182500():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([30, 70, 255], 500)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 1500)

    def a183000():
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Pot_12_RGBW), bpm_millis * 2,
                          colors=[[30, 70, 255], Colors.Black])



    # Store events
    events.add_event(0, a0, name="Start (blackout)")
    events.add_event(500, a500, name="Riff (pale purple)")
    events.add_event(9000, a9000, name="2nd Riff (pale purple)")
    events.add_event(16500, a16500, name="3rd Riff (med purple)")
    events.add_event(23500, a23500, name="4th Riff (med purple)")
    events.add_event(27000, a27000, name="Door (warm)")
    events.add_event(28000, a28000, name="5th Riff (med purple)")
    events.add_event(39500, a39500, name="Wide (red)")
    events.add_event(55000, a55000, name="Corridor (dim)")
    events.add_event(58500, a58500, name="Corridor close-up (chase)")
    events.add_event(68000, a68000, name="Pictures (warm)")
    events.add_event(69500, a69500, name="Elsa (warm)")
    events.add_event(77000, a77000, name="To outdoors (cool)")
    events.add_event(86750, a86750, name="Outdoors push (cool)")
    events.add_event(101000, a101000, name="Outdoors far (cool)")
    events.add_event(108000, a108000, name="Outdoors river (fade)")
    events.add_event(132000, a132000, name="Magic prep (dim)")
    events.add_event(134000, a134000, name="Single magic")
    events.add_event(135500, a135500, name="Small magic")
    events.add_event(136500, a136500, name="Jet prep")
    events.add_event(137000, a137000, name="1st magic jet")
    events.add_event(138000, a138000, name="Clear 1st jet")
    events.add_event(139000, a139000, name="2nd magic jet")
    events.add_event(140000, a140000, name="Clear 2nd jet")
    events.add_event(141000, a141000, name="3rd magic jet")
    events.add_event(142000, a142000, name="Clear 3rd jet")
    events.add_event(143000, a143000, name="1st Boost")
    events.add_event(145000, a145000, name="2nd Boost")
    events.add_event(146000, a146000, name="3rd Boost")
    events.add_event(147000, a147000, name="4th Boost")
    events.add_event(148000, a148000, name="5th Boost")
    events.add_event(153000, a153000, name="Vision magic")
    events.add_event(156000, a156000, name="Vision chase prep")
    events.add_event(156500, a156500, name="Vision chase")
    events.add_event(160000, a160000, name="Vision exit")
    events.add_event(163000, a163000, name="1st magic burst (single)")
    events.add_event(164000, a164000, name="2nd magic burst (single)")
    events.add_event(165000, a165000, name="3rd magic burst (dual)")
    events.add_event(166000, a166000, name="4th magic burst (ground)")
    events.add_event(167000, a167000, name="Clear burst")
    events.add_event(168000, a168000, name="Spiral")
    events.add_event(169000, a169000, name="Spiral purple")
    events.add_event(170000, a170000, name="Spiral slow")
    events.add_event(176000, a176000, name="Sprial end")
    events.add_event(178000, a178000, name="1st burst")
    events.add_event(180000, a180000, name="2nd burst")
    events.add_event(182500, a182500, name="3rd burst")
    events.add_event(183000, a183000, name="Close chase")  # TODO: finish
    events.add_event(209000, controller.all_off, 500, name="End (blackout)")

    return events
