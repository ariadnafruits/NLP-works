#!/usr/bin/env python
# coding: utf-8

# IMPORTACIÓN DE LIBRERÍAS

import getopt, sys
import tkinter as tk
from tkinter import filedialog
import glob
import nltk
import re
from datetime import datetime



# ABRIR CARPETA  

def browse_directory():

    """
    Abre el navegador de archivos del cliente para que el usuario seleccione la carpeta
    dónde se ubican los documentos a analizar para generar el grafo.

    REQUISITOS:
    * Módulo tkinter y filedialog:
     >>> import tkinter as tk
     >>> from tkinter import filedialog

    PARÁMETROS DE ENTRADA:
    Ninguno

    SALIDA
    * Ruta del directorio
    
    """

    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root,initialdir="/",
                    title="""Seleccione la carpeta donde se encuentran los archivos""")

    return directory

def get_arguments():

    """
    Asigna el valor de los parametros opcionales, leyendo primero los pasados por consola y
    preguntando explícitamente el resto. 
    """

    # DEFINICION DE ARGUMENTOS 
    
    input_folder = ""
    output_folder = ""
    window = ""
    tags =  ["NN", "NNS", "JJ", "JJR", "JJS"]
    show_help = False

    # MENSAJE DE AYUDA
    
    help_message = """
					Este programa obtiene un grafo de co-apariciones de términos en una colección de documentos. Los argumentos requeridos pueden proporcionarse contestando las preguntas una vez iniciado el programa
					o directamente a través de la línea de comandos.

					-h, --help: Consulta de la ayuda

					-i --input_path: Ruta de la carpeta de los documentos a analizar. Si no se informa, el programa abrirá el explorador de archivos.

					Los documentos deben ser textos etiquetados con mediante el formalismo término/etiqueta. Por ejemplo:

					A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS

					Para obtener textos etiquetados en este formato, puede utilizarse el etiquetador de Standford, http://nlp.stanford.edu/software/tagger.shtml.

					-o, --output: Ruta de la carpeta donde se guardará la red. Si no se informa, el fichero se guardara en la carpeta del programa

					-t, --tags: Listado de etiquetas de Penn Treebank aceptadas como nodos del grafo. Si no se informa, se tomarán las etiquetas ["NN", "NNS", "JJ", "JJR", "JJS"].

					Las etiquetas del Penn Treebank pueden consultarse en https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html.

					"""
    
    # RASTREO DE ARGUMENTOS PASADOS POR CONSOLA

    print("")

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "hi:o:w:t:"
    long_options = ["help", "input_folder=", "output_folder=", "window=", "tags="]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)
    
    for argument, value in arguments:
        
        if argument in ("-h", "--help"):
            show_help = True
        elif argument in ("-i", "--input_folder"):
            input_folder = value        
        elif argument in ("-o", "--output_folder"):
            output_folder = value        
        elif argument in ("-w", "--window"):
            window = int(value)
        elif argument in ("-t", "--tags"):
            tags = value        

    if (show_help == True):
        print(help_message)
    else:
        if (input_folder == ""):
            input_folder = browse_directory()
        if (output_folder == ""):
            output_folder = "./"
        elif (not output_folder.endswith(('/', '\\'))):
              output_folder = output_folder + "/"
        if (window == ""):
            window = int(input("Número de palabras de la ventana de concurrencia: "))
        if (tags == ""):
            tags = ["NN", "NNS", "JJ", "JJR", "JJS"]
    		
    return input_folder, output_folder, window, tags

def get_documents(input_folder):
    
    """
    Crea una lista de textos completos en formato original a partir de los ficheros de una carpeta
    
    REQUISITOS
    - Módulo Glob
    >>> import glob

    PARÁMETROS
    - input_folder (string): Carpeta que contiene los ficheros a analizar. Los ficheros deben contener únicamente
    texto en formato utf-8.
      
    SALIDA
    - titles: lista de nombres de los ficheros
    - texts: lista de textos
    """
    
    path_to_files = input_folder + "/*"

    files = glob.glob(path_to_files)
    texts = list(range(len(files)))
    titles = []

    for i, file in enumerate(files):
        title = file.replace(input_folder + "/", '')
        titles.append(title)
        with open(file, 'r', encoding='utf-8') as text:
            texts[i] = text.read()
    
    return titles, texts

def get_tokens (text):

    """
    Convierte un texto etiquetado en formato término/etiqueta en una lista de tuplas (termino, etiqueta)

    REQUISITOS
    - Libreria nltk
      >>> import nltk

    PARÁMETROS
    - text (string): Texto en formato término/etiqueta. Ejemplo:
      A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS 
    """
    
    tokens = [nltk.tag.str2tuple(t) for t in text.split()]
   
    return tokens

