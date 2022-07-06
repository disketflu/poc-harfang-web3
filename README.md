
# Proof of concept - Harfang App with multiplayer socket / client and possibly Web3 / Blockchain interactions

This project  was made by **Clément BEUDOT** using the **HarfangHighLevel** Python library.
I might switch to the complete **Harfang 3D** framework soon if HHL is so high level that i can't do what I want.

This **concept** demonstrates the usage of the socket library to create a fully-functional server/client game using the HARFANG API in **Python**.

The main idea behind this project is to create a sort of **minimal** 3D Metaverse, containing every aspect that one should need :

* ECDSA Signatures authentication with the server
* Smart Contracts storing user data (no database needed + server-wide data)
* Possibility to send Tokens (ERC20, NFT etc...) through the game interface

## How to run the program

### Python
1. Get [Python 3](https://www.python.org/downloads/)
2. Get HARFANG HIGH LEVEL using PIP in the command line, type '*pip install harfanghighlevel*'
3. Clone/download this repository
4. run *server.py*
5. run *client.py*
