class delete:

    def __init__(self, studentcursor, studentconn):
        self.studentcursor = studentcursor
        self.studentconn = studentconn

    def delete_data(self, project_name):

        self.studentcursor.execute("""SELECT project_id
                                   FROM project
                                   WHERE project_name = ?""", (project_name,))
        project_id = self.studentcursor.fetchone()
        project_id = project_id[0]

        self.studentcursor.execute("""DELETE FROM project
                                   WHERE project_id = ?""", (project_id,))
        self.studentconn.commit()