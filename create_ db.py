import sqlite3
import os
import sys

def main(args):
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
    if not databaseexisted:  # First time creating teh database. Create teh tables
        # table courses
        dbcon.execute(
            '''CREATE TABLE courses
                 (id INTEGER PRIMARY KEY,
                 course_name TEXT NOT NULL,
                 student TEXT NOT NULL,
                 number_of_students INTEGER NOT NULL ,
                 class_id INTEGER REFERENCES  classrooms(id),
                 course_length INTEGER NOT NULL);''')
        #table students
        dbcon.execute(
            '''CREATE TABLE students
             (grade TEXT PRIMARY KEY,
             count INTEGER NOT NULL);''')
        #table classroom
        dbcon.execute(
            '''CREATE TABLE classrooms
                 (id INTEGER PRIMARY KEY,
                 location TEXT NOT NULL,
                 current_course_id INTEGER NOT NULL ,
                 current_course_time_left INTEGER NOT NULL);''')

    file = open(sys.argv[1],"r")
    for line in file:
        words = line.split(', ')
        if line.startswith("C"):
            id = words[1]
            course_name = words[2]
            student = words[3]
            number_of_students = words[4]
            class_id = words[5]
            endline = words[6].split('\n')
            course_length = endline[0]
            dbcon.execute(
                "INSERT INTO courses (id,course_name,student,number_of_students,class_id,course_length) \
                 VALUES (?,?,?,?,?,?);", (id, course_name, student, number_of_students, class_id, course_length))


        elif line.startswith("S"):
            grade = words[1]
            endline = words[2].split('\n')
            count = endline[0]
            dbcon.execute(
                "INSERT INTO students (grade,count) \
                  VALUES (?,?);", (grade, count))


        elif line.startswith("R"):
            id = words[1]
            endline = words[2].split('\n')
            location = endline[0]
            current_course_id = 0
            current_course_time_left =0
            dbcon.execute(
                "INSERT INTO classrooms (id,location,current_course_id,current_course_time_left) \
                  VALUES (?,?,?,?);", (id, location, current_course_id, current_course_time_left))

    #print courses
    cursor.execute("SELECT * FROM courses;")
    courseslist = cursor.fetchall()
    print("courses")
    for rowcourses in courseslist:
        print(rowcourses)

    #print classrooms
    cursor.execute("SELECT * FROM classrooms;")
    classroomslist = cursor.fetchall()
    print("classrooms")
    for classroomsrow in classroomslist:
          print(classroomsrow)

    #print students
    cursor.execute("SELECT * FROM students;")
    studentslist = cursor.fetchall()
    print("students")
    for row in studentslist:
        print(row)
    dbcon.commit()
    dbcon.close()
if __name__ == '__main__':
    main(sys.argv)