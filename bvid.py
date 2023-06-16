XOR = 177451812
ADD = 100618342136696320
TABLE = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
MAP = {
    0:9,
    1:8,
    2:1,
    3:6,
    4:2,
    5:4,
    6:0,
    7:7,
    8:3,
    9:5
}

def av2bv(av):
    av = (av ^ XOR) + ADD
    bv = [""]*10
    for i in range(10):
        bv[MAP[i]] = TABLE[(av//58**i)%58]
    return "".join(bv)

def bv2av(bv):
    av = [""]*10
    s = 0
    for i in range(10):
        s += TABLE.find(bv[MAP[i]])*58**i
    av=(s-ADD)^XOR

    return(av)

print(
    bv2av('BV1nP411B7kX')
)