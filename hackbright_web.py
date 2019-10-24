"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html", 
                           students=students, 
                           projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    project_grade_list = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           project_grade_list= project_grade_list)   

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/new-student-info")
def get_new_student_info():
    """Renders a form to get new student info."""

    return render_template("add_student.html")   


@app.route("/student-add", methods=['POST'])
def add_student():
    """Add a student to the database."""

    first = request.form.get('first_name')
    last = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("confirm_add_student.html",
                           first_name=first,
                           last_name=last,
                           github=github)


@app.route("/project", methods=['GET'])
def display_projects():
    """Display information about a project"""

    project = request.args.get('prj')

    project_title, description, grade = hackbright.get_project_by_title(project)

    student_grades = hackbright.get_grades_by_title(project)

    return render_template("project_info.html",
                           project_title=project_title,
                           description=description,
                           grade=grade,
                           student_grades=student_grades
                           )


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
