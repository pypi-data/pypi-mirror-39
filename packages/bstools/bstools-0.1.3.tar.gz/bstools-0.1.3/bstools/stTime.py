import time

# public symbols

__all__ = ["tsToLocalTime", "PerformCacl"]

def performCacl(func):
    def main(*argv, **keys):
        timeStart = time.time()
        result = func(*argv, **keys)
        timeEnd = time.time()
        print(u"模块%s耗时: %.15f秒"%(func.__name__,timeEnd - timeStart))
        return result
    return main

def tsToLocalTime(timestamp, timeType = "ms"):
    if timeType not in ["ms","s"]:
        raise arrTypeErr("参数错误, 接受'ms' 和's' ")
    else:
        tType = timeType
    timestamp = float(timestamp) if timeType == "s" else float(timestamp)*0.001
    timeArray = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)