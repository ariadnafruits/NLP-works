#!/usr/bin/env python
# coding: utf-8


# IMPORTACIÓN DE LIBRERÍAS

import os 
import getopt, sys
import tkinter as tk
from tkinter import filedialog
import glob
import nltk
from nltk.stem import WordNetLemmatizer
import re
from datetime import datetime
import csv

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# ABRIR CARPETA  

def browse_directory():

    """
    Abre el navegador de archivos del cliente para que el usuario seleccione la carpeta
    dónde se ubican los ficheros de texto de los que hay que extraer palabras clave.

    REQUISITOS:
    * Módulo tkinter y filedialog:
     >>> import tkinter as tk
     >>> from tkinter import filedialog

    PARÁMETROS DE ENTRADA:
    Ninguno

    SALIDA:
    * Ruta del directorio
    
    """

    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root,initialdir="/",
                    title="""Seleccione la carpeta donde se encuentran los archivos""")

    return directory

def browse_file():

    """
    Abre el navegador de archivos del cliente para que el usuario seleccione el fichero
    de texto que contiene el grafo con los nodos del vocabulario del corpus y los pesos
    en formato Pajek.

    REQUISITOS:
    * Módulo tkinter y filedialog:
     >>> import tkinter as tk
     >>> from tkinter import filedialog

    PARÁMETROS DE ENTRADA:
    Ninguno

    SALIDA
    * Ruta del fichero
    
    """

    root = tk.Tk()
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Seleccione el fichero de texto que contiene el grafo",filetypes = (("text files","*.txt"),("text files","*.txt")))

    return filename

def get_arguments():

    """
    Asigna el valor de los parametros opcionales, leyendo primero los pasados por consola y
    preguntando explícitamente el resto o asignando los valores por defecto.
    """

    # DEFINICION DE ARGUMENTOS 

    input_folder = ""   
    input_graph = ""
    output_folder = ""
    window = ""
    tags =  ["NN", "NNS", "JJ", "JJR", "JJS"]    
    d = ""
    threshold = ""
    show_help = False

    # MENSAJE DE AYUDA
    
    help_message = """

AYUDA DE palabras_clave-lem.py
==================================================================================================

Este programa identifica las palabras clave de una colección de textos aplicando el metodo TextRank.
Los argumentos requeridos pueden proporcionarse contestando las preguntas una vez iniciado el programa
o directamente a través de la línea de comandos.

-h, --help: Consulta de la ayuda

-i --input_path: Ruta de la carpeta de los documentos a analizar. Si no se informa, el programa abrirá
el explorador de archivos.

Los documentos deben ser textos etiquetados con mediante el formalismo término/etiqueta. Por ejemplo:

A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS

Para obtener textos etiquetados en este formato, puede utilizarse el etiquetador de Standford:
http://nlp.stanford.edu/software/tagger.shtml.

-o, --output: Ruta de la carpeta donde se guardarán los archivos con las palabras clave. Si no se informa
el programa creará la carpeta “output” en el directorio donde se encuentre el fichero palabras_clave-lem.py
y los guardará allí.

-g, --graph: Ruta del fichero donde se encuentra el fichero de texto en formato Pajek con los pesos de los
enlaces.
					
-w, --window: Ventana de co-ocurrencia. Debe ser un número entero. El programa lo utilizará para definir la
ventana de términos máxima que debe darse entre una pareja de términos para que se considere que co-ocurren.
Se recomienda, por coherencia, utilizar el mismo valor de la ventana de términos, aunque no es obligatorio.                                      

-d, --damp: Factor de corrección (damping factor). Debe ser un número entre 0 y 1, sin incluir el 0. En
[Mihalcea 2004] se recomienda asignar d = 0,85.

-l, --threshold: Límite de convergencia (threshold). Debe ser un número decimal. En [Mihalcea 2004] se asigna
l = 0,0001. 

-t, --tags: Listado de etiquetas del Penn Treebank [Marcus 1993] aceptadas como nodos del grafo. Por ejemplo: 
["NN", "NNS", "JJ", "JJR", "JJS"].
Si no se informa, o si se informa con la cadena “all”,  se incluirán todas las etiquetas (no se filtrará).
Las etiquetas del Penn Treebank pueden consultarse en:
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html.
Es importante filtrar, como mínimo, por las mismas etiquetas con que se han filtrado los términos del grafo de pesos,
ya que si se aceptan más categorías que allí habrá términos inexistentes en el grafo y el programa generará un error. 

	"""
    
    # RASTREO DE ARGUMENTOS PASADOS POR CONSOLA

    print("")

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "hi:g:o:w:t:d:l:"
    long_options = ["help", "input_folder=", "input_graph=", "output_folder=", "window=", "tags=" "damp=", "threshold="]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)
    
    for argument, value in arguments:
        
        if argument in ("-h", "--help"):
            show_help = True
        elif argument in ("-i", "--input_folder"):
            input_folder = value        
        elif argument in ("-g", "--input_graph"):
            input_graph = value        
        elif argument in ("-o", "--output_folder"):
            output_folder = value        
        elif argument in ("-w", "--window"):
            window = int(value)       
        elif argument in ("-t", "--tags"):
            tags = value         
        elif argument in ("-d", "--damp"):
            d = float(value)          
        elif argument in ("-l", "--threshold"):
            threshold = float(value)  

    if (show_help == True):
        print(help_message)
        sys.exit()
    else:
        if (input_folder == ""):
            input_folder = browse_directory()
        if (input_graph == ""):
            input_graph = browse_file()
        if (output_folder == ""):
            output_folder = "./output"
        elif (not output_folder.endswith(('/', '\\'))):
              output_folder = output_folder + "/"
        if (window == ""):
            window = int(input("Ventana de términos para considerar co-ocurrencia: "))
        if (tags == ""):
            tags = ["NN", "NNS", "JJ", "JJR", "JJS"]
        if (d == ""):
            d = float(input("Factor de corrección d: "))
        if (threshold == ""):
            threshold = float(input("Límite de convergencia (threshold) l: "))
    		
    return input_folder, input_graph, output_folder, window, tags, d, threshold
                
