import sqlite3
from dhe import *
# Table Format:
#   Table Name: conversation_user1_user2
#   Table Columns: (line_num) (sender) (message)
# For each table, conversation_user1_user2 there is an equivalent conversation_user2_user1
# Create ROLE called 'client' with SELECT, INSERT, DROP permissions 
# create a db user with client role, for conversations where user=user1
# create user_table

# NOTE: MySQL connector syntax
# mydb = connectUser("root", "banana1234")
# mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE conversation_1 (line_num INT AUTO_INCREMENT PRIMARY KEY, sender VARCHAR(30) NOT NULL, message TEXT NOT NULL)")
# CREATE TABLE user_table (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) NOT NULL, passwd VARCHAR(30) NOT NULL);
# querry = "INSERT INTO conversation_1 (sender, message) VALUES (%s, %s)"
# param = ("World", "Hello John!")
# mycursor.execute(querry, param)
# mydb.commit()


def connectDB(database):
    """
    Connect with the specified database
    
    Parameters
    ----------
    database : str
        Database name

    Returns
    -------
    Connection object for interfacing with 'chat_database'
    """
    mydb = sqlite3.connect(database)
    try: 
        mydb.cursor()
    except Exception:
        print('Connection failed!')
        return
        
    print('Connection successful!')
    return mydb

def addUser(usr, passwd, conn):
    """
    Create a new user in the database

    Parameters
    ----------
    usr : str
        Username to add (must be <= 30 characters)
    passwd : str
        Password for usr
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM user_table WHERE username=?", (usr,))
    if(mycursor.fetchall()):
        print("User already exists!")
        return
    
    mycursor.execute("INSERT INTO user_table (username, password) VALUES (?, ?)", (usr, passwd))
    setPrivateKey(usr, conn)
    setPublicKey(usr, conn)
    conn.commit()
    print(f"{usr} added!")

def setPrivateKey(usr, conn):
    """
    Create a private key and assign it to a user

    Parameters
    ----------
    usr : str
        User to receive key
    conn : Connection Object
        Active database connection 
    """
    private_key = generate_private_key()
    mycursor = conn.cursor()
    mycursor.execute("UPDATE user_table SET private_key=? WHERE username=?", (private_key, usr))
    conn.commit()
    
def setPublicKey(usr, conn):
    """
    Create a private key and assign it to a user

    Parameters
    ----------
    usr : str
        User to receive key
    conn : Connection Object
        Active database connection 
    """
    public_key = generate_public_key(getPrivateKey(usr, conn))
    mycursor = conn.cursor()
    mycursor.execute("UPDATE user_table SET public_key=? WHERE username=?", (public_key, usr))
    conn.commit()

def getPrivateKey(usr, conn):
    """
    Retrieve a user's private key from database

    Parameters
    ----------
    usr : str
        Username
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT private_key FROM user_table WHERE username=?", (usr,))

    return mycursor.fetchone()[0]

def getPublicKey(usr, conn):
    """
    Retrieve a user's public key from database

    Parameters
    ----------
    usr : str
        Username
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT public_key FROM user_table WHERE username=?", (usr,))
    
    return mycursor.fetchone()[0]

def setSessionKey(usr1, usr2, conn):
    """
    Append session_table with session key between users

    Parameters
    ----------
    usr1 : str
        First user
    usr2 : str
        Second user
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()

    mycursor.execute("SELECT * FROM user_table WHERE username=?", (usr1,))
    if not mycursor.fetchall():
        print(f"{usr1} does not exists!")
        return
    mycursor.execute("SELECT * FROM user_table WHERE username=?", (usr2,))
    if not mycursor.fetchall():
        print(f"{usr2} does not exists!")
        return

    pk1 = getPrivateKey(usr1, conn)
    pk2 = getPrivateKey(usr2, conn)
    sk = generate_session_key(pk1, pk2)

    try:
        mycursor.execute("INSERT INTO session_table (user1, user2, session_key) VALUES (?, ?, ?)", (usr1, usr2, sk))
    except Exception:
        print("Session already active!")
    conn.commit()

