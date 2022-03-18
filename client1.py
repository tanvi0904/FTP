import socket
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 4458
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
# uname = "CNFTP"
# password = "cnftp"
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Using TCP as the Transport Protocol
    client.connect(ADDR)

    name = input("Enter UserName: ")
    pwd = input("Enter Password: ")
    str = name + " " +  pwd
    client.send(str.encode(FORMAT))


    data = client.recv(SIZE).decode(FORMAT)
    cmd, msg = data.split("@")
    if cmd.upper() == "DISCONNECTED":
        print(f"[SERVER]: {msg}")
        quit()
    elif cmd.upper() == "OK":
        print(f"{msg}")
    print("Type 'HELP' to start \n")
    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd.upper() == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd.upper() == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd.upper() == "HELP":
            client.send(cmd.encode(FORMAT))
        
        elif cmd.upper() == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd.upper() == "LIST":
            client.send(cmd.encode(FORMAT))
        
        elif cmd.upper() == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        
        elif cmd.upper() == "UPLOAD":
            path = data[1]
            with open(f"{path}", "r") as f:
                text = f.read()
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
        else:
            client.send(cmd.encode(FORMAT))

    else:
        print("Wrong username or password")

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()