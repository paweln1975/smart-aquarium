import file_manager
from flask import Flask, render_template, send_from_directory, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

PICTURES_ROOT_FOLDER = "c:\\Users\\pawel\\Pictures"
app = Flask(__name__)

def get_secret_from_file(filename: str) -> str:
    with open(filename, "r") as f:
        content = f.read()
        return content

app = Flask(__name__, static_folder=PICTURES_ROOT_FOLDER, template_folder='templates')
app.secret_key = '51dd82d9db76728aacac869c2bf734856ac36bf3ef8e11724c5146d040bbe01e'

login_manager = LoginManager()
login_manager.init_app(app)
users = {'admin': {'password': get_secret_from_file("secret.txt")}}

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@login_manager.request_loader
def request_loader(request):
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    password = request.form.get("password")
    if password == users['admin']['password']:
        user = User()
        user.id = 'admin'
        login_user(user)
        return redirect("/")
    else:
        return redirect(url_for('login', error='invalid_password'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/")
@login_required
def index():
    print('Logged in as', current_user)
    fm = file_manager.FileManager(PICTURES_ROOT_FOLDER)
    folders = fm.get_folders()
    return render_template('index.html', folders=folders)

@app.route("/<dirname>")
@login_required
def directory(dirname):
    fm = file_manager.FileManager(PICTURES_ROOT_FOLDER)
    folder = fm.get_folder(dirname)
    if folder:
        images = fm.get_images_in_folder(folder.name)
        return render_template('gallery.html', folder=folder, images=images)
    return "Folder not found", 404

@app.route("/<dirname>/<filename>")
@login_required
def image(dirname, filename):
    return send_from_directory(PICTURES_ROOT_FOLDER + "/" + dirname, filename)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login', error='unauthorized'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
