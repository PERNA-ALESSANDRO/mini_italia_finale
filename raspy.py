0# Analisi sw su Raspberry per Italy4you
# protocollo:
# da Arduino a Raspberry: 1 carattere per ogni pulsante da codice 00000000 a codice 00010100(20)
# da Raspberry ad Arduino: carattere =risposta GIUSTA 01100011 ('c')  risposta sbagliata 01110111 ('w')
#                         carattere= suono x fine risposte se indovinate (entro 11 tentativi) 11001100
#                         carattere= suono per numero tentativi max raggiunti senza indovinare 10101010
# costanti
# OK    01100011  'c'
# ERR   01110111  'w'
# SOUND_OK 11001100
# SOUND_ERR 10101010
# var 
# domande, elenco delle domande, array di stringhe
# risposte, elenco delle risposte per ogni domanda, matrice di bit n domande x 21 risposte (0,1)
# ndom, numero delle domande presenti nel file csv, intero
# regioni, vettore associativo con indici = ai nomi delle 21 regione italiane e valore =posizione da 0 a 20 dei sensori a pulsante
# numtent, numero tentativi, intero
# inizio
#     carica da file csv "test.csv" ogni riga carica le due var domande, risposte ed ndom
#     apri file di testo "risultati.csv" (output)
#     per ogni stringa k presente in domande 
#         visualizza la domanda k su monitor
#         conta numero di 1 in risposte[k] in tot
#         numtent=0
#         ripeti
#             visualizza tot e numtent su monitor
#             ripeti
#                 attendi carattere da Arduino
#             finche' carattere arrivato
#             se risposte[k][carattere] = 1
#             allora
#                 tot=tot-1
#                 invia ad Arduino carattere OK
#             altrimenti
#                 invia ad Arduino carattere ERR
#             fse
#             numtent++
#         finche' tot=0 or numtent=11
#         se (tot==0)
#         allora
#             invia ad Arduino carattere SOUND_OK
#         altrimenti
#             invia ad Arduino carattere SOUND_ERR
#         fse
#         scrivi su file di testo risultati.csv la riga domanda[k];risultato ("OK" o "ERR");numero tentativi;
#     fine ciclo
#     chiudi file testo "risutati.csv"
# fine

# procedura carica file csv  ("test;0,0,1,1,....,0; 21 numeri per risposte giuste o sbagliate")
# parametri
# nf, nome del file stringa
# dom, array delle domande, array di nel stringhe
# risp, matrice delle risposte, matrice nelx21 di interi(0/1)
# nel, numero elementi del vettore o righe della matrice, intero
# var
# str, riga del file csv, stringa

# inizio 
# apri file  nf (input)
# se file esiste
# allora     
#     per ogni riga k del file
#         leggi la riga dal file in str
#         metto item 0 in domande[k]
#         per ogni item successivo j da 1 a 21 
#             metti item[j] in risp[k][j]
#         fciclo
#     fciclo
#     chiudi file nf
# altrimenti
#     scrivi a monitor "Manca file domande!!!!!"
# fse
# fine 

import tkinter as tk
import serial as s
import time
from os import *
import serial.tools.list_ports
import RPi.GPIO as GPIO

led_rosso = 18
led_verde = 16

# Dizionario di regioni
r = {
    "abruzzo": 30,
    "basilicata": 31,
    "calabria": 32,
    "campania": 33,
    "emilia": 34,
    "friuli": 35,
    "lazio": 36,
    "liguria": 37,
    "lombardia": 38,
    "marche": 39,
    "molise": 40,
    "piemonte": 41,
    "puglia": 42,
    "sardegna": 43,
    "sicilia": 44,
    "toscana": 45,
    "trentino": 46,
    "umbria": 47,
    "aosta": 48,
    "veneto": 49
}

GPIO.setmode(GPIO.BOARD)

GPIO.setup(led_rosso, GPIO.OUT)
GPIO.setup(led_verde, GPIO.OUT)

