# Lab7-
Michelle Mejía 22596 y  Silvia Illescas 22376

ENLACE DE YOUTUBE CON EXPLICACIÓN: https://youtu.be/a51OKaoF3Y8

Este proyecto tiene como objetivo la simplificación de gramáticas contextuales libres (CFGs) utilizando Python. El programa carga archivos de texto que contienen gramáticas y realiza las siguientes operaciones:

1. Validación del formato de las gramáticas.
2. Eliminación de producciones-𝜀.
3. Eliminación de producciones unitarias.
4. Eliminación de símbolos inútiles.
5. Conversión de las gramáticas a la **Forma Normal de Chomsky (CNF)**.

El programa está diseñado para trabajar con dos archivos de gramáticas proporcionadas por el usuario y utiliza las convenciones de que las letras en mayúscula representan no-terminales y las letras en minúscula representan terminales.

## Instrucciones para ejecutar el programa

1. **Clonar el repositorio**:
git clone https://github.com/michellemej22596/Lab7-.git

2. **Preparar el entorno**:
Asegúrate de tener Python instalado en tu sistema.

3. **Ejecutar el programa**:
Para ejecutar el programa, navega a la carpeta donde se encuentra el archivo simplificar_gramatica.py y ejecuta el siguiente comando:

python simplificar_gramatica.py

Archivos de gramáticas:

El programa lee dos archivos de texto: gramatica1.txt y gramatica2.txt.
Cada archivo debe seguir el formato de gramáticas contextuales libres, donde cada producción está separada por una flecha (->) y múltiples producciones están separadas por el operador |.

Validación del Formato
El programa utiliza una expresión regular para validar que cada línea en los archivos de gramáticas esté correctamente escrita. Si se encuentra un error en el formato, la ejecución se detendrá y se mostrará un mensaje de error.

Ejemplo de gramática válida:

S -> 0A0 | 1B1 | BB
A -> C
B -> S | A
C -> S | ε

Si el archivo contiene una producción mal escrita, como:
S -> aAa | Bb1b | ε

El programa mostrará un error de validación y se detendrá.


Eliminación de Producciones-𝜀
El programa elimina todas las producciones que contienen el símbolo ε. Para eliminar correctamente las producciones-𝜀, se siguen estos pasos:

Se identifican los símbolos anulables.
Se generan nuevas producciones considerando todas las combinaciones posibles de las producciones que contienen símbolos anulables.
El resultado de la gramática sin producciones-𝜀 se muestra en pantalla.

Eliminación de Producciones Unitarias
Después de eliminar las producciones-𝜀, el programa también elimina las producciones unitarias. Estas son producciones de la forma A -> B, donde tanto A como B son no-terminales.

Eliminación de Símbolos Inútiles
El programa elimina los símbolos inútiles, aquellos que no producen cadenas de terminales o que no son alcanzables desde el símbolo inicial.

Conversión a Forma Normal de Chomsky (CNF)
Finalmente, el programa convierte las gramáticas a la Forma Normal de Chomsky (CNF). En CNF, todas las producciones tienen una de las siguientes formas:

𝐴
→
𝐵
𝐶
A→BC, donde 
𝐴
A, 
𝐵
B, y 
𝐶
C son no-terminales.
𝐴
→
𝑎
A→a, donde 
𝐴
A es un no-terminal y 
𝑎
a es un terminal.
El proceso de conversión incluye:

Reemplazo de terminales cuando aparecen junto a no-terminales.
Reestructuración de las producciones para asegurar que todas las producciones tengan exactamente dos no-terminales en el lado derecho.

Ejemplo de Uso
Al ejecutar el programa, se mostrarán las diferentes etapas de la simplificación de las gramáticas:

Gramática original.
Gramática después de eliminar producciones-𝜀.
Gramática después de eliminar producciones unitarias.
Gramática después de eliminar símbolos inútiles.
Gramática convertida a CNF.

Video de Demostración
Puedes ver el video de demostración aquí.