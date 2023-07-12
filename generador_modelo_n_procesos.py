# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 19:29:05 2023

@author: Sergio
"""
#Pregunta el número de procesos 
numero_procesos = int(input("Introduce número de procesos: "))

#Genera el código según el número de procesos introducido
codigo_modelo = '''MODULE main
DEFINE
  n:='''
codigo_modelo += str(numero_procesos) + ";"
codigo_modelo += '''
VAR
  semaphore : boolean;
  next_process: 1..n;'''
  
for i in range(1,numero_procesos+1):
    codigo_modelo += "\n  proc" + str(i) + ":process user(semaphore,next_process,n," + str(i) + "); "

codigo_modelo += '''
ASSIGN

 init(semaphore) := FALSE;	
'''
codigo_modelo += "SPEC AG ! ("
for i in range(1,numero_procesos+1):
    codigo_modelo += "proc" + str(i) + ".state = critical" 
    if i != numero_procesos:
        codigo_modelo += " & "
    else:
        codigo_modelo += ");"
        
codigo_modelo += '''
SPEC AG (proc1.state = entering -> AF proc1.state = critical);

MODULE user(semaphore, next_process, n, number)
VAR
  state : {idle, entering, critical, exiting};
ASSIGN
  init(state) := idle;
  next(state) :=
    case
      state = idle : 						{idle,entering};
      state = entering & !semaphore & next_process=number: 	critical;
      state = critical : 					{critical, exiting};
      state = exiting : 					idle;
      TRUE: 							state;
    esac;

  next(semaphore) :=
    case
      state = entering & next_process=number: TRUE;
      state = exiting: 	FALSE;
      TRUE: 		semaphore;
    esac;

  next(next_process) :=
    case
      state = exiting : (next_process mod n) + 1;
      TRUE:				next_process;
    esac;

FAIRNESS
  running
FAIRNESS !(state = idle)
FAIRNESS !(state = critical)
'''

#Escribe el código generado
try:
    archivo = open("concurrencia_modificada_n.smv", "w")
    archivo.write(codigo_modelo)
    archivo.close()
    
    print("Modelo de exlusión mutua de " + str(numero_procesos) + " procesos creado con éxito")
    
except PermissionError:
    print("No tienes permisos suficientes para crear o escribir en el archivo.")
except IOError:
    print("Ocurrió un error de entrada/salida al trabajar con el archivo.")    


