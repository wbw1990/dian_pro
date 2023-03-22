# coding:utf-8
import open3d as o3d
import os
import numpy as np 
import cv2
from lib.utils import * 
from lib.config import * 

class PCDOperator():


    def __init__(self, pcs_path, obj_path, tai_path):
        self.objects =[]
        self.points =[]
        self.load(pcs_path, obj_path, tai_path)

        pass


    def load(self,pcd_path, obj_path, tai_path):
        
        if pcd_path !='':
            self.pcd = o3d.io.read_point_cloud(pcd_path)
            self.points = np.asarray(self.pcd.points)

        if obj_path !='':
            self.objects = load_json(obj_path)

        if tai_path !='':
            self.devices = load_json(tai_path)
        
        self.device_points = {}

        # for dev in self.devices:
        #     d_points,classIndex = self.get_position_by_device_id(dev['id'])
        #     dev['classIndex'] = classIndex
        #     self.device_points[dev['id']] = d_points

        self.device_points['04M72000034629775'] = [np.array([-713,135,136])]
        self.device_points['04M72000034629777'] = [np.array([-699,119,138])]
        self.device_points['04M72000034629776'] = [np.array([-711,123,138])]
        self.device_points['04M72000034629771'] = [np.array([-721,136,141])]
        self.device_points['04M72000034629772'] = [np.array([-708,131,142])]
        self.device_points['04M72000034629773'] = [np.array([-696,125,136])]
        
        # self.colors = np.asarray(pcd.colors) * 255

    def cal_nearst_point(self,x1, y1, z1, device_id):
        distince = 1000000000
        points = self.get_position_by_device_id(device_id)
            # points = points[0:4]  #--------------------
        # current_dis = distince
        near_point = None
        for p in points:
            dis = get_distince(np.float64(x1),np.float64(y1),np.float64(z1) ,np.float64(p[0]) ,np.float64(p[1]) ,np.float64(p[2]))
            if dis< distince:
                near_point = p
                distince = dis
        
        return near_point, distince

    def cal_nearest_distince(self, x1, y1, z1, device_ids):

        distince=1000000000
        near_device = None
        near_point =  None
        for id in device_ids:
            cur_point, current_dis = self.cal_nearst_point(x1, y1, z1,id)
            if current_dis<distince:
                distince = current_dis
                near_point = cur_point
                near_device = self.get_device_by_id(id)

        return distince, near_device, near_point
    
    def get_point_ids_by_device_ids(self,device_ids):
        point_ids = []
        for ob in self.objects:
            if ob['device_id'] in device_ids:
                s_p =  ob['points']
                point_ids = point_ids + s_p

        return point_ids
    
    def get_position_by_device_id(self, device_id):

        return self.device_points[device_id]
    
        # for ob in self.objects:
        #     if ob['device_id'] == device_id:
        #         point_ids = ob['points']
        #         classIndex = ob['classIndex']
        #         # point_ids = point_ids[0:4]  #--------------------
        #         positions = self.get_points_by_ids(point_ids)
        #         return positions, classIndex
        
        # return []


    def get_xy_points_by_ids(self, ids):
        
        list = []
        for id in ids:
            list.append((int(self.points[id][0]),int(self.points[id][1])))
        return list
    
    def get_points_by_ids(self, ids):
        
        list = []
        for id in ids:
            list.append(self.points[id])
        return list 
    
    def get_min_area_rect(self, points_xy):
        # c_points_xy =[]
        # for p in points_xy:
        #     c_points_xy.append((p[0]+2000,p[1]+2000))
        box = cv2.minAreaRect(np.array(points_xy,dtype=np.float32))
        points = cv2.boxPoints(box)

        # result = []
        # for point in points:
        #     result.append(np.array([point[0]-2000,point[1]-2000 ]))
        # result = np.array(result)
        return points
    
    def convert_box(self, points, min_h):
        result = []
        for p in points:
            item1 =[int(p[0]),int(p[1]),int(min_h)]

            result.append(item1)

        return result
    
    def get_point_height(self, points):

        min_h = 100000
        max_h = -100000
        for p in points:
            if p[2] < min_h:
                min_h = p[2]
            if p[2] > max_h:
                max_h = p[2]

        return int(min_h), int(max_h)

    def get_rec(self, points):
        min_x = min(points[0][0],points[1][0],points[2][0],points[3][0])
        min_y = min(points[0][1],points[1][1],points[2][1],points[3][1])
        max_x = max(points[0][0],points[1][0],points[2][0],points[3][0])
        max_y = max(points[0][1],points[1][1],points[2][1],points[3][1])
        return (min_x, min_y, max_x, max_y)

    # iou: https://blog.csdn.net/qq_35896136/article/details/105518416
    def compute_iou(self, rec1, rec2):
        """
        computing IoU
        rec1: (x0, y0, x1, y1)
        rec2: (x0, y0, x1, y1)
        :return: scala value of IoU
        """
        # computing area of each rectangle
        S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
        S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

        # computing the sum_area
        sum_area = S_rec1 + S_rec2

        # find the each edge of intersect rectangle
        left_line = max(rec1[1], rec2[1])
        right_line = min(rec1[3], rec2[3])
        top_line = max(rec1[0], rec2[0])
        bottom_line = min(rec1[2], rec2[2])
        # print(top_line, left_line, right_line, bottom_line)

        # judge if there is an intersect area
        if left_line >= right_line or top_line >= bottom_line:
            return 0
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            return (intersect / (sum_area - intersect)) * 1.0

    def find_device_by_name(self, name):

        col_names = ['dianya', 'name', 'type_name', 'jiange', 'run_code', 'remark1', 'remark2', 'remark3', 'remark4', 'remark5', 'remark6']
        devices = self.devices
        for col in col_names:

            res_devices = self.find_device_by(devices,col,name)

            if len(res_devices) ==0:
                continue
            elif len(res_devices) == 1:
                devices = res_devices
                break
            else:
                if col == 'type_name':
                    type_names =[]
                    for i in res_devices:
                        if i['type_name'] not in type_names:
                            type_names.append(i['type_name'])
                    if len(type_names)>1:
                        last_one = type_names[-1]
                        res_devices_t = []
                        for i in res_devices:
                            if i['type_name'] == last_one:
                                res_devices_t.append(i)
                        res_devices= res_devices_t

                devices = res_devices
        
        print('解析结果:--------------- start ---------------')
        print('共 【'+str(len(devices)) + '】 条数据')

        result = []
        if len(devices)>6:
            return result
        
        for d in devices:
            print('------------------------------')
            print('设备名称:' + d['name'])
            print('json:',d)
            result.append({'id':d['id'],'uuid':d['uuid'],'name':d['name'], 'person_safe':d['person_safe'], 'car_safe':d['car_safe']})
        print('------------------------------')
        print('------------------------------')
        print('------------------------------')
        print('------------------------------')
        print('------------------------------')
        print('------------------------------')
        


        return result

        
    def find_device_by(self, devices, col_name, name):
        data = []
        for d in devices:  
            col = str(d[col_name])

            if col!='' and col in name:
                data.append(d)

        return data

    def get_device_by_id(self, device_id):

        for dev in self.devices:
            if dev['id'] == device_id:
                return dev
        return None


