import sys
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    print(len(sys.argv))
    print("Error with command line inputs")
    sys.exit(0)
else:
    fileName = sys.argv[1]
    tick = sys.argv[2]
    attribute = int(sys.argv[3])

f = open(fileName, "r")

inArea = False
attArray = []

for line in f:
    if len(line.split()) > 20 and inArea == False:
        inArea = True
        continue
    if inArea:
        line = line.split()[0::2]
        if line[0] == tick:
            attArray.append(line[attribute])
            inArea = False

print(attArray[len(attArray)-1])

plt.plot(attArray)
plt.show