def get_weights(filename):

    """
    Importa un grafo en formato Pajek y extrae el vocabulario y los pesos de los enlaces.

    PARÁMETROS:
    - filename (str): fichero con el grafo en formato Pajek.

    SALIDA
    - vocabulary (list of strings): Lista con los términos del vocabulario. El índice del termino en la lista
    se corresponde con la numeración asignada en el grafo original, menos uno (ya que en formato Pajek los
    nodos se empiezan a numerar por 1, y las listas de Python, por 0).
    - N (int): Número de términos del vocabulario
    - weights (dict): Ddiccionario cuyas claves son 2-tuplas indicando enlaces entre vértices, y cuyos
    valores son el peso del enlace correspondiente.
    """

    with open(filename, 'r') as file:
        graph = file.readlines()
        graph = [line.rstrip('\n') for line in graph]

        for i in range(len(graph)):
            line = graph[i]
            if "*Vertices" in line:
                N = int(line.split()[1])
                vertices_start = i + 1
            if "*Edges" in line:
                edges_start = i + 1
                break
            
        vocabulary = [""] * N
        
        for i in range (vertices_start, vertices_start + N):
            term = graph[i]. split()
            vocabulary[int(term[0])-1] = term[1].replace("\"", "")

        weights = {}
             
        for i in range(edges_start, len(graph)): 
            edge = graph[i].split()
            edge = [int(x) for x in edge]
            weights[(edge[0]-1, edge[1]-1)] = edge[2]
            
        return(N, vocabulary, weights)
    
