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

@app.route("/thread/edit", methods=["get","post"])
def edit():
    message_id = request.form["message_id"]
    thrd = request.form["thread_id"]
    content = request.form["content"]
    messages.edit(message_id, content)
    return redirect("/thread/"+str(thrd))

@app.route("/thread/edit_starter/<int:id>", methods=["get","post"])
def starter_edit(id):
    content = request.form["content"]
    threads.edit_content(id, content)
    return redirect("/thread/"+str(id))

@app.route("/friendlist/<int:id>", methods=["get","post"])
def add_friends_to_thread(id):
    if request.method == "POST":
        return redirect("/thread/"+str(id))
    friends = users.get_friends(id)
    for friend in friends:
        print(friend[0])
    starter = threads.get_thread(id)
    title = starter[0][0]
    return render_template("add_f_to_threads.html", friends=friends, title=title, id=id)

@app.route("/add_friends_to_thread/<int:id>", methods=["get", "post"])
def add_f(id):
    friend = request.form["friend"]
    friend_id = request.form[friend]
    threads.add_user(friend_id, id)
    return redirect("/friendlist/"+str(id))

@app.route("/new_thread")
def new():
    if users.logged() != True:
        return redirect("/login")
    return render_template("new_thread.html", error=False, title="")

@app.route("/send", methods=["post"])
def send_thread():
    title = request.form["title"]
    content = request.form["content"]
    privat = request.form["private"]
    thread_id = 0
    if int(privat) == 0:
        thread_id = threads.new_thread(title, content, 0)
    if int(privat) == 1:
        thread_id = threads.new_thread(title, content, 1)
    if thread_id == 0:
        return render_template("new_thread.html", error=True, title=title, content=content)
    return redirect("/thread/"+str(thread_id))

@app.route("/search", methods=["get","post"])
def search():
    srch_word = request.form["srch"]
    if srch_word == "":
        return redirect("/")
    t = request.form["thrd"]
    m = request.form["mssg"]
    title_list = []
    message_list = []
    from_t = False
    from_m = False
    if t == "t":
        from_t = True
        title_list = threads.search(srch_word)
    if m == "m":
        from_m = True
        message_list = messages.search(srch_word)
    return render_template("search_results.html", title_list=title_list, message_list=message_list, from_m=from_m, from_t=from_t)

@app.route("/save/<int:id>", methods=["get","post"])
def save(id):
    if users.logged():
        users.save(id)
    return redirect("/thread/"+str(id))


#Profiili

@app.route("/profile/<int:user_id>", methods=["get","post"])
def profile(user_id):
    if request.method == "POST":
        users.add_friend(user_id)
    username = users.get_name(user_id)
    public_threads = users.get_threads(user_id, 0)
    private_threads = users.get_threads(user_id, 1)
    followed = users.get_saved(user_id)
    friend_requests = users.get_friend_requests()
    own_profile = False
    if (user_id==users.user_id()):
        own_profile = True
    return render_template("profile.html", username=username, public_threads=public_threads,
    private_threads=private_threads, followed=followed, f_requests=friend_requests, profile_id=user_id, own=own_profile)

@app.route("/profile")
def my_profile():
    if (users.logged() == False):
        return redirect("/")
    profile(users.user_id())
    return redirect("/profile/"+str(users.user_id()))

@app.route("/add_friend/<int:id>", methods=["post"])
def add_friend(id):
    users.add_friend(id)
    my_profile()
    return redirect("/profile/"+str(users.user_id()))

@app.route("/reject/<int:id>", methods=["post"])
def delete_friend(id):
    users.delete_friend(id)
    my_profile()
    return redirect("/profile/"+str(users.user_id()))

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
