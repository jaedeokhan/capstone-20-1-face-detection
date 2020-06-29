import pymysql

def get_mysql():

    mydb = pymysql.connect(
        host="your ip",
        port=3306,
        user="your id",
        passwd="your passwd",
        db="your db name",
        charset='utf8'
    )
    mycursor = mydb.cursor()
    return mydb, mycursor