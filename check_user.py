import sqlite3
class user:
    
    def __init__(self, studentcursor, projectdb):
        self.studentcursor = studentcursor
        self.projectdb = projectdb

    def format_list(self, list):
        list = [str(item) for item in list]
        new_list = '\n'.join(list)
        new_list = new_list.replace('[', '')
        new_list = new_list.replace(']', '')
        new_list = new_list.replace("'", "")
        new_list = new_list.replace('(', '')
        new_list = new_list.replace(')', '')
        new_list = new_list.replace(',', '')
        return new_list
    
    def create_user(self, username):
        try:
            #check to see if the user exists in the database
            self.studentcursor.execute('SELECT username FROM user')
            users = self.studentcursor.fetchall()
            users = self.format_list(users)
            if username in users:
                #self.studentcursor.close()
                return True, username
            else:
                self.studentcursor.execute('INSERT INTO user (username) VALUES (?)', (username,))
                self.projectdb.commit()
                print('User inserted successfully')
                return True, username
            
        except sqlite3.Error as err:
            print(f'Error: {err}')
            return False