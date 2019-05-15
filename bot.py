import pymysql
import pymysql.cursors
import random

def OpenJson(arg):
    with open(arg, "r") as file:
        myFile = json.load(file)
        return myFile[arg]

GREETING_INPUTS = ("bonjour", "salut", "yo", "salutations", "sup","hey",)
GREETING_RESPONSES = ["Bonjour", "Yo", "Salut!", "Salutations", "hey"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

dico = {OpenJson()}

def ditSImotRECONNU(motaCHERCHER):

    for cles, valeurs in dico.items():
        for mots in valeurs:
            if motaCHERCHER == mots:
                return True

def donnelemotCLEF(motaCHERCHER):

    for cles, valeurs in dico.items():
        for mots in valeurs:
            if motaCHERCHER == mots:
                return cles


def makeListe(s):
    l = s.split()
    print(l)
    return l

def selectRequest(data, dataTable, whereCol = "NULL", whereVal = "NULL" ):

    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 password='pass',
                                 db='database',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:

        with connection.cursor() as cursor:
            if whereCol == "NULL":
                sql = """SELECT `%s` FROM `%s`""" % (data, dataTable)
            else:
                sql = """SELECT `%s` FROM `%s` WHERE `%s` = '%s'""" % (data, dataTable, whereCol, whereVal)
            cursor.execute(sql)
            dataList = cursor.fetchall()
            list = []
            for elt in dataList:
                list.append(elt[data])
            return list


    finally:
        connection.close()


#print("Bonjour! Je suis Bobot. Que veux tu savoir sur quelle personne?")

def bobot(question):
    requetesur = ""
    question = question
    #print(question)
    question = question.lower()
    ListeMots = makeListe(question)
    ListeInfosDemand = []
    ListeTypeInfosDemand = []
    CompteurdINFOS = 0

    if question != "q":
        for mot in ListeMots:
            if ditSImotRECONNU(mot) == True:
                paramrequet = donnelemotCLEF(mot)
                if paramrequet == "prenom":
                    nomintero = mot.capitalize()
                    #print(nomintero)

        for mot in ListeMots:
            if ditSImotRECONNU(mot) == True:
                paramrequet = donnelemotCLEF(mot)
                if paramrequet != "prenom":
                    CompteurdINFOS = CompteurdINFOS + 1
                    ListeTypeInfosDemand.append(paramrequet)
                    infosurNOM = selectRequest(paramrequet, "Students", "prenom", nomintero)
                    for i in infosurNOM:
                        ListeInfosDemand.append(i)

        # print(ListeInfosDemand)
        # print(ListeTypeInfosDemand)
        # print(CompteurdINFOS)
        ListeRepBOT = []
        for i in range(0 , CompteurdINFOS):
            RepBOT = "{}: {}".format(ListeTypeInfosDemand[i] , ListeInfosDemand[i])
            ListeRepBOT.append(RepBOT)
            # print(ListeRepBOT)
        StringRepBot = ", ".join(ListeRepBOT)
        # print(StringRepBot)

        if CompteurdINFOS <= 1:
            print("nomintero = ", nomintero)
            return "Tu as demandé {} info sur {}, la voici : ".format(CompteurdINFOS, nomintero) + StringRepBot
        else:
            return "Tu as demandé {} infos sur {}, les voici : ".format(CompteurdINFOS, nomintero) + StringRepBot

    else:
        return "Ciao"

#bobot("nory telephone")