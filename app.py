import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from ocr_core import imgstring,textspeech,openfile,applythresh
from PIL import Image

# define upload folder
UPLOAD_FOLDER = '/static/files/'
UPLOAD_FOLDER_AUDIO = '/static/audio/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check file extention
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route to handle upload page
@app.route('/home', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('home.html', msg='No file selected')
        file = request.files['file']
     
        # if no file is selected
        if file.filename == '':
            return render_template('home.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # save it to Files folder
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/files', filename))

            # open file
            openfiles = openfile(file)

            # apply threshold
            thresh = applythresh(openfiles)

            # call OCR function
            extracted_text = imgstring(thresh)
        
            # call gTTS function
            filenameaudio = str(filename)
            audio = os.path.splitext(filenameaudio)[0]
            audiofile = audio + '.mp3'
            extracted_audio = textspeech(extracted_text)
            extracted_audio.save(os.path.join('static/audio/', audiofile))   

            # extract the text and display 
            return render_template('home.html',msg='Success', extracted_text=extracted_text, img_src= UPLOAD_FOLDER + file.filename, audio_src= UPLOAD_FOLDER_AUDIO + audiofile)

    elif request.method == 'GET':
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)