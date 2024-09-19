import re

# Expresión regular para validar una producción (acepta ε y combinaciones de no terminales)
regex_produccion = r"^[A-Z] -> (([A-Za-z0-9]+|ε)( \| )?)+$"

# Función para leer el archivo de la gramática
def leer_gramatica(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:  # Usar UTF-8 para leer correctamente caracteres como ε
        lineas = f.readlines()
    return [linea.strip() for linea in lineas]

# Función para validar las gramáticas usando regex
def validar_gramatica(producciones):
    for produccion in producciones:
        if not re.match(regex_produccion, produccion):
            print(f"Error en la producción: {produccion}")
            return False
    return True

# Función para encontrar los símbolos anulables
def encontrar_anulables(producciones):
    anulables = set()
    # Paso 1: Encontrar símbolos que derivan en ε directamente
    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        if "ε" in derecha:  # Buscamos ε en lugar de 'e'
            anulables.add(izquierda)

    # Paso 2: Encontrar símbolos anulables por transitividad
    cambio = True
    while cambio:
        cambio = False
        for produccion in producciones:
            izquierda, derecha = produccion.split(" -> ")
            partes = derecha.split(" | ")
            for parte in partes:
                if all(simbolo in anulables or simbolo == "ε" for simbolo in parte):  # También verificamos por ε
                    if izquierda not in anulables:
                        anulables.add(izquierda)
                        cambio = True
    return anulables

# Función para eliminar producciones ε
def eliminar_producciones_epsilon(producciones):
    anulables = encontrar_anulables(producciones)
    nuevas_producciones = []

    for produccion in producciones:
        izquierda, derecha = produccion.split(" -> ")
        partes = derecha.split(" | ")
        nuevas_partes = set()

        for parte in partes:
            if parte != "ε":  # Ignorar producciones que sean solo ε
                combinaciones = [parte]
                for simbolo in parte:
                    if simbolo in anulables:
                        # Generar combinaciones sin el símbolo anulable
                        nuevas = [c.replace(simbolo, "", 1) for c in combinaciones]
                        combinaciones.extend(nuevas)

                nuevas_partes.update(filter(None, combinaciones))  # Evita combinaciones vacías

        nuevas_producciones.append(f"{izquierda} -> {' | '.join(nuevas_partes)}")

    return nuevas_producciones

# Función para imprimir las producciones
def imprimir_producciones(titulo, producciones):
    print(f"\n{titulo}:")
    for p in producciones:
        print(p)

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

# Eliminar producciones ε para ambas gramáticas
producciones_sin_epsilon_1 = eliminar_producciones_epsilon(producciones_gramatica1)
producciones_sin_epsilon_2 = eliminar_producciones_epsilon(producciones_gramatica2)

# Imprimir resultados
imprimir_producciones("Gramática 1 sin producciones-ε", producciones_sin_epsilon_1)
imprimir_producciones("Gramática 2 sin producciones-ε", producciones_sin_epsilon_2)