def getSessionKey(usr1, usr2, conn):
    """
    Retrieve session key between users from session_table

    Parameters
    ----------
    usr1 : str
        First user
    usr2 : str
        Second user
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT session_key FROM session_table WHERE user1=? and user2=?", (usr1, usr2))
    sk = mycursor.fetchall()
    if not sk:
        mycursor.execute("SELECT session_key FROM session_table WHERE user1=? and user2=?", (usr2, usr1))
        sk = mycursor.fetchall()
        if not sk:
            print("Session does not exist!")
            return
    
    return sk[0][0]

def removeSessionKey(usr1, usr2, conn):
    """
    Delete tupple in session_table with session key between user1 and user2

    Parameters
    ----------
    usr1 : str
        First user
    usr2 : str
        Second user
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT session_key FROM session_table WHERE user1=? and user2=?", (usr1, usr2))
    sk = mycursor.fetchall()
    if not sk:
        mycursor.execute("SELECT session_key FROM session_table WHERE user1=? and user2=?", (usr2, usr1))
        sk = mycursor.fetchall()
        if not sk:
            print("Session does not exist!")
            return
    mycursor.execute("DELETE FROM session_table WHERE user1=? and user2=?", (usr1, usr2))
    mycursor.execute("DELETE FROM session_table WHERE user1=? and user2=?", (usr2, usr1))
    conn.commit()
    print(f"Terminated session between {usr1} & {usr2}")


def createConversation(usr1, usr2, conn):
    """
    Create a new conversation between existing users

    Parameters
    ----------
    usr1 : str
        User initiating conversation
    usr2 : str
        User receiving conversation
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = mycursor.fetchall()
    if table_list.count(("conversation_"+usr1+"_"+usr2,)) != 0:
        print("Conversation already exists!")
        return

    mycursor.execute("SELECT username FROM user_table")
    user_list = mycursor.fetchall()
    
    if user_list.count((usr1,)) == 0:
        print(f"{usr1} does not exist!")
        return
    if user_list.count((usr2,)) == 0:
        print(f"{usr2} does not exist!")
        return

    q1 = "CREATE TABLE conversation_"+usr1+"_"+usr2+" (line_num INTEGER PRIMARY KEY, sender VARCHAR(300) NOT NULL, message TEXT NOT NULL)"
    q2 = "CREATE TABLE conversation_"+usr2+"_"+usr1+" (line_num INTEGER PRIMARY KEY, sender VARCHAR(300) NOT NULL, message TEXT NOT NULL)"

    #Always execute 1st query 
    mycursor.execute(q1)
    #Don't execute 2nd query if a user is messagin themselves or if a second table already exists (in case of previous deletion) 
    if usr1 != usr2 and table_list.count(("conversation_"+usr2+"_"+usr1,)) == 0:
        mycursor.execute(q2)

    setSessionKey(usr1, usr2, conn)
    
    conn.commit()

def deleteConversation(usr1, usr2, conn):
    """
    Delete conversation between usr1 and usr2 for usr1 only

    Parameters
    ----------
    usr1 : str
        User who initiated the conversation deletion
    usr2 : str
        Specifies conversation to be deleted 
    conn : Connection Object
        Active database connection
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = mycursor.fetchall()
    c_str1 = "conversation_"+usr1+"_"+usr2
    if table_list.count((c_str1,)) == 0:
        print("Conversation does not exist!")
        return
    
    mycursor.execute("DROP TABLE "+c_str1)
    removeSessionKey(usr1, usr2, conn)
    conn.commit()

def appendConversation(usr1, usr2, message, conn):
    """
    Append an existing conversation with a new message

    Parameters
    ----------
    usr1 : str
        Sender
    usr2 : str
        Receiver
    message : str
        Message to be stored in encrypted form 
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = mycursor.fetchall()
    c_str1 = "conversation_"+usr1+"_"+usr2
    c_str2 = "conversation_"+usr2+"_"+usr1
    if table_list.count((c_str1,)) == 0:
        print("Conversation between {usr1} & {usr2} does not exist!\nCreating conversation...")
        createConversation(usr1, usr2, conn)
    

    q1 = "INSERT INTO "+c_str1+" (sender, message) VALUES (?, ?)"
    q2 = "INSERT INTO "+c_str2+" (sender, message) VALUES (?, ?)"
    mycursor.execute(q1, (usr1, message))
    if usr1 != usr2:
        mycursor.execute(q2, (usr1, message))
    conn.commit()



def deleteUser(usr, conn):
    """
    Delete a user and all conversations where user1=usr

    Parameters
    ----------
    usr : str
        String corresponding to a valid and connected user
    """
    mycursor = conn.cursor()

def getConversation(usr1, usr2, conn):
    """
    Retrieve a conversation from the database and serve it to the correct user

    Parameters
    ----------
    usr1 : str
        User who "owns" the conversation 
    usr2 : str
        Specifies conversation to be deleted
    
    Returns
    -------
    A list of tupples of the form (line_num, sender, message)
    """
    mycursor = conn.cursor()
    mycursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = mycursor.fetchall()
    c_str1 = "conversation_"+usr1+"_"+usr2
    
    if table_list.count((c_str1,)) == 0:
        print("Conversation does not exist!")
        return
    
    q = "SELECT * FROM "+c_str1
    mycursor.execute(q)
    conversation_list = mycursor.fetchall()
    return conversation_list
    

