#####################################################################################################################
__author__ = ["Cristian Laynez", "Oscar Estrada"]
__copyright__ = "Copyright 2021, Universidad del Valle de Guatemala"
__credits__ = ["Algoritmos y Estructuras de Datos", "Creado: 4 de Marzo de 2021"]
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = ["lay201281@uvg.edu.gt", ""]
__status__ = "Students of Computer Science & BioInformatics"

"""
    Class [Main]

 -> Hoja de Trabajo #05:
    Simulación de un Sistema operativo con Simpy.
"""
#####################################################################################################################

from Functions import *

memoryAmount = random.randint(1, 10)
instructions = random.randint(1, 10)


# Programa que se ejecutará
def program(env):
    print("")

# Sistema Operativo
class SystemOperative(object):

    # --> Constructor y Atributos
    def __init__(self, env) -> None:
        self.env = env
        self.action = env.process(self.newProcess())
        self.RAM = simpy.Container(env, init=100, capacity=100)
        self.data = []
        self.instructionsCount = 0

    # --> Métodos
    # Si hay memoria disponible puede pasar al estado "Ready"
    # Si no se pasará haciendo cola
    def newProcess(self):   
        while True:
            # print("Capacidad RAM: " + str(self.RAM.capacity))     
            # Memoria al azar (del 1 al 10)
            self.RAM.get(100)
            yield env.timeout(self.instructionsCount)
            # Empezar a hacer el proceso
            print("Ejecutando proceso con " + str(env.now) + " de memoria")

            # Para verificar si hay memoria disponible
            if(self.RAM.level <= 0): # Lleno
                print("Lleno Xd")
                # Se estará esperando por memoria y permanece haciendo cola
                getWaiting = env.process(self.waiting(env))
            else: # Disponible
                print("Disponible ;)")
                getReady = env.process(self.ready(env))
        
    # Esperar para que el CPU nos Atienda
    def ready(self, env):
        print("Instruccioens a realizar: " + str(env.now))  
        self.instructionsCount += 1
        yield env.timeout(self.instructionsCount)

    # El CPU atiende al proceso por un tiempo limitado, suficiente para realizar solamente 3 instrucciones
    # (Se debe de actualizar el contador de instrucciones a realizar)
    def running(self, env):
        print("")

    # Para concluir con el proceso
    def terminated(self, env):
        print("")

    # Para esperar, se generaran numero al azar entre 1 y 2
    # 1- Estará en la cola de Waiting (Atras)
    # 2- Para dejar esa cola y regresa a "ready" (Adelante )
    def waiting(self, env):
        ready = random.randint(1, 2)
        if(ready == 1):
            print("Waiting")
            print("Colas: " + str(env.now))
            self.instructionsCount += 1
            yield env.timeout(self.instructionsCount)
        else:
            print("Ready")
            print("Instruccioens a realizar: " + str(env.now))
            self.instructionsCount += 1
            yield env.timeout(self.instructionsCount)

if __name__ == "__main__":
    
    env = simpy.Environment()
    systemO = SystemOperative(env)
    PROCESSES = 5 # Para realizar los procesos solicitados
    env.run(until=PROCESSES)
    