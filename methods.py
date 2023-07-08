from machine import Pin, I2C

def configure_PWM_0 (ad,baud):
    if not (isinstance(ad,int) and isinstance(baud,int)):
        print("one param is not an integer")
        return 2
    i2c = I2C(0)
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=baud)
    avl = i2c.scan()
    if ad in avl:
        cfg=bytearray(2)
        #Config mode reg 1
        cfg[0]=0x00
        cfg[1]=0x20
        i2c.writeto(ad, config)
        #config mode reg 2
        cfg[0]=0x01
        cfg[1]=0x04
        i2c.writeto(ad, cfg)
        #config period
        cfg[0]=0xFE
        cfg[1]=0x79
        i2c.writeto(ad, cfg)
        return 0
    else:
        return 1

def set_PWM_signals(ad,signals):
    #PWM signal 0 to PWM signal 15
    if not isinstance(signals,list):
        print("type error, signals must be a list")
        return 2
    for signal in signals:
        if not isinstance(signal,int):
            print("type error, signals in list must be int")
            return 2
        if signal > 4095:
            print("Any signal can be greater than 4095")
            return 2
    if len(signals)>16:
        print("Signals cannot have more than 16 elements")
        return 2
    for _ in range(16-len(signals)):signals.append(0)
    buffer = bytearray(65)
    idx=0
    buffer[idx]=0x06
    idx=idx+1
    for signal in signals 
        buffer[idx]=0x00
        idx=idx+1
        buffer[idx]=0x00
        idx=idx+1        
        buffer[idx]=int(signal/256)
        idx=idx+1 
        buffer[idx]=signal-MSBs*256
        idx=idx+1 
    if i2c.writeto(ad, buffer) == 64:
        return 0
    else:
        print("Not all signals where received")
        return 1