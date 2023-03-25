from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import live_mask_detector
import image_mask_detector
import video_mask_detector

app=Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER='static/results/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER']=RESULT_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live', methods=['GET','POST'])
def live_detection():
    live_mask_detector.live_stream()
    return redirect('/')

@app.route('/video')
def video_detection():
    return render_template('video_detector.html')

@app.route('/video',methods=['POST'])
def upload_video():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_mask_detector.video_stream(path)
    return render_template('video_detector.html')

@app.route('/image')
def image_detection():
    return render_template('image_detector.html')

@app.route('/image',methods=['POST'])
def upload_image():
    print(request)
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('image_detector.html',filename=filename)

@app.route('/image/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/image/detect/<filename>')
def detect(filename):
    path='static/uploads/'+filename
    img=image_mask_detector.mask_image(path)
    img.save(os.path.join(app.config['RESULT_FOLDER'], filename))
    return redirect(url_for('static', filename='results/' + filename), code=301)


@app.route('/image/result/<filename>')
def result_image(filename):
    return redirect(url_for('static', filename='results/' + filename), code=301)







    

if __name__=='__main__':
    app.run(debug=True)