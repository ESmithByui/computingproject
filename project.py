try:
    import streamlit as st
except ImportError or ModuleNotFoundError:
    import os
    os.system('pip install streamlit')
    import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

from check_user import *
from create_database import *
from credentials import *
from delete_project import *
from insert_project_data import *
from update_project_data import *

projectconn = sqlite3.connect('project.db')
projectcursor = projectconn.cursor()

placeholder = st.empty()
placeholder1 = st.empty()
username = placeholder.text_input('Enter your username: ', key = 1)
password = placeholder1.text_input('Enter your username: ', key = 2)

if (username == credentials["student"]["username"] and password == credentials["student"]["password"]) or (username == credentials["admin"]["username"] and password == credentials["admin"]["password"]):
    st.success('Login Successful')
    st.write("\n")


    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    st.write('Current Date: ', current_date)

    if username == credentials["admin"]["username"] and password == credentials["admin"]["password"]:
        st.write("To reset the database, you must select the 'Select An Option' choice first, then select 'Reset Database'")
        username = 'Admin'
        user_check = user(projectcursor, projectconn)
        user_check.create_user(username)
        options = ['Select An Option', 'Reset Database', 'Add Project', 'Update Project', 'Delete Project']
        option = st.selectbox('Select An Option', options)
    
    else:
        user_check = user(projectcursor, projectconn)
        user_check.create_user(username)
        options = ['Select An Option', 'Add Project']
        option = st.selectbox('Select An Option', options)

    if (option == 'Reset Database'):
        confirm_reset = st.button('Reset database')
        if confirm_reset:
            reset = create(projectcursor, projectconn)
            reset.create_db()
            st.write('Database reset successful')

    elif (option == 'Add Project'):
        st.write(f'`{username}` user active')

        project_name = st.text_input('Enter the project name: ')
        project_description = st.text_input('Enter the project description: ')
        confirm_insert = st.button('Insert data')

        if confirm_insert:
            insert_data = insert(projectcursor, projectconn)
            insert_data.insert_data(project_name, project_description, username, current_date)
            st.write('Data inserted successfully!')

    elif (option == 'Update Project'):
        try:
            projectcursor.execute("""SELECT user_project
                                  FROM user_project
                                  WHERE user_project_id IS NOT NULL""")
        except sqlite3.Error as err:
            users = None

        if not users:
            st.write('No users with projects in the database')

        else:
            projectcursor.execute("""SELECT project_name
                                  ,     project_description
                                  ,     username
                                  ,     last_update_date
                                  FROM project p
                                  INNER JOIN user_project up
                                  ON p.project_id = up.project_id
                                  INNER JOIN user u
                                  ON u.user_id = up.user_id""")
            data = projectcursor.fetchall()
            df = pd.DataFrame(data, columns=['Project Name', 'Project Description', 'Owner', 'Date Added'])
            st.write(df)

            project_name = st.text_input('Enter the project name to update: ')
            project_description = st.text_input('Enter the new project description: ')

            update_name = st.checkbox('Update the project name?')

            if update_name:
                new_project_name = st.text_input('Enter the new project name: ')
                confirm_name_update = st.button('Update project name')
                if confirm_name_update:
                    new_project_name = new_project_name
            else:
                new_project_name = None

            confirm_update = st.button('Update data')
            if confirm_update:
                if project_description == '':
                    project_description = None
                
                update_data = update(projectcursor, projectconn)
                update_data.update_data(project_name, project_description, username, current_date, new_project_name)
                st.write('Data updated successfully!')

    elif (option == 'Delete Project'):
        try:
            projectcursor.execute("""SELECT user_project
                                  FROM user_project
                                  WHERE user_project_id IS NOT NULL""")
        except sqlite3.Error as err:
            users = None   

        if not users:
            st.write('No users with projects in the database')

        else:
            projectcursor.execute("""SELECT project_name
                                  ,     project_description
                                  ,     username
                                  ,     last_update_date
                                  FROM project p
                                  INNER JOIN user_project up
                                  ON p.project_id = up.project_id
                                  INNER JOIN user u
                                  ON u.user_id = up.user_id""")
            data = projectcursor.fetchall()
            df = pd.DataFrame(data, columns=['Project Name', 'Project Description', 'Username', 'Date Added'])
            st.write(df)

            project_name = st.text_input('Enter the project name to delete: ')
            confirm_delete = st.button('Delete data')
            if confirm_delete:
                delete_data = delete(projectcursor, projectconn)
                delete_data.delete_data(project_name)
                st.write('Data deleted successfully!')

view = st.checkbox('View the data?')

if view:
    try:
        projectcursor.execute("""SELECT user_project_id
                              FROM user_project
                              WHERE user_project_id IS NOT NULL""")
        users = projectcursor.fetchall()

    except sqlite3.Error as err:
        users = None

    if not users:
        st.write('No users with projects in the database')

    else:
        projectcursor.execute("""SELECT project_name
                              ,     project_description
                              ,     u.username
                              ,     date_added
                              ,     u2.username
                              ,     last_update_date
                              FROM project p
                              LEFT JOIN user_project up
                              ON p.project_id = up.project_id
                              LEFT JOIN user u
                              ON u.user_id = up.user_id
                              LEFT JOIN user u2
                              ON u.user_id = up.last_updated_by""")
        data = projectcursor.fetchall()

        df = pd.DataFrame(data, columns = ['Project Name', 'Project Description', 'Owner', 'Date Added', 'Last Updated By', 'Last Update Date'])
        st.write(df)
