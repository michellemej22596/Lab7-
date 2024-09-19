import re

# Expresión regular para validar una producción
regex_produccion = r"^[A-Z] -> (([A-Za-z0-9]+)( \| )?)+$"

def leer_gramatica(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    return [linea.strip() for linea in lineas]

def validar_gramatica(producciones):
    for produccion in producciones:
        if not re.match(regex_produccion, produccion):
            print(f"Error en la producción: {produccion}")
            return False
    return True

# Leer y validar las gramáticas
producciones_gramatica1 = leer_gramatica('gramatica1.txt')
producciones_gramatica2 = leer_gramatica('gramatica2.txt')

if validar_gramatica(producciones_gramatica1):
    print("Gramática 1 válida")
else:
    print("Gramática 1 inválida")

if validar_gramatica(producciones_gramatica2):
    print("Gramática 2 válida")
else:
    print("Gramática 2 inválida")


def encontrar_anulables(producciones):
    anulables = set()

    # Paso 1: Encontrar símbolos que derivan en e directamente
    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        if "e" in derecha:
            anulables.add(izquierda)

    # Paso 2: Encontrar símbolos anulables por transitividad
    cambio = True
    while cambio:
        cambio = False
        for produccion in producciones:
            izquierda, derecha = produccion.split(" -> ")
            partes = derecha.split(" | ")
            for parte in partes:
                if all(simbolo in anulables or simbolo == "e" for simbolo in parte):
                    if izquierda not in anulables:
                        anulables.add(izquierda)
                        cambio = True
    return anulables


def eliminar_producciones_epsilon(producciones):
    anulables = encontrar_anulables(producciones)
    nuevas_producciones = []

    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")
        nuevas_partes = set()

        for parte in partes:
            if parte != "e":
                combinaciones = [parte]
                for simbolo in parte:
                    if simbolo in anulables:
                        # Generar combinaciones sin el símbolo anulable
                        nuevas = [c.replace(simbolo, "", 1) for c in combinaciones]
                        combinaciones.extend(nuevas)

                nuevas_partes.update(filter(None, combinaciones))  # Evita combinaciones vacías

        nuevas_producciones.append(f"{izquierda} -> {' | '.join(nuevas_partes)}")

    return nuevas_producciones

def eliminar_producciones_unitarias(producciones):
    unitarias = {}
    nuevas_producciones = []

    # Paso 1: Identificar producciones unitarias
    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")
        
        for parte in partes:
            if parte.isupper():  # Es un no-terminal (producción unitaria)
                if izquierda not in unitarias:
                    unitarias[izquierda] = set()
                unitarias[izquierda].add(parte)
            else:
                nuevas_producciones.append(f"{izquierda} -> {parte}")
    
    # Paso 2: Reemplazar producciones unitarias
    for izq, derechos in unitarias.items():
        for derecho in derechos:
            for produccion in producciones:
                izq_produccion, der_produccion = produccion.split(" -> ")
                if izq_produccion == derecho:
                    partes = der_produccion.split(" | ")
                    for parte in partes:
                        nuevas_producciones.append(f"{izq} -> {parte}")

    return nuevas_producciones

def eliminar_simbolos_inutiles(producciones, simbolo_inicial):
    # Paso 1: Encontrar símbolos que producen terminales
    productores = set()
    cambiando = True
    
    while cambiando:
        cambiando = False
        for produccion in producciones:
            izquierda, derecha = produccion.split(" -> ")
            partes = derecha.split(" | ")
            
            for parte in partes:
                if all(simbolo.islower() or simbolo in productores for simbolo in parte):
                    if izquierda not in productores:
                        productores.add(izquierda)
                        cambiando = True

    # Paso 2: Encontrar símbolos alcanzables desde el símbolo inicial
    alcanzables = {simbolo_inicial}
    cambiando = True
    
    while cambiando:
        cambiando = False
        for produccion in producciones:
            izquierda, derecha = produccion.split(" -> ")
            if izquierda in alcanzables:
                partes = derecha.split(" | ")
                for parte in partes:
                    for simbolo in parte:
                        if simbolo.isupper() and simbolo not in alcanzables:
                            alcanzables.add(simbolo)
                            cambiando = True

    # Paso 3: Filtrar producciones útiles
    nuevas_producciones = []
    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        if izquierda in alcanzables and izquierda in productores:
            nuevas_producciones.append(produccion)

    return nuevas_producciones

def eliminar_producciones_repetidas(producciones):
    producciones_unicas = list(set(producciones))  # Elimina duplicados usando un set
    return producciones_unicas


import string

# Generar nuevas variables para los terminales
def reemplazar_terminales(producciones):
    nuevos_terminales = {}
    nuevas_producciones = []
    nuevo_simbolo = iter(string.ascii_uppercase)  # Para asignar nuevos no-terminales

    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")

        for parte in partes:
            nueva_parte = []
            for simbolo in parte:
                if simbolo.islower():  # Es un terminal
                    if simbolo not in nuevos_terminales:
                        # Crear un nuevo símbolo no-terminal para el terminal
                        nuevo_no_terminal = next(nuevo_simbolo)
                        nuevos_terminales[simbolo] = nuevo_no_terminal
                        nuevas_producciones.append(f"{nuevo_no_terminal} -> {simbolo}")
                    nueva_parte.append(nuevos_terminales[simbolo])
                else:
                    nueva_parte.append(simbolo)
            # Reemplazar terminales solo si la parte contiene tanto terminales como no-terminales
            nuevas_producciones.append(f"{izquierda} -> {''.join(nueva_parte)}")
    
    return nuevas_producciones, nuevos_terminales


# Asegurarse que cada producción tenga exactamente dos no-terminales
# Asegurarse que cada producción tenga exactamente dos no-terminales
def forzar_producciones_binarias(producciones):
    nuevas_producciones = []
    nuevo_simbolo = iter(string.ascii_uppercase)  # Para asignar nuevos no-terminales
    simbolos_usados = set()  # Llevar un control de los símbolos ya usados

    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")

        for parte in partes:
            if len(parte) > 2:  # Si hay más de dos símbolos en el lado derecho
                anterior = parte[0]
                for i in range(1, len(parte) - 1):
                    nuevo_no_terminal = next(nuevo_simbolo)
                    while nuevo_no_terminal in simbolos_usados:  # Evitar duplicados
                        nuevo_no_terminal = next(nuevo_simbolo)
                    simbolos_usados.add(nuevo_no_terminal)
                    nuevas_producciones.append(f"{anterior} -> {parte[i]}{nuevo_no_terminal}")
                    anterior = nuevo_no_terminal
                nuevas_producciones.append(f"{anterior} -> {parte[-2:]}")  # La última pareja
            else:
                nuevas_producciones.append(f"{izquierda} -> {parte}")
    
    # Eliminar producciones repetidas al final
    nuevas_producciones = eliminar_producciones_repetidas(nuevas_producciones)
    
    return nuevas_producciones



def eliminar_producciones_ciclicas(producciones):
    nuevas_producciones = []
    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")
        # Eliminar producciones donde el lado derecho es igual al izquierdo (producción cíclica)
        partes = [parte for parte in partes if parte != izquierda]
        if partes:
            nuevas_producciones.append(f"{izquierda} -> {' | '.join(partes)}")
    return nuevas_producciones

# Función para imprimir producciones
def imprimir_producciones(titulo, producciones):
    print(f"\n{titulo}:")
    for p in producciones:
        print(p)

# Ejemplo de uso ELIMINAR 
producciones_sin_epsilon_1 = eliminar_producciones_epsilon(producciones_gramatica1)
producciones_sin_epsilon_2 = eliminar_producciones_epsilon(producciones_gramatica2)

# Eliminar producciones repetidas después de eliminar producciones-𝜀
producciones_sin_epsilon_1 = eliminar_producciones_repetidas(producciones_sin_epsilon_1)
producciones_sin_epsilon_2 = eliminar_producciones_repetidas(producciones_sin_epsilon_2)

imprimir_producciones("Gramática 1 sin producciones-e", producciones_sin_epsilon_1)
imprimir_producciones("Gramática 2 sin producciones-e", producciones_sin_epsilon_2)

# Ejemplo de uso PRODUCCIONES UNITARIAS
producciones_sin_unitarias_1 = eliminar_producciones_unitarias(producciones_sin_epsilon_1)
producciones_sin_unitarias_2 = eliminar_producciones_unitarias(producciones_sin_epsilon_2)

# Eliminar producciones repetidas después de eliminar producciones unitarias
producciones_sin_unitarias_1 = eliminar_producciones_repetidas(producciones_sin_unitarias_1)
producciones_sin_unitarias_2 = eliminar_producciones_repetidas(producciones_sin_unitarias_2)

imprimir_producciones("Gramática 1 sin producciones unitarias", producciones_sin_unitarias_1)
imprimir_producciones("Gramática 2 sin producciones unitarias", producciones_sin_unitarias_2)

# Ejemplo de uso ELIMINAR PRODUCCIONES CÍCLICAS
producciones_sin_ciclicas_1 = eliminar_producciones_ciclicas(producciones_sin_unitarias_1)
producciones_sin_ciclicas_2 = eliminar_producciones_ciclicas(producciones_sin_unitarias_2)

# Eliminar producciones repetidas después de eliminar producciones cíclicas
producciones_sin_ciclicas_1 = eliminar_producciones_repetidas(producciones_sin_ciclicas_1)
producciones_sin_ciclicas_2 = eliminar_producciones_repetidas(producciones_sin_ciclicas_2)

imprimir_producciones("Gramática 1 sin producciones cíclicas", producciones_sin_ciclicas_1)
imprimir_producciones("Gramática 2 sin producciones cíclicas", producciones_sin_ciclicas_2)

# Ejemplo de uso SIMBOLOS INUTILES
producciones_utiles_1 = eliminar_simbolos_inutiles(producciones_sin_ciclicas_1, "S")
producciones_utiles_2 = eliminar_simbolos_inutiles(producciones_sin_ciclicas_2, "S")

# Eliminar producciones repetidas después de eliminar símbolos inútiles
producciones_utiles_1 = eliminar_producciones_repetidas(producciones_utiles_1)
producciones_utiles_2 = eliminar_producciones_repetidas(producciones_utiles_2)

imprimir_producciones("Gramática 1 sin símbolos inútiles", producciones_utiles_1)
imprimir_producciones("Gramática 2 sin símbolos inútiles", producciones_utiles_2)

# Ejemplo de uso CHOMSKY - Reemplazar terminales
producciones_con_terminales_1, terminales_1 = reemplazar_terminales(producciones_utiles_1)
producciones_con_terminales_2, terminales_2 = reemplazar_terminales(producciones_utiles_2)

# Eliminar producciones repetidas después de reemplazar terminales
producciones_con_terminales_1 = eliminar_producciones_repetidas(producciones_con_terminales_1)
producciones_con_terminales_2 = eliminar_producciones_repetidas(producciones_con_terminales_2)

imprimir_producciones("Gramática 1 con terminales reemplazados", producciones_con_terminales_1)
imprimir_producciones("Gramática 2 con terminales reemplazados", producciones_con_terminales_2)

# Ejemplo de uso CNF - Forzar producciones binarias
producciones_binarias_1 = forzar_producciones_binarias(producciones_con_terminales_1)
producciones_binarias_2 = forzar_producciones_binarias(producciones_con_terminales_2)

# Eliminar producciones repetidas después de convertir a forma binaria
producciones_binarias_1 = eliminar_producciones_repetidas(producciones_binarias_1)
producciones_binarias_2 = eliminar_producciones_repetidas(producciones_binarias_2)

imprimir_producciones("Gramática 1 en Forma Normal de Chomsky", producciones_binarias_1)
imprimir_producciones("Gramática 2 en Forma Normal de Chomsky", producciones_binarias_2)
