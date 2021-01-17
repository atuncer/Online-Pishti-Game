import socket
from _thread import *
import pickle
import sqlite3
from game import Game

server = "localhost"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, port

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    flag = True
    p0rematch = False
    p1rematch = False
    isfirstround = True
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()  # get

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if (len(game.p1cards) + len(game.p2cards) + len(game.leftCards) == 0) and flag and not isfirstround:
                        flag = False
                        try:
                            sqlconn = sqlite3.connect('db1.db')
                            c = sqlconn.cursor()

                            c.execute("SELECT COUNT(*) FROM USERS WHERE username = '{usr}'".format(usr=game.p1username if game.getwinner() else game.p2username))
                            if str(c.fetchone())[1] != '1':
                                c.execute(
                                    "INSERT INTO USERS (username,points) VALUES ('{usr}','{score}')".format(score="1", usr= game.p1username if game.getwinner() else game.p2username))
                            else:
                                c.execute(
                                    "UPDATE USERS SET points = points + {score} WHERE username = '{usr}'".format(score="1", usr=game.p1username if game.getwinner() else game.p2username))

                            sqlconn.commit()
                            sqlconn.close()
                        except sqlite3.Error as e:
                            print("An error occurred:", e.args[0])


                    if data == 'dealfirst':
                        isfirstround = False
                        game.deal_cards_first()
                    elif data == 'deal' and p == 1:
                        game.deal_cards()
                    elif len(data) == 2:
                        game.card_played(p, data)
                    elif data.split(',')[0] == 'username':
                        game.setUserName(p, data.split(',')[1])
                    elif data == 'hscores':

                        try:
                            sqlconn = sqlite3.connect('db1.db')
                            c = sqlconn.cursor()
                            c.execute("SELECT * FROM USERS ORDER BY points DESC")
                            arr = c.fetchall()
                            sqlconn.close()
                            game.sethighscores(arr[:min(5, len(arr))])

                        except sqlite3.Error as ex:
                            print("An error occurred:", ex.args[0])

                    elif data == 'rematch':
                        if p == 0: p0rematch = True
                        else: p1rematch = True

                        game.rematch(p)

                        if p0rematch and p1rematch:
                            flag = True
                            isfirstround = True


                    conn.sendall(pickle.dumps(game))

            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    if (idCount == 30):
        print("Server Full")
        break


    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
