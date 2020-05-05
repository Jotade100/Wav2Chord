import tkinter as tk
import time
from tkinter import filedialog as fd
from tkinter import *
from tkinter.ttk import *
import pygame
import threading
from red_aplicada import *

acordes = []
decodificador = ['A#dim', 'A#maj', 'A#min', 'Adim', 'Amaj', 'Amin', 'Bdim', 'Bmaj',
       'Bmin', 'C#dim', 'C#maj', 'C#min', 'Cdim', 'Cmaj', 'Cmin', 'D#dim',
       'D#maj', 'D#min', 'Ddim', 'Dmaj', 'Dmin', 'Edim', 'Emaj', 'Emin',
       'F#dim', 'F#maj', 'F#min', 'Fdim', 'Fmaj', 'Fmin', 'G#dim',
       'G#maj', 'G#min', 'Gdim', 'Gmaj', 'Gmin']

def callback():
    try:
        progress['value'] = 0
        name = fd.askopenfilename() 
        lbl.configure(text = name)
        # acorde.configure(text = pygame.mixer.music.get_pos())
        pygame.mixer.music.load(name)
        t1 = threading.Thread(target=actualizar_tiempo, args=())
        # Barra y cargar el modelo
        barra_analisis(name)
        # Activar botones
        boton_pausa.configure(state=NORMAL)
        boton_play.configure(state=NORMAL)
        boton_continuar.configure(state=NORMAL)
        # hilo para la duración de la melodía
        t1.start()
    except:
        acorde.configure(text = "Error cargando archivo")
    
def actualizar_tiempo():
    while(pygame.mixer.music.get_busy):
        time.sleep(1)
        tiempo.configure(text = str(int(pygame.mixer.music.get_pos()/1000)) + ' segundos')
        # print(len(acordes))
        acorde.configure(text = decodificador[acordes[(int(pygame.mixer.music.get_pos()/1000))]] )
        window.update_idletasks() 


def barra_analisis(name):
    global acordes
    acorde.configure(text = "¡Archivo cargado!")
    dataset = partir_archivo(name)
    progress['value'] = 20
    window.update_idletasks() 
    time.sleep(1) 
    acorde.configure(text = "Importando el modelo")
    window.update_idletasks() 
    time.sleep(1) 
    modelo = importar_modelo()
    progress['value'] = 40
    window.update_idletasks() 
    time.sleep(0.5) 
    acorde.configure(text = "¡Modelo importado!")
    window.update_idletasks() 
    time.sleep(1) 
    prob = modelo.predict(dataset)
    progress['value'] = 60
    window.update_idletasks() 
    acorde.configure(text = "Probabilidades calculadas")
    window.update_idletasks() 
    time.sleep(1) 
    res = [i.argmax() for i in prob]
    acorde.configure(text = "Acordes computados")
    progress['value'] = 80
    window.update_idletasks() 
    time.sleep(1) 
    acordes = res
    # Para los finales
    acordes.append(acordes[len(acordes) - 1])
    acordes.append(acordes[len(acordes) - 1])
    progress['value'] = 100
    window.update_idletasks() 
    

def play():
    pygame.mixer.music.play()


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


    
window = Tk()
window.title("Mus2Chord")
window.geometry('700x600')

pygame.mixer.init()



errmsg = 'Error!'


boton = tk.Button(text='Click to Open File', 
    command=callback)
boton.place(x=350, y=25, anchor="center")

boton_play = tk.Button(text='Play', 
    command=play, state=DISABLED)
boton_play.place(x=150, y=125, anchor="center")

boton_pausa = tk.Button(text='Pausa', 
    command=pause, state=DISABLED)
boton_pausa.place(x=350, y=125, anchor="center")

boton_continuar = tk.Button(text='Continuar', 
    command=unpause, state=DISABLED)
boton_continuar.place(x=550, y=125, anchor="center")

lbl = Label(window, text="Hello", font=("Arial Bold", 5))
lbl.grid(column=2, row=1)

acorde = Label(window, text="Acordes", font=("Arial Bold", 40))
acorde.place(x=350, y=300, anchor="center")

tiempo = Label(window, text="Archivo no cargado", font=("Arial Bold", 10))
tiempo.place(x=350, y=350, anchor="center")

progress = Progressbar(window, orient = HORIZONTAL, 
    length = 300, mode = 'determinate') 
progress.place(x=350, y=200, anchor="center")

window.mainloop()