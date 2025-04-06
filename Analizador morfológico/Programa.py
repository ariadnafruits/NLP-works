#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import Counter
from importlib import reload #Python 3.6
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

reload(sys)  
#sys.setdefaultencoding('utf8')   #Not necessary in Python 3.6

#Lectura del fichero de texto
f = open ('texto.txt',encoding="utf-8")   # Modificado para codificación correcta del texto 
freqdist = nltk.FreqDist()
words=nltk.word_tokenize(f.read().lower())   # Modificado para que el texto esté en minúscula
fd = nltk.FreqDist(word.lower() for word in words)
fdf= fd.most_common(30)

print ('Palabras del texto ordenadas por frecuencia')
t=''
for w in fdf:
    t+='('+w[0]+','+str(w[1])+') '
print (t)


# ********** DICCIONARIO ************#

# Se han incluído aquí todas las partículas que no tienen flexión (preposiciones, conjunciones, abreviaturas, 
# algunos adverbios), así como algunos nombres y verbos irregulares que aparecían en el texto de entramiento
# Para los grupos cerrados o semicerrados de partículas (preposiciones, conjunciones, adverbios), se ha consultado
# el Manual de la Nueva Gramática de la Lengua Española (RAE 2010)  y se han incorporado todas las más usuales.

dict ={}

dict['computadora']='NCFS'
dict['es']='VMIP3S'
dict['que']='PRON'
dict['y']='CONJ'
dict['para']='PREP'
dict['en']='PREP'
dict['a']='PREP'
dict['de']='PREP'
dict['salida']='NCFS'
dict['.']='PUNT'
dict['o']='CONJ'
dict['sistema']='NCMS'
dict['por']='PREP'
dict[',']='PUNT'
dict['como']='CONJ'
dict['autómata']='NCMS'
dict['más']='ADV'
dict['material']='NCMS'
dict['sobre']='PREP'
dict['permite']='VMIP3S'
dict[';']='PUNT'
dict['partes']='NCFP'
dict[':']='PUNT'
dict['computadoras']='NCFP'
dict['dispositivo']='NCMS'
dict['etc.']='ABRV'
dict['al']='PREP+ART'
dict['gestión']='NCFS'
dict['bases']='NCFP'
dict['informática']='NCFS'
dict['cables']='NCMP'
dict['e']='CONJ'
dict['conoce']='VMIP3S'
dict['comprende']='VMIP3S'
dict['son']='VMIP3P'
dict['entre']='PREP'
dict['hace']='VMIP3S'
dict['(']='PUNT'
dict['u']='CONJ'
dict[')']='PUNT'
dict['envía']='VMIP3S'
dict['ejecuta']='VMIP3S'
dict['cpu']='NCFS'
dict['dispositivos']='NCMP'
dict['interpreta']='VMIP3S'
dict['programa']='NCMS'
dict['mediante']='PREP'
dict['del']='PREP+ART'
dict['han']='VAIP3P'
dict['estado']='VAP0MS'
dict['desde']='PREP'
dict['ha']='VAIP3S'
dict['primeros']='NUM'
dict['pero']='CONJ'
dict['sigue']='VMIP3S'
dict['misma']='ADJ'
dict['bajo']='PREP'
dict['controla']='VMIP3S'
dict['está']='VAIP3S'
dict['con']='PREP'
dict['directa']='ADJ'
dict['escritas']='VMP0FP'
dict['fuente']='NCFS'
dict['le']='PRON'
dict['líneas']='NCFP'
dict['dicho']='VMP0MS'
dict[' ']='PUNT'
dict['   ']='PUNT'
dict['-']='PUNT'
dict['!']='PUNT'
dict['¡']='PUNT'
dict['¿']='PUNT'
dict['...']='PUNT'
dict['"']='PUNT'
dict['abajo']='ADV'
dict['acaso']='ADV'
dict['adelante']='ADV'
dict['adentro']='ADV'
dict['afuera']='ADV'
dict['ahí']='ADV'
dict['ahora']='ADV'
dict['algo']='PRON'
dict['alguien']='PRON'
dict['allá']='ADV'
dict['allí']='ADV'
dict['ante']='PREP'
dict['antes']='ADV'
dict['aquí']='ADV'
dict['arriba']='ADV'
dict['así']='ADV'
dict['atrás']='ADV'
dict['aunque']='CONJ'
dict['bastantes']='DET'
dict['bien']='ADV'
dict['cabe']='VMIPES'
dict['cada']='DET'
dict['cerca']='ADV'
dict['cómo']='PRON'
dict['conque']='CONJ'
dict['contra']='PREP'
dict['cuando']='CONJ'
dict['cuánta']='PRON'
dict['cuanto']='PRON'
dict['debajo']='ADV'
dict['delante']='ADV'
dict['demás']='PRON'
dict['demasiado']='ADV'
dict['dentro']='ADV'
dict['después']='ADV'
dict['detrás']='ADV'
dict['donde']='PRON'
dict['durante']='PREP'
dict['él']='PRON'
dict['encima']='ADV'
dict['enseguida']='ADV'
dict['entonces']='ADV'
dict['fuera']='ADV'
dict['hacia']='PREP'
dict['hasta']='PREP'
dict['hoy']='ADV'
dict['incluso']='ADV'
dict['lejos']='ADV'
dict['mal']='ADV'
dict['mañana']='ADV'
dict['mas']='CONJ'
dict['mí']='PRON'
dict['mucho']='ADV'
dict['nada']='PRON'
dict['nadie']='PRON'
dict['ni']='CONJ'
dict['no']='ADV'
dict['nunca']='ADV'
dict['poco']='ADV'
dict['porque']='CONJ'
dict['pronto']='ADV'
dict['qué']='PRON'
dict['quien']='PRON'
dict['quienes']='PRON'
dict['quizá']='ADV'
dict['salvo']='PREP'
dict['según']='PREP'
dict['si']='CONJ'
dict['sí']='ADV'
dict['siempre']='ADV'
dict['sin']='PREP'
dict['sino']='CONJ'
dict['también']='ADV'
dict['tan']='ADV'
dict['tanto']='ADV'
dict['temprano']='ADV'
dict['tras']='PREP'
dict['tú']='PRON'
dict['uno']='PRON'
dict['versus']='PREP'
dict['yo']='PRON'
dict['menos']='ADV'
dict['eso']='PRON'

