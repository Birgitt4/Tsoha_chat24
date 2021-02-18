from app import app
from flask import render_template, request, redirect
import users
import messages
import threads

@app.route("/")
def home():
    list = threads.get_threads()
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
    starter = threads.get_thread(id)
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
            starter = threads.get_thread(thrd)
            return render_template("thread.html", starter = starter, messages = list, id = thrd, is_admin = is_admin, message_id = id)
    return redirect("/thread/"+str(thrd))

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
    thread_id = threads.new_thread(title, content, 0)
    print(thread_id)
    if thread_id == 0:
        #error viesti ? kirjautumaton käyttäjä
        return redirect("/")
    return redirect("/thread/"+str(thread_id))

#Profiili

@app.route("/profile/<int:user_id>")
def profile(user_id):

    username = users.get_name(user_id)
    public_threads = users.get_threads(user_id, 0)
    private_threads = users.get_threads(user_id, 1)
    followed = users.get_followed(user_id)
    return render_template("profile.html", username=username, public_threads=public_threads,
    private_threads=private_threads, followed=followed)

@app.route("/profile")
def my_profile():
    if (users.logged() == False):
        return redirect("/")
    user_id = users.user_id()
    profile(user_id)
    return redirect("profile/"+str(user_id))

#Sisään ja ulos kirjautumiset:

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error=True, message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["get", "post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", error=False)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.username_taken(username):
            message = "Käyttäjänimi on jo käytössä"
            return render_template("signup.html", error=True, message=message)
        if password != request.form["passcheck"]:
            message = "Salasanat eivät täsmää"
            return render_template("signup.html", error=True, message=message)
        if users.signup(username, password):
            return redirect("/login")
        else:
            message = "Rekisteröinti ei onnistunut"
            return render_template("signup.html", error=True, message=message)
