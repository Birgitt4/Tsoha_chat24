from app import app
from flask import render_template, request, redirect
import users
import messages
import threads

@app.route("/")
def home():
    list = threads.get_threads()
    return render_template("home.html", threads=list)

@app.route("/thread/<int:id>/<int:m_id>/<int:e>")
def thread(id, m_id, e):
    allow = False
    list = messages.get_messages(id)
    starter = threads.get_thread(id)
    if starter[0][4] == 1:
        if users.logged():
            if users.private_access(id):
                allow = True
    elif starter[0][4] == 0:
        allow = True
    if users.logged() == True:
        is_admin = users.is_admin()
    else:
        is_admin = False
    return render_template("thread.html", starter=starter, messages=list, id=id, 
        is_admin=is_admin, message_id=m_id, allow=allow, error=error(e))

@app.route("/thread/<int:id>")
def to_thread(id):
    return redirect("/thread/"+str(id)+"/0/0")

def error(e):
    error = ""
    if e == 1:
        error = "Viesti on liian pitkä. Viestin pituus on max 500 merkkiä"
    elif e == 2:
        error = "Viesti ei voi olla tyhjä"
    elif e == 3:
        error = "Kirjaudu sisään lähettääksesi viestin"
    return error

@app.route("/thread/add/<int:id>", methods=["get", "post"])
def new_message(id):
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    e = 0
    content = request.form["content"]
    if not users.logged():
        e = 3
        print("false")
    elif len(content) > 500:
        e = 1
    elif len(content) == 0:
        e = 2
    elif 0 < len(content) <=500:
        messages.add_message(content, id)
    return redirect("/thread/"+str(id)+"/0/"+str(e))

@app.route("/thread/edit/<int:id>", methods=["get", "post"])
def del_or_edit(id):
    option = request.form["option"+str(id)]
    thrd = request.form["thread_id"]
    if (option != "empty"):
        if option == "delete":
            messages.delete(id)
        elif option == "edit":
            return redirect("/thread/"+str(thrd)+"/"+str(id)+"/0")
    return redirect("/thread/"+str(thrd))

@app.route("/thread/edit", methods=["get","post"])
def edit():
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    e = 0
    message_id = request.form["message_id"]
    thrd = request.form["thread_id"]
    content = request.form["content"]
    if len(content) > 500:
        e = 1
    elif len(content) == 0:
        e = 2
    else:
        messages.edit(message_id, content)
    return redirect("/thread/"+str(thrd)+"/0/"+str(e))

@app.route("/thread/edit_starter/<int:id>", methods=["get", "post"])
def starter_edit(id):
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    content = request.form["content"]
    e = 0
    if len(content) > 500:
        e = 1
    elif len(content) == 0:
        e = 2
    else:
        threads.edit_content(id, content)
    return redirect("/thread/"+str(id)+"/0/"+str(e))

@app.route("/save/<int:id>")
def save(id):
    allow = False
    if users.logged():
        if threads.is_private(id):
            print("on yksityinen")
            allow = False
        else:
            allow = True
        if allow:
            users.save(id)
    return redirect("/thread/"+str(id))

@app.route("/friendlist/<int:id>")
def friends_to_thread(id):
    allow = False
    if threads.get_thread(id)[0][3] == users.user_id():
        allow = True
    if allow:
        friends = users.get_friends(id)
        starter = threads.get_thread(id)
        title = starter[0][0]
        return render_template("friendlist.html", friends=friends, title=title, id=id)
    return redirect("/thread/"+str(id))

@app.route("/add_friends/<int:id>", methods=["get", "post"])
def add_f(id):
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    friend = request.form["friend"]
    friend_id = request.form[friend]
    threads.add_user(friend_id, id)
    return redirect("/friendlist/"+str(id))

@app.route("/new_thread")
def new():
    if users.logged() != True:
        return redirect("/login")
    return render_template("new_thread.html", error=False, title="")

@app.route("/send", methods=["get", "post"])
def send_thread():
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    title = request.form["title"]
    content = request.form["content"]
    privat = request.form["private"]
    message = ""
    error = False
    thread_id = 0
    if len(content) > 500:
        message = "Viesti saa olla max 500 merkkiä"
        error = True
    elif len(content) == 0:
        message = "Viesti ei voi olla tyhjä"
        error = True
    elif len(title) > 100:
        message = "Otsikko saa olla max 100 merkkiä"
        error = True
    elif len(title) == 0:
        message = "Otsikko ei saa olla tyhjä"
        error = True
    if not error:
        if int(privat) == 0:
            thread_id = threads.new_thread(title, content, 0)
        if int(privat) == 1:
            thread_id = threads.new_thread(title, content, 1)
        if thread_id == 0:
            message = "Jokin meni vikaan, yritä uudelleen"
            error = True
    if error:
        return render_template("new_thread.html", error=True, title=title, content=content, message=message)
    return redirect("/thread/"+str(thread_id))

@app.route("/search", methods=["get", "post"])
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
    return render_template("search_results.html", title_list=title_list, 
        message_list=message_list, from_m=from_m, from_t=from_t)


@app.route("/profile/<int:user_id>", methods=["get", "post"])
def profile(user_id):
    if request.method == "POST":
        if users.session["csrf_token"] != request.form["csrf_token"]:
            #abort
            pass
        users.add_friend(user_id)
    username = users.get_name(user_id)
    public_threads = users.get_threads(user_id, 0)
    private_threads = users.get_threads(user_id, 1)
    followed = users.get_saved(user_id)
    friend_requests = users.get_friend_requests()
    own_profile = False
    if (user_id == users.user_id()):
        own_profile = True
    return render_template("profile.html", username=username, public_threads=public_threads,
        private_threads=private_threads, followed=followed, f_requests=friend_requests, 
        profile_id=user_id, own=own_profile)

@app.route("/profile")
def my_profile():
    if (users.logged() == False):
        return redirect("/")
    profile(users.user_id())
    return redirect("/profile/"+str(users.user_id()))

@app.route("/add_friend/<int:id>", methods=["get", "post"])
def add_friend(id):
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    users.add_friend(id)
    my_profile()
    return redirect("/profile/"+str(users.user_id()))

@app.route("/reject/<int:id>", methods=["get", "post"])
def delete_friend(id):
    if users.session["csrf_token"] != request.form["csrf_token"]:
        #abort
        pass
    users.delete_friend(id)
    my_profile()
    return redirect("/profile/"+str(users.user_id()))


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
            message = "Väärä tunnus tai salasana"
            return render_template("login.html", error=True, message=message)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["get", "post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", error=False)
    if request.method == "POST":
        error = False
        message = ""
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 30:
            error = True
            message = "Käyttäjänimi on liian pitkä (max 30 merkkiä)"
        elif len(password) < 6:
            error = True
            message = "Salasanan on oltava vähintään 6 merkkiä"
        elif users.username_taken(username):
            error = True
            message = "Käyttäjänimi on jo käytössä"
        elif password != request.form["passcheck"]:
            error = True
            message = "Salasanat eivät täsmää"
        if error:
            return render_template("signup.html", error=True, message=message)
        if users.signup(username, password):
            return redirect("/login")
        else:
            message = "Rekisteröinti ei onnistunut"
            return render_template("signup.html", error=True, message=message)
