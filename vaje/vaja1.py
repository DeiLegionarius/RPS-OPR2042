import time

def timedPrint(data, end="\n"):
    txtData = data[0::2]
    etData = data[1::2]
    for i in range(len(txtData)):
        elapsedT = etData[i]
        txt = txtData[i]
        perNum = elapsedT / len(txt)
        for letter in txt:
            print(letter, end="", flush=True)
            time.sleep(perNum)
    print(end)
        
        
timedPrint(("", 1, ))