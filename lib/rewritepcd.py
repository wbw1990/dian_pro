 
# coding:utf-8
import open3d as o3d
import os
import numpy as np 
import json
import opener
from io import BytesIO,StringIO
import chardet #pip install chardet
# import magic    #pip install python-magic


BASE_DIR = os.path.dirname(os.path.abspath(__file__))   


file_path = os.path.join(BASE_DIR,'pcd','newpcd.pcd.objects')

# # 创建magic对象
# magic_obj = magic.Magic()

# # 获取文件类型
# file_type = magic_obj.from_file(file_path)

# # 检查是否为应用程序/octet-stream类型
# if file_type == 'application/octet-stream':
#     # 处理应用程序/octet-stream类型
#     ...

# opener.open()

with open(file_path,'rb+') as f:
    data = f.read()
    ss  = str(data)
    type = chardet.detect(data)
    print(type)
    print(data.decode(type['encoding']))


with open(file_path,'rb+') as f:

    con = f.read()
    # sss= str(con, 'UTF-8')

    # print(sss)
    f = BytesIO(con)
    ss= f.read()
    print(ss)
#     sss = bytes.decode(f.read())
#     print(sss)


with opener.open(os.path.join(BASE_DIR,'pcd','bdz.pcd.objects'),'rb+') as f:

    # new_dict = json.load(f)
    # print(new_dict)
    # con= cStringIO.StringIO(f.read())
    con = f.read()
    info = ''.join([chr(i) for i in [int(b, 2) for b in con.split(' ')]])
    # info = str(con, encoding='utf-8')
    # dic = json.load(con)
    # dic = con.decode('utf-8')
    # print(dic)



print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud(os.path.join(BASE_DIR,'pcd','newpcd.pcd'))
print(pcd)

colors = np.asarray(pcd.colors) * 255
points = np.asarray(pcd.points)
# print(points.shape, colors.shape)
# 	return np.concatenate([points, colors], axis=-1)
# return points
 
 
print("->正在RANSAC平面分割...")
distance_threshold = 1   # 内点到平面模型的最大距离
ransac_n = 3                # 用于拟合平面的采样点数
num_iterations = 1000       # 最大迭代次数
 
# 返回模型系数plane_model和内点索引inliers，并赋值
plane_model, inliers = pcd.segment_plane(distance_threshold, ransac_n, num_iterations)
 
# 输出平面方程
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
 
# 平面内点点云
inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([0, 0, 1.0])
#print(inlier_cloud)
 
# 平面外点点云
outlier_cloud = pcd.select_by_index(inliers, invert=True)
#outlier_cloud.paint_uniform_color([1.0, 0, 0])
print(outlier_cloud)

newoutlier = outlier_cloud.uniform_down_sample(8)
#newoutlier.paint_uniform_color([1.0, 0, 0])
print(newoutlier)

#newlier = outlier_cloud.uniform_down_sample(20)

o3d.io.write_point_cloud("newquchudimian200.pcd",newoutlier)


# 可视化平面分割结果
# o3d.visualization.draw_geometries([ outlier_cloud],window_name="去除地面的效果图")
o3d.visualization.draw_geometries([newoutlier],window_name="地面的效果图")
 
# def ransac_p(pcd):
#     print("->正在RANSAC平面分割...")
#     distance_threshold = 8.6  # 内点到平面模型的最大距离
#     ransac_n = 3  # 用于拟合平面的采样点数
#     num_iterations = 1000  # 最大迭代次数
 
#     # 返回模型系数plane_model和内点索引inliers，并赋值
#     plane_model, inliers = pcd.segment_plane(distance_threshold, ransac_n, num_iterations)
 
#     # 输出平面方程
#     [a, b, c, d] = plane_model
#     print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
 
#     # 平面内点点云
#     inlier_cloud = pcd.select_by_index(inliers)
#     inlier_cloud.paint_uniform_color([0, 0, 1.0])
#     print(inlier_cloud)
 
#     # 平面外点点云
#     outlier_cloud = pcd.select_by_index(inliers, invert=True)
#     outlier_cloud.paint_uniform_color([1.0, 0, 0])
#     print(outlier_cloud)
    
#     return inlier_cloud, outlier_cloud