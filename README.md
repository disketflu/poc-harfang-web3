
# Proof of concept - Harfang App with multiplayer socket / client and possibly Web3 / Blockchain interactions

This project  was made by **Clément BEUDOT** using the **HarfangHighLevel** Python library.
I might switch to the complete **Harfang 3D** framework soon if HHL is so high level that i can't do what I want.

This **concept** demonstrates the usage of the socket library to create a fully-functional server/client game using the HARFANG API in **Python**.

The main idea behind this project is to create a sort of **minimal** 3D Metaverse, containing every aspect that one should need :

* ECDSA Signatures authentication with the server
* Smart Contracts storing user data (no database needed + server-wide data)
* Possibility to send Tokens (ERC20, NFT etc...) through the game interface

## How does it work ?

### Socket Communication
1. The server listens for incoming connections
2. It accepts the client and does the auth process
3. It receives positions from each client in a thread
4. It sends all players positions to each client in another thread

### ECDSA Signatures
1. The client currently generates a Wallet on each launch (the objective is to add a MetaMask / Private Key auth and this is 100% doable)
2. The client signs a message ("auth") using it's wallet private key
3. The server awaits for the client's address and it's signed message
4. The server reverses the signed message to obtain an address and compares it with the client address to make sure both correspond
5. Connection is either authorized or refused after the last step

## How to run the program

### Python
1. Get [Python 3](https://www.python.org/downloads/)
2. Get HARFANG HIGH LEVEL using PIP in the command line, type '*pip install harfanghighlevel*'
3. Clone/download this repository
4. run *server.py*
5. run *client.py*
