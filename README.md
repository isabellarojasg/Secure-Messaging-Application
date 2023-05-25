# Secure Messaging Application
Our team implemented a Secure messaging application in Python for the final assignment. The application can operate the Diffie–Hellman key exchange method to encrypt messages and preserve chat history. The application starts by asking the user to log in and verify its database credentials. This report will further explain the application and its functionalities in detail.

## Prototype Description

### Code Structure Description and how to run the code
Our application can be run by first starting the server and then connecting each client with the server. Once the clients successfully connect with the server, they can exchange messages. In the following sections, we will explain the limitations encountered with the code and why some functionalities are party implemented.

To start the server, we run the `server.py` file. This file contains a list of the successful clients when logging in. The file also contains a function that verified the user when logging and ran the DHE key exchange protocol. The server is always running in a continuous loop to accept new incoming connections. When the clients are connected and want to start exchanging messages, the server will use the functions `broadcast(message)` to send the message to all the connected clients. 

To start the client, we run the `client.py` file. In this file, we ask the user to input their credentials and allow them to send messages to the server so that other connected clients can see their messages. 

The `dhe.py` file contains multiple functions that each create unique keys and the keys created are the following: private keys, public keys, and session keys. It also includes functions for both encryption of a message and decryption. These two functions iteratively encrypt and decrypt by taking the position of each character in the message or encrypted message, respectively, adding it with the session key, then converting that into their unicode character. 

The database is initialized by running the `init_database.py` file, which creates a database instance within the current directory. It then creates a user_table, to store user information, and a session_table, which stores session key information. The user table is also propagated with some sample usernames and passwords along with their respective private and public keys. The `daManagement.py` file contains functions that dictate interactions with the database. The first two functions are connectDb, which returns a connection object for the database, and addUser, which appends the user_table with a tuple of the form (username, password, null, null). The null values are placeholders for the private and public keys respectively, which are assigned by the setter functions setPrivateKey and setPublicKey. There is also a setter for assigning the session key in the session_table and all setters have corresponding getter functions. 

To preserve message history after deletion by 1 user, our idea was to create two tables for each conversation. If Alice initiated a conversation with Bob then the tables created would be conversation_Alice_Bob and conversation_Bob_Alice, and Alice would only interact with the tables where her name comes first. Therefore, if Alice wanted to delete a conversation then the first table would be dropped and nothing on Bob's side would be affected. Then if another conversation between Alice and Bob was initiated, Alice would get a new table and Bob's would be preserved. The appendConversation function appends a message to both tables and getConversation returns a list of tuples, each containing one line of conversation represented as (line_num, sender, message).



##### To run the server file 

> `python3 server.py`

##### To run the client file 

> `python3 client.py`


##### To run the database

> `python3 init_database.py`

### Data-Flow Diagram 
![Untitled__1_](https://github.com/isabellarojasg/Secure-Messaging-Application/assets/68630621/93efc0bf-7528-4485-9c0e-d2c0abba309c)


### Limitations 
During this assignment, the team encountered some limitations. Since we were approaching the end of the semester, the workload of classes prevented us from devoting our time to this project. With more time, the team could have adequately implemented all the requirements. The second limitation that our team ecnountered was the size of the session key which ended up being too big to store on the database. Our team had to decrese the size of it which means that the key became less complex. The third limitation involved needing to refactor every function in `dbManagement.py` due to the local database instance. The file was originally set up and tested with the myslq connector for python because we initially planed to host a remote database. However, due to the time constraint we switched to using sqlite3 which uses a different enough syntax that none of the original code maintained its functionality. 


### Video of Prototype 

[Video of Prototype](https://youtu.be/SJvV2O3gGIc )

### Resources 
To build the `server.py` and `client.py` files we used the following resources:  
https://www.youtube.com/watch?v=sopNW98CRag  

https://www.youtube.com/watch?v=3UOyky9sEQY

