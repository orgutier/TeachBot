from machine import Pin, I2C
import testmap, json 

def configure_PWM_0 (ad,baud):
    from machine import Pin, I2C
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
        i2c.writeto(ad, cfg, True)
        #config mode reg 2
        cfg[0]=0x01
        cfg[1]=0x04
        i2c.writeto(ad, cfg, True)
        #config period
        cfg[0]=0xFE
        cfg[1]=0x79
        i2c.writeto(ad, cfg, True)
        return 0
    else:
        return 1

def set_PWM_signals(ad,signals):
    from machine import Pin, I2C
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
    for _ in range(16-len(signals)):
        signals.append(0)
    buffer = bytearray(65)
    idx=0
    buffer[idx]=0x06
    idx=idx+1
    for signal in signals:
        buffer[idx]=0x00
        idx=idx+1
        buffer[idx]=0x00
        idx=idx+1        
        buffer[idx]=signal-256*int(signal/256)
        idx=idx+1 
        buffer[idx]=int(signal/256)
        idx=idx+1
    print(str(ad)+str(signals))
    i2c = I2C(0)
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
    if i2c.writeto(ad, buffer, True) == 65:
        return 0
    else:
        print("Not all signals where received")
        return 1

def run_PWM_vector(vec,add):
    timing = 20000
    for index in range(len(vec[0])):
        for idx in range(len(add)):
            set_PWM_signals(add[idx],vec[idx][index])
        for _ in range(timing):
            a=10

timing = 10000
# min=350
# max=2000

#####Map lines
# min=1100
# max=1250
# steps=50
# n=min
# vector1=[n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n]
# test_adds=[64,65,66]
# for test_add in test_adds:
#     configure_PWM_0(test_add,400000)
#     set_PWM_signals(test_add,vector1)
# for _ in range (timing): 
#     a=10
# for test_add in test_adds:
#     vector1=[n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n]
#     for index in range(16):
#         print("Signal you saw is "+str(test_add)+" and address  --  "+str(index))
#         vector1[index]=max
#         set_PWM_signals(test_add,vector1)
#         for _ in range (timing):
#             a=10
#####Map lines


##Sequence lines
test_adds=[64,65,66]
for test_add in test_adds:
    configure_PWM_0(test_add,400000)

###Sequence configuration
sequences={}

mapper = json.load(open("map.json"))
sequence = json.load(open("frontwalk.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["frontwalk"]=[vector0,vector1,vector2]

sequence = json.load(open("karlasteps.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["karlasteps"]=[vector0,vector1,vector2]

sequence = json.load(open("babysteps.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["babysteps"]=[vector0,vector1,vector2]

sequence = json.load(open("standup.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["standup"]=[vector0,vector1,vector2]

sequence = json.load(open("funnystandup.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["funnystandup"]=[vector0,vector1,vector2]

sequence = json.load(open("sleep.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["sleep"]=[vector0,vector1,vector2]

sequence = json.load(open("hi.json"))
vector0, vector1, vector2= testmap.nestlist(mapper,sequence,[64,65,66])
sequences["hi"]=[vector0,vector1,vector2]
##Sequence configuration


##Motion configuration
motion1 = json.load(open("motion1.json"))
##Motion configuration


##Variable definition for timmed sequences
from machine import Timer
##Variables for simulated "for"
global_sequence=0
global_address=0
global_sequence_dots=1
global_sequence_dots_idx=0
global_sequence_idx=0
global_running=True
def init_move_variables(sequence,address,dots):
    global global_sequence
    global global_address
    global global_sequence_idx
    global global_running
    global global_sequence_dots
    global_sequence_dots=dots
    global_sequence_dots_idx=0
    global_sequence=sequence
    global_address=address
    global_sequence_idx=0
    global_running=True

def run_PWM_vector_integrate(t):
    global global_sequence
    global global_address
    global global_sequence_idx
    global global_running
    global global_sequence_dots_idx
    global global_sequence_dots
    global tim0
    add=global_address
    index=global_sequence_idx
    dots=global_sequence_dots
    dot=global_sequence_dots_idx
    if global_running==False:
        return
    print(index)
    print(dot)
    for idx in range(len(add)):
        vector=[0]*16
        if global_sequence_idx>=len(global_sequence[0])-1:
            vector=global_sequence[idx][index]
        else:
            for point in range(len(global_sequence[idx][index])):
                vector[point]=int(global_sequence[idx][index][point]+dot*(global_sequence[idx][index+1][point]-global_sequence[idx][index][point])/dots)
        set_PWM_signals(add[idx],vector)
    if global_sequence_idx>=len(global_sequence[0])-1:
        global_sequence_idx=0
        tim0.deinit()
        print("Process stopped0")
        global_running=False
    dot=dot+1
    if dot>=dots:
        dot=0
        global_sequence_idx=global_sequence_idx+1
        if global_sequence_idx>=len(global_sequence[0]):
            global_sequence_idx=0
            tim0.deinit()
            print("Process stopped1")
            global_running=False
    global_sequence_dots_idx=dot
    # for index in range(len(vec[0])):
    #     for idx in range(len(add)):
    #         set_PWM_signals(global_address[global_address_idx],global_sequence[global_address_idx][global_sequence_idx])
    #         global_address_idx=global_address_idx+1
    #         if global_address_idx>=global_address_len:
    #             global_address_idx=0
    #             global_sequence_idx=global_sequence_idx+1
    #             if global_sequence_idx>=global_sequence_len:
                    # global_sequence_idx=0
                    # global tim0
                    # tim0.deinit()
                    

tim0 = Timer(0)
##This is going to start the movement

def fullmotion (working_motion):
    global tim0
    global sequences
    import time
    for task in working_motion:
        if task[0] == "delay":
            time.sleep(task[1])
        else:
            for _ in range(task[1]):
                init_move_variables(sequences[task[0]],[64,65,66],int(task[2]/4))
                tim0.init(period=40, mode=Timer.PERIODIC,callback=run_PWM_vector_integrate)
                while(global_running):
                    pass


while(1):
    instruction = input()
    if instruction in motion1:
        fullmotion(motion1[instruction])
    elif instruction == "stop":
        break
    else:
        print("invalid instruction")
##run_PWM_vector(standup,[64,65,66])

##Sequence lines


#set_PWM_signals(64,vector0[0])
#for _ in range(timing):
#    a=10
#set_PWM_signals(65,vector1[0])