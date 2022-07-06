import socket
import threading
import pickle
import random
import time

s = socket.socket()
port = 12345
s.bind(('', port))
s.listen(5)

print("Server is listening and waiting for clients")

num_clients = 0
pos_clients = []

def handleClientRcv(c, addr, id_client):
	playerAlive = True
	while playerAlive:
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
