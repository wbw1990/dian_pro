# pip install pdfplumber -i https://pypi.tuna.tsinghua.edu.cn/simple
# https://bbs.huaweicloud.com/blogs/373410

import os

from flask import Flask,Blueprint,request,jsonify,make_response
import json
from werkzeug.utils import secure_filename
from lib.domain import AreaStore
from lib.utils import *
from lib.pcd_operator import PCDOperator
import random

step = 0

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

        #识别
        name,contents,elec_contents = read_pdf(absolute_path)

        ass = AreaStore(name)
        for it in contents:
            # ass.add_device(it['area'],it['device'])
            ass.add_device_name(it['device'])

        for it in elec_contents:
            ass.add_elec_device_name(it)
        

        result =  ass.to_dict()

        
        devices=[]
        elec_devices= []

        for device_name in result['devices_names']:
            print('--------------------工作票识别名称 【'+device_name+'】 --------------------')
            ls = pcd_opr.find_device_by_name(device_name)
            for l in ls:
                devices.append(l)

        for elec_device_name in result['elec_devices_names']:
            print('--------------------工作票识别名称 【'+elec_device_name+'】 --------------------')
            ls = pcd_opr.find_device_by_name(elec_device_name)
            for l in ls:
                elec_devices.append(l)
                
        rsp = {
            'name':result['name'],
            'devices': devices,
            'elec_devices': elec_devices
        }
        
        os.remove(absolute_path)

        
        return jsonify(rsp), 200

    except Exception as e:
        return error(e.args[0])

@app.route("/get_safe_area", methods=["POST"])
def get_safe_area():

    jsonDict = json.loads(request.get_data(as_text=True))
    device_ids  = jsonDict['device_ids']
    elec_device_ids = jsonDict['elec_device_ids']

    device_ids = pcd_opr.get_point_ids_by_device_ids(device_ids)
    elec_device_ids = pcd_opr.get_point_ids_by_device_ids(elec_device_ids)
    # device_ids = device_ids[0:4] #--------------------
    # elec_device_ids = elec_device_ids[0:4]  #--------------------

    if len(device_ids) > 0 and len(elec_device_ids)>0:
        points = pcd_opr.get_xy_points_by_ids(device_ids)
        box = pcd_opr.get_min_area_rect(points)
        rec =  pcd_opr.get_rec(box)

        points2 = pcd_opr.get_xy_points_by_ids(elec_device_ids)
        box2 = pcd_opr.get_min_area_rect(points2)
        rec2 =  pcd_opr.get_rec(box2)

        iou = pcd_opr.compute_iou(rec,rec2)

        safe_distance = 0

        points_all = pcd_opr.get_points_by_ids(device_ids)
        # points_all = points_all[0:4]  #--------------------
        min_h, max_h  = pcd_opr.get_point_height(points_all)
        if iou >0:

            elec_points_all = pcd_opr.get_points_by_ids(elec_device_ids)
            # elec_points_all = elec_points_all[0:4]  #--------------------
            min_h2, max_h2  = pcd_opr.get_point_height(elec_points_all)

            safe_distance = min_h - min_h2


        box3 = pcd_opr.convert_box(box,min_h)
        h = max_h - min_h

        # print(result)
        result = {'data': box3, 'height': h, 'safe_distance': safe_distance}
        return jsonify(result), 200
    else: 
        result = {'data': [], 'height': 0, 'safe_distance': 0}
        return jsonify(result), 200


@app.route("/get_position", methods=["POST"])
def get_position():
    global step
    jsonDict = json.loads(request.get_data(as_text=True))
    biaoqians = jsonDict['biaoqian']
# 原点坐标
    # o_x = -713.349609375
    # o_y = 149.6861572265625
    # o_z = 166.3239288330078
        # base_x = -719
        # base_y = 215
        # base_z = 134
    result= [] 

    for bq in biaoqians:
        # x1,y1,z1 = latlontoxyz(lng, lat, height)
        base_x = -720
        base_y = 153
        base_z = 134
        step = step + 1 
        if step == 50:
            step = 0
        
        print("step" + str(step))
        # x = random.randint(0,15)
        # y = random.randint(0,15)
        z = 0 #random.randint(0,1)

        x = base_x 
        y = base_y -step
        z = base_z + z


        code = bq['code']
        type = bq['type']
        item = {'code': code, 'type': type, 'x': x, 'y': y,'z':z}
        result.append(item)
        
    
    elec_device_ids = jsonDict['elec_device_ids']
    
    for r in result:
        distince, near_device, near_point = pcd_opr.cal_nearest_distince(r['x'],r['y'],r['z'],elec_device_ids)
        safe_dis = 0
        if r['type'] == 'person':
            safe_dis = near_device['person_safe']
        else:
            safe_dis = near_device['car_safe']

        if distince< safe_dis:
            r['alarm'] = True
        else:
            r['alarm'] = False
        
        r['distince'] = distince
        r['near_device'] = near_device
        r['near_point'] = near_point.tolist()

    
    # 115.599801, 39.138076 
    
    return jsonify(result), 200


if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

    AREA_LIST = ['1000kV设备区','500kV设备区','220kV设备区','110kV设备区','35kV设备区','主变设备区']
    
    pcd_path = os.environ.get("PCD_PATH", os.path.join(BASE_DIR,'pcd','bdzdianyun.pcd'))
    pro_path = os.environ.get("PRO_PATH", os.path.join(BASE_DIR,'pcd','pro.pcd.json'))
    tai_path = os.environ.get("TAI_PATH", os.path.join(BASE_DIR,'pcd','tai.json'))

     
    print("->正在加载点云... ")
    pcd_opr = PCDOperator(pcd_path, pro_path ,tai_path)
    print("->加载点云完成... ")

    app.run(
        host='0.0.0.0',
        port= 80,
        debug=False
        )
    
# 115.599801, 39.138076 
    # print('---------- ---------- ----------')
    # # print(result)
    # print(result2)
    # print('---------- finished ----------')

# 0300c3dfdb8afa98925b01653f015b0300c28501e8
# e9547475be8afa98935a712e89015ae9511515668c