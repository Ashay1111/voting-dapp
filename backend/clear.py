from pyteal import *

def clear():
    return Return(Int(1))

if __name__ == "__main__":
    print(compileTeal(clear(), mode=Mode.Application))
