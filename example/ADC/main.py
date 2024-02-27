from instr.ad1220 import ADC1220

while True:
    try:
        with ADC1220() as runner:
            runner.run()
    except KeyboardInterrupt:
        break
    except Exception as e:
        pass
