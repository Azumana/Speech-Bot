import pymysql
import pymysql.cursors
import requests
from bs4 import BeautifulSoup


class sql:

    def __init__(self, data, dataTable, whereCol, whereVal):
        self.data = data
        self.dataTable = dataTable
        self.whereCol = whereCol
        self.whereVal = whereVal


    def selectRequest(self):

        connection = pymysql.connect(host='localhost',
                                     user='mcdb',
                                     password='marina',
                                     db='promodataia',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:

            with connection.cursor() as cursor:

                sqlListe = []
                print("type(self.data) = ", type(self.data))
                if type(self.data) != str:
                    for info in self.data:

                        if info == "horoscope":
                            info = "astro"

                        if self.whereVal == "NULL":
                            sqlRequest = """SELECT `%s` FROM `%s`""" % (info, self.dataTable)
                        else:
                            sqlRequest = """SELECT `%s` FROM `%s` WHERE `%s` = '%s'""" % (info,
                                                                                          self.dataTable,
                                                                                          self.whereCol,
                                                                                          self.whereVal)
                    cursor.execute(sqlRequest)
                    dataList = cursor.fetchall()

                    for elt in dataList:
                        sqlListe.append(elt[info])

                else:

                    if self.data == "horoscope":
                        self.data = "astro"

                    if self.whereVal == "NULL":
                        sqlRequest = """SELECT `%s` FROM `%s`""" % (self.data, self.dataTable)
                    else:
                        sqlRequest = """SELECT `%s` FROM `%s` WHERE `%s` = '%s'""" % (self.data,
                                                                                      self.dataTable,
                                                                                      self.whereCol,
                                                                                      self.whereVal)

                    cursor.execute(sqlRequest)
                    dataList = cursor.fetchall()

                    for elt in dataList:
                        sqlListe.append(elt[self.data])

                return sqlListe

        finally:
            connection.close()


    def getHoroscope(self):

        print("START")
        web = requests.get("https://www.20minutes.fr/horoscope/")
        page = BeautifulSoup(web.content, "html.parser")

        signe = page.find_all("h2", {"class": "titleblock-titles-title"})
        p = page.find_all("p", {"class": "mb2"})

        horoscope = {}

        for i, v in enumerate(signe):
            horoscope[signe[i].string.replace("Horoscope ", "").lower()] = p[i * 2].string + p[i * 2 + 1].string

        print("dico : ", horoscope)
        horoscope_perso = horoscope[str(self.selectRequest()).strip("[]'")]

        return horoscope_perso
