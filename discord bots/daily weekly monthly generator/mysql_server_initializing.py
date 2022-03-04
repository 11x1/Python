import mysql.connector

def check_if_database_exists():
    # Try connecting to database
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='generator_db'
        )
    except:
        print('MySQL | Server login/database is invalid')
    
    print('MySQL | Trying to login without any specified database')
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
    )

    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")

    does_our_database_exist = False
    for x in cursor:
        if x == ('generator_db',):
            does_our_database_exist = True

    if not does_our_database_exist:
        cursor.execute('CREATE DATABASE generator_db')
        does_our_database_exist = True


    if does_our_database_exist:
        print('MySQL | Database found')
        cursor.execute('USE generator_db')

        cursor.execute("CREATE TABLE IF NOT EXISTS users (userid VARCHAR(255), unixtime_daily VARCHAR(255), unixtime_weekly VARCHAR(255), unixtime_monthly VARCHAR(255))")
        print('MySQL | Tables created')


def return_and_delete():
    with open('data.txt', 'r+') as file:
        lines = file.readlines()
        file.truncate(0)
        file.seek(0)
        file.writelines(lines[1:])
        try:
            return lines[0]
        except:
            return 'err_no_available_stock'

def fix_datafile_spacing():
    with open('data.txt', 'r+') as file:
        final = ''
        for line in file.readlines():
            if len(line) > 1:
                final += line
        file.truncate(0)
        file.seek(0)
        file.write(final)

