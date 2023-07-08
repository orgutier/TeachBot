import serial

bot = serial.Serial("COM3")
bot.baudrate = 115200
bot.bytesize = 8
bot.parity = "N"
bot.stopbits = 1
bot.timeout = 1


print(bot.write(b"test\n"))
print(bot.read(10))

bot.close()