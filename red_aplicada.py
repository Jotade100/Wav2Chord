import os
from pydub import AudioSegment
import librosa
import scipy.io.wavfile
import numpy as np
from keras.models import model_from_json

def limpiar_folder():
    dir_path = '/tmp'

    try:
        os.rmdir(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

def crear_folder():
    path = "/tmp"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)

def partir_archivo(nombre_archivo):
    limpiar_folder()
    crear_folder()
    lista_general = []
    x, Fs = librosa.load(nombre_archivo, sr=8000)
    print(x, Fs)
    print(len(x)/Fs)
    lista = range(int(len(x)/Fs))
    for i in lista:
        print(i)
        if i != lista[-1]:
            librosa.output.write_wav('tmp/' + str(i) + '.wav', x[Fs*i:Fs*(i+2)], 16000)
            samples, sample_rate = librosa.load('tmp/' + str(i) +'.wav', sr = 8000)
            samples = librosa.resample(samples, sample_rate, 8000)
            lista_general.append(samples)
        else:
            print(sample_rate)
            librosa.output.write_wav('tmp/' + str(i) + '.wav', x[Fs*i:], 16000)
            samples, sample_rate = librosa.load('tmp/' + str(i) +'.wav', sr = 8000, duration=2.0)
            samples = librosa.resample(samples, sample_rate, 8000)
            # de momento no lo añadiremos
            # lista_general.append(samples)
    print("sample rate", sample_rate)
    lista_general = np.array(lista_general)
    for i in lista_general:
        print(i.shape)
    print(lista_general.shape)
    lista_general = lista_general.reshape(-1, 8000, 1)
    print(lista_general.shape)
    return lista_general    

# Prueba del método
#partir_archivo('ejemplospanish2.wav')


def importar_modelo():
    json_file = open('model8000.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model.h5")
    print("Loaded model from disk")
    
    # evaluate loaded model on test data
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',metrics=['accuracy'])
    return model

     