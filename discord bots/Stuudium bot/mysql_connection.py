import mysql.connector

database = 'hwbotweb'
data_table = 'users'

def connect_to_database_and_register_user(userid, username, password):
    connection = mysql.connector.connect(user="root", password="password", host="localhost", port=3306,
                                                database=database,
                                                auth_plugin="mysql_native_password")
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute("SET SQL_SAFE_UPDATES=0")
    cursor.execute(f"SELECT * FROM `{database}`.`{data_table}`")

    existing_user = False
    for row in cursor:
        print(row['userid'])
        if str(userid) == row["userid"]:
            existing_user = True

    if existing_user:
        print("override")
        cursor.execute(f"UPDATE `{data_table}` SET `username` = %s, `password` = %s WHERE `userid` = %s",
                            (username, password, userid))

        cursor.execute(f"SELECT * FROM `{database}`.`{data_table}`")
        connection.commit()
        cursor.close()
        connection.close()
        return "succesfully_updated_userdata"
    else:
        print("new")
        cursor.execute(f"INSERT INTO `{database}`.`{data_table}` VALUES(%s,%s,%s)",
                            (userid, username, password))

        connection.commit()
        cursor.close()
        connection.close()
        return "succesfully_saved_userdata"

def connect_to_database_and_return_username_password(user_id):
    database = 'hwbotweb'
    data_table = 'users'
    
    connection = mysql.connector.connect(user="root", password="password", host="localhost", port=3306,
                                                database=database, auth_plugin="mysql_native_password")
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute("SET SQL_SAFE_UPDATES=0")
    cursor.execute(f"SELECT * FROM `{database}`.`{data_table}`")

    should_send_error = True
    username_row = None
    for row in cursor:
        if str(user_id) == row["userid"]:
            should_send_error = False
            username_row = row
            break
    if should_send_error:
        return "err_user_not_found"

    connection.commit()
    cursor.close()
    connection.close()
    return {
        "username": username_row["username"],
        "password": username_row["password"]
    }

def connect_to_database_and_wipe_data(user_id):
    database = 'hwbotweb'
    data_table = 'users'

    connection = mysql.connector.connect(user="root", password="password", host="localhost", port=3306,
                                                database=database,
                                                auth_plugin="mysql_native_password")
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute("SET SQL_SAFE_UPDATES=0")
    cursor.execute(f"DELETE FROM `{database}`.`{data_table}` WHERE userid = %s", (user_id,))

    connection.commit()
    cursor.close()
    connection.close()
    return "deleted_userdata"