import asyncio
import websockets
from ssh2client import Ssh2Client
import json

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
async def echo(websocket, path):
    async for message in websocket:
        message = json.loads(message)
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
            url = (message['data']['host'], message['data']['port'])
            username = message['data']['username']
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


        print(f"Received msg type: {message['type']}")
        print(f"Received msg data: {message['data']}")

async def start_server():
    server = await websockets.serve(echo, 'localhost', 7070)
    await server.wait_closed()

asyncio.get_event_loop().run_until_complete(start_server())
