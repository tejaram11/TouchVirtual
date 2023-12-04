from flask import Flask,render_template,Response, stream_with_context
from hand_roi import detector


detect=detector()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def gen(detect):
    while True:
        frame=detect.hand_detector()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

@app.route("/video")
def stream():
    return render_template("video.html")

@app.route("/video_frame")
def video_frame():
    return Response(stream_with_context(gen(detect)), mimetype='multipart/x-mixed-replace;boundary=frame')

'''        
@app.route("/home")
def start():
    return Response(gen(detect),mimetype='multipart/x-mixed-replace;boundary=frame')
'''

app.run(debug=True)