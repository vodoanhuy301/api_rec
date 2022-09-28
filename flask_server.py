from flask import Flask,redirect,url_for,render_template,request,jsonify
from face import tagging_image
import json
from flask_cors import CORS

app=Flask(__name__)
cors = CORS(app)
@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/face_recognition',methods=['POST'])
def face_recognition():
    res = request.data
    obj = json.loads(res)
    base64_str=obj['base64']
    result = tagging_image(base64_str)
    if (result!="null"):
        return json.dumps(result,indent = 4)
    else:
        return json.dumps({'name':"Không tìm thấy gương mặt", 'similarity': '0'},indent = 4)

# @app.route('/test',methods=['POST'])
# def test():
#     res = request.data
#     obj = json.loads(res)
#     return obj['base64']
### Result checker
# @app.route('/results/<int:marks>')
# def results(marks):
#     result=""
#     if marks<50:
#         result='fail'
#     else:
#         result='success'
#     return redirect(url_for(result,score=marks))

    

if __name__=='__main__':
  app.run (host = "localhost", port = 9566)