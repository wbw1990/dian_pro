# pip install pdfplumber -i https://pypi.tuna.tsinghua.edu.cn/simple
# https://bbs.huaweicloud.com/blogs/373410

import os

from flask import Flask,Blueprint,request,jsonify,make_response
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

@app.errorhandler(500)
def error(error):
    return make_response(jsonify({'error': error}), 500)


@app.route("/upload_file", methods=["POST"])
def upload_file():

    try:
        save_path = os.path.join(BASE_DIR,'piao') 
        if not os.path.exists(save_path):
            os.makedirs(save_path) 
            # shutil.rmtree(save_path)
        # os.makedirs(save_path) 

        file = request.files.get('file')
        # 判断是否有空文件
        if file is None:
            return error("No upload file.")

        
        filename = secure_filename(file.filename)
        # filepath, shotname, extension = get_filePath_fileName_fileExt(filename)


        absolute_path = os.path.join(save_path, filename)
        file.save(absolute_path)

       
        
        return jsonify(absolute_path), 200

    except Exception as e:
        return error(e.args[0])

if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

    app.run(
        host='0.0.0.0',
        port= 80,
        debug=False
        )
    