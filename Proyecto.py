import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial 
import serial,time,collections
import matplotlib.animation as animacion
from threading import Thread
from tkinter import Tk,Frame,StringVar,Label,Button

isReceiving = False
isRun = True
datos = 0.00
muestraD = 100
data = collections.deque([0]*muestraD, maxlen = muestraD)
xmin = 0
xmax = muestraD
ymin = 0
ymax = 40

try:
    arduino = serial.Serial("COM3", 9600, timeout=1)

except:
    print("Error de coneccion con el puerto")

def Iniciar():
    global datos
    global isReceiving
    global isRun
    global ventiestado
    isReceiving = True
    isRun = True
    #arduino.write(b'w')
    thread.start()
    anim = animacion.FuncAnimation(fig, plotData, fargs=(muestraD, lines), interval = 100, blit = False)
    lienzo.draw()

def DatosA():
    time.sleep(1)
    arduino.reset_input_buffer()
    while (isRun):
        global isReceive
        global datos
        datos = float(arduino.readline().decode('utf-8'))
        isReceive = True

def plotData(self,muestraD,lines):
    data.append(datos)
    lines.set_data(range(muestraD), data)
    labelx.set("TEMP:" + str(datos))
    barraProgreso["value"]=datos
    barraProgreso.update()
    if datos >= tempMax.get():
        #arduino.write(b'x')
        #arduino.write(b'y')
        ventiestado.config(text="ON")
        resestado.config(text="OFF")
    if datos <= tempMin.get():
        #arduino.write(b'w')
        #arduino.write(b'z')
        ventiestado.config(text="OFF")
        resestado.config(text="ON")

thread = Thread(target=DatosA)

def Salir():
    global isRun
    isRun = False
    thread.join()
    arduino.close()
    time.sleep(1)
    raiz.destroy()
    raiz.quit()
    print("proceso finalizado")

fig = plt.figure(facecolor="0.50", figsize=(7,5), dpi=100)
ax = plt.axes(xlim=(xmin,xmax), ylim=(ymin,ymax))
plt.title("GRAFICA || TEMPERATURA REAL")
ax.set_xlabel("Muestras")
ax.set_ylabel("Temperatura")
ax.grid(axis = 'both', color = 'black', linestyle = 'dashed')

lines = ax.plot([], [], 'r', color = 'red', label="Temperatura Actual")[0]
ax.legend(loc = 'upper right')

raiz = Tk()
raiz.title("PROYECTO FINAL || CONTROL DE TEMPERATURA")
raiz.iconbitmap("termometro.ico")
raiz.protocol("WM_DELATE_WINDOW",Salir)
raiz.resizable(0,0)

frame = Frame(raiz, bg = "#a0a0a0")
frame.pack()

lienzo = FigureCanvasTkAgg(fig, master = frame)
lienzo.get_tk_widget().grid(row = 1, column = 0, rowspan=6, padx=10, pady=10)

tempMin = IntVar()
tempMax = IntVar()

###############################INTERVALOS_DE_TEMPERATURA###########################################################

tempMin.set(35)
tempMax.set(36)

###################################################################################################################

#TITULO DEL INTERFAZ

titulo = Label(frame, text="CONTROL DE TEMPERATURA", font=("Roboto",40,"bold"), bg="#a0a0a0")
titulo.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

titulo = Label(frame, text="PANEL DE CONTROL", font=("Roboto",20,"bold"), bg="#a0a0a0")
titulo.grid(row=1, column=2, columnspan=2, padx=10)

#BOTONES

botoninicio = Button(frame, text="INICIAR", command = Iniciar, bg="#a0a0a0", font=("Roboto", 15), width=10)
botoninicio.grid(row=6, column=2, padx=10)

botonsalir = Button(frame, text="SALIR", command=Salir, bg="#a0a0a0", font=("Roboto", 15), width=10)
botonsalir.grid(row=6, column=3, padx=10)

#ETIQUETAS

labelx = StringVar(raiz, "TEMP: 0.00")

label = Label(frame, textvariable = labelx, bg="#5CFE05", font=("Roboto",15,"bold"))
label.grid(row=1, column=1, padx=10)

ventilador = Label(frame, text="Estado del Ventilador:", font=("Roboto",15,"bold"), bg="#a0a0a0")
ventilador.grid(row=4, column=2, padx=10)

ventiestado = Label(frame, text="OFF", font=("Roboto",15,"bold"), bg="#a0a0a0")
ventiestado.grid(row=4, column=3, padx=10)

resistencia = Label(frame, text="Estado de la Resistencia:", font=("Roboto",15,"bold"), bg="#a0a0a0")
resistencia.grid(row=5, column=2, padx=10)

resestado = Label(frame, text="OFF", font=("Roboto",15,"bold"), bg="#a0a0a0")
resestado.grid(row=5, column=3, padx=10)

#BARRA DE PROGRESO

barraProgreso = ttk.Progressbar(frame, orient="vertical", length=550)
barraProgreso.grid(row=2, column=1, rowspan=5, padx=5, pady=10)

#INTERVALO DE TEMPERATURA

temp_min = Label(frame, text="Temperatura Mínima", font=("Roboto", 15,"bold"), bg="#a0a0a0")
temp_min.grid(row=2, column=2, padx=5)

tempmin = Label(frame, font=("Roboto", 15,"bold"), bg="#a0a0a0")
tempmin.grid(row=3, column=2, padx=5)

temp_max = Label(frame, text="Temperatura Máxima", font=("Roboto", 15,"bold"), bg="#a0a0a0")
temp_max.grid(row=2, column=3, padx=5)

tempmax = Label(frame, font=("Roboto", 15, "bold"), bg="#a0a0a0")
tempmax.grid(row=3, column=3, padx=5)

tempmin.config(text = f'{tempMin.get()} °C')
tempmax.config(text = f'{tempMax.get()} °C')


raiz.mainloop()