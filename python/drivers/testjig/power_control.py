import platform
import time

isRaspberryPi = platform.uname().machine in ['armv7l', 'aarch64']
if isRaspberryPi:
    import RPi.GPIO as GPIO


class PowerControl():
    """
    Class for controlling power using GPIO on Raspberry Pi connected to a relay.

    Args:
        active_high (bool): True if HIGH signal turns the power ON, False if HIGH turns it OFF.
    """
    GPIO_POWER_CONTROL = 18

    def rpi_check_decorator(function):
        def wrapper(self, *args, **kwargs):
            if isRaspberryPi:
                return function(self, *args, **kwargs)
            else:
                print('Power control only working on RPi')
        return wrapper

    @rpi_check_decorator
    def __init__(self, active_high=False):
        """
        Initializes the PowerControl instance.

        Args:
            active_high (bool): True if HIGH signal turns the power ON, False if HIGH turns it OFF.
        """
        self.active_high = active_high
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_POWER_CONTROL, GPIO.OUT)

    @rpi_check_decorator
    def power_off(self):
        GPIO.output(self.GPIO_POWER_CONTROL, GPIO.LOW if self.active_high else GPIO.HIGH)

    @rpi_check_decorator
    def power_on(self):
        GPIO.output(self.GPIO_POWER_CONTROL, GPIO.HIGH if self.active_high else GPIO.LOW)

    @rpi_check_decorator
    def power_cycle(self, delay_ms=0):
        self.power_off()
        time.sleep(delay_ms / 1000)
        self.power_on()

    @rpi_check_decorator
    def power_status(self):
        """ Check the power status

        Returns:
            bool: True if the power is ON, False if it's OFF.
        """
        return GPIO.input(self.GPIO_POWER_CONTROL) == (GPIO.HIGH if self.active_high else GPIO.LOW)
