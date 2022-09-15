def binToHex(number):
    try:
        return int(number,2)

    except Exception as e:
        print(e)
        return

def hexToBin(number, length):
    try:
        return format(int(number), f'0'+str(length)+'b')
    except Exception as e:
        print(e)
        return