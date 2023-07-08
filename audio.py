import pyaudio
import wave
from array import array
from struct import pack

def play(file):
    CHUNK = 1024

    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()

    #To record or play audio, open a stream on the desired device
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) >0:

        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def width(file):
    wf = wave.open(file, 'rb')
    frames = wf.getnframes()
    rate = wf.getframerate()
    return round(frames / float(rate))

def record(outputFile,RECORD_SECONDS):
    #//size in bytes
    CHUNK = 1024 
    #bit depth (16 bits)
    FORMAT = pyaudio.paInt16
    #stereo, better than monochannel
    CHANNELS = 1
    #sampling frecuency-
    RATE = 44100
    #i want to record audio for 5 sec

    p = pyaudio.PyAudio()

    #open stream object as input
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    #lenght of audio buffer
                    frames_per_buffer=CHUNK)
    
    print("* recording")

    #blank list
    frames = []

    #store in stream 
    for i in range (0, int(RATE / CHUNK * RECORD_SECONDS)): #4400/1024*5
        #store audio frames in data
        data = stream.read (CHUNK)
        frames.append (data)

    print ("* done recording")

       #stop stream
    stream.stop_stream ()
    stream.close ()
    p.terminate ()
       
       #store recording in a wave
    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#play('grabacion.wav')