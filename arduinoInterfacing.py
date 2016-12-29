import serial
import time

class arduinoCom:
	#class for communication with arduino
	def sendWord(s):
		#takes
		ser = serial.Serial('COM3')
		line = ser.readline()
		line = 'Start'	
		while line!='Done':
			ser.write(bytes(s+'|||', 'utf-8'))