if __name__ == '__main__':
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
    print("->正在加载点云... ")
    path = os.path.join(BASE_DIR,'pcd','newpcd.pcd')


    tai_path = os.path.join(BASE_DIR,'pcd','tai.json')
     
    pcd_opr = PCDOperator('','',tai_path)
    
    # content = '应在500kV台彭一线5022断路器及其就地控制柜、500kV台彭一线5022-2隔离开关、500kV台彭一线√5023断路器及其就地控制柜、500kV台彭一线5023-1隔离开关、500kV台彭二线5031断路器及其就地控制柜、500kV台彭二线5031-2隔离开关、500kV台彭二线/台宗一线5032断路器及其就地控制柜、500kV台彭二线/台宗一线5032-1隔离开关、500kV台彭一线线路电压互感器、500kV台彭一线线路避雷器、500kV台彭二线线路电压互感器、500kV台彭二线线路避雷器、500kV台彭一线出线套管及相邻的检修电源箱处设置围栏，挂“止步，高压危险”标示牌，字面向里并留有通道'
    # content2 = '、应在1000kV洪台Ⅰ线T021/T022高压电抗器及其端子箱、1000kV洪台Ⅰ线T021/T022高压电抗器风冷√控制箱、1000kV洪台Ⅰ线T021/T022中性点小电抗、1000kV洪台Ⅰ线T021/T022高压电抗器中性点避雷器、1000kV洪台Ⅰ线T021断路器及其就地控制柜、1000kV洪台Ⅰ线T022断路器及其就地控制柜、1000kV洪台Ⅰ线T0212隔离开关、1000kV洪台Ⅰ线T0221隔离开关、1000kV洪台Ⅰ线T021/T022避雷器、1000kV洪台Ⅰ线T021/T022电压互感器及相邻的检修电源箱处设围栏'
    # content = content + content2
    content = '1000kV洪台Ⅰ线T021/T022高压电抗器中性点避雷器'
    names = content.split('、')
    for name  in names :
        print('--------------------工作票识别名称 【'+name+'】 --------------------')

        devices= pcd_opr.find_device_by_name(name)











    pass
    device_ids = [10,13,17,19]
    ela_device_ids = [12,16,17,19]
    pcd_opr = PCDOperator(path)



    points = pcd_opr.get_xy_points_by_ids(device_ids)
    print(points)
    print('--------------------------')

    box = pcd_opr.get_min_area_rect(points)

    print(box)
    rec =  pcd_opr.get_rec(box)
    print(rec)
    print('--------------------------')

    points = pcd_opr.get_points_by_ids(device_ids)
    print(points)
    print('--------------------------')

    min_h, max_h  = pcd_opr.get_point_height(points)
    print(min_h)
    print(max_h)
    print('--------------------------')

    points = pcd_opr.get_xy_points_by_ids(ela_device_ids)
    box2 = pcd_opr.get_min_area_rect(points)
    print(box2)
    rec2 =  pcd_opr.get_rec(box2)
    print(rec2)
    print('--------------------------')

    iou = pcd_opr.compute_iou(rec,rec2)
    print(iou)
    print('--------------------------')


    box3 = pcd_opr.convert_box(points,max_h)
    print(box3)
    print('--------------------------')


    obj_path = os.path.join(BASE_DIR,'pcd','bdz.pcd.objects')