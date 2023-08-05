import sys
from . import ArgParser
import time

t1 = time.time()

args = " ".join(sys.argv[1:])
parser = ArgParser(args)
while True:
    try:
        arg = next(parser)
        print(arg)
    except StopIteration:
        break

print("Execution time: {} ms".format(round((time.time() - t1) * 1000)))
