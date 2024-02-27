import lib.instr as SCPI

import random, _thread, time, machine

led = machine.Pin(25, machine.Pin.OUT)

class MeasurementUnit():
    def __init__(self):
        self.number = 0
        self.n = 0
        self.lock = _thread.allocate_lock()

    def loop(self):
        global interupt, led
        while not interupt:
            led.toggle()
            self.lock.acquire()
            self.number += random.random()
            self.lock.release()
            time.sleep_ms(100)

    def get_number(self):
        return self.number
    
    def add_number(self, toadd):
        self.lock.acquire()
        self.number += toadd
        self.lock.release()


@SCPI.BuildCommands
class MyInstrument(SCPI.SCPIInstrument):
    def __init__(self, uart, measurement_unit):
        super().__init__(input_stream=uart, output_stream=uart, debug=True)
        self.meas = measurement_unit

    @SCPI.Command(command="SYSTem:PRINt", parameters=(str,))
    async def print(self, string):
        """Test command to echo back the input."""
        await self.write(string)

    @SCPI.Command(command="MEASure:ADD", parameters=(int,))
    def add(self, number):
        """Test command to echo back the input."""
        self.meas.add_number(number)

    @SCPI.Command(command="MEASure:GET")
    async def retrieve(self):
        """Test command to echo back the input."""
        await self.write(self.meas.get_number())


interupt = False
if __name__ == '__main__':
    import machine
    uart = machine.UART(0, baudrate=9600, tx=16, rx=17, timeout=0)
    uart.init(bits=8, parity=None, stop=1)

    meas = MeasurementUnit()
    other_thread_pid = _thread.start_new_thread(lambda meas: meas.loop(), (meas,))

    while True:
        try:
            # REPL based instrument use SCPI.SCPIInstrument() as instr
            with MyInstrument(uart, meas) as instr:
                instr.run()
        except KeyboardInterrupt as e:
            break
        except Exception:
            pass
        interupt = True



