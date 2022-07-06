import socket
import threading
import pickle
import random
import time
from web3.auto import w3
from eth_account.messages import encode_defunct

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)

print("Server is listening and waiting for clients")

num_clients = 0
pos_clients = []

def handleClientRcv(c, addr, id_client):
	playerAlive = True
	playerAuth = False

	#authenticate player with erc20 address and signed message	
	while playerAuth == False:
		try:
			data = c.recv(4096)
			if data:
				try:
					final_data = pickle.loads(data)
					print(final_data)
					client_address = final_data[0]
					client_signature = final_data[1]
					message = encode_defunct(text="auth")
					recovered_message = w3.eth.account.recover_message(message, signature=client_signature)
					print(recovered_message)
					if client_address == recovered_message:
						print("Player AUTH")
						playerAuth = True

				except:
					print("Data error while auth")
	
		except Exception as err: # client connection lost or any other error
			print(err)
			print("Disconnected client ID : #" + str(id_client))
			pos_clients[id_client] = [0, 0, 0]
			playerAlive = False

	while playerAlive and playerAuth:
		try:
			data = c.recv(4096)
			if data:
				try:
					final_data = pickle.loads(data)
					pos_clients[id_client][0] = final_data[0]
					pos_clients[id_client][1] = final_data[1]
				except:
					print("Data error")
	
		except Exception as err: # client connection lost or any other error
			print(err)
			print("Disconnected client ID : #" + str(id_client))
			pos_clients[id_client] = [0, 0, 0]
			playerAlive = False

def handleClientSnd(c, addr, id_client):
	while True:
		c.send(pickle.dumps([id_client, pos_clients]))
		time.sleep(0.01) # 100 requests / second (tested and okay for client)

while True:
	c, addr = s.accept()
	data = c.recv(4096)
	if data: 
		print('Server accepted client : ', addr)
		threading.Thread(target=handleClientRcv, args=(c,addr, num_clients)).start()
		pos_clients.append([0, 0])
		threading.Thread(target=handleClientSnd, args=(c,addr, num_clients)).start()
		num_clients += 1
