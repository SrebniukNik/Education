file = open("test.txt", "r")

while True:
    x = file.readline()
    if x.count("ERROR"):
        print x
