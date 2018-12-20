# ELEC-H417-BlockChain-Project

The blockchain network consist of 6 nodes and one authentication center. In order to run the network
the authentication center has to be launched first so every node can be authenticated.


NODES

There are two files, node.py and node_test.py, that can run as main.
node.py is a user interactive node through which the user can introduce
transactions.
node_test.py is a non-user interactive node. We can not introduce transactions 
through it but it prints the information about the blockchain.

The nodes communicates sending tuples indicating their address and the message.
This methode had to be integrated since the returned address from the socket.accept()
 fucntion always gives 127.0.0.1 and a port number when not using virtual machines. 
