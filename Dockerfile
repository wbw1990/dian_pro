# FROM registry.cn-beijing.aliyuncs.com/qqjy/dian_pro:1.0
FROM python:3.9
COPY requirements.txt /tmp/
RUN pip install -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com -r /tmp/requirements.txt

RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN apt -y install vim
RUN mkdir -p /runtime
# RUN mkdir -p /runtime/pcd
# RUN mkdir -p /runtime/lib
# RUN mkdir -p /runtime/piao

COPY startup.sh /runtime/
COPY index.py /runtime/
COPY index_init.py /runtime/
COPY lib/ /runtime/lib/
# COPY lib/bluetooth_client.py /runtime/lib/
# COPY domain.py /runtime/
# COPY pcd_operator.py /runtime/
# COPY utils.py /runtime/
# COPY config.py /runtime/

# COPY pcd/bdzdianyun.pcd /runtime/pcd/
# COPY pcd/pro.pcd.json /runtime/pcd/
# COPY pcd/tai.json /runtime/pcd/


WORKDIR /runtime

CMD [ "sh", "startup.sh" ]





# docker rmi $(docker images -q -f dangling=true)

