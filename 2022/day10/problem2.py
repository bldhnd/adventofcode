import puzzleinput as pi
from commDevice import CommunicationDevice


def problem_2():
    program = pi.program

    device = CommunicationDevice(program)

    output = device.run()

    print(f"Problem 2 : \n{output}")
