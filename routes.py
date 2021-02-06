from app import app
from flask import render_template, request, redirect
import users
import messages

@app.route("/")
def home():
    list = messages.get_threads()
    return render_template("home.html", threads = list)

@app.route("/thread/<int:id>", methods=["get","post"])
def thread(id):
    if request.method == "POST":
        content = request.form["content"]
        if (content != ""):
            messages.add_message(content, id)
    if users.logged() == True:
        is_admin = users.is_admin()
    else:
        is_admin = False
    list = messages.get_messages(id)
    starter = messages.get_thread(id)
    return render_template("thread.html", starter = starter, messages = list, id = id, is_admin = is_admin, message_id = 0)

@app.route("/thread/edit", methods=["get","post"])
def edit():
    message_id = request.form["message_id"]
    thrd = request.form["thread_id"]
    content = request.form["content"]
    messages.edit(message_id, content)
    return redirect("/thread/"+str(thrd))

@app.route("/thread/edit/<int:id>", methods=["get","post"])
def del_or_edit(id):
    option = request.form["option"+str(id)]
    thrd = request.form["thread_id"]
    if (option != "empty"):
        if option == "delete":
            messages.delete(id)
        if option == "edit":
            is_admin = users.is_admin()
            list = messages.get_messages(thrd)
            starter = messages.get_thread(thrd)
            return render_template("thread.html", starter = starter, messages = list, id = thrd, is_admin = is_admin, message_id = id)
    return redirect("/thread/"+str(thrd))

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["get", "post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.signup(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/new_thread")
def new():
    if users.logged() != True:
        return redirect("/login")
    return render_template("new_thread.html")

@app.route("/send", methods=["post"])
def send_thread():
    title = request.form["title"]
    content = request.form["content"]
    #mahdollisuus luoda privaatti thread
    thread_id = messages.new_thread(title, content)
    if thread_id == 0:
        #error viesti ? kirjautumaton käyttäjä
        return redirect("/")
    return redirect("/thread/"+str(thread_id))
