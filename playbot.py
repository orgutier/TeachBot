
def play (record,delay):
    import audio as k
    import json
    print("start movements when I say START")
    import time
    for tim in range(delay,0,-1):
        print(tim)
        time.sleep(1)
    print("START!!!!")
    audios = json.load(open("audio_sequence.json"))
    for aud in audios[record]:
        k.play(aud)

def width (record):
    import audio as k
    import json
    a=0
    audios = json.load(open("audio_sequence.json"))
    for aud in audios[record]:
        print(f"Audio: {aud} "+" "*(15-len(str(aud)))+f" is: {k.width(aud)}")
        a=a+k.width(aud)
    print(f"Total len is: {a}")
    return a

def width_m (movement):
    import json
    a=0
    moves = json.load(open("motion1.json"))
    for mov in moves[movement]:
        if mov[0]=="delay":
            tim=mov[1]
        else:
            mo = json.load(open(mov[0]+".json"))
            le = len(mo["front"]["left"]["0"])
            tim = round(0.04*le*mov[1]*mov[2])
            a=a+tim
        print(f"Motion {mov[0]} will last: "+" "*(20-len(str(mov[0])))+str(tim))
    print("Total len is : {a}")
    return a

play("records1",10)
play("records2",0)
play("records3",0)