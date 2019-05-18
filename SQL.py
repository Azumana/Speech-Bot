import pymysql
import pymysql.cursors


class sql:

    def __init__(self, data, dataTable, whereCol, whereVal):
        self.data = data
        self.dataTable = dataTable
        self.whereCol = whereCol
        self.whereVal = whereVal


    def selectRequest(self):

        connection = pymysql.connect(host='localhost',
                                     user='user',
                                     password='pass',
                                     db='database',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:

            with connection.cursor() as cursor:

                sqlListe = []
                for info in self.data:

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

                return sqlListe

        finally:
            connection.close()
