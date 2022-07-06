import HarfangHighLevel as hl
import random
import socket            
import threading
import pickle
import time
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_account import Account
import secrets

priv = secrets.token_hex(32)
private_key = "0x" + priv
print ("SAVE BUT DO NOT SHARE THIS:", private_key)
acct = Account.from_key(private_key)
print("Address:", acct.address)
msg = "auth"
message = encode_defunct(text=msg)
signed_message = w3.eth.account.sign_message(message, private_key=private_key)
print(signed_message.signature)
# message = encode_defunct(text="auth")
# print(w3.eth.account.recover_message(message, signature=signed_message.signature))
print([acct.address, signed_message.signature])

res_x = 1000
res_y = 600

pos_x = res_x / 2
old_pos_x = 0
pos_y = res_y / 2
old_pos_y = 0
players = []

# Initialize server socket
s = socket.socket()        
port = 12345
s.connect(('127.0.0.1', port))

def handleConnection(s):
    global pos_y, old_pos_y, pos_x, old_pos_x, players
    playerAuth = False
    while playerAuth == False:
        infos = [acct.address, signed_message.signature]
        data = pickle.dumps(infos)
        s.send(data) # send it first so the server accepts connexion
        time.sleep(2)
        s.send(data)

        playerAuth = True

    while playerAuth:
        if old_pos_y != pos_y or old_pos_x != pos_x:
            old_pos_y = pos_y
            positions = [pos_x, pos_y]
            data = pickle.dumps(positions)
            s.send(data)
            time.sleep(0.01) # send every 0.01 sec

def handleReceive(s):
    global pos_y, old_pos_y, players
    while True:
        data = s.recv(4096)
        if data:
            try:
                final_data = pickle.loads(data)
                playerindex = final_data[0]
                playerposlist = final_data[1]
                lenlist = len(playerposlist)
                final_player_list = []
                for i in range(lenlist):
                    if i != playerindex and len(playerposlist[i]) == 2: # check if player is not our client and not a dead / disconnected client (length is 3 when player is disconnected)
                        final_player_list.append(playerposlist[i])
                players = final_player_list

            except: print(data)

threading.Thread(target=handleConnection, args=(s,)).start()
threading.Thread(target=handleReceive, args=(s,)).start()

hl.Init(res_x, res_y)
hl.SetLogLevel(hl.LL_Normal)

while not hl.UpdateDraw():
    hl.DrawQuad2D(pos_x, pos_y, 10, 10, color=hl.Color.Green, depth=1)
    for i in players:
        hl.DrawQuad2D(i[0], i[1], 10, 10, depth=1)

    fps = 1 / hl.time_to_sec_f(hl.gVal.dt)

    if hl.KeyDown(hl.K_Up):
        old_pos_y = pos_y
        pos_y += 100 / fps

    if hl.KeyDown(hl.K_Down):
        old_pos_y = pos_y
        pos_y -= 100 / fps

    if hl.KeyDown(hl.K_Right):
        old_pos_x = pos_x
        pos_x += 100 / fps

    if hl.KeyDown(hl.K_Left):
        old_pos_x = pos_x
        pos_x -= 100 / fps