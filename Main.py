#####################################################################################################################
__author__ = ["Cristian Laynez", "Oscar Estrada"]
__copyright__ = "Copyright 2021, Universidad del Valle de Guatemala"
__credits__ = ["Algoritmos y Estructuras de Datos", "Creado: 4 de Marzo de 2021"]
__license__ = "GPL"
__version__ = "1.0.0"
__status__ = "Students of Computer Science & BioInformatics"

"""
    Class [Main]

 -> Hoja de Trabajo #05:
    Simulación de un Sistema operativo con Simpy.
"""
#####################################################################################################################
#Importaciones
import random
import simpy
import statistics 

#Variables solicitadas en documento
RANDOM_SEED = 69 #Je
intervalo = 10.0
processTime = [] #Donde se guarda la cantidad de cada pro
cantProc = 25
rangeInstructions = [1, 10]
rangeRam = [1,10]
instruccionesPorProceso = 3
totalTime = 0

def proc(env, numProcess, cpu, ram, waiting, tiempoLlegada):
    global totalTime #Para acumular el tiempo utilizado
    global processTime #Lista que guarda cuanto tarda cada proceso
    yield env.timeout(tiempoLlegada)
    start = env.now
    end = 0
    print('Proceso # %d ingreso al sistema en %s' % (numProcess, start))
    instProcess = random.randint(*rangeInstructions) #Cantidad de instrucciones que el proceso va a realizar
    ramProcess = random.randint(*rangeRam) #Cantidad de ram que el proceso necesita
    with ram.get(ramProcess) as cola:
        print('Proceso # %d necesita de espacio %s de ram' % (numProcess, ramProcess))
        while instProcess > 0:
            with cpu.request() as colaEspera:
                yield colaEspera
                print('El proceso # %d entra al CPU en %s' % (numProcess, env.now))
                yield env.timeout(1) #El CPU ejecuta las instrucciones en 1 unidad de timepo
                instProcess -= instruccionesPorProceso
                if instProcess <=0:
                    instProcess = 0
                    end = env.now
                    print('El proceso # %d sale del CPU en %s' % (numProcess, end))
                else:
                    option = random.randint(1,2)
                    if(option == 1): #Para ver si pasa a waiting o a ready
                        with waiting.request() as colaWaiting:
                            yield colaWaiting
                            yield env.timeout(1)
                    #No es necesario el else ya que de por si se tiene que volver al
                    #pasar al inicio, es el siguiente.
    time = end - start
    processTime.append(time)
    totalTime = end #Cambio de tiempo total para que el ultimo proceso sea el guardado.

def entry_proc(env, cpu, ram, waiting):
    for i in range(cantProc):
        timeToStart = random.expovariate(1.0 / intervalo)
        env.process(proc(env, i, cpu, ram, waiting, timeToStart))
        
#Variables de cuerpo
random.seed(RANDOM_SEED) #Semilla solicitada para que siempre se genere la misma secuencia
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity = 1)
waiting = simpy.Resource(env, capacity = 1)

entry_proc(env, cpu, ram, waiting)
env.run()

#Calculo de promedio y desviacion estandar
average = totalTime/cantProc
deviation = statistics.stdev(processTime)

#imprimir en pantalla resultados
print ('\nTiempo total', totalTime)
print('Promedio de tiempo por instruccion: ', average)
print('Desviacion Estandar: ', deviation)