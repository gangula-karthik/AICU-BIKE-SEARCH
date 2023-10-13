from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc as odbc
import sys


connection_string = '''
    Driver={SQL Server};
    Server=tcp:aicudb.database.windows.net,1433;
    Database=aicudb;
    Uid=aicu_admin;
    Pwd=P4bAjrpkhafM2Z@;
    Trust_Connection=yes;
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
'''


app = Flask(__name__)


# testing page
@app.route('/test')
def test():
    # insert users statement
    # try:
    #     conn = odbc.connect(connection_string)
    # except Exception as e:
    #     print(e)
    #     print('Cannot connect to database, task is terminated.')
    #     sys.exit()
    # else:
    #     print('Successfully connected to database!')
    #     cursor = conn.cursor()
    # try:
    #     records = [
    #         ['Lim Yi Cheng', 'https://media.discordapp.net/attachments/1162003771476422768/1162283868502638682/lim_yi_cheng_pfp.jpeg?ex=653b6034&is=6528eb34&hm=1546f26c07496f13aa16d4d28302bf8cc53ed9e7085026dff819189fda13f095&=&width=625&height=625', 'resident', 0, 0, ''],
    #         ['Huang Yu Xuan', 'https://media.discordapp.net/attachments/1162003771476422768/1162283867793801216/huang_yu_xuan_pfp.jpeg?ex=653b6034&is=6528eb34&hm=d2be0c011eda1b1ff8db23bdd24462752f95c48c0d9f6fb6e9849c9a5b2d5d8f&=&width=625&height=625', 'resident', 0, 0, ''],
    #         ['Andrew Ng', 'https://media.discordapp.net/attachments/1162003771476422768/1162283868167086211/andrew_ng_pfp.jpeg?ex=653b6034&is=6528eb34&hm=53f8b4dc5cbeb3805e14f62fc3dc9175790e3fdc5a3d0883a5aa9001c4d60def&=&width=625&height=625', 'vendor', 0, 0, ''],
    #         ['Desmond Tan', 'https://media.discordapp.net/attachments/1162003771476422768/1162283868896895036/desmond_tan_pfp.jpeg?ex=653b6034&is=6528eb34&hm=271dd5a63cd57baae9f7e30d1bbe34f9824002a70c2e381ed1a41fff2f05ef09&=&width=625&height=625', 'police', 0, 0, '']
    #     ]
    #     insert_statement = '''
    #         INSERT INTO Users (name, profile_pic, role, level_exp, case_solved, transcript)
    #         VALUES (?, ?, ?, ?, ?, ?)
    #     '''
    #     for record in records:
    #         print(record)
    #         cursor.execute(insert_statement, record)
    # except Exception as e:
    #     cursor.rollback()
    #     print(e.value)
    #     print('Transaction is unsuccessfull & rolled back.')
    # else:
    #     print('Transaction is successful & records inserted successfully!')
    #     cursor.commit()
    # finally: 
    #     print('Cursor & connection closed.')
    #     cursor.close()
    #     conn.close()

    # retrieve users statement
    try:
        conn = odbc.connect(connection_string)
    except Exception as e:
        print(e)
        print('Cannot connect to database, task is terminated.')
        sys.exit()
    else:
        print('Successfully connected to database!')
        cursor = conn.cursor()
    try:
        retrieve_statement = '''
            SELECT * FROM Users
        '''
        cursor.execute(retrieve_statement)
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print('Transaction is unsuccessfull & rolled back.')
    else:
        rows = cursor.fetchall()  # Fetch all records
        print(rows)
        # for row in rows:
            # Access columns by index or name
            # column1_value = row[0]  # Example: Access the first column
            # column2_value = row['ColumnName2']  # Example: Access a column by name
            # print(column1_value, column2_value)
        print('Transaction is successful & records retrieved successfully!')
    finally: 
        print('Cursor & connection closed.')
        cursor.close()
        conn.close()

    return render_template('test.html', rows=rows)


# base template to check
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/qr_code')
def qr_code():
    return render_template('qr_code.html')


@app.route('/approving_login')
def approving_login():
    return render_template('approving_login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