def normalize(tokens, banned_tokens):
    
    """
    Normaliza los tokens de una lista de tuplas (token, etiqueta):
    - Elimina todos los caracteres no alfabéticos
    - Convierte mayúsculas a minúsuclas
    - Elimina tokens censurados y las palabras vacias (stopwords)

    REQUISITOS
    - Módulo de expresiones regulares re
    >>> import re

    PARAMETROS
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) original
    - banned_tokens (lista de strings): Lista de tokens no permitidos.
      Esta pensado para excluir tokens como <s> y <f>

    SALIDA
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) normalizada

	NOTAS
	- En la fase de eliminación de los caracteres no alfabéticos, el token se mantiene, aunque quede vacío, para que al calcular las concurrencias se contabilice el término dentro de la ventana de texto.
    """
    

    # Eliminación de caracteres no alfabéticos
   
    tokens = [(re.sub("[^a-zA-Z]+", '', t[0]) , t[1]) for t in tokens]
    
    # Eliminación de los tokens censurados (marcas de inicio y final de texto)
    
    tokens = [t for t in tokens if t[0] not in banned_tokens]
    
    # Conversión a minúsculas
    
    tokens = [(t[0].lower(), t[1]) for t in tokens]
    
    # Eliminación de stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    tokens = [t for t in tokens if t[0] not in stopwords]

      
    return tokens

def stem(tokens):

    """
    Trunca los tokens utilizando el algoritmo e Porter

    REQUISITOS:
    - librería nltk
      >>> import nltk

    PARAMETROS
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) normalizada
    
    SALIDA
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) truncada
    """
      
    for i in range(len(tokens)):
        tokens[i] = (nltk.PorterStemmer().stem(tokens[i][0]), tokens[i][1])
        
    return tokens

def filter_category(tokens, tags="all"):

    """
    Filtra una lista de tuplas (token, etiqueta) según las etiquetas permitidas.

    PARAMETROS
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) truncada
    - tags (lista de cadenas): lista de etiquetas del Penn Treebank permitidas.
      Ej: ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
      Si en lugar de una lista, se informa con la cadena "all", se incluirán todas las etiquetas (no se filtrara).
    SALIDA
    - terms (lista de strings): Lista de términos filtrados por categoría.
    """
    
    if (tags == "all"):
        terms = [t[0] for t in tokens]

    else:
        terms = [t[0] for t in tokens if t[1] in tags]
    
    return terms

def indices(word, words):

    """
    Busca una palabra en una lista.

    PARAMETROS
    - word (string): Palabra a buscar
    - words (lista de strings): Lista de palabras
    
    SALIDA
    - indices (lista de números enteros): lista con las ubicaciones de las instancias encontradas.
    """
    
    indices = []
    offset = -1
    while True:
        try:
            offset = words.index(word, offset+1)
        except ValueError:
            return indices
        indices.append(offset)
    
    return(indices)

def get_coocurrencies(indices_term1, indices_term2, window):

    """
    Rastrea la matriz de índices en busca de co-ocurrencias de parejas de palabras dentro de una ventana.

    PARÁMETROS
    - indices_term1, indices_term2 (string): Pareja de terminos cuyas occurrencias se buscan
    - window (int): Distancia maxima entre las parejas de terminos, contados como número de palabras entre ellos.

    NOTA: Las coocurrencias se calcularán entre los términos del vocabulario (nodos del grafo), que, en general,
    sera una selección de las palabras del corpus. La ventana se refiere al número de palabras que separe los terminos
    en los documentos, independientemente de si estas palabras forman parte del vocabulario o no.
    
    """
    indices_term2_copy = indices_term2.copy()
    count = 0
    for index1 in indices_term1:
        #print("indices_term1", indices_term1)
        for index2 in indices_term2_copy:            
            #print("indices_term2", indices_term2)
            diff = abs(index1 - index2)
            #print(index1, index2, diff)
            if (diff <= window):
                count += 1
                # Eliminamos el término para no volverlo a contar si hay una segunda pareja cerca.
                indices_term2_copy.remove(index2)
               
    return count

