import sqlite3
dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()
def UpdateAndDelete(courseid,classroomid):
    dbcon.execute("UPDATE classrooms set current_course_id = 0 where id =?",(classroomid,))
    dbcon.commit()
    dbcon.execute("DELETE from courses where id = ?",(courseid,))
    dbcon.commit()


def DecreaseStudents(grade,count):
    todecrease = 0
    cursor.execute("SELECT count FROM students WHERE grade = ?", (grade,))
    rows = cursor.fetchall()
    for row in rows:
        todecrease = int(row[0]) - count
    dbcon.execute("UPDATE students set count = ? where grade = ?", (todecrease, grade,))
    dbcon.commit()

def SetCourseTimeLeft ():
    dbcon.execute("UPDATE classrooms set current_course_time_left = current_course_time_left-1 where current_course_id!=0 and current_course_time_left > 0;")
    dbcon.commit()

def Schedule(start,classroomid,row):
    cursor.execute("SELECT id,course_name,course_length,number_of_students,student FROM courses WHERE class_id = ?",
                   (classroomid,))
    courses = cursor.fetchall()
    for course in courses:
        numberofstudents = int(course[3])
        DecreaseStudents(course[4], numberofstudents)
        # insert to classroom
        courseid = int(course[0])
        courselength = int(course[2])
        dbcon.execute("UPDATE classrooms set current_course_id = ?,current_course_time_left =? where id = ?",
                      (courseid, courselength, classroomid,))
        dbcon.commit()
        scheduleprint = "(" + str(itertor) + ") " + row[1] + ": " + course[1] + " is schedule to start"
        print(scheduleprint)
        if start:
            break

def Occupied():
    cursor.execute(
        "SELECT current_course_id,location FROM classrooms WHERE current_course_time_left > 0 and current_course_id != 0;")
    rows = cursor.fetchall()
    for row in rows:
        occupiedprint = "(" + str(itertor) + ") " + row[1] + ": occupied by "
        courseid = int(row[0])
        cursor.execute("SELECT course_name FROM courses WHERE id = ?", (courseid,))
        courses = cursor.fetchall()
        for coursename in courses:
            occupiedprint = occupiedprint + coursename[0]
            print(occupiedprint)
def DoneCourses():
    cursor.execute(
        "SELECT current_course_id,location,id FROM classrooms WHERE current_course_time_left = 0 and current_course_id != 0;")
    rows = cursor.fetchall()
    for row in rows:
        doneprint = "(" + str(itertor) + ") " + row[1] + ": "
        courseid = int(row[0])
        classroomid = int(row[2])
        cursor.execute("SELECT course_name FROM courses WHERE id = ?", (courseid,))
        courses = cursor.fetchall()
        for coursename in courses:
            doneprint = doneprint + coursename[0] + " is done"
            UpdateAndDelete(courseid, classroomid)
            print(doneprint)
            Schedule(False, classroomid, row)
def main():
    global itertor
    itertor = 0
    isdone = False
    while not isdone and dbcon != None:
        Occupied()
        DoneCourses()
        cursor.execute("SELECT id FROM courses;")
        rows = cursor.fetchall()
        isdone = len(rows)== 0
        i=0
        if not isdone:
            cursor.execute("SELECT id,location FROM classrooms WHERE current_course_time_left = 0 and current_course_id = 0;")
            rows = cursor.fetchall()
            for row in rows:
                classroomid = int(row[0])
                Schedule(True, classroomid,row)
        # print DB
        # print courses
        cursor.execute("SELECT * FROM courses;")
        courseslist = cursor.fetchall()
        print("courses")
        for rowcourses in courseslist:
            print(rowcourses)

        # print classrooms
        cursor.execute("SELECT * FROM classrooms;")
        classroomslist = cursor.fetchall()
        print("classrooms")
        for classroomsrow in classroomslist:
            print(classroomsrow)

        # print students
        cursor.execute("SELECT * FROM students;")
        studentslist = cursor.fetchall()
        print("students")
        for row in studentslist:
            print(row)

        itertor += 1
        SetCourseTimeLeft()
    dbcon.commit()
    dbcon.close()
if __name__ == '__main__':
    main()