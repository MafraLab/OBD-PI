__author__ = 'Bruno'
#import RPi.GPIO as GPIO
import obd
import sys
import os
import time

from colorama import  init, Fore, Style, Back
init()
option = 0
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(23, GPIO.IN)
#GPIO.setup(22, GPIO.IN)
print "Press button 1 to connect"
print "Press button 2 to exit"
#while(option != 1):
#	if (GPIO.input(23)== True):
#		print "button pressed"
#		option = 2
#	elif (GPIO.input(22) == True):
#		option = 1

#	if option == 2:
ports = obd.scanSerial() # return list of valid USB or RF ports
print ports
connection = obd.OBD(ports[0]) # connect to the first port in the list
#connection = obd.OBD("COM3") # coneco obd (no rpi ddeve ser algo do genero /dev/ttyUSB0

commandRPM = obd.commands.RPM
commandSpeed = obd.commands.SPEED
commandTHROTTLE_POS = obd.commands.THROTTLE_POS
commandMAF = obd.commands.MAF
commandCOOLANT_TEMP = obd.commands.COOLANT_TEMP

while(True):
    responseRPM = connection.query(commandRPM)
    responseSpeed = connection.query(commandSpeed)
    responseTHROTTLE_POS = connection.query(commandTHROTTLE_POS)
    responseMAF = connection.query(commandMAF)
    responseCOOLANT_TEMP = connection.query(commandCOOLANT_TEMP)
    print str(responseRPM)
    print str(responseSpeed)

    os.system('cls' if os.name == 'nt' else 'clear')  # limpar ecra
    output = "-----------------------------\r \n" \
             "|     Menu Benite            \r \n" \
             "-----------------------------\r \n"

    if responseSpeed.value > 120:
        output = output + Back.BLUE+ Fore.RED + Style.BRIGHT + "ATENCAO A VELOCIDADE\r\n" + Fore.RESET + Back.RESET + Style.RESET_ALL


    output = output + str(" - RPM: %s \n\r" \
                          " - Velocidade: %s \n\r"
                          " - THROTTLE_POS: %s \n\r"
                          " - MAF: %s \n\r"
                          " - COOLANT_TEMP: %s \n\r")
    sys.stdout.write(output % (responseRPM, responseSpeed, responseTHROTTLE_POS, responseMAF, responseCOOLANT_TEMP) )  #escrve cena pipi


    #DESENHAR GRAFICO DA TEMPERATURA ##################################################################
    maxbar = 20
    nbar = int((int(responseCOOLANT_TEMP.value) * maxbar ) / 215) # calcular numero de barras a apresentar
    barstr = ""                                          # string com spacos (barras do grafico)

    for i in range(0, nbar):                             # de 0 ate o numero de barras a desenhar
        if i < 6:
            barstr = barstr + Back.GREEN + " " + Back.RESET
        elif i >= 6 and i < 8:
            barstr = barstr + Back.YELLOW + " " + Back.RESET
        else:
            barstr = barstr + Back.RED + " " + Back.RESET

    sys.stdout.write(barstr)
    sys.stdout.flush() #limpa memoria do stdout
    ###################################################################################################
#time.sleep(5)
#print "going to check on commands"
#for command in connection.supportedCommands:
#	print str(command)                      # prints the command name
#    	response = connection.query(command)    # sends the command, and returns the decoded response
#    	print response.value, response.unit     # prints the data and units returned from the car
