
class connect(object):

    # 0=user,1=money

    def __init__(self, database, address, port="", user="", password="", data=""):
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        if database == "sqlite":
            import sqlite3
            self.conn = sqlite3.connect(address)
            self.cursor = self.conn.cursor()
        elif database == "mysql":
            import mysql.connector
            self.conn = mysql.connector.connect(host=address, port=int(port), user=user, password=password, database=data)
            self.cursor = self.conn.cursor()
        else:
            raise Exception("Database Not Selected")

    def close(self):
        self.conn.commit()
        self.conn.close()

    def init_database(self):
        self.cursor.execute("CREATE TABLE user (user text, money text)")
        self.cursor.execute("CREATE TABLE logs (from text, to text, money text)")
        self.conn.commit()
        return

    def get(self, user):
        user = str(user)
        if self.database == "sqlite":
            self.cursor.execute("select * from user where user=?", (user, ))
        else:
            self.cursor.execute("select * from user where user=%s", (user, ))
        values = self.cursor.fetchall()
        if len(values) < 1:
            raise Exception("Can't find user %s" % user)
        value = float(values[0][1])/100
        return value

    def new(self, user):
        user = str(user)
        if self.database == "sqlite":
            self.conn.execute(
                "insert into user (user, money) values (?,?)", (user, "000", ))
        else:
            self.cursor.execute(
                "insert into user (user, money) values (%s,%s)", (user, "000", ))
        self.conn.commit()
        return

    def income(self, user, money):
        user = str(user)
        money = str(money)
        if self.database == "sqlite":
            self.cursor.execute("select * from user where user=?", (user,))
        else:
            self.cursor.execute("select * from user where user=%s", (user,))
        values = self.cursor.fetchall()
        if len(values) < 1:
            raise Exception("Can't find user %s" % user)
        value = str(int(float(values[0][1])) + int(float(money)*100))
        if self.database == "sqlite":
            self.conn.execute("UPDATE user SET money=? WHERE user=?", (value, user,))
        else:
            self.cursor.execute("UPDATE user SET money=%s WHERE user=%s", (value, user,))
        if self.database == "sqlite":
            self.conn.execute("insert into user (from, to, money) values (?,?,?)", ("system", user, money ))
        else:
            self.conn.execute("insert into user (from, to, money) values (%s,%s,%s)", ("system", user, money ))
        self.conn.commit()
        return float(value)/100

    def expenditure(self, user, money):
        user = str(user)
        money = str(money)
        if self.database == "sqlite":
            self.cursor.execute("select * from user where user=?", (user, ))
        else:
            self.cursor.execute("select * from user where user=%s", (user, ))
        values = self.cursor.fetchall()
        if len(values) < 1:
            raise Exception("Can't find user %s" % user)
        value = str(int(float(values[0][1])) - int(float(money)*100))
        if self.database == "sqlite":
            self.conn.execute("UPDATE user SET money=? WHERE user=?", (value, user, ))
        else:
            self.cursor.execute("UPDATE user SET money=%s WHERE user=%s", (value, user, ))
        if self.database == "sqlite":
            self.conn.execute("insert into user (from, to, money) values (?,?,?)", (user, "system", money ))
        else:
            self.conn.execute("insert into user (from, to, money) values (%s,%s,%s)", (user, "system", money ))
        self.conn.commit()
        return float(value)/100

    def transfer(self, fromuser, touser, money):
        money = str(money)
        self.expenditure(fromuser, money)
        self.income(touser, money)
        if self.database == "sqlite":
            self.conn.execute("insert into user (from, to, money) values (?,?,?)", (fromuser, touser, money ))
        else:
            self.conn.execute("insert into user (from, to, money) values (%s,%s,%s)", (fromuser, touser, money ))
        self.conn.commit()

    def query_logs(self, user):
        if self.database == "sqlite":
            self.cursor.execute("select * from logs where fromuser=?", (user, ))
        else:
            self.cursor.execute("select * from logs where fromuser=%s", (user, ))
        values = self.cursor.fetchall()
        if self.database == "sqlite":
            self.cursor.execute("select * from logs where touser=?", (user, ))
        else:
            self.cursor.execute("select * from logs where touser=%s", (user, ))
        values.append(self.cursor.fetchall())
        return values