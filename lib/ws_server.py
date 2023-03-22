
# https://www.jianshu.com/p/b7df44b7c7f7
# pip install websockets-routes

import asyncio
import websockets
import websockets_routes
import time
import json
# import functools
# 初始化一个router对象
import utils
router = websockets_routes.Router()

POS_STATUS = False
# queue = asyncio.Queue(maxsize=10)
WS = None

@router.route("/event") #添加router的route装饰器，它会路由uri。
async def light_status(websocket, path):
    global POS_STATUS
    global queue
    global WS
    WS = websocket
    async for message in websocket:
        print("got a message:{}".format(message))

        # print(path.params['status'])
        await asyncio.sleep(0.1) 
        if message == 'on':
            POS_STATUS = True

            await  websocket.send("turned on")            
        elif message == 'off':
            POS_STATUS = False
            await  websocket.send("turned off")
        else:
            await  websocket.send("invalid params")




async def get_position():
    global POS_STATUS
    # global queue
    global WS
    # index = 1


    while True:
        if POS_STATUS:
            lng, lat = utils.generate_random_gps(base_log=115.599801 , base_lat=39.138076, radius=100)
            x,y,z = utils.latlontoxyz(lat,lng,0)
            data = json.dumps({'lng':lng,'lat':lat,'x':x,'y':y,'z':z})
            # await queue.put(str(index))
            if WS is not None:
                await WS.send(data)
            # index =index +1
        await asyncio.sleep(1)

async def main():
    # rooter是一个装饰器，它的__call__函数有三个参数，第一个参数是self。
    # 所以这里我们需要使用lambda进行一个转换操作，因为serv的wshander函数只能接收2个参数
    # async with websockets.serve(lambda x, y: router(x, y), "127.0.0.1", 8765):
    
    # async with websockets.serve(functools.partial(light_status, queue=queue, POS_STATUS=POS_STATUS), "127.0.0.1", 8765):
    async with websockets.serve(lambda x, y: router(x, y), "127.0.0.1", 8765):
        print("======")
        # await  asyncio.Future()  # run forever
        cur =  asyncio.Future() 
        pos = asyncio.create_task(get_position())
        await asyncio.gather(cur,pos, return_exceptions=True)




if __name__ == "__main__":
    asyncio.run(main())




# python -m websockets ws://localhost:8765/event