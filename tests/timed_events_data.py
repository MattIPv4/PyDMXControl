from PyDMXControl import Colors
from PyDMXControl.audio import player
from PyDMXControl.controllers import Controller
from PyDMXControl.effects.Color import Chase
from PyDMXControl.profiles.Stairville import LED_Par_36, LED_Par_10mm
from PyDMXControl.profiles.funGeneration import LED_Pot_12_RGBW
from PyDMXControl.utils.timing import TimedEvents


def you_will_be_found(controller: Controller) -> TimedEvents:
    events = TimedEvents(True)

    def store(time, name):
        def wrap(func):
            events.add_event(time, func, name=name)
            return func
        return wrap

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

    @store(0, "Start (dim blue)")
    def a0():
        controller.all_off()
        controller.clear_all_effects()
        controller.all_color(Colors.Black)
        controller.all_on()
        controller.all_color([0, 0, 15], 12000)

    @store(12400, "Evan first")
    def a12400():
        controller.all_on(2000)
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving'):
            f.color([50, 100, 255], 2000)

    @store(16800, "Blue")
    def a16800():
        controller.all_color(Colors.Blue, 1000)

    @store(18900, "Evan second")
    def a18900():
        for f in controller.get_fixtures_by_name_include('Desk'):
            f.color([160, 140, 255], 2000)

    @store(38000, "Blue")
    def a38000():
        controller.all_color(Colors.Blue, 1000)

    @store(45000, "Evan third")
    def a45000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([0, 150, 255])
            fixture.color([0, 0, 255], 15000)

    @store(69000, "'And OoooOh'")
    def a69000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.White, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color([0, 128, 255], 5000)

    @store(93000, "'You will be found' boost")
    def a93000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([0, 25, 255], 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.White, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.White, 5000)

    @store(125000, "Into social dark")
    def a125000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Black, 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Black, 5000)

    @store(138000, "Social chase")
    def a138000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.dim(0)
            fixture.dim(255, 15000)

        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), bpm_millis * 4, colors=[
            [50, 128, 255], Colors.Black, Colors.Black, Colors.Black])

    @store(152000, "Out of social")
    def a152000():
        controller.clear_all_effects()
        controller.all_color(Colors.Blue)
        controller.all_color([50, 100, 255], 2000)

    @store(174000, "News voices")
    def a174000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 8000)

        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Blue, 8000)

    @store(216000, "Last 'Thank you, Evan Hansen'")
    def a216000():
        controller.all_color([100, 128, 255])

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

    @store(248900, "Chase cyan")
    def a248900():
        c = [100, 128, 255]
        controller.all_color(c)

        Chase.group_apply(controller.get_fixtures_by_profile(LED_Par_36), bpm_millis * 4, colors=[c, Colors.Blue, c, c])

    @store(270000, "End chase, 'you are not alone'")
    def a270000():
        controller.clear_all_effects()

        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color(Colors.Blue, 5000)

    @store(292300, "End of 'you are not alone'")
    def a292300():
        for fixture in controller.get_fixtures_by_profile(LED_Par_36):
            fixture.color([128, 128, 255], 5000)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Blue, 5000)

    @store(303000, "'You will be found' boost")
    def a303000():
        controller.all_color(Colors.White, 500)

    @store(333200, "Blue")
    def a333200():
        controller.all_color(Colors.Blue, 800)

    @store(334000, "Evan spot")
    def a334000():
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving'):
            f.color([50, 100, 255], 1000)

    @store(344000, "Blue")
    def a344000():
        controller.all_color(Colors.Blue, 1000)

    @store(345000, "End (blackout)")
    def a345000():
        controller.all_off(500)

    return events


