import json 

def nestlist(map,sequence,order):
    position=["front","middle","back"]
    sides=["left","right"]
    motor=["0","1","2"]
    length = len(sequence[position[0]][sides[0]][motor[0]])
    map0=[]
    map1=[]
    map2=[]
    #print(map0)
    #print(length)
    b=1200
    for vector in range(length):
        map0.append([0]*16)
        map1.append([0]*16)
        map2.append([0]*16)
        #print(map0)
        for pos in position:
            for sid in sides:
                for mot in motor:
                    if sid == sides[0]:
                        a=10
                    else:
                        a=-10
                    if map[pos][sid][mot][0]==order[0]: 
                        #print(f"vector : {vector}  -  map : {map[pos][sid][mot][1]}   -   sequence : {sequence[pos][sid][mot][vector]}")
                        map0[vector][map[pos][sid][mot][1]] = a*(sequence[pos][sid][mot][vector]+map[pos][sid][mot][2])+b
                    if map[pos][sid][mot][0]==order[1]: 
                        #SecondVector = slope adjusment ( "i" position of sequence + fase adjusment )  +  Constant adjusment
                        map1[vector][map[pos][sid][mot][1] ] = a*(sequence[pos][sid][mot][vector]+map[pos][sid][mot][2])+b
                    if map[pos][sid][mot][0]==order[2]: 
                        map2[vector][map[pos][sid][mot][1] ] = a*(sequence[pos][sid][mot][vector]+map[pos][sid][mot][2])+b
    return map0, map1, map2

def  angleleft(degree):
    a=10
    b=1200
    return a*degree + b

def angleright(degree):
    a=-10
    b=1200
    return a*degree + b

#mapper = json.load(open("map.json"))
#sequence_0 = json.load(open("secuencetest.json"))

#vector0, vector1 = nestlist(mapper,sequence_0,[64,65])

#print(vector0)
#print(vector1)