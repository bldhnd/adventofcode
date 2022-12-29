class CommunicationDevice(object):
    def __init__(self, program: str) -> None:
        self._program: str = program
        self._clock_circuit: ClockCircuit = ClockCircuit()
        self._cpu: SimpleCPU = SimpleCPU(program)
        self._crt_video: CRTScreen = CRTScreen()

    def run(self) -> str:
        while not self._cpu.is_halted():
            self._clock_circuit.tick()

            cycle = self._clock_circuit.cycle()

            self._crt_video.draw(cycle, self._cpu._reg_x)
            self._cpu.clock_cycle(cycle)

        return self._crt_video.screen()

    def get_signal_strength(self) -> int:
        while not self._cpu.is_halted():
            self._clock_circuit.tick()

            cycle = self._clock_circuit.cycle()

            self._cpu.clock_cycle(cycle)

        return self._cpu.signal_strength()


class ClockCircuit(object):
    def __init__(self) -> None:
        self._cycle: int = 0

    def cycle(self) -> int:
        return self._cycle

    def tick(self) -> None:
        self._cycle += 1


class SimpleCPU(object):
    def __init__(self, program: str) -> None:
        self._program: list[str] = program.split("\n")
        self._reg_ip: int = 0
        self._reg_x: int = 1
        self._cycle: int = 0
        self._cycle_counter: int = 20
        self._busy_cycles: int = 0
        self._update_reg_value: int = 0
        self._signal_strength: int = 0

    def clock_cycle(self, cycle: int) -> None:
        if self.is_halted():
            return

        self._cycle = cycle

        if self._is_busy():
            return

        instruction = self._fetch_instruction()

        if instruction == "noop":
            self._noop()
        elif instruction.startswith("addx"):
            operand = instruction.split(" ")[-1:][0]

            self._add(int(operand))

    def _is_busy(self) -> bool:
        still_busy = self._busy_cycles > 0

        if still_busy:
            self._calc_signal_strength()
            self._busy_cycles -= 1

            if self._busy_cycles == 0:
                self._reg_x += self._update_reg_value

        return still_busy

    def is_halted(self) -> bool:
        return self._reg_ip == len(self._program) - 1

    def signal_strength(self) -> int:
        return self._signal_strength

    def _fetch_instruction(self) -> str:
        return self._program[self._reg_ip]

    def _next_ip(self) -> None:
        self._reg_ip += 1

    def _noop(self) -> None:
        self._calc_signal_strength()
        self._next_ip()

    def _add(self, value: int) -> None:
        self._calc_signal_strength()

        self._busy_cycles = 1
        self._update_reg_value = value
        self._next_ip()

    def _calc_signal_strength(self) -> None:
        if self._should_calc_sig_strength():
            self._signal_strength += self._cycle * self._reg_x
            self._cycle_counter += 40

    def _should_calc_sig_strength(self) -> bool:
        return self._cycle == self._cycle_counter


class CRTScreen(object):
    def __init__(self) -> None:
        self._row = ["." for _ in range(240)]

    def draw(self, cycle: int, position_x: int) -> None:
        index = cycle - 1

        row = index // 40
        offset = row * 40

        pixel_char = "#" if cycle >= position_x + \
            offset and cycle <= position_x + offset + 2 else "."

        self._row[index] = pixel_char

    def screen(self) -> str:
        start = 0
        finish = 40

        output = ""

        for _ in range(6):
            output += "".join(self._row[start:finish]) + "\n"
            start += 40
            finish += 40

        return output