def into_the_unknown(controller: Controller) -> TimedEvents:
    events = TimedEvents(True)

    def store(time, name):
        def wrap(func):
            events.add_event(time, func, name=name)
            return func
        return wrap

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
    side_wall = controller.get_fixtures_by_name_include('Board') + \
                controller.get_fixtures_by_name_include('Art') + \
                controller.get_fixtures_by_name_include('Shelf') + \
                controller.get_fixtures_by_name_include('Shelving')
    walls = side_wall + controller.get_fixtures_by_name_include('Books')
    red = [255, 20, 100]

    @store(0, "Start (blackout)")
    def a0():
        controller.all_off()
        controller.clear_all_effects()
        controller.all_color(Colors.Black)
        controller.all_on()

    @store(500, "Riff (pale purple)")
    def a500():
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving'):
            f.color([60, 60, 255, 191], 2500)

    @store(9000, "2nd Riff (pale purple)")
    def a9000():
        for f in controller.get_fixtures_by_name_include('Art') + \
                 controller.get_fixtures_by_name_include('Board'):
            f.color([60, 60, 255], 2500)

    @store(16500, "3rd Riff (med purple)")
    def a16500():
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving'):
            f.color([60, 40, 255, 0], 2500)

    @store(23500, "4th Riff (med purple)")
    def a23500():
        for f in controller.get_fixtures_by_name_include('Art') + \
                 controller.get_fixtures_by_name_include('Board'):
            f.color([40, 20, 255], 2500)

    @store(27000, "Door (warm)")
    def a27000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.mix(Colors.Warm, Colors.Black, 0.4), 500)

    @store(28000, "5th Riff (med purple)")
    def a28000():
        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color([40, 20, 255, 0], 2500)

        for fixture in controller.get_fixtures_by_name_include('Shelf') + \
                       controller.get_fixtures_by_name_include('Shelving'):
            fixture.color([40, 20, 255, 0], 5000)

        for f in controller.get_fixtures_by_name_include('Art') + \
                 controller.get_fixtures_by_name_include('Board'):
            f.color([40, 10, 255], 5000)

    @store(39500, "Wide (red)")
    def a39500():
        for i, f in enumerate(walls):
            f.color(Colors.Warm if i % 2 == 0 else red, 2500 if i % 2 == 0 else 1500)

        for f in controller.get_fixtures_by_name_include('Desk'):
            f.color([0, 0, 0, 0], 1500)

    @store(55000, "Corridor (dim)")
    def a55000():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.mix(Colors.Warm, Colors.Black, 0.1), 1000)

        for i, f in enumerate(walls):
            f.color(Colors.Warm if i == len(walls) - 1 else red, 3500)

    @store(58500, "Corridor close-up (chase)")
    def a58500():
        Chase.group_apply(
            walls,
            bpm_millis * 6 * 3, colors=[
                Colors.Warm, red, red,
                red, red, red
            ])

    @store(68000, "Pictures (warm)")
    def a68000():
        controller.clear_all_effects()

        for f in controller.get_fixtures_by_name_include('Board'):
            f.color(Colors.Warm, 1500)

        for f in controller.get_fixtures_by_name_include('Art') + \
                 controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving') + \
                 controller.get_fixtures_by_name_include('Books'):
            f.color(red, 1500)

    @store(69500, "Elsa (warm)")
    def a69500():
        for fixture in controller.get_fixtures_by_profile(LED_Pot_12_RGBW):
            fixture.color(Colors.Warm, 7500)

    @store(77000, "To outdoors (cool)")
    def a77000():
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving') + \
                 controller.get_fixtures_by_name_include('Desk') + \
                 controller.get_fixtures_by_name_include('Books'):
            f.color(Colors.Black, 8000)

        for f in controller.get_fixtures_by_name_include('Board') + \
                 controller.get_fixtures_by_name_include('Art'):
            f.color([60, 60, 255], 8000)

    @store(86750, "Outdoors push (cool)")
    def a86750():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([40, 50, 255], 500)

        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving') + \
                 controller.get_fixtures_by_name_include('Desk') + \
                 controller.get_fixtures_by_name_include('Books'):
            f.color([40, 50, 255], 500)

    @store(101000, "Outdoors far (cool)")
    def a101000():
        for f in controller.get_fixtures_by_name_include('Board') + \
                 controller.get_fixtures_by_name_include('Art'):
            f.color([40, 50, 255], 500)

    @store(108000, "Outdoors river (fade)")
    def a108000():
        for f in controller.get_fixtures_by_name_include('Shelf') + \
                 controller.get_fixtures_by_name_include('Shelving') + \
                 controller.get_fixtures_by_name_include('Desk') + \
                 controller.get_fixtures_by_name_include('Books'):
            f.color(Colors.Black, 2500)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color(Colors.Black, 24000)

    @store(132000, "Magic prep (dim)")
    def a132000():
        for f in controller.get_fixtures_by_name_include('Board') + \
                 controller.get_fixtures_by_name_include('Art'):
            f.color(Colors.Black, 2000)

    @store(134000, "Single magic")
    def a134000():
        controller.get_fixtures_by_name_include('Art')[0].color([100, 100, 255], 1500)

    @store(135500, "Small magic")
    def a135500():
        for f in controller.get_fixtures_by_name_include('Board') + \
                 controller.get_fixtures_by_name_include('Art'):
            f.color(Colors.mix([130, 130, 255], Colors.Black, .5), 1000)

    @store(136500, "Jet prep")
    def a136500():
        for f in controller.get_fixtures_by_name_include('Board') + \
                 controller.get_fixtures_by_name_include('Art'):
            f.color(Colors.Black, 500)

    @store(137000, "1st magic jet")
    def a137000():
        controller.get_fixtures_by_name_include('Board')[0].color([30, 70, 255], 1000)

    @store(138000, "Clear 1st jet")
    def a138000():
        controller.get_fixtures_by_name_include('Board')[0].color(Colors.Black, 250)

    @store(139000, "2nd magic jet")
    def a139000():
        controller.get_fixtures_by_name_include('Shelf')[1].color([30, 70, 255], 1000)

    @store(140000, "Clear 2nd jet")
    def a140000():
        controller.get_fixtures_by_name_include('Shelf')[1].color(Colors.Black, 250)

    @store(141000, "3rd magic jet")
    def a141000():
        controller.get_fixtures_by_name_include('Shelf')[0].color([30, 70, 255], 1000)

    @store(142000, "Clear 3rd jet")
    def a142000():
        controller.get_fixtures_by_name_include('Shelf')[0].color(Colors.Black, 250)

    @store(143000, "1st Boost")
    def a143000():
        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color([30, 70, 255], 500)

        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([30, 70, 255], 10000)

    @store(145000, "2nd Boost")
    def a145000():
        controller.get_fixtures_by_name_include('Shelf')[1].color([30, 70, 255], 1000)

    @store(146000, "3rd Boost")
    def a146000():
        controller.get_fixtures_by_name_include('Board')[0].color([30, 70, 255], 1000)

    @store(147000, "4th Boost")
    def a147000():
        controller.get_fixtures_by_name_include('Shelf')[0].color([30, 70, 255], 1000)

    @store(148000, "5th Boost")
    def a148000():
        controller.get_fixtures_by_name_include('Art')[0].color([30, 70, 255], 1000)

    @store(153000, "Vision magic")
    def a153000():
        for fixture in not_flood:
            fixture.color([30, 70, 255], 2500)

    @store(156000, "Vision chase prep")
    def a156000():
        for fixture in controller.get_all_fixtures():
            fixture.color(Colors.Black, 500)

    @store(156500, "Vision chase")
    def a156500():
        Chase.group_apply(walls, 3500, colors=[
            [30, 70, 255], Colors.Black, Colors.Black,
            Colors.Black, Colors.Black, Colors.Black
        ])

    @store(160000, "Vision exit")
    def a160000():
        controller.clear_all_effects()
        for fixture in controller.get_all_fixtures():
            fixture.color(Colors.Black, 1500)

    @store(163000, "1st magic burst (single)")
    def a163000():
        controller.get_fixtures_by_name_include('Board')[0].color([30, 70, 255], 500)

    @store(164000, "2nd magic burst (single)")
    def a164000():
        controller.get_fixtures_by_name_include('Board')[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name_include('Shelf')[0].color([30, 70, 255], 500)

    @store(165000, "3rd magic burst (dual)")
    def a165000():
        controller.get_fixtures_by_name_include('Shelf')[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name_include('Art')[0].color([30, 70, 255], 500)
        controller.get_fixtures_by_name_include('Shelf')[1].color([30, 70, 255], 500)

    @store(166000, "4th magic burst (ground)")
    def a166000():
        controller.get_fixtures_by_name_include('Art')[0].color(Colors.Black, 1500)
        controller.get_fixtures_by_name_include('Shelf')[1].color(Colors.Black, 1500)

        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color([30, 70, 255, 128], 500)

    @store(167000, "Clear burst")
    def a167000():
        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color(Colors.Black, 1500)

    @store(168000, "Spiral")
    def a168000():
        # Fixed speed, irrespective of fixture count
        Chase.group_apply(walls, 1000,
                          colors=[[30, 70, 255], Colors.Black, Colors.Black, Colors.Black, Colors.Black, Colors.Black])

    @store(169000, "Spiral purple")
    def a169000():
        # Fixed speed, irrespective of fixture count
        controller.clear_all_effects()
        Chase.group_apply(walls, 1000,
                          colors=[[70, 30, 255], Colors.Black, Colors.Black, Colors.Black, Colors.Black, Colors.Black])

    @store(170000, "Spiral slow")
    def a170000():
        # Fixed speed, irrespective of fixture count
        controller.clear_all_effects()
        Chase.group_apply(walls, 3000,
                          colors=[[70, 30, 255], Colors.Black, Colors.Black, Colors.Black, Colors.Black, Colors.Black])

    @store(176000, "Spiral end")
    def a176000():
        # Fixed speed, irrespective of fixture count
        controller.clear_all_effects()
        Chase.group_apply(walls, 2000,
                          colors=[[30, 70, 255], [30, 70, 255], Colors.Black, Colors.Black, Colors.Black, Colors.Black])

    @store(178000, "1st burst")
    def a178000():
        controller.clear_all_effects()
        for fixture in walls:
            fixture.color([70, 30, 255], 500)

    @store(180000, "2nd burst")
    def a180000():
        for fixture in walls:
            fixture.color([30, 70, 255], 500)

    @store(182500, "3rd burst")
    def a182500():
        for fixture in controller.get_fixtures_by_profile(LED_Par_10mm):
            fixture.color([30, 70, 255], 500)

        for fixture in walls:
            fixture.color(Colors.Black, 1500)

    @store(183000, "Close chase")
    def a183000():
        Chase.group_apply(controller.get_fixtures_by_profile(LED_Pot_12_RGBW), bpm_millis * 4,
                          colors=[[30, 70, 255], Colors.Black, Colors.Black, Colors.Black])

    @store(185000, "Jet")
    def a185000():
        controller.clear_all_effects()

        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color(Colors.Black, 500)

        # Fixed speed, irrespective of fixture count
        Chase.group_apply(side_wall, 1000,
                          colors=[[30, 70, 255], Colors.Black, Colors.Black, Colors.Black, Colors.Black])

    @store(186000, "Glow build-up")
    def a186000():
        controller.clear_all_effects()

        for fixture in side_wall:
            fixture.color(Colors.Black, 500)

        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color([30, 70, 255], 5000)

    @store(191000, "Glow chase")
    def a191000():
        Chase.group_apply(controller.get_fixtures_by_name_include('Desk'), bpm_millis * 2 * 2,
                          colors=[[30, 70, 255], Colors.mix([30, 70, 255], Colors.Black, 0.1)])

    @store(195000, "Slow fade")
    def a195000():
        controller.clear_all_effects()

        for fixture in controller.get_fixtures_by_name_include('Desk'):
            fixture.color(Colors.Black, 5000)

    @store(202250, "Burst")
    def a202250():
        for fixture in not_flood:
            fixture.color([30, 70, 255], 500)

    @store(203750, "Twinkle")
    def a203750():
        # Fixed speed, irrespective of fixture count
        Chase.group_apply(
            walls,
            1000, colors=[
                [30, 70, 255], [60, 140, 255], [30, 70, 255],
                [30, 70, 255], [30, 70, 255], [30, 70, 255]
            ])

    @store(204750, "End (blackout)")
    def a204750():
        controller.clear_all_effects()
        controller.all_off(1000)

    return events
