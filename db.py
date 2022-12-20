import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             database='tts_bot',
                             cursorclass=pymysql.cursors.DictCursor)


def insert_user1(message):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`user_id`, `user_name`, `name`) VALUES (%s, NOW(), %s)"
        cursor.execute(sql, (message.from_user.id, message.from_user.username, message.from_user.first_name))
    connection.commit()

def insert_user(user_id, user_name = "0", name = "0"):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`user_id`, `user_name`, `name`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user_id, str(user_name), str(name)))
    connection.commit()

def insert_voice(user_id, user_name = "0", message="Test"):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `tts_voices` (`user_id`, `user_name`,`voice`) VALUES (%s, %s,%s)"
        cursor.execute(sql, (user_id, str(user_name), message))
    connection.commit()

def select_user(user_id=0):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users` WHERE `user_id` = %s"
        cursor.execute(sql, (user_id, ))
        result = cursor.fetchone()
    return result

def select_users():
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM `users` WHERE %s"
        cursor.execute(sql, (1, ))
        result = cursor.fetchone()
    return result

async def select_users_all():
    with connection.cursor() as cursor:
        sql = "SELECT `user_id` FROM `users` WHERE %s"
        cursor.execute(sql, (1, ))
        result = cursor.fetchall()
    return result

def select_voices():
    with connection.cursor() as cursor:
        sql = """SELECT count(*) as count from tts_voices
                    where %s"""
        cursor.execute(sql, (1, ))
        result = cursor.fetchone()
    return result

