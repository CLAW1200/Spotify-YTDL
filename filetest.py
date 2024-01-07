import os 
keys = os.path.join(os.getcwd() , "secret.keys")

def read_keys():
    with open(keys, "r") as f:
        return f.read().splitlines()

def write_keys(clientId, secret):
    with open(keys, "w") as f:
        f.write(clientId + "\n")
        f.write(secret)

def remove_keys():
    with open(keys, "w") as f:
        f.write("")


if __name__ == "__main__":
    print(read_keys())
    write_keys("test", "test")
    print(read_keys())
    remove_keys()
    print(read_keys())


