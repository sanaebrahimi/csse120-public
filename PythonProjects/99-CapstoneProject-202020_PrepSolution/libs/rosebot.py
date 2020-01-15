"""
Capstone Team Project.  Code to run on the EV3 robot (NOT on a laptop).

This code defines the RoseBot class (the top-level class for a robot).

Authors:  Your professors (for the framework)
    and PUT_YOUR_NAMES_HERE.
Winter term, 2019-2020.
"""
# TODO: Put the name of EACH team member who contributes
#   to this module in the above.

import rosebot_arm_and_claw
import rosebot_brick_buttons
import rosebot_color_sensor
import rosebot_drive_system
import rosebot_leds
import rosebot_remote_control
import rosebot_touch_sensor

import rosebot_ev3dev_api

###############################################################################
#    RoseBot class.
#
# NOTE TO STUDENTS:
#   You should construct a  RoseBot  object for the Snatch3r robot.
#   Do ** NOT ** construct any instances of any other classes in this module,
#   since a RoseBot constructs instances of all the sub-systems that provide
#   ALL of the functionality available to a Snatch3r robot.
#
#   Use those sub-systems (and their instance variables)
#   to make the RoseBot (and its associated Snatch3r robot) do things.
###############################################################################
class RoseBot(object):
    def __init__(self):
        # TODO: Implement this class with your instructor.
        self.drive_system = rosebot_drive_system.DriveSystem('B', 'C')
        self.touch_sensor = rosebot_touch_sensor.TouchSensor(1)
        self.arm_and_claw = rosebot_arm_and_claw.ArmAndClaw('A', self.touch_sensor)
        self.leds = rosebot_leds.Leds()
        self.brick_buttons = rosebot_brick_buttons.BrickButtons()
        self.remote_control = rosebot_remote_control.RemoteControl()
        self.color_sensor = rosebot_color_sensor.ColorSensor(3)
        # self.camera = rosebot_ev3dev_api.Camera()
        self.infrared_proximity_sensor = rosebot_ev3dev_api.InfraredProximitySensor(4)
