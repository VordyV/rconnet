from rconnet.rconbf2142 import Default

address, password, port = ("127.0.0.1", "super123", 4711)

with Default(address, password, port=port) as rcon:
    print("Connected.")
    while True:
        try:
            command = input("")
            print(rcon.rcon_invoke(command))
        except Exception as error:
            print(error)
            break
print("Bye")