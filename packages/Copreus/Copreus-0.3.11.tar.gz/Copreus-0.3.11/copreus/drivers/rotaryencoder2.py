from time import time
import RPi.GPIO as GPIO
from copreus.baseclasses.adriver import ADriver
from copreus.baseclasses.aevents import AEvents
from copreus.schema.rotaryencoder import get_schema


class RotaryEncoder2(ADriver, AEvents):
    """Driver for rotary encoder like the KY-040 together with schmitttriggers for debouncing and a flipflop for
    direction detection in hardware. (e.g. http://www.bristolwatch.com/ele2/rotary.htm)

    The driver entry in the yaml file consists of:
      * ADriver entries
        * topics_pub:
          * rotate - mqtt-translations.rotate-left and mqtt-translations.rotate-right
          * button_pressed - mqtt-translations.button_pressed
          * button_state - mqtt-translations.button_state-open and mqtt-translations.button_state-closed
      * RotaryEncoder entries
        * sw: gpio pin for pressing the rotary encoder
        * dt: dt gpio pin
        * clk: clk gpio pin

    Example:
    device:
        type: rotaryencoder
        pin_sw:  12
        pin_dt:  16
        pin_clk: 20
        topics-pub:
            rotate: /input1/rotate
            button_pressed: /input1/button/pressed
            button_state:   /input1/button/state
        mqtt-translations:
            rotate-left: LEFT
            rotate-right: RIGHT
            button_pressed: PRESSED
            button_state-open: OPEN
            button_state-closed: CLOSED

    """

    _clk = -1  # clk gpio pin id
    _dt = -1  # dt gpio pin id
    _sw = -1  # sw gpio pin id
    _last_clk = -1  # last clk value - used for rotation direction detection
    _last_time = -1 # time stamp of the last rotation step
    _last_direction = 0  # rotation direction of the last rotation step
    _min_time_gap = 0.100  # minimum time gap between direction changes
    _LEFT = -1  # internal constant - rotation direction left
    _RIGHT = 1  # internal constant - rotation direction right

    def __init__(self, config, mqtt_client=None, logger=None):
        ADriver.__init__(self, config, mqtt_client, logger, logger_name=__name__)
        AEvents.__init__(self, self._config, self._logger)

        self._clk = self._config["pin_clk"]
        self._dt = self._config["pin_dt"]
        self._sw = self._config["pin_sw"]

        self._add_event(self._clk, self._callback_rotary, 1)
        self._add_event(self._sw, self._callback_sw)

        self._last_time = time()

    def _callback_sw(self, channel):
        """Event handler for gpio pin 'sw'. Publishes to the topics 'button_state' and 'button_pressed'."""
        self._logger.info("SW-event detected.")
        state = GPIO.input(self._sw)
        if not state:
            self._publish_value(self._topics_pub["button_pressed"], self._mqtt_translations["button_pressed"])
            self._publish_value(self._topics_pub["button_state"], self._mqtt_translations["button_state-closed"])
        else:
            self._publish_value(self._topics_pub["button_state"], self._mqtt_translations["button_state-open"])

    def _callback_rotary(self, channel):
        """Event handler for gpio pin 'clk'. Reads the direction from 'dt'."""
        akt_clk = GPIO.input(self._clk)
        self._logger.info("Rotary-event detected.")

        if GPIO.input(self._dt):
            self._publish_value(self._topics_pub["rotate"], self._mqtt_translations["rotate-right"])
        else:
            self._publish_value(self._topics_pub["rotate"], self._mqtt_translations["rotate-left"])

    def _driver_start(self):
        """ADriver._driver_start"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._last_clk = GPIO.input(self._clk)
        self._register_events()

    def _driver_stop(self):
        """ADriver._driver_stop"""
        self._unregister_events()
        GPIO.cleanup(self._dt)
        GPIO.cleanup(self._sw)
        GPIO.cleanup(self._clk)

    @classmethod
    def _get_schema(cls):
        return get_schema()


def standalone():
    """Calls the static method RotaryEncoder.standalone()."""
    RotaryEncoder2.standalone()


if __name__ == "__main__":
    RotaryEncoder2.standalone()
