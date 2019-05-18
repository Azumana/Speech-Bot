import json
import random
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
    docDico = openjson("document.json")
    userDico = docDico["dico_1"]
    botDico = docDico["dico2"]

    for word in sentence.split():
        if word.lower() in userDico:

            for k, v in userDico.items():
                for w in v:
                    if word.lower() == w.lower():
                        botrep = random.choice(botDico[k])
                        return botrep


def getkeyword(word):
    """Use to find key word for sql request"""
    dico = getdico()
    for k, v in dico.items():
        for w in v:
            if word == w:
                return k


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
                namelist.append(word)
            elif keyword != "":
                keylist.append(keyword)

            if word == "son" or word == "leur":
                lastAnswer = memory.getLast().split()

        if len(namelist) == 0 or lastAnswer is not None:
            for name in lastAnswer:
                if getkeyword(name) == "prenom":
                    namelist.append(name)

        return getanswer(namelist, keylist, memory)

    else:
        return "Je n'ai pas compris ta demande."
