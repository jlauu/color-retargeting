from FDO import *
import sys,os

def HextoRGB(c):
    strColors = (c[0:2], c[2:4], c[4:6])
    return tuple(int(c,16) for c in strColors)


def parse(data):
    colors = list()
    with open(data) as f:
        for line in f.readlines()[1:]:
            colors.append(line[1:-1])
    return [ HextoRGB(hexc) for hexc in colors ]
        
def main(data):
    colors = parse(data)
    optc = optimize(colors)
    print(optc)

def optimize(colors):
    fdo = buildGraph(colors)
    fdo.run()
    return [ tuple(round(c) for c in color) for color in fdo.results()]

def buildGraph(colors):
    fdo = FDO(3)
    nodes = []
    for c in colors:
        n = fdo.addNode(*c)
        nodes.append(n)

    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            fdo.addSpring(nodes[i], nodes[j])

    return fdo


if __name__ == '__main__':
    main(sys.argv[1])
