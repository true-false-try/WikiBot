import sqlite3

class SQLscript:
    def __init__(self, database_file):
        #Connect to db
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscribers(self, status=1):
        #Get active subscribers
            with self.connection:
                return self.cursor.execute("SELECT * FROM `subscribers` WHERE `status` = ?", (status,)).fetchall()

    def subscribers_exists(self, user_id):
        #Check for we , if we have user in db
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscribers` WHERE `id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=1):
        #Add subscriber
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscribers` (`id`, `status`) VALUES (?,?)", (user_id, status))

    def update_subscription(self, user_id, status):
        #Reload status subscribe
        return self.cursor.execute("UPDATE `subscribers` SET `status` = ? WHERE `id` = ?", (user_id, status))

    def close(self):
        self.connection.close()