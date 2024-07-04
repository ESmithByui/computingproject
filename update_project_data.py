class update:
    def __init__(self, studentcursor, projectdb):
        self.studentcursor = studentcursor
        self.projectdb = projectdb

    def update_data(self, project_name, project_description, username, current_date, new_project_name):
        self.studentcursor.execute("""SELECT project_id 
                                   FROM project 
                                   WHERE project_name = ?""",
                                   (project_name,))
        project_id = self.studentcursor.fetchone()
        project_id = project_id[0]

        if new_project_name is not None:
            self.studentcursor.execute("""UPDATE project
                                       SET project_name = ?
                                       WHERE project_id = ?""",
                                       (new_project_name, project_id))
            self.projectdb.commit()
            self.studentcursor.execute("""SELECT user_id
                                       FROM user
                                       WHERE username = ?""",
                                       (username,))
            user_id = self.studentcursor.fetchone()
            user_id = user_id[0]

            self.studentcursor.execute("""UPDATE user_project
                                       SET last_update_date = ?,
                                       last_updated_by = ?
                                       WHERE project_id = ?""",
                                       (current_date, user_id, project_id))
            self.projectdb.commit()

        if project_description is not None:
            self.studentcursor.execute("""UPDATE project
                                       SET project_description = ?
                                       WHERE project_id = ?""",
                                       (project_description, project_id))
            self.projectdb.commit()
            self.studentcursor.execute("""SELECT user_id
                                       FROM user
                                       WHERE username = ?""",
                                       (username,))
            user_id = self.studentcursor.fetchone()
            user_id = user_id[0]

            self.studentcursor.execute("""UPDATE user_project
                                       SET last_update_date = ?,
                                       last_updated_by = ?
                                       WHERE project_id = ?""",
                                       (current_date, user_id, project_id))
            self.projectdb.commit()