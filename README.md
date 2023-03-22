conda create -n dian python=3.8

conda activate dian


<!-- RUN pip install -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com -r /tmp/requirements.txt -->
<!--  -->


docker build -t registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0 .

sudo docker run  --name dian_pro -d -p 52010:80 -v /home/nanchang/pcd/bdzdianyun.pcd:/runtime/pcd/bdzdianyun.pcd registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0

sudo docker run  --name dian_pro -d -p 52010:80 registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0

docker logs -t -f --tail=200 dian_pro

sudo docker stop dian_pro
sudo docker rm dian_pro



docker login --username=606taobao registry.cn-beijing.aliyuncs.com
$ docker tag dian_pro:1.0 registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0
$ docker push registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0


sudo docker pull registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0


<!-- docker run  --name dian_pro -d -p 52010:80 registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0 -->

firewall-cmd --permanent --zone=public --add-port=52010/tcp

systemctl restart firewalld.service


[dian_pdf]
type = tcp
local_ip = 127.0.0.1
local_port = 52010
remote_port = 52010



pcd:

http://www.open3d.org/docs/release/python_api/open3d.geometry.PointCloud.html

pip3 install open3d




链接：https://pan.baidu.com/s/1UUtLejVIP3_og90gbAYiLg?pwd=vdr3 
提取码：vdr3 
--来自百度网盘超级会员V4的分享@吴伯文 

大疆激光雷达
https://www.livoxtech.com/cn/downloads


pip 安装
https://www.lfd.uci.edu/~gohlke/pythonlibs/

-v /dev:/dev -v /run/dbus:/run/dbus -v /var/run/dbus:/var/run/dbus

sudo docker run  --name dian_pro -d -p 52010:80 -v /dev:/dev -v /run/dbus:/run/dbus -v /var/run/dbus:/var/run/dbus registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0