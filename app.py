from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask.ext.moment import Moment

from uuid import uuid4

from libs import sorter, format_dueDate

from creds import *

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User

register(PARSE_appId, PARSE_apiKey)

class Projects(Object):
	pass
class Tasks(Object):
	pass
class _User(Object):
	pass
app = Flask(__name__)
moment = Moment(app)

@app.before_request
def setup_env():
	app.jinja_env.globals["len"] = len
	app.jinja_env.globals["sorter"] = sorter

@app.route("/")
@app.route("/list")
def list_projects():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	projects = Projects.Query.filter(userId=session.get("uid"))
	return render_template("listProjects.html", projects=projects)
@app.route("/newproj", methods=["GET", "POST"])
def new_project():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if request.method == "POST":
		Projects(
			name=request.form["projectName"],
			detail=request.form["projectDetail"],
			url=uuid4().hex,
			theme=request.form["projectTheme"],
			user=_User.Query.get(objectId=session.get("uid")),
			userId=session.get("uid")
			).save()
		return redirect(url_for("list_projects"))
	return render_template("newProject.html")
@app.route("/editproj/<projectUrl>", methods=["GET", "POST"])
def edit_project(projectUrl=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if projectUrl == None:
		return redirect(url_for("list_projects"))
	try:
		project = Projects.Query.get(url=projectUrl)
	except:
		return redirect(url_for("list_projects"))
	if project.userId != session.get("uid"):
		return redirect(url_for("list_projects"))
	if request.method == "POST":
		project(
		name=request.form["projectTitle"],
		detail=request.form["projectDetail"],
		theme=request.form["projectTheme"]
		).save()
		return redirect(url_for("list_projects"))
	return render_template("editProject.html", project=project)
@app.route("/delproj/<projectUrl>")
def delete_project(projectUrl=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if projectUrl == None:
		return redirect(url_for("list_projects"))
	try:
		project = Projects.Query.get(url=projectUrl)
	except:
		flash("No such project")
		return redirect(url_for("list_projects"))
	if project.userId != session.get("uid"):
		flash("You do not own this project")
		return redirect(url_for("list_projects"))
	project.delete()
	flash("deleted")
	return redirect(url_for("list_projects"))

@app.route("/tasks/<projectUrl>")
def project_tasks(projectUrl=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if projectUrl == None:
		return redirect(url_for("list_projects"))
	try:
		project = Projects.Query.get(url=projectUrl)
	except:
		return redirect(url_for("list_projects"))
	if project.userId != session.get("uid"):
		return redirect(url_for("list_projects"))
	tasks = Tasks.Query.filter(userId=session.get("uid"), projectUrl=projectUrl).order_by("-dueDate")
	return render_template("listTasks.html", tasks=tasks, project=project)
@app.route("/newtask/<projectUrl>", methods=["GET","POST"])
def new_task(projectUrl=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if projectUrl == None:
		redirect(url_for("project_tasks",projectUrl=projectUrl))
	try:
		project = Projects.Query.get(url=projectUrl, userId=session.get("uid"))
	except:
		return redirect(url_for("list_projects"))
	if request.method == "POST":
		Tasks(
			title=request.form["taskTitle"],
			detail=request.form["taskDetail"],
			dueDate=format_dueDate(request.form["taskDueDate"]),
			user=_User.Query.get(objectId=session.get("uid")),
			userId=session.get("uid"),
			project=project,
			projectId=project.objectId,
			projectUrl=project.url
		).save()
		return redirect(url_for("project_tasks", projectUrl=projectUrl))
	return render_template("newTask.html", project=project)
@app.route("/all")
def all_tasks():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	z = Tasks.Query.filter(userId=session.get("uid"))#.order_by("-dueDate")
	if z == None:
		z = []
	return render_template("allTasks.html", tasks=z)
@app.route("/edittask/<taskId>", methods=["GET", "POST"])
def edit_task(taskId=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if taskId == None:
		return redirect(url_for("project_list"))
	try:
		task = Tasks.Query.get(objectId=taskId, userId=session.get("uid"))
	except:
		return redirect(url_for("project_list"))
	if request.method == "POST":
		task(
			title=request.form["taskTitle"],
			detail=request.form["taskTitle"],
			dueDate=format_dueDate(request.form["taskDueDate"]),
		).save()
		return redirect(url_for("project_tasks", projectUrl=task.projectUrl))
	return render_template("editTask.html", task=task)
@app.route("/deltask/<taskId>")
def delete_task(taskId=None):
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	if taskId == None:
		return redirect(url_for("project_list"))
	try:
		task = Tasks.Query.get(objectId=taskId, userId=session.get("uid"))
	except:
		return redirect(url_for("project_list"))
	task.delete()
	return redirect(url_for("project_tasks", projectUrl=task.projectUrl))

@app.route("/login", methods=["POST","GET"])
def login():
	if session.get("logged_in"):
		return redirect(url_for("list_projects"))
	if request.method == "POST":
		try:
			u = User.login(request.form["username"], request.form["password"])
			session["logged_in"] = True
			session["uid"] = u.objectId
		except:
			flash("bad login")

	return render_template("login.html")
@app.route("/logout")
def logout():
	if not session.get("logged_in"):
		return redirect(url_for("login"))
	else:
		session.pop("logged_in", None)
		return redirect(url_for("login"))

if __name__ == "__main__":
	app.secret_key = "907470"
	app.run(debug=True)
