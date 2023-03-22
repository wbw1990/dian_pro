
import os

import time
import open3d as o3d
import numpy as np 
import json
from lib.pylvx import *

def LivoxFileRead(ReadFileName, verbose=False):
    # Input: Read File Name
    # Output: [y,z,x,distance(r),Lidar ID]
    
    Idx = 28
    rf = open(ReadFileName, 'rb')
    d = rf.read()
    print(d[0:16].decode())
    FSIZE = len(d)
    DeviceCount = d[Idx]
    Idx += 1
    print("LidarSN", d[Idx:Idx+16].decode())
    
    Idx = Idx + 59 * DeviceCount
    list1 = []
    
    end = 0
    
    while (Idx < FSIZE) :
        if verbose:
            print("Idx", Idx)
            print("current offset:", int.from_bytes(d[Idx:(Idx+8)],'little'))
            print("next offset:", int.from_bytes(d[Idx+8:(Idx+16)],'little'))
            print("frame index:", int.from_bytes(d[Idx+16:(Idx+24)],'little'))
        nxt = int.from_bytes(d[Idx+8:(Idx+16)],'little')
               
        Idx = Idx + 24
        
        while Idx < nxt:
            if Idx +10 >len(d):
                break       
            dtype = d[Idx+10]
            Idx = Idx + 19
            
            if dtype==6:
                # The data is gyro outputs. Please modify here if you want to use that data.
                Idx = Idx + 24
            elif dtype==2:
                # Data is point clouds.
                for i in range(96):
                    
                    B2D_X = int.from_bytes(d[Idx:Idx+4],'little', signed=True)
                    B2D_Y = int.from_bytes(d[Idx+4:Idx+8],'little', signed=True)
                    B2D_Z = int.from_bytes(d[Idx+8:Idx+12],'little', signed=True)
                    list_tmp = ([B2D_Y, 
                                 B2D_Z,
                                 B2D_X,
                                 d[Idx+12]
                                 ])
                    if not B2D_X+B2D_Y+B2D_Z==0 and B2D_X+B2D_Y+B2D_Z<1e6:
                        list1.append(list_tmp)
                    Idx = Idx + 14
            else:
                # Something is wrong..
                print("dtype",dtype)
                
    rf.close
    OutData = np.array(list1)
    return OutData


if __name__ == '__main__':

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
    lvx_path = os.environ.get("LVX_PATH", os.path.join(BASE_DIR,'pcd','dianyun','1.lvx'))
    
    
    # out_path = os.path.join(BASE_DIR,'pcd','to')
    # lvx = LvxFile(lvx_path)
    # topcds(lvx_path,out_path)

    # pcd = o3d.io.read_point_cloud(out_path)
    # points = np.asarray(pcd.points)


    draw_start = time.time()
    result = LivoxFileRead(lvx_path)
    draw_end = time.time()
    ts =  draw_end - draw_start
    print('%.3f' % ts)
    # print(json.dumps(result))


    print('finished')

    # https://zhuanlan.zhihu.com/p/377272161
    # https://gist.github.com/kentaroy47/6e8081df81785342cbf8daedde1928ce


    # https://zhuanlan.zhihu.com/p/523014472?utm_id=0