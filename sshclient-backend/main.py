import asyncio
import websockets
from ssh2client import Ssh2Client
import json
import os

'''
ssh example
{
    "url" : ("127.0.0.1", 22),
    "username" : "root",
    "password" : "toor",
    "sshc" : Ssh2Client(),
}
'''
sshs = [
]
sftps = []
start_id = 1
async def echo(websocket, path):
    global start_id
    async for message in websocket:
        message = json.loads(message)
        print(message)
        if message['type'] == 'initssh' :
            if len(sshs) >= 10:
                await websocket.send('Quantity reaches upper limit')
            else:
                url = (message['data']['host'], message['data']['port'])
                username = message['data']['username']
                password = message['data']['password']
                ssh = Ssh2Client(url)
                ssh.connect(username, password)
                sshs.append({
                    "url" : url,
                    "username" : username,
                    "password" : password,
                    "sshc" : ssh,
                }
                )
                result = ssh.recv(30)
                print(result, end='')
                print(sshs)
                await websocket.send(json.dumps({'type' : 'sshcmdreponse', 'data' : result}))
        elif message['type'] == 'sshcmd':
            print(message)
            url = (message['data']['host'], message['data']['port'])
            username = message['data']['username']
            print(sshs)
            for ssh in sshs:
                if ssh['url'] == url and ssh['username'] == username:
                    result = ssh['sshc'].exec(message['data']['cmd'])
                    print('wwxnb')
                    print(result, end='')
                    print('wwxnb')
                    await websocket.send(json.dumps({'type' : 'sshcmdreponse', 'data' : result}))
                    break
            else:
                await websocket.send(json.dumps({'type' : 'sshcmdwarning', 'data' : '找不到连接的ssh'}))
        elif message['type'] == 'getconfig':
            if not os.path.exists('./config.json'):
                with open('./config.json', 'w') as f:
                    #使用json.dump()将数字列表存储到文件numbers.json中
                    json.dump({}, f)
            with open('./config.json', 'r') as f:
                config = json.load(f)
                for key in config.keys():
                    if int(key) >= start_id:
                        start_id = int(key) + 1
                print(start_id)
                print(config)
                await websocket.send(json.dumps({'type' : 'config' , 'data' : json.dumps(config)}))
        elif message['type'] == 'deleteconfig':
            config = None
            with open('./config.json', 'r') as f:
                config = json.load(f)
            del config[message['data']['id']]
            i = int(message['data']['id'])
            while True:
                if str(i + 1) in config:
                    config[str(i)] = config[str(i + 1)]
                    del config[str(i + 1)]
                else:
                    break
                i += 1
            start_id -= 1
            with open('./config.json', 'w') as f:
                #使用json.dump()将数字列表存储到文件numbers.json中
                json.dump(config, f)
            await websocket.send(json.dumps({'type' : 'deleteconfig' , 'data' : {'id' : message['data']['id'], 'msg' : 'Success!'}}))
        elif message['type'] == 'updateconfig':
            config = None
            with open('./config.json', 'r') as f:
                config = json.load(f)            
            config[message['data']['id']]['name'] = message['data']['name']
            config[message['data']['id']]['ip'] = message['data']['ip']
            config[message['data']['id']]['username'] = message['data']['username']
            config[message['data']['id']]['password'] = message['data']['pwd']
            with open('./config.json', 'w') as f:
                #使用json.dump()将数字列表存储到文件numbers.json中
                json.dump(config, f)
            await websocket.send(json.dumps({'type' : 'updateconfig' , 'data' : {'id' : message['data']['id'], 'msg' : 'Success!'}}))
        elif message['type'] == 'createconfig':
            config = None
            with open('./config.json', 'r') as f:
                config = json.load(f)      
            config[str(start_id)] = {
                'name' : message['data']['name'],
                'ip' : message['data']['ip'],
                'username' : message['data']['username'],
                'password' : message['data']['pwd'],
            }
            start_id += 1
            with open('./config.json', 'w') as f:
                #使用json.dump()将数字列表存储到文件numbers.json中
                json.dump(config, f)
            await websocket.send(json.dumps({'type' : 'createconfig' , 'data' : {'id' : str(start_id - 1), 'msg' : 'Success!'}}))
        print(f"Received msg type: {message['type']}")
        print(f"Received msg data: {message['data']}")

async def start_server():
    server = await websockets.serve(echo, 'localhost', 7070)
    await server.wait_closed()

asyncio.get_event_loop().run_until_complete(start_server())