def main():

    """
    REQUISITOS:
    - Módulo datetime
      >>> from datetime import datetime

    Véanse los requisitos de las funciones anteriores para otros modulos requeridos.

    """
    
    # PARÁMETROS DE ENTRADA
    
    input_folder, output_folder, window, tags = get_arguments()
    print("")
    print("La red se calculará utilizando los siguientes valores:")
    print("****************************************")
    print("Ruta de entrada: " + input_folder)
    print("Ruta de salida: " + output_folder)
    print("Ventana: " + str(window))
    print("Etiquetas aceptadas: " + str(tags))
    print("****************************************")


    # RUTA A LOS FICHEROS DE ENTRADA Y SALIDA
    
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_name = str(now) + "_Grafo_Ventana_" + str(window) + "_Etiquetas_" + str(tags) + ".txt"
    output_path = output_folder + output_name

    # TOKENS NO ACEPTADOS
    
    banned_tokens = ['<s>', '<f>']

    # IMPORTACIÓN DE LOS TEXTOS DEL CORPUS

    print("")
    print("Importando textos...")
	
    try: 
        titles, texts = get_documents(input_folder)
        n = len(texts)
    except:
        print("""!!! No se pudieron importar los textos. Asegurese de que la carpeta contiene ficheros en formato utf-8\n""")


    print(str(n) + " textos importados: ")
    print("****************************************")	
    for i in range(n):
        print("\'" + titles[i] + "\' \'" + texts[i][:50] +"...\'")
    print("****************************************")

    # GENERACIÓN DE LA LISTA DE LISTAS DE TOKENS DE LOS DOCUMENTOS Y DEL VOCABULARIO

    print("")
    print("""Conversión el corpus en una lista de documentos con los tokens en formato lista
y generación del vocabulario...""")
    
    # TEXTOS EN FORMATO LISTA: lista de listas, con las palabras que forman cada texto original
    texts_words = []

    # VOCABULARIO: lista de terminos únicos normalizados y truncados de todo el corpus
    vocabulary = []

    # TRATAMIENTO DE TEXTOS ORIGINALES
    for i in range(n):

        # EXTRACCIÓN DE TUPLAS (token, etiqueta) 
        try:
            tokens = get_tokens(texts[i])
        except:
            print("""No se pudieron importar las tuplas (token, etiqueta). Asegurese de que los textos
están etiquetados siguiendo el esquema término/etiqueta. Por ejemplo:

A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS
""")


        # NORMALIZACIÓN
        tokens = normalize(tokens, banned_tokens)

        # TRUNCADO
        tokens = stem(tokens)

        # FILTRADO POR CATEGORIAS
        words = filter_category(tokens)

        # UNIÓN A LA LISTA DE LISTAS
        texts_words.append(words)

        # TÉRMINOS A INCLUIR EN EL VOCABULARIO
        terms = filter_category(tokens, tags)     
               
        vocabulary = vocabulary + terms

        if (len(vocabulary) == 0):
            print(f"""El programa ha generado un vocabulario vacío. Asegurese de que los textos están etiquetados siguiendo el esquema término/etiqueta y de que existen términos con las etiquetas aceptadas.
Etiquetas aceptadas: {tags}.
Ejemplo de etiquetado correcto:
A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS
""")
            exit()
  
    vocabulary = list(set(vocabulary))
    vocabulary = list(filter(None, vocabulary))
    vocabulary.sort()
    m = len(vocabulary)

    print("Vocabulario generado: " + str(m) + " términos. Mostrando los 10 primeros: ")
    print("****************************************")
    for i in range(10):
        print(vocabulary[i])
    print("...")
    print("****************************************")

        
    # MATRIZ DE ÍNDICES m X n
    # Las filas son las palabras del vocabulario, y las columnas, los documentos del corpus. 
    # El elemento texts_indices[i][j] es la lista localizaciones del término i del vocabulario 
    # en el documento j del corpus

    print("")
    print("Generando matriz de índices...")

    texts_indices = [] 

    for i in range(m):
        words_indices = []
        for j in range(n):
            words_indices.append(indices(vocabulary[i], texts_words[j]))
        texts_indices.append(words_indices)

    print("Matriz de índices generada. Mostrando índices de los 10 primeros terminos en los 3 primeros documentos")
    print("****************************************")
    for i in range(10):
        print("Término " + str(i) + "(" + vocabulary[i] + "): " + str(texts_indices[i][:3]))
    print("****************************************")
    
    # CÓMPUTO DE CO-OCURRENCIAS E IMPRESIÓN DE RESULTADOS

    print("")
    print("Calculando e imprimiendo el grafo... ")

    # GENERACIÓN DEL FICHERO DE SALIDA

    with open(output_path, "w", encoding="utf-8") as output:

        output.write("*Vertices " + str(len(vocabulary)))
        output.write("\n")

        for i, t1 in enumerate(vocabulary):
            output.write(str(i+1) + " \"" + t1 + "\"")        
            output.write("\n")

        output.write("*Edges ")
        output.write("\n")

        num_edges = 0
        
        # Recorremos el vocabulario dos veces, para hallar todas las parejas de términos
        for i in range(m):

            for j in range(i+1, m):

                # Recorremos los documentos en busca de coocurrencias de las parejas de términos
                coocurrencies = 0
                for k in range(n):
                    coocurrencies += get_coocurrencies(texts_indices[i][k], texts_indices[j][k], window)

                # Si el número de co-ocurrencias es mayor que cero, incluimos el resultado

                if (coocurrencies !=0):
                    output.write(str(i+1) + " " + str(j+1) + " " + str(coocurrencies))
                    num_edges += 1
                    output.write("\n")

    print("Grafo generado")
    print("****************************************")
    print("Ruta del grafo: " + output_path)
    print("Número de vértices: " + str(len(vocabulary)))
    print("Número de enlaces: " + str(num_edges))

if __name__ == "__main__":

    main()