dict['entrada/salida']='NCFP' # Aunque no sea exactamente asi, preferimos que el sistema lo etiquete así.

#SINGULARES Y PLURALES de palabras que aparecen en el texto de entrenamiento
dict['salidas']='NCFP'
dict['sistemas']='NCMP'
dict['autómatas']='NCMP'
dict['materiales']='NCMP'
dict['base']='NCCS'
dict['dato']='NCMS'
dict['parte']='NCFS'
dict['fuentes']='NCFP'
dict['cable']='NCMS'
dict['interpretan']='VMIP3P'
dict['programas']='NCMP'
dict['dispositivos']='NCMP' #para excluirlo de la regla ADJ -ivo(s)
dict['estados']='NCMP'

#FIN DICCIONARIO#


# ************ EXPRESIONES REGULARES ************#

p=[

#PALABRAS COMPLETAS flexionadas# (se consideran únicamente las que aparecen en el texto de entrenamiento)
################################
#Se presentan ordenadas por categorías (al ser reglas específicas para palabras completas, el orden no es importante, mientras estén antes que las reglas más genéricas)

#Determinantes (artículos)
(r'\b(el|l[ao]s?)?$','ART'),  #el

#Determinantes (otros)
#demostrativos
(r'\best?[eao]?s?$','DET'),  #este, ese
(r'\baquel(l[ao]s?)?$','DET'),  #aquella, aquellas, aquellos (aceptará aquela,etc.)


#indefinidos
(r'\bun[a]?(os|s)?$','DET'),  #un
(r'\balg[uú]n[a]?(os|s)?$','DET'),  #algún (aceptará "algun")
(r'\bning[uú]n[a]?(os|s)?$','DET'),  #ningún (aceptará "ningun")
(r'\btod[oa]s?$','DET'),  #todo
(r'\botr[oa]s?$','DET'),  #otro
(r'\bmuch[oa]s?$','DET'),  #mucho (Ídem)
(r'\bpoc[oa]s?$','DET'),  #poco (Ídem)
(r'\btant[oa]s?$','DET'),  #tanto (Ídem)
(r'\bvari[oa]s$','DET'),  #varias, varios (Nótese que esta forma no tiene singular) 
(r'\bamb[oa]s$','DET'),  #ambos
(r'\bbastantes?$','DET'),  #bastante
(r'\bciert[oa]s?$','DET'),  #cierto
(r'\bcual(es)?quiera?$','DET'),  #cualquier
(r'\bdemasiad[oa]s?$','DET'),  #demasiado (la forma masculina presente coincide en forma con el adverbio "demasiado", de categoría prioritaria (se incluye en el diccionario)
(r'\bescas[oa]s?$','DET'),  #escaso
(r'\bsendo[oa]s?$','DET'),  #
(r'\btal(es)?$','DET'),  #
(r'\bbastantes?$','DET'),  #



#posesivos
(r'\bmis?$','DET'),  #mi mis
(r'\b[ts]us?$','DET'),  #su sus tus sus
(r'\b[nv]uestr[oa]s?$','DET'),  #nuestro vuestro

#Numerales
(r'\b[0-9]+\.?$','NUM'),  #números del cero al 99999... (en cifras) Se incluye la posibilidad que, trás la cifra, haya un número.
(r'\b(((diez)|((on|do|tre|cator|quin|)ce)|((dieci)(séis|siete|ocho|nueve)))|(((veint[ei])|((trein|cuaren|cincuen|sesen|seten|ochen|noven)ta(\sy\s)?)))?([uú]n[oa]?|d[oó]s|tr[eé]s|cuatro|cinco|s[eé]is|siete|ocho|nueve)?)$','NUM'),  #cardinales del uno al noventa y nueve (en texto). Para el "uno" se acepta también la versión apocopada "un". Las versiones ortográficamente incorrectas veintiúno y veintiúna también se aceptan. La palabra "uno" se ha incluído en el diccionario como pronombre.
(r'\b((primer|tercer)|(primer|segund|tercer|cuart|quint|sext|sépt|octav|noven|décim|undécim|duodécim)[oa]s?)$','NUM'),  #Ordinales del primero al duodécimo. Para el singular masculino de "primero" y "tercero", se añaden las formas apocopadas "primer" y "tercer".


#Pronombres
#personales
(r'\bell[ao]s?$','PRON'),  #personales ella  ellos ellas
(r'\b[nv](osotr)[oa]s$','PRON'),  #personales nosotros/as vosotros/as 
(r'\busted(es)?$','PRON'),  #personales usted, ustedes
(r'\b[mtls]es?$','PRON'),  #personales átonos (clíticos) me te le se (aceptará "ses")
(r'\b[nv]?os$','PRON'),  #personales átonos (clíticos) nos os

#demostrativos
(r'\best?[eao]?s?$','PRON'),  #este,ese,... Como también son determinantes y estos tienen prioridad (se han incluído antes), esta regla no será tenida en cuenta.
(r'\baquell[ao]s?$','PRON'),  #aquella, aquellas Ídem.

#relativos
(r'\bcual(es)?$','PRON'),  #cual cuales
(r'\bcuy[oa]s?$','PRON'),  #cuyo cuyas ...


#r'\balgun[oa]s?$','PRON'),  #alguno (detrás de los determinantes indefinidos, para dar prioridad a estos)

(r'\b$','PRON'),   #plantilla para nuevas regex

#Abreviaturas
(r'\betc.?$','ABRV'),  #incluímos el punto opcional, por si algún analizador lo incluye (Freeling lo hace).
(r'\b$','ABRV'),  #plantilla para nuevas regex


#adjetivos terminados en sufijos característicos
#terminación .*[oa]s?
(r'\b.*(a|i)d[oa]s?$','ADJ'),  # -ado / -ido (integrado, interrelacionadas). En algunos casos, el participio correspondiente se ha incluído en el diccionario, de modo que sea elegido de forma prioritaria. El criterio se ha basado en la probabilidad de aparicíón de la palabra según Freeling, con algunas excepciones, en que nos hemos basado en el texto de entrenamiento.
(r'\b.*ic[oa]s?$','ADJ'),  #-ico (informático, electróni""co, eléctrico, electromecánicos, periféricos)
(r'\b.*iv[oa]s?$','ADJ'),  #-ivo (operativo)
#(r'\b.*ífic[oa]s?$','ADJ'),  #-ífico (específicas)
(r'\b.*XX[oa]s?$','ADJ'),  #-

#terminación .*(es)?
(r'\b.*al(es)?$','ADJ'),  #-al (digital, central, personal)
(r'\b.*XX(es)?$','ADJ'),  #-

#terminación .*s?
(r'\b.*antes?$','ADJ'),   #-ante (importante)
(r'\b.*ables?$','ADJ'),   #-able (interpretable, microprogramable, ejecutable)
(r'\b.*ibles?$','ADJ'),   #-ible (tangibles, intangible, posible, legible)
#(r'\b.*XXs?$','ADJ'),   #-XX

#otros adjetivos (se consideran únicamente los que aparecen en el texto de entrenamiento)
#flexión .*[oa]s?
(r'\bpequeñ[oa]s?$','ADJ'),
(r'\bextern[oa]s?$','ADJ'),
(r'\búltim[oa]s?$','ADJ'),
(r'\bnecesari[oa]s?$','ADJ'),
(r'\bmism[oa]s?$','ADJ'),
(r'\bhuman[oa]s?$','ADJ'),
(r'\bescas[oa]s?$','ADJ'),
(r'\bsol[oa]s?$','ADJ'),
(r'\bXXX[oa]s?$','ADJ'),  #plantilla para nuevas regex

#flexión .*(es)?
(r'\bútil(es)?$','ADJ'),  
(r'\bXXX(es)?$','ADJ'),  #plantilla para nuevas regex

#flexión .*s?
(r'\bconvenientes?$','ADJ'),
(r'\bimportantes?$','ADJ'),
(r'\bhuman[oa]s?$','ADJ'),
(r'\bXXXs?$','ADJ'),  #plantilla para nuevas regex

#Nombres
(r'\bware$','NCMS'),  #angicismos -ware (software,...)
(r'\bwares$','NCMP'),  

#Excepciones a reglas que se incluirán más abajo
(r'\b.*imagen$','NCMS'),  # imagen, contraimagen


#TERMINACIONES que se presentan con cierta regularidad#
#######################################################
#Se presentan ordenadas por prioridad de ejecución, de más específicas a más genéricas. Si tienen la misma prioridad, es decir, no se sustituyen entre ellas, se agrupan por categorías.

#adverbios
(r'.*mente$','ADV'),  #-mente

#verbos
#formas impersonales
(r'\b.*(a|e|i)r$','VMN'),  # infinitivos (almacenar, procesar)
(r'\b.*(a|ie)ndo$','VMG'),  # gerundios (haciendo) EXCEPCIONES: cuando,bando,blando,comando,doctorando,mando...)

#formas impersonales con pronombres enclíticos
(r'\b.*(a|e|i)r(([mts]e)|(l[aeo]s?)|(n?os))$','VMN+PRON'),  #infinitivos + pronombres #me, te, se, le, les, la, las, lo, los, nos, os
(r'\b.*(a|ie)ndo(([mts]e)|(l[aeo]s?)|(n?os))$','VMG+PRON'),  #gerundios #me, te, se, le, les, la, las, lo, los, nos, os
(r'\b.*(a|ie)ndo(([mts]e)|(l[aeo]s?)|(n?os))$','VMG+PRON'),  #gerundios #me, te, se, le, les, la, las, lo, los, nos, os

#Verbo Principal Indicativo Presente Tercera Singular
(r'\b.*ee$','VMIP3S'),  # -ee (lee)
(r'\b.*iza$','VMIP3S'),  # -iza (realiza)(hay muchos más verbos acabados en -izar que nombres acabados en -iza)
(r'\b.*ye$','VMIP3S'),  # -ye (incluye)
(r'\b.*iere$','VMIP3S'),  # -iere (requiere)
(r'\b.*iene$','VMIP3S'),  # -iene (única EXCEPCIÓN: higiene)
(r'\b.*ede$','VMIP3S'),  # -ede (única EXCEPCIÓN importante: sede)
(r'\b.*ebe$','VMIP3S'),  # -ebe (únicas EXCEPCIÓN plebe, percebe)
(r'\b.*ece$','VMIP3S'),  # -ece (únicas EXCEPCIÓN trece, contemplada más arriba)
(r'\b$','VMIP3S'),   #plantilla para nuevas regex


#Verbo Principal Indicativo Presente Tercera Plural
(r'\b.*[ae]n$','VMIP3P'),  # -an, -en (envían, fabrican, componen) (EXCEPCIONES IMPORTANTES: imagen, plan)
#(r'\b.*izan$','VMIP3P'),  # -izan (hay muchos más verbos acabados en -izar que nombres acabados en -iza
#(r'\b.*ten$','VMIP3P'),  # -ten (hay muchos más verbos acabados en -izar que nombres acabados en -iza
(r'\b$','VMIP3P'),   #plantilla para nuevas regex



#Nombres femeninos que no acaban en -a
(r'\b.*[cs]ión$','NCFS'),  #-ión (información, dimensión)
(r'\b.*[cs]iones$','NCFP'),  #-ciones -siones
(r'\b.*idad$','NCFS'),  #-idad (unidad)
(r'\b.*idades?$','NCFP'),  #-idades 
(r'\b.*[cr]ie$','NCFS'),  #-cie -rie superfície
(r'\b.*[cr]ies?$','NCFP'),  #-cies -ries


#REGLAS FINALES#
#######################################################
#Las palabras que no sigan las reglas anteriores y no estén en diccionario, se clasificarán como nombres, según las reglas finales.
(r'.*as$','NCFP'),
(r'.*s$','NCMP'),

#femenino singular
(r'.*a$','NCFS'),

#masculino singular
(r'.*$','NCMS'),

    ]

#FIN EXPRESIONES REGULARES#


rt=nltk.RegexpTagger(p)
taggedText=rt.tag(words)
for item in taggedText:
#   if dict.has_key(item[0]):   #has_key was removed in Python 3
    if item[0] in dict:         # use "in" instead
        print (item[0],' ',dict[item[0]])
    else:
        print (item[0]+' '+item[1])
    
sys.exit()
