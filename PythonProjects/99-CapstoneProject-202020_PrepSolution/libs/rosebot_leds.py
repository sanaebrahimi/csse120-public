"""
Capstone Team Project.  Code to run on the EV3 robot (NOT on a laptop).

This code defines the DriveSystem class, for making the robot move.

Authors:  Your professors (for the framework)
    and PUT_YOUR_NAMES_HERE.
Winter term, 2019-2020.
"""
# TODO: Put the name of EACH team member who contributes
#   to this module in the above.


import rosebot_ev3dev_api as rose_ev3


###############################################################################
#    LEDs
###############################################################################
class Leds(object):
    """
    Controls the two red-green LEDs on the front of the EV3 brick.
    """

    # -------------------------------------------------------------------------
    # NOTE:
    #   These 2 LEDs are RG leds, meaning they are really a red and a green LED
    #   on the left side and a red and a green LED on the right side.
    # -------------------------------------------------------------------------

    def __init__(self):
        """
        Constructs two LED objects (for the left and right leds).
          """
        # ---------------------------------------------------------------------
        # TODO: With your instructor, implement this method.
        # ---------------------------------------------------------------------
        self.left_led = rose_ev3.Led("left")
        self.right_led = rose_ev3.Led("right")

    def turn_on(self):
        """
        Sets this both Led to 100% of its RED and GREEN, which results in AMBER.
        """
        # ---------------------------------------------------------------------
        # TODO: With your instructor, implement this method.
        # ---------------------------------------------------------------------
        self.left_led.turn_on()
        self.right_led.turn_on()

    def turn_off(self):
        """ Turns both LEDs off off. """
        # ---------------------------------------------------------------------
        # TODO: With your instructor, implement this method.
        # ---------------------------------------------------------------------
        self.left_led.turn_off()
        self.right_led.turn_off()

    def set_color_by_name(self, color_name):
        """
          Turns both LEDs on to the same color.
          Valid color_names include "off", "red", "green", or "amber"
          "off" --> the red LED is off, the green LED is off
          "red" --> the red LED is on, the green LED is off
          "green" --> the red LED is off, the green LED is on
          "amber" --> the red LED is on, the green LED is on
        """
        # ---------------------------------------------------------------------
        # TODO: With your instructor, implement this method.
        # ---------------------------------------------------------------------
        self.left_led.set_color_by_name(color_name)
        self.right_led.set_color_by_name(color_name)