def get_documents(input_folder):
    
    """
    Crea una lista de textos completos en formato original a partir de los ficheros de la carpeta de entrada.
    
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
        title = file.replace(input_folder, '')      
        #print(title)
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


def lemmatize(tokens):

    """
    Lematiza los tokens utilizando la libreria WordNetLemmatizer.

    REQUISITOS:
    - librería nltk
      >>> import nltk

    PARAMETROS
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) normalizada
    
    SALIDA
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) con los tokens lematizados.
    """
      
    wnl = WordNetLemmatizer()
      
    for i in range(len(tokens)):
        tokens[i] = (wnl.lemmatize(tokens[i][0]), tokens[i][1])
        
    return tokens

def filter_category(tokens, tags="all"):

    """
    Filtra una lista de tuplas (token, etiqueta) según las etiquetas permitidas.

    PARAMETROS
    - tokens (lista de 2-tuplas (string, string)): Lista de tuplas (token, etiqueta) truncada
    - tags (lista de cadenas): lista de etiquetas del Penn Treebank permitidas.
      Ej: ['NN', 'NNS', 'JJ', 'JJR', 'JJS']
      Si en lugar de una lista, se informa con la cadena "all", se incluirán todas las etiquetas (no se filtrará).
    SALIDA
    - terms (lista de strings): Lista de términos filtrados por categoría.
    """
    
    if (tags == "all"):
        terms = [t[0] for t in tokens]

    else:
        terms = [t[0] for t in tokens if t[1] in tags]
    
    return terms

def words_to_numbers(words, vocabulary):

    """

    PARÁMETROS:
    - words (list): Lista de términos de un documento.
    - vocabulary: Lista con los términos únicos del vocabulario, con índice igual al valor del nodo
    asignado en el grafo del vocabulario original, menos uno.
    """

    numbers = []
    
    for i, word in enumerate(words):
        
        number = word.replace(word, str(vocabulary.index(word)))
        number = int(number)
        numbers.append(number)

    return(numbers)

def number_to_word(number, vocabulary):

    """
    PARÁMETROS:
    - number (int): Número del vértice a convertir
    - vocabulary (list): Lista con los términos únicos del vocabulario, con índice igual al valor del nodo
    asignado en el grafo del vocabulario original, menos uno.
    """

    word = vocabulary[number]

    return(word)

def get_pairs(numbers, window):
    
    """
    Obtiene un listado con las parejas de nodos que coocurren dentro de una ventana

    PARAMETROS
    - numbers  (list): Lista de nodos ordenados según se presentan en el documento a analizar.
    - window (int): Tamaño de la ventana de términos.

    SALIDA:
    - nodes (lista de enteros): Lista de vértices únicos presentes en el texto
    - pairs (lista de 2-tuplas): Parejas de términos
    """

    nodes = list(set(numbers))
    nodes.sort()
    
    pairs = []
    
    for i, number in enumerate(numbers):  # CANVI
        for j in range(i+1, i+window):
            if j >= len(numbers):
                break
            pair = (number, numbers[j])
            if pair not in pairs:
                pairs.append(pair)

    return(nodes, pairs)


            
def get_scores(nodes, pairs, N, vocabulary, weights, d, threshold):

    """
    Obtiene el listado de puntuaciones para cada término de un texto segun el algoritmo TextRank con pesos.

    PARÁMETROS
    - nodes (lista de enteros): lista de nodos únicos del documento
    - pairs (lista de 2-tuplas): Lista con las parejas de nodos que coocurren en el texto
    - N (int): Número de nodos del vocabulario global.
    - vocabulary (list): nodos del vocabulario global.
    - weigths (dict): Diccionario cuyas claves son 2-tuplas con las parejas de nodos del vocabulario 
    con enlace, y el peso de dicho enlace.
    - d (float): Factor de correccion ("damping factor")
    - threshold (float): Límite de convergencia

    SALIDA:
    - WS (diccionario): Diccionario cuyas claves son los nodos del texto y cuyo valor, la puntuación obtenida
    aplicando el algoritmo TextRank con pesos ("Weighted Score").
    """

    # VÉRTICES
    
    m = len(nodes)

    # PESOS
    
    edges_out = [""] * m # Para cada vértice i, enlaces del tipo (i, j)
    edges_in = [""] * m  # Para cada vértice i, enlaces del tipo (j, i)
    edges = [""] * m
    
    # Suma de los pesos de los enlaces de cada vértice
    W = [0] * m 

    for v in range(0, m):
        edges_out[v] = [edge for edge in pairs if (edge[0]==nodes[v] and edge in weights)]  # Si el enlace no esta en el grafo, lo obviamos. 
        edges_in[v] = [edge for edge in pairs if (edge[1]==nodes[v] and edge in weights)]  # Si el enlace no esta en el grafo, lo obviamos. 
        edges[v] = edges_out[v] + edges_in[v]
        edges_weights = [weights[edge] for edge in edges[v] if edge in weights]
        weigths_sum = sum(edges_weights)
        W[v] = weigths_sum
    
    # Puntuaciones de cada vértice
    WS = [1] * m
    WS_new = [0] * m
    previous = 0

    
    # Iteraciones 
    print("")
    print("Cálculo de puntuaciones: iteraciones TextRank...")
    i = 0

    while (abs(previous - sum(WS)) > threshold):
        i += 1
        previous = sum(WS)
        for v in range(0, m):

            score = 0
            for v1, v2 in edges_out[v]:            
                WS_v2 = WS[nodes.index(v2)] # Puntuacion ponderada del nodo v2
                W_v2 = W[nodes.index(v2)] # Suma de los pesos de los enlaces de v2                
                score += WS_v2 * (weights[(v1,v2)]) / W_v2
            for (v2, v1) in edges_in[v]:            
                WS_v2 = WS[nodes.index(v2)]             
                W_v2 = W[nodes.index(v2)] 
                score += WS_v2 * (weights[(v2,v1)]) / W_v2        
            score = (1 - d) + d * score
            WS_new[v] = score

        WS = WS_new

    print("")
    print("Suma de puntuaciones final: ", sum(WS), "; Diferencia: ", abs(previous - sum(WS)), "; Threshold: " ,
            threshold, "; Verdad: ", (abs(previous - sum(WS)) > threshold), "Número de iteraciones:", i)
    
    summary = [sum(WS), abs(previous - sum(WS)), i]
    
    return WS, summary

def get_keynodes(WS):

    """
    Obtiene el listado de nodos con mayor puntuación, ordenado por puntuacion descendente.
    
    PARÁMETROS
    - WS (dict): Diccionario con las puntuaciones de los nodos.

    SALIDA:
    - keynodes (dict): Diccionario anterior, filtrado por los nodos que han obtenido mayor puntuación, ordenados
    por puntuación descendente
    """

    num_keynodes = int(len(WS) / 20)

    if num_keynodes < 5:
        num_keynodes = 5
    elif num_keynodes > 20:
        num_keynodes = 20

    WS_sorted = WS.copy()
    WS_sorted.sort(reverse = True)
    min_keynode = WS_sorted[num_keynodes]

    keynodes = {i: WS[i] for i in range(len(WS)) if WS[i] >= min_keynode}
    
    keynodes = {k: v for k, v in sorted(keynodes.items(), key=lambda item: item[1], reverse=True)}
  
    return keynodes

def create_folder (folder):
        
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
        except: 
            print("No se ha podido crear el la carpeta" + folder)
        else:
            print("Se ha creado la carpeta " + folder)

def export_keywords (title, output_folder, keywords, summary):
    
    output_name = title + ".result"

    with open(output_folder + output_name, 'w', encoding="utf-8") as output:
        for key, value in keywords.items():
            output.write(key + " " + str(value))
            output.write("\n")

    with open(output_folder + "summary.csv", 'a+') as summ:
        wr = csv.writer(summ, quoting=csv.QUOTE_ALL)
        wr.writerow(summary)
     
    print("Palabras clave almacenadas en el fichero: ", output_folder + output_name)

            
def main():

    """
    REQUISITOS:
    - Módulo datetime
      >>> from datetime import datetime

    Véanse los requisitos de las funciones anteriores para otros modulos requeridos.

    """
    
    # PARÁMETROS DE ENTRADA
    
    input_folder, input_graph, output_folder, window, tags, d, threshold = get_arguments()
    print("")
    print("La red se calculará utilizando los siguientes valores:")
    print("****************************************")
    print("Ruta de los documentos a analizar: " + input_folder)
    print("Fichero con el grafo de entrada: " + input_graph)
    print("Ruta de salida: " + output_folder)
    print("Ventana de terminos para considerar co-ocurrencia: " + str(window))
    print("Etiquetas aceptadas: " + str(tags))
    print("Factor de correccion: " + str(d))
    print("Límite de convergencia (threshold) l: " + str(threshold))
    print("****************************************")

    print("")
    input("Pulsa enter para continuar")

    # CREACIÓN DE LA CARPETA Y EL FICHERO SUMMARY.CSV, DONDE SE ESCRIBIRÁ LA INFORMACIÓN RESUMEN DE TEXTRANK
    create_folder(output_folder)

    with open(output_folder + "summary.csv", 'w+') as summ:
        wr = csv.writer(summ, quoting=csv.QUOTE_ALL)
        wr.writerow(["Fichero de entrada", "Fichero de salida", "Ventana", "Factor de amortiguacion", "Límite de convergencia", "Suma de puntuaciones", "Convergencia", "Número de iteraciones"])    

    # VOCABULARIO Y PESOS DE LOS ENLACES

    print("")
    print("Extrayendo el vocabulario y el peso de los enlaces...")
    print("")
    
    N, vocabulary, weights = get_weights(input_graph)

    print("")
    print("Datos del grafo del grafo importado:")
    print("****************************************")
    print("Número de nodos:", len(vocabulary))
    print("Número de enlaces:", len(weights))

    print("")
    input("Pulsa enter para continuar")
    
    # TOKENS NO ACEPTADOS
    
    banned_tokens = ['<s>', '<f>']

    # IMPORTACIÓN DE LOS DOCUMENTOS DE LOS QUE EXTRAER PALABRAS CLAVE

    print("")
    print("Importando textos...")
    print("")
	
    try: 
        titles, texts = get_documents(input_folder)
        n = len(texts)
    except:
        print("""!!! No se pudieron importar los textos. Asegurese de que la carpeta contiene ficheros en formato utf-8\n""")


    print(str(n) + " textos importados: ")
    print("****************************************")	
    for i in range(n):
        print("\'" + "Documento" + str(i) + ": " + titles[i] + "\' \'" + texts[i][:50] +"...\'")
    print("****************************************")

    print("")
    input("Pulsa enter para continuar")

    # GENERACIÓN DE LA LISTA DE LISTAS DE TOKENS DE LOS DOCUMENTOS 

    print("")
    print("""Normalización de textos y calculo de palabras clave...""")
    print("")
    print("****************************************")
    
    # TEXTOS EN FORMATO LISTA: lista de listas, con las palabras que forman cada texto original
    texts_pairs = []

    # TRATAMIENTO DE TEXTOS ORIGINALES
    for i in range(n):

        print("")
        print("TEXTO", i, ":", titles[i])
        print("")

        # EXTRACCIÓN DE TUPLAS (token, etiqueta) 
        try:
            tokens = get_tokens(texts[i])
        except:
            print("""No se pudieron importar las tuplas (token, etiqueta). Asegurese de que el texto esta 
