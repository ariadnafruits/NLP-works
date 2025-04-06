#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk import load_parser

cp = load_parser('gramatica_base.fcfg')


infile = open('textosTest.txt',encoding="utf-8")
# Mostramos por pantalla lo que leemos desde el fichero
for line in infile:
    print(line)
    try:
        tokens=line.split()
        trees = cp.parse(tokens)
        for tree in trees:
            print(tree)
    except ValueError as err:
        print('Frase no reconocida: ', line, 'Error: ',err)
infile.close()
    
