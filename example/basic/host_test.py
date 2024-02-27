import pyvisa, time

rm = pyvisa.ResourceManager('@py')

# List all available resources
print(rm.list_resources())

# Connect to RP Pico instrument
instr = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
# Set read terminator char so that lines can be separated
instr.read_termination = '\n'
print('Connected to device')

try:
    while True:
        now = time.time()
        print(instr.query('MEAS:GET'))
        # print(instr.query('*IDN?'), f'{1/(time.time()-now):.0f} Hz') # approx 14 Hz
except KeyboardInterrupt:
    pass