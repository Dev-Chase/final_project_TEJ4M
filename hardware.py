from utils import *
from gpiozero import LED, TonalBuzzer
from gpiozero.devices import Device
from gpiozero.pins.mock import MockFactory
from gpiozero.tones import Tone
import time

# TODO: consider setting up i2c RGB LCD for feedback
class Hardware():
    def __init__(self, red_pin=14, green_pin=15, buzzer_pin=18, testing=False):
        if testing:
            Device.pin_factory = MockFactory()

        self.red_light = LED(red_pin)
        self.green_light = LED(green_pin)
        self.set_lights(False, False)
        try:
            self.buzzer = TonalBuzzer(buzzer_pin)
        except Exception:
            pass

    def set_lights(self, red, green):
        if red:
            self.red_light.on()
        else:
            self.red_light.off()

        if green:
            self.green_light.on()
        else:
            self.green_light.off()

    def fail_sound(self):
        if isinstance(Device.pin_factory, MockFactory):
            print("I played the fail sound!")
        else:
            tune = ["E5", "C5", "A4"]
            for note in tune:
                self.buzzer.play(Tone(note))
                time.sleep(0.15)

            self.buzzer.stop()

    def success_sound(self):
        if isinstance(Device.pin_factory, MockFactory):
            print("I played the success sound!")
        else:
            tune = ["C5", "E5", "G5"]
            for note in tune:
                self.buzzer.play(Tone(note))
                time.sleep(0.15)

            self.buzzer.stop()
