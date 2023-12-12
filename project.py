import mysql.connector
from mysql.connector import errorcode


try:
    my_connection = mysql.connector.connect(
        user = "root",
        password = "Kteasley",
        host = "localhost",
        database = "project"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invaild credentials")
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("No database available")
    else:
        print("Error occured", err)

else:
    print('Connection Successful')
    #Create a cursor from the connection
    user_cursor = my_connection.cursor()
    course_cursor = my_connection.cursor()
    compensation_cursor = my_connection.cursor()
    enrollment_cursor = my_connection.cursor()
    #schema_cursor = my_connection.cursor()
    #schema_cursor.execute("CREATE SCHEMA IF NOT EXIST project")
    #table = my_connection.cursor()
    #table.execute("CREATE TABLE IF NOT EXIST project.user (user_id int AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(40), last_name VARCHAR(40), title VARCHAR(40))")
    #table.execute("SHOW TABLES")

    #Create the sql query
    user_input = input("Are you a new user. (Yes or No): ").lower()
    if user_input == "yes":
        user_firstname_input = input("Enter your First Name: ")
        user_lastname_input = input("Enter your Last Name: ")
        user_title_input = input("Enter your title (Student, Instructor, Admin): ").lower()
        query = "INSERT INTO user (first_name, last_name, title) VALUES (%s,%s,%s)"
        user_cursor.execute(query, (user_firstname_input, user_lastname_input, user_title_input))

        user_id = user_cursor.lastrowid


        print(f"\nNew User Added with ID: {user_id}")

        if user_title_input == "instructor":
            instructor_menu = input("Menu (Select Number)\n"+
                                    "1. Add Course\n"+
                                    "2. Delete Course\n"
                                    "Selection: ")
            if instructor_menu == "1":
                course = input("Name of Course: ")
                subject = input("Name of Subject: ")
                query = "INSERT INTO course (user_id, course_name, subject) VALUES (%s,%s,%s)"
                course_cursor.execute(query, (user_id, course, subject))
                print("You've Added the Course.")

            elif instructor_menu == "2":
                course = input("CourseID: ")
                query = "DELETE FROM course WHERE course_id = %s"
                course_cursor.execute(query, (course,))
                print("You've Deleted the course.")
                delete_null_course_query = "DELETE FROM enrollment WHERE course_id IS NULL"
                enrollment_cursor.execute(delete_null_course_query)

        elif user_title_input == "student":
            student_menu = input("Menu (Select Number)\n"+
                                    "1. Enroll in a Course.\n"+
                                    "2. Delete a Course.\n"
                                    "Selection: ")
            
            if student_menu == "1":
                course_cursor.execute("SELECT course_id FROM course")
                all_course_ids = course_cursor.fetchall()
                print("Available Course IDs:", all_course_ids)
                enroll = input("CourseID: ")
                progress = input("Progress In Course(DNF,INP,Complete): ").lower()

                if progress == "dnf":
                    query = "SELECT course_id FROM course WHERE course_id = %s"
                    course_cursor.execute(query, (enroll,))
                    specific_course_id_result = course_cursor.fetchone()
                    if specific_course_id_result:
                        course_id = specific_course_id_result[0]
                    else:
                        print(f"No information found for course_id {enroll}.")
                elif progress == "inp":
                    query = "SELECT course_id FROM course WHERE course_id = %s"
                    course_cursor.execute(query, (enroll,))
                    specific_course_id_result = course_cursor.fetchone()
                    if specific_course_id_result:
                        course_id = specific_course_id_result[0]
                elif progress == "complete":
                    query = "SELECT course_id FROM course WHERE course_id = %s"
                    course_cursor.execute(query, (enroll,))
                    specific_course_id_result = course_cursor.fetchone()
                    if specific_course_id_result:
                        course_id = specific_course_id_result[0]
                    else:
                        print(f"No information found for course_id {enroll}.")

                else:
                    print("Wrong Entry (DNF, INP, Complete)")
                query = "INSERT INTO enrollment(user_id, course_id, progress) VALUES(%s, %s, %s)"
                enrollment_cursor.execute(query, (user_id, course_id, progress))
                print("Course Added!")

            elif student_menu == "2":
                print("Enter a Course First.")
            
            else:
                print("Invalid Entry")

        elif user_title_input == "admin":
            admin_menu = input("Menu (Select Number)\n"+
                                    "1. Add Course\n"+
                                    "2. Delete Course\n"
                                    "3. Delete Instructor User\n"
                                    "4. Delete Student User\n"
                                    "Selection: ")
            if admin_menu == "1":
                course = input("Name of Course: ")
                subject = input("Name of Subject: ")
                query = "INSERT INTO course (user_id, course_name, subject) VALUES (%s,%s,%s)"
                course_cursor.execute(query, (user_id, course, subject))
                print("You've Added the Course.")

            elif admin_menu == "2":
                course = input("Course ID: ")
                query = "DELETE FROM course WHERE course_id = %s"
                course_cursor.execute(query, (course,))
                print("You've Deleted the course.")
                delete_null_course_query = "DELETE FROM enrollment WHERE course_id IS NULL"
                enrollment_cursor.execute(delete_null_course_query)

            elif admin_menu == "3":
                instructor = input("Instructor ID: ")
                query = "DELETE FROM user WHERE user_id = %s"
                course_cursor.execute(query, (instructor,))
                print(f"You've Deleted Instructor {instructor}.")
                delete_null_course_query = "DELETE FROM course WHERE user_id IS NULL"
                course_cursor.execute(delete_null_course_query)

            elif admin_menu == "4":
                student = input("Student ID: ")
                query = "DELETE FROM user WHERE user_id = %s"
                user_cursor.execute(query, (student,))
                print(f"Student Deleted {student}.")
                delete_null_enroll_query = "DELETE FROM enrollment WHERE user_id IS NULL"
                course_cursor.execute(delete_null_enroll_query)

            else:
                print("Wrong Entry.")
        else:
            print("Wrong Entry.")
                



    elif user_input == "no":
        user_id = int(input("Enter ID: "))
        query = "SELECT * FROM user WHERE user_id = %s"
        user_cursor.execute(query, (user_id,))
        result = user_cursor.fetchone()

        if result:
            print("You are in the system!\n")
            user_title_query = "SELECT title FROM user WHERE user_id = %s"
            user_cursor.execute(user_title_query, (user_id,))
            user_title_input = user_cursor.fetchone()
            
            if user_title_input == ('instructor',):
                instructor_menu = input("Menu (Select Number)\n"+
                                    "1. Add Course\n"+
                                    "2. Delete Course\n"
                                    "Selection: ")
                if instructor_menu == "1":
                    course = input("Name of Course: ")
                    subject = input("Name of Subject: ")
                    query = "INSERT INTO course (user_id, course_name, subject) VALUES (%s,%s,%s)"
                    course_cursor.execute(query, (user_id, course, subject))
                    print("You've Added the Course.")
                    
                elif instructor_menu == "2":
                    course = input("CourseID: ")
                    query = "DELETE FROM course WHERE course_id = %s"
                    course_cursor.execute(query, (course,))
                    print("You've Deleted the course.")
                    delete_null_course_query = "DELETE FROM enrollment WHERE course_id IS NULL"
                    enrollment_cursor.execute(delete_null_course_query)

            elif user_title_input == ('student',):
                student_menu = input("Menu (Select Number)\n"+
                                    "1. Enroll in a Course.\n"+
                                    "2. Delete a Course.\n"
                                    "Selection: ")
                
                if student_menu == "1":
                    course_cursor.execute("SELECT course_id FROM course")
                    all_course_ids = course_cursor.fetchall()
                    print("Available Course IDs:", all_course_ids)
                    enroll = input("CourseID: ")
                    progress = input("Progress In Course(DNF,INP,Complete): ").lower()

                    if progress == "dnf":
                        query = "SELECT course_id FROM course WHERE course_id = %s"
                        course_cursor.execute(query, (enroll,))
                        specific_course_id_result = course_cursor.fetchone()
                        if specific_course_id_result:
                            course_id = specific_course_id_result[0]
                        else:
                            print(f"No information found for course_id {enroll}.")
                    elif progress == "inp":
                        query = "SELECT course_id FROM course WHERE course_id = %s"
                        course_cursor.execute(query, (enroll,))
                        specific_course_id_result = course_cursor.fetchone()
                        if specific_course_id_result:
                            course_id = specific_course_id_result[0]
                    elif progress == "complete":
                        query = "SELECT course_id FROM course WHERE course_id = %s"
                        course_cursor.execute(query, (enroll,))
                        specific_course_id_result = course_cursor.fetchone()
                        if specific_course_id_result:
                            course_id = specific_course_id_result[0]
                        else:
                            print(f"No information found for course_id {enroll}.")

                    else:
                        print("Wrong Entry (DNF, INP, Complete)")

                    query = "INSERT INTO enrollment(user_id, course_id, progress) VALUES(%s, %s, %s)"
                    enrollment_cursor.execute(query, (user_id, course_id, progress))
                    print("Course Added!")

                elif student_menu == "2":
                    course_id = input("Enter CourseID: ")
                    query = ("DELETE FROM enrollment WHERE course_id = %s")
                    enrollment_cursor.execute(query, (course_id,))
                    print("Course Has been deleted. ")
            
                else:
                    print("Invalid Entry")

            elif user_title_input == ('admin',):
                admin_menu = input("Menu (Select Number)\n"+
                                    "1. Add Course\n"+
                                    "2. Delete Course\n"
                                    "3. Delete Instructor User\n"
                                    "4. Delete Student User\n"
                                    "Selection: ")
                if admin_menu == "1":
                    course = input("Name of Course: ")
                    subject = input("Name of Subject: ")
                    query = "INSERT INTO course (user_id, course_name, subject) VALUES (%s,%s,%s)"
                    course_cursor.execute(query, (user_id, course, subject))
                    print("You've Added the Course.")

                elif admin_menu == "2":
                    course = input("Course ID: ")
                    query = "DELETE FROM course WHERE course_id = %s"
                    course_cursor.execute(query, (course,))
                    print("You've Deleted the course.")
                    delete_null_course_query = "DELETE FROM enrollment WHERE course_id IS NULL"
                    enrollment_cursor.execute(delete_null_course_query)

                elif admin_menu == "3":
                    instructor = input("Instructor ID: ")
                    query = "DELETE FROM user WHERE user_id = %s"
                    course_cursor.execute(query, (instructor,))
                    print(f"You've Deleted Instructor {instructor}.")
                    delete_null_course_query = "DELETE FROM course WHERE user_id IS NULL"
                    course_cursor.execute(delete_null_course_query)

                elif admin_menu == "4":
                    student = input("Student ID: ")
                    query = "DELETE FROM user WHERE user_id = %s"
                    user_cursor.execute(query, (student,))
                    print(f"Student Deleted {student}.")
                    delete_null_enroll_query = "DELETE FROM enrollment WHERE user_id IS NULL"
                    course_cursor.execute(delete_null_enroll_query)

                else:
                    print("Wrong Entry.")
            else:
                print("Wrong Entry.")

            
            



        else:
            print("The ID you entered is not in the system.")
    else:
        print("Invalid Entry (Yes/No).")

    

    
    
    #Execute the query and provide data for the query
    
    my_connection.commit()
    my_connection.close()