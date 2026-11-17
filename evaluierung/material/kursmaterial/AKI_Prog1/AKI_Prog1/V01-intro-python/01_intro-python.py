#Automatically extracted from ./01_intro-python.md on 2026-09-29 07:07:56.326893 UTC



#-------------------------------------------------
#Definition von Variablen in einer Datei speichern
#-------------------------------------------------

#[./01_intro-python.md:327]
name = 'Stefan'



#---------------------------
#Funktionen selbst schreiben
#---------------------------

#[./01_intro-python.md:377]
def double(x):
    return x + x



#--------------------------------
#Funktionen mit mehreren Eingaben
#--------------------------------

#[./01_intro-python.md:394]
# Nur zur Übung definieren wir unsere eigene Additionsfunktion.
# Normalerweise benutzen wir natürlich weiterhin den + Operator.
def add(x, y):
    return x + y



#---------------------------------------
#Funktionen mit mehreren Zeilen im Rumpf
#---------------------------------------

#[./01_intro-python.md:420]
def double2(x):
    y = x + x
    return y



#--------------------------------
#`print` innerhalb von Funktionen
#--------------------------------

#[./01_intro-python.md:460]
def double3(x):
    y = x + x
    print('x = ' + str(x) + ', y = ' + str(y))
    return y



#-------------------------
#Spezialzeichen in Strings
#-------------------------

#[./01_intro-python.md:510]
print('Hello\n\'Stefan\'')


#[./01_intro-python.md:516]
print("Hello\n'Stefan'")



#-----------------
#Multiline Strings
#-----------------

#[./01_intro-python.md:536]
print("""Hello
'Stefan'""")



#-------------------------
#Noch mehr Zeilen im Rumpf
#-------------------------

#[./01_intro-python.md:550]
def double4(x):
    round(x)
    print('double4 mit Argument ' + str(x))
    y = double2(x)
    return y



#--------------------
#`print` vs. `return`
#--------------------

#[./01_intro-python.md:573]
def doubleFail(x):
    print(x + x)



#------------------------------------
#Funktionen und globale Variablen (1)
#------------------------------------

#[./01_intro-python.md:619]
PI = 3.14

def circleArea(r):
    area = PI * r * r
    return area



#------------------------------------
#Funktionen und globale Variablen (2)
#------------------------------------

#[./01_intro-python.md:634]
PI = 3.14

def circleAreaFail(r):
    PI = 0
    area =  PI * r * r
    return area

