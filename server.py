import socket
from _thread import *
import pickle
from game import Game

server = '192.168.0.41'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print('Server started test')

connected = set()
games = {}
idCount = 0

def threading_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ''
    while True:

        try:
            data = conn.recv(2048 * 2).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.resetWent()

                    elif data != 'get':
                        game.play(p, data)
                    
                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print('Lost connection')

    try:
        del games[gameId]
        print('Closing', gameId)
    except:
        pass

    idCount -= 1
    conn.close()
                    

while True:
    conn, addr = s.accept()
    print('Connect to:', addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print('testid')
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threading_client,(conn, p, gameId))