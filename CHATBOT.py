import json
import random
import difflib
import SQL


def openjson(arg):
    """Use to open json files"""
    with open(arg, "r") as file:
        myfile = json.load(file)
        return myfile


def getdico():
    """Use to get Chatbot SQL Key - key words values"""
    dico = openjson("chatbot_dico.json")
    return dico


def getconvers(sentence):
    """Use to get usual conversations"""
    docDico = openjson("conversation.json")
    userDico = docDico["dico_1"]
    botDico = docDico["dico2"]

    for word in sentence.split():
        if word.lower() in userDico:

            for k, v in userDico.items():
                for w in v:
                    if difflib.SequenceMatcher(None, w.lower(), word.lower()).ratio() > 0.8:
                    #if word.lower() == w.lower():
                        botrep = random.choice(botDico[k])
                        return botrep


def getkeyword(word):
    """Use to find key word for sql request"""
    dico = getdico()
    for k, v in dico.items():
        for w in v:
            if difflib.SequenceMatcher(None, w, word).ratio() > 0.8:
            #if word == w:
                return k


def getdiffword(word):
    dico = getdico()
    for k, v in dico.items():
        for w in v:
            if difflib.SequenceMatcher(None, w, word).ratio() > 0.8:
                return w


def createsql(colum, table, wherecol="Students", whereval="NULL"):
    """Use to create a sql object"""
    print("IN")
    sqlobject = SQL.sql(colum, table, wherecol, whereval)

    return sqlobject


def getsql(colum, table, wherecol="Students", whereval="NULL"):
    """Use to make a sql request"""
    sqlobject = SQL.sql(colum, table, wherecol, whereval)
    result = sqlobject.selectRequest()
    return result


def getanswer(name, info, memory):
    """Use to get a specific answer"""
    name = list(set([_ for _ in name if _ is not None]))
    info = list(set([_ for _ in info if _ is not None]))

    if len(name) == 0 and len(info) == 0:
        return "Je n'ai pas compris ta demande."

    elif len(name) != 0 and len(info) == 0:
        nlen = len(name)
        result = "Que veux-tu savoir sur "
        for n in name:
            nlen -= 1
            memory.name.append(name)
            if nlen > 1:
                result = result + n + ", "
            elif nlen == 1:
                result = result + n + " et "
            else:
                result = result + n + " ?"
        return result

    elif len(name) == 0 and len(info) != 0:
        ilen = len(info)
        result = "Sur qui veux-tu avoir les infos suivantes : "
        for i in info:
            ilen -= 1
            if info == 'astro':
                info = 'signe astrologique'
            memory.info.append(info)
            if ilen > 1:
                result = result + i + ", "
            elif ilen == 1:
                result = result + i + " et "
            else:
                result = result + i + " ?"
        return result

    else:
        nalen = len(name)
        inlen = len(info)
        if nalen == 1 and inlen == 1:
            sql = getsql(info, "Students", "prenom", name[0])
            print("info ! ", info)
            if info[0] == "horoscope":
                print("One !")
                objSQL = createsql(info[0], "Students", "prenom", name[0])
                result = "l'horoscope de " + name[0] + " est " + objSQL.getHoroscope()

            else:
                if info[0] == 'astro':
                    info[0] = 'signe astrologique'
                result = "le " + info[0] + " de " + name[0] + " est " + sql[0]
            memory.answer.append(result)
            return result

        else:
            result = ""
            for na in name:
                nalen -= 1

                sql = getsql(info, "Students", "prenom", na)
                count = 0

                for i in info:
                    inlen -= 1
                    record = sql[count]

                    if i == "horoscope":
                        print("new !")
                        objSQL = createsql(i, "Students", "prenom", na)
                        result = "l'horoscope de " + na + " est " + objSQL.getHoroscope()

                    else:
                        if i == 'astro':
                            i = 'signe astrologique'
                        result = result + "le " + i + " de " + na + " est "
                        if inlen > 1:
                            result = result + record + ", "
                        elif inlen == 1:
                            result = result + record + " et "
                        else:
                            result = result + record
                    count += 1

                if nalen > 1:
                    result = result + ", "
                elif nalen == 1:
                    result = result + " et "
                else:
                    result = result + ". "
            memory.answer.append(result)
            return result


def bobot(question, memory):
    """main function for chatbot code"""
    if question != "":

        if getconvers(question):
            return getconvers(question)

        qliste = question.lower().split()
        namelist = []
        keylist = []
        lastAnswer = None

        for word in qliste:

            keyword = getkeyword(word)
            if keyword == "prenom":
                namelist.append(getdiffword(word))
            elif keyword != "":
                keylist.append(keyword)

            if word == "l'horoscope" or word == "horoscope":
                keylist.append("horoscope")

            if word == "son" or word == "leur":
                lastAnswer = memory.getLast().split()

        if len(namelist) == 0 and lastAnswer is not None:
            for name in lastAnswer:
                if getkeyword(name) == "prenom":
                    namelist.append(name)

        if len(list(set([_ for _ in keylist if _ is not None]))) == 0 and len(namelist) != 0:
            for info in memory.getInfo():
                print("info : ", getkeyword(info))
                if getkeyword(info):
                    keylist.append(info)

        print(namelist, keylist, memory)
        return getanswer(namelist, keylist, memory)

    else:
        return "Je n'ai pas compris ta demande."