etiquetado siguiendo el esquema término/etiqueta. Por ejemplo:

A/DT challenging/JJ problem/NN faced/VBN by/IN researchers/NNS and/CC developers/NNS
""")

        # NORMALIZACIÓN
        tokens = normalize(tokens, banned_tokens)

        # LEMATIZADO
        tokens = lemmatize(tokens)
      
        # FILTRADO POR CATEGORIAS Y ELEMENTOS NO VACÍOS
        words = filter_category(tokens, tags) # ATENCIÓN: CRITERIO DISTINTO AL EJERCICIO ANTERIOR: AHORA LA VENTANA NO TIENE EN CUENTA TÉRMINOS DE LAS CATEGORIAS DESCARTADAS.
        words = list(filter(None, words))

        print("Documento normalizado y filtrado:", [[word for word in words[0 : window + 2]] + ["  ...  "] + [word for word in words[len(words)-window-1:len(words)]]])

        # CONVERSIÓN DE TÉRMINOS A VERTICES, SEGÚN NUMERACIÓN DEL GRAFO

        numbers = words_to_numbers(words, vocabulary)

        print("")
        print("Nodos ordenados del documento: (", len(numbers), "en total)", i, ":", [[number for number in numbers[0 : window + 2]] + ["  ...  "] + [number for number in numbers[len(numbers)-window-1:len(numbers)]]])

        # EXTRACCIÓN DE PAREJAS DE TOKENS QUE CO-OCURREN DENTRO DE UNA VENTANA
        nodes, pairs = get_pairs(numbers, window)

        #print("Número de nodos únicos:", len (nodes))

        print("")
        print("Nodos únicos del documento: (", len(nodes), "en total)", i, ":", [[node for node in nodes[0 : window + 2]] + ["  ...  "] + [node for node in nodes[len(nodes)-window-1:len(nodes)]]])
        print("")
        print("Parejas del documento:", [[pair for pair in pairs[0 : window * 2]] + ["  ...  "] + [pair for pair in pairs[len(pairs) - window * 2: len(pairs)]]])

        # CÁLCULO DE PUNTUACIONES SEGUN EL ALGORITMO TEXTRANK
        WS, summary = get_scores(nodes, pairs, N, vocabulary, weights, d, threshold)
        summary = [titles[i], titles[i] + ".result", window, d, threshold] + summary

        # EXTRACCIÓN DE PALABRAS CLAVE
        keynodes = get_keynodes(WS)
                    
        keywords = {number_to_word(nodes[i], vocabulary):keynodes[i] for i in keynodes}
            
        print("Palabras clave: ", keywords)   
    
        export_keywords(titles[i], output_folder, keywords, summary)              

        print("________________________")

    print("Identificación de palabras clave finalizada")
    print("Ruta de los archivos con las palabras clave:", output_folder)
    print("Resumen de ejecucion:", output_folder + "/summary.csv")

if __name__ == "__main__":

    main()

