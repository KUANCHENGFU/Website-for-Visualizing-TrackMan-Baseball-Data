# ========== import ==========
# basic
from flask import Flask, render_template, request
from model import InputForm
from compute import heatmap
from werkzeug.utils import secure_filename
import os


# ========== initialize ==========
app = Flask(__name__)
app.config.from_pyfile('config.py')

# ========== upload ==========
UPLOAD_DIR = 'uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.secret_key = 'MySecretKey'

if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def allowed_file(filename):
    """Does filename have the right extension?"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# ========== main ==========
@app.route("/", methods=['GET', 'POST'])
def home():

    form = InputForm(request.form)
    filename = None
    if request.method == 'POST':

        if request.files:
            file = request.files[form.FileName.name]

            if file and allowed_file(file.filename):
                # Make a valid version of filename for any file ystem
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))

        result = heatmap(filename,
                         form.Goal.data,
                         form.PitchType.data,
                         form.PitcherThrows.data,
                         form.BatterSide.data
                         )

    else:
        result = None

    return render_template('home.html', form=form, result=result)


if __name__ == '__main__':
    app.run(debug=True)
