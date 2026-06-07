import flask
import file_manager
from flask import render_template, send_from_directory

PICTURES_ROOT_FOLDER = "/home/pi/Pictures"

app = flask.Flask(__name__, static_folder=PICTURES_ROOT_FOLDER, template_folder='templates')

@app.route("/")
def index():
    fm = file_manager.FileManager(PICTURES_ROOT_FOLDER)
    folders = fm.get_folders()
    return render_template('index.html', folders=folders)

@app.route("/<dirname>")
def directory(dirname):
    fm = file_manager.FileManager(PICTURES_ROOT_FOLDER)
    folder = fm.get_folder(dirname)
    if folder:
        images = fm.get_images_in_folder(folder.name)
        return render_template('gallery.html', folder=folder, images=images)
    return "Folder not found", 404

@app.route("/<dirname>/<filename>")
def image(dirname, filename):
    return send_from_directory(PICTURES_ROOT_FOLDER + "/" + dirname, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
