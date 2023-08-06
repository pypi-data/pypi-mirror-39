from tkinter import messagebox

from mjlib.util import say,micros,append,appendln
from time import sleep
from mjlib.config import Config


led = None

# unused now, but can control frequency of arduino LED stim
def LED_stim(cfg):
    global led
    led = arduino.LEDSSVEP()
    led.initialize()
    one = True
    sleep(2)  # unfortunately have to wait, flush doesnt help

    led.start_frequency_a(cfg.FREQ1)
    led.start_frequency_b(cfg.FREQ2)

    while True:
        if one:
            stim = str(int(cfg.FREQ1))
        else:
            stim = str(int(cfg.FREQ2))

        led.start_frequency_a(stim)

# true when participant sits at far end of room, this is for labeling
distant = False

# top level experimental procedure
def run_experiment(cfg: Config):

    global distant, led

    led = arduino.LEDSSVEP()
    led.initialize()

    sleep(2)  # unfortunately have to wait, flush doesnt help

    test_f_1 = 15
    test_f_2 = 22
    test_f_3 = 28
    test_f_4 = 36

    if not messagebox.askokcancel("Test Preparation","Check LED Flicker Frequency with multimeter"):
        return

    if not messagebox.askokcancel("Test Preparation","Check for electromagenetic interference"):
        return

    if not messagebox.askokcancel("Tell subject which LEDs to look at and to do anything while resting"):
        return

    # if not messagebox.askokcancel("Prepare Part 1","Participant sits upright in chair at edge of desk with LEDS on desk"):
    #     return
    # distant = False
    #
    # cfg.FREQ1 = test_f_1
    # cfg.FREQ2 = test_f_2
    # led.start_frequency_a(cfg.FREQ1)
    # led.start_frequency_b(0)
    # run_stare_trials(cfg)
    # cfg.FREQ1 = test_f_3
    # cfg.FREQ2 = test_f_4
    # led.start_frequency_a(cfg.FREQ1)
    # led.start_frequency_b(0)
    # run_stare_trials(cfg)
    #
    # cfg.FREQ1 = test_f_1
    # cfg.FREQ2 = test_f_2
    # led.start_frequency_a(cfg.FREQ1)
    # led.start_frequency_b(cfg.FREQ2)
    # run_compete_trials(cfg)
    # cfg.FREQ1 = test_f_3
    # cfg.FREQ2 = test_f_4
    # led.start_frequency_a(cfg.FREQ1)
    # led.start_frequency_b(cfg.FREQ2)
    # run_compete_trials(cfg)
    # 
    # say('close part complete, prepare for distant part')

    if not messagebox.askokcancel("Prepare Part 2","Participant sits upright in chair at back of room with LEDS on wall"):
        return
    distant = True

    cfg.FREQ1 = test_f_1
    cfg.FREQ2 = test_f_2
    led.start_frequency_a(cfg.FREQ1)
    led.start_frequency_b(0)
    run_stare_trials(cfg)
    cfg.FREQ1 = test_f_3
    cfg.FREQ2 = test_f_4
    led.start_frequency_a(cfg.FREQ1)
    led.start_frequency_b(0)
    run_stare_trials(cfg)

    cfg.FREQ1 = test_f_1
    cfg.FREQ2 = test_f_2
    led.start_frequency_a(cfg.FREQ1)
    led.start_frequency_b(cfg.FREQ2)
    run_compete_trials(cfg)
    cfg.FREQ1 = test_f_3
    cfg.FREQ2 = test_f_4
    led.start_frequency_a(cfg.FREQ1)
    led.start_frequency_b(cfg.FREQ2)
    run_compete_trials(cfg)

def dist():
    global distant
    if distant:
        return "distant"
    else:
        return "close"

# text-to-speech automated data collection procedure designed for no interface to arduino, instead subject just looks at different stimuli
def run_compete_trials(cfg: Config):



    trial = cfg.TRIAL_LENGTH
    rest = cfg.REST_LENGTH
    stims = cfg.N_STIMS
    loops = cfg.N_LOOPS

    say("Starting test in")
    for n in reversed(range(3)):
        say(n + 1)
        sleep(0.6)

    cfg.IS_RECORDING = True

    for l in range(loops):
        for n in range(1, stims + 1):



            t = int(round(micros()))
            say('look at LED ' + str(n))
            led.start_frequency_a(cfg.FREQ1)
            led.start_frequency_b(cfg.FREQ2)
            vars.current_stim = n
            if n is 1:
                appendln(cfg.LABELS_LOG_FILE,str(t) + "," + str(cfg.FREQ1) + "Hz," + dist() + ",compete")
            elif n is 2:
                appendln(cfg.LABELS_LOG_FILE,str(t) + "," + str(cfg.FREQ2) + "Hz," + dist() + ",compete")
            else:
                print('handle other numbers of stim')
                sys.exit(0)
            sleep(trial)

            t = int(round(micros()))
            say('Rest')
            led.start_frequency_a(0)
            vars.current_stim = 0
            appendln(cfg.LABELS_LOG_FILE,str(t) + ",rest,"+dist() + ",compete")
            sleep(rest)
    t = int(round(micros()))
    appendln(cfg.LABELS_LOG_FILE,str(t) + ",done," + dist() + ",compete")
    # say('Test complete, thank you.')
    cfg.IS_RECORDING = False

# text-to-speech automated data collection procedure in which subject stares at only one set of LEDs that is changes flicker frequency at runtime
def run_stare_trials(cfg: Config):




    led.start_frequency_b(0)

    trial = cfg.TRIAL_LENGTH
    rest = cfg.REST_LENGTH
    stims = cfg.N_STIMS
    loops = cfg.N_LOOPS * 2

    say("Starting test in")
    for n in reversed(range(3)):
        say(n + 1)
        sleep(0.6)

    cfg.IS_RECORDING = True

    for l in range(loops):
        t = int(round(micros()))
        say('look at LED 1')
        if l % 2 is 0:
            led.start_frequency_a(cfg.FREQ2)
        else:
            led.start_frequency_a(cfg.FREQ1)
        vars.current_stim = l % 2 is not 0
        if l % 2 is not 0:
            appendln(cfg.LABELS_LOG_FILE,str(t) + "," + str(cfg.FREQ1) + "Hz," + dist() + ",stare")
        elif l % 2 is 0:
            appendln(cfg.LABELS_LOG_FILE,str(t) + "," + str(cfg.FREQ2) + "Hz," + dist() + ",stare")
        else:
            print('handle other numbers of stim')
            sys.exit(0)
        sleep(trial)

        t = int(round(micros()))
        say('Rest')
        led.start_frequency_a(0)
        vars.current_stim = 0
        appendln(cfg.LABELS_LOG_FILE,str(t) + ",rest," + dist() + ",stare")
        sleep(rest)
    t = int(round(micros()))
    appendln(cfg.LABELS_LOG_FILE,str(t) + ",done," + dist() + ",stare")
    # say('Test complete, thank you.')
    cfg.IS_RECORDING = False
