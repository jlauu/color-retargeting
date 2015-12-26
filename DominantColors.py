from ClusterKMeans import *
from ArffData import *
from PIL import Image
import sys, os
from subprocess import call
import json

quality_epsilon = 0.5

def rgbToHex(r, g, b):
    f = lambda c: hex(c)[2:]
    return "#"+f(r)+f(g)+f(b)

def main(filename, guess):
    image = Image.open(filename)
    attr = [#('x','numeric'),
            #('y','numeric'),
            ('r','numeric'),
            ('g','numeric'),
            ('b','numeric')]
    data = ArffData('img', *attr)

    for r,g,b in image.getdata():
        data.add_point((r,g,b))
    
    colors = findColors(data, guess)
    print('c')
    for c in colors: 
        print(rgbToHex(int(c[0]),int(c[1]), int(c[2])))
    image.save("image.jpg", "JPEG")

def findColors(data, guess=5):
    results = list()
    cluster = ClusterKMeans(data, 1)
    for k_centers in range(guess,guess+1):
            #print("Testing for %d centers" % k_centers)
            for t_tests in range(1):
                    cluster.reset(k_centers)
                    quality = cluster.calc_quality()
                    min_quality = quality
                    new_quality = quality + quality_epsilon * 5
                    while abs(quality - new_quality) > quality_epsilon:
                            quality = cluster.calc_quality()
                            cluster.iterate()
                            new_quality = cluster.calc_quality()
                    if new_quality < min_quality:
                            min_quality = new_quality

            results.append((min_quality, list(cluster.centers)))

    return min(results, key=lambda x: x[0])[1]

    
        

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
