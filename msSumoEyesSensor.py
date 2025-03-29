from ev3dev2.sensor import Sensor
from ev3dev2.port import LegoPort
from ev3dev2 import get_current_platform
from time import sleep
import sys

class MsSumoEyesSensor(Sensor):
    # Settings for the setRange method
    LONG_RANGE = "ANALOG-0"
    SHORT_RANGE = "ANALOG-1"

    platform = get_current_platform()

    # Responses for SumoEyes
    SE_None = [0, "None"]
    if platform == "ev3":
        SE_Values = {
            170: [1, "Front"],
            210: [3, "Right"],
            320: [2, "Left"]
        }
    else : # tested only with pistorms
        SE_Values = {
            220: [1, "Front"],
            270: [3, "Right"],
            390: [2, "Left"]
        }

    def __init__(self,  address=None, name_pattern=Sensor.SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        self.port = LegoPort(address)
        sleep(0.2)
        self.port.mode="nxt-analog"
        super().__init__(address, name_pattern, name_exact, **kwargs)
        #give some times to the system to cretae the sensor
        sleep(0.8)

    ## Check the zones for an obstacle
    #  @param self The object pointer.
    #  @param verbose Outputs the string value of the direction if set to True
    #  @remark
    #  Example implementation in your program:
    #  @code
    #  ...
    #  sumoEyes = MsSumoEyesSensor(INPUT_1)
    #  print(sumoEyes.detectObstactleZone())
    #  ...
    #  @endcode
    def detectObstactleZone(self, verbose = False):
        reading = self.value(0) // 10

        for reference in self.SE_Values.keys():
            if self.isNear(reference, reading):
                output = self.SE_Values[reference]
                return output[1] if verbose else output[0]
        return self.SE_None[1] if verbose else self.SE_None[0]
     
    ## Sets the sensor range to LONG_RANGE or SHORT_RANGE setting
    #  @param self The object LONG_RANGE.
    #  @param range The range (long is default)
    #  @remark
    #  Example implementation in your program:
    #  @code
    #  ...
    #  sumoEyes = MsSumoEyesSensor(INPUT_1)
    #  sumoEyes.setRange(MsSumoEyesSensor.SHORT_RANGE)
    #  ...
    #  @endcode
    def setRange(self, range = LONG_RANGE):
        if self.mode != range:
            self.mode = range
            sleep(0.4)

    ## Checks if the sensor reading is within a tolerance to find the zone
    #  @param self The object pointer.
    #  @param reference The reference value.
    #  @param value The sensor measurement.
    #  @param tolerance The tolerance.
    #  @remark
    #  Should not be used in other programs
    def isNear(self, reference, value, tolerance = 20):
        return (value > (reference - tolerance)) and (value < (reference + tolerance))