import puzzleinput as pi
from commDevice import CommunicationDevice


def problem_1():
    device = CommunicationDevice(pi.program)

    result = device.get_signal_strength()

    print(f"Problem 1 : {result}")
