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
# ready = random.randint(1, 2)

# Programa que se ejecutará
def program(env):
    print("")

# Sistema Operativo
class SystemOperative(object):

    # --> Constructor y Atributos
    def __init__(self, env, ram, data) -> None:
        self.env = env
        self.action = env.process(self.newProcess())
        self.ram = ram
        self.data = data
        self.instructionsCount = 0

    # --> Métodos
    # Si hay memoria disponible puede pasar al estado "Ready"
    # Si no se pasará haciendo cola
    def newProcess(self):        
        # Memoria al azar (del 1 al 10)
        yield env.timeout(memoryAmount)
        # Empezar a hacer el proceso
        print("Ejecutando proceso con " + str(env.now) + " de memoria")
        # Para verificar si hay memoria disponible
        if(memoryAmount == 10): # Lleno
            # Se estará esperando por memoria y permanece haciendo cola
            self.waiting()
        else:
            getReady = env.process(self.ready(env))
        
    # Esperar para que el CPU nos Atienda
    def ready(self, env):
        yield env.timeout(instructions)
        # self.instructionsCount += instructions
        print("Instruccioens a realizar: " + str(env.now))  

    # El CPU atiende al proceso por un tiempo limitado, suficiente para realizar solamente 3 instrucciones
    # (Se debe de actualizar el contador de instrucciones a realizar)
    def running(self):
        print("")

    # Para concluir con el proceso
    def terminated(self):
        print("")

    # Para esperar, se generaran numero al azar entre 1 y 2
    # 1- Para pasar a la cola de Waiting
    # 2- Para dejar esa cola y regresa a "ready"
    def waiting(self):
        print("")

if __name__ == "__main__":
    
    data = []   
    env = simpy.Environment()
    RAM = simpy.Container(env, init=100, capacity=100)
    systemO = SystemOperative(env, RAM, data)
    env.run()
    