def pause(text):
    try: 
        ser.reset_input_buffer()
        p = int((ser.read(1)).encode("hex"), 16)
    except: 
        pass

porte = serial.tools.list_ports.comports()

# Funzione per aprire la porta di Arduino
def open_port():
    for port, desc, hwid in porte:
        global ser
        if "Arduino Mega 2560" in desc:
            ser = s.Serial(str(port), 9600, bytesize=s.EIGHTBITS)
                
            break
   
g = 0
ris = False


window = tk.Tk()
window.title("Quiz")
window.geometry("720x600")
window.resizable(width=False, height=False)

# PAUSA FINO A INVIO
def pause(text):
    try: 
        #input(text)
        p = int.from_bytes(ser.read(1))
    except: 
        pass

# CAMBIA COLORE DI UN LABEL
def change_color(label, color, t = -1):
    label.config(fg=color)
    label.update()

    if t != -1:
        time.sleep(t)
        label.config(fg=color)
        label.update()



# CONTROLLA SE INPUT inp E' LA RISPOSTA ALLA DOMANDA d
# inizio
#     se inp è una risposta alla domanda d
#     allora
#       aggiungi inp a corrette 
#       incrementa g
#       ris = true
#     fse
# fine

# VARIABILI
# inp - risposta data in input - intero
# d - domanda attuale - stringa
# g - contatore di risposte corrette date - intero

def check(inp, d):
    global g
    global ris
    
    ris = False
    if inp in risposte[d] and not inp in corrette:
        corrette.append(inp)
        g += 1
        c.set("{}/{} risposte indovinate.".format(g, len(risposte[idx])))
        ris = True
        change_color(dom, "green", 1)
    elif inp in corrette:
        change_color(dom, "gold", 1)
    else:
        change_color(dom, "red", 1)
    change_color(dom, "black")
    return g # Numero di risposte corrette univoche date



open_port()
domande = ["Pinco?", "Palla? ", "Pippo?"]

risposte = [[r["molise"]], [r["piemonte"], r["puglia"]], [r["piemonte"], r["sicilia"], r["molise"]]]
c = tk.StringVar()

for idx, d in enumerate(domande):
    # Variabile per incrementare il contatore di risposte esatte 
    c.set("{}/{} risposte indovinate.".format(g, len(risposte[idx])))

    # Visualizzazione domanda d su schermo
    dom = tk.Label(window, text=d, font=("Helvatica", 30), anchor='center')
    counter = tk.Label(window, textvariable=c, font=("Helvatica", 25))
    
    dom.pack()
    counter.pack(pady=10)

    inp = int.from_bytes((ser.read(1)), "little") # --> Trasformare carattere in arrivo dalla porta seriale in intero
    # inp = int.from_bytes(ser.read(1))
    # inp = int(input(d))
    corrette = []


    # inizio
    #     mentre n° risposte corrette date < n° risposte corrette totali
    #         se risposta data è corretta
    #         allora 
    #             accendi led led_verde
    #         altrimenti
    #             accendi led led_rosso
    #     fciclo
    # fine

    while check(inp, idx) < len(risposte[idx]):
        if ris: 
            print("Risposta esatta.")
            #ser.writ e("c".encode("utf-8"))
            GPIO.output(led_verde, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_verde, GPIO.LOW)
        else: 
            print("Risposta errata.")
            #ser.write("w".encode("utf-8"))
            GPIO.output(led_rosso, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_rosso, GPIO.LOW)
        
        print("Regioni indovinate: " + str(g))
        # inp = int(s.read(1))
        ser.reset_input_buffer()
        inp = int.from_bytes((ser.read(1)), "little")
        # inp = int.from_bytes(ser.read(1))

    fine = tk.Label(window, text="Tutte le regioni indovinate!", font=("Helvatica", 40), fg="green")
    fine.pack(pady=10)

    print("Tutte le regioni indovinate!")
    pause("Premere invio per continuare...")
    system("cls")
    
    dom.destroy()
    counter.destroy()
    fine.destroy()
    g = 0


window.mainloop()
