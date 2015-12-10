"""
Johnny Lau

Summary: k-means clustering client.

Usage: python kclusters.py [arff file] -k <run for 1 to k centers> 
                                       -t <for each k run t tests>

Note: passing only the file and no flags runs the interpreter mode.

Sample Output:

        Results:
                k=1     quality=1273351.380000
                k=2     quality=1002400.663724
                k=3     quality=560684.908501
                k=4     quality=342560.145952
                k=5     quality=123543.086958
                k=6     quality=336340.188436

Note: quality is the sum of distances of each center to points in the same cluster.

"""

import sys, os, math
from ClusterKMeans import ClusterKMeans
from ArffData import *

def main(filename, *flags):
        data = read_arff(filename)

        flags = flags[0] #get the list not tuple
        k = None
        t = None
        flags.reverse()
        while len(flags) > 0:
                flag = flags.pop()
                if "-k" in flag:
                        k = flags.pop()
                elif "-t" in flag:
                        t = flags.pop()
        if k is None: 
                interpreter_mode(data)
        elif t is None:
                t = 20
        else:
                k = int(k)
                t = int(t)
        run_tests(data, k, t)

def run_tests(data, k, t):
        k = int(k)
        cluster = ClusterKMeans(data, 1)
        quality_epsilon = 0.5
        results = dict.fromkeys(range(1,k+1), 0)
        for k_centers in range(1,k+1):
                for t_tests in range(t):
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

                results[k_centers] = min_quality
                
        print("Results:")
        for kth_center, quality in results.items():
                print ("k=%d\tquality=%f" % (kth_center, quality))


def interpreter_mode(data):
        cluster = ClusterKMeans(data, 1)
        while True:
                usr_in = input("Continue iteration? Y/N: ")
                usr_in = usr_in.lower()
                if 'y' in usr_in:
                        cluster.iterate()
                        print("Quality: %f" % (cluster.calc_quality()))
                elif 'n' in usr_in:
                        usr_in = input("Reset for how many k clusters? ")
                        usr_in = int(usr_in)
                        cluster.reset(usr_in)
                        print("Quality: %f" % (cluster.calc_quality()))
                else:
                        continue
        return 0

def read_arff(filename):
        with open(filename, "r") as arff_fp:
                line = arff_fp.readline()
                attr = []
                attrname = ""
                attrtype = ""
                assert "@relation" in line, "%s does not have a valid header" % filename
                name = line.split(' ')[1][:-1]

                for line in arff_fp:
                        if "@data" in line:
                                break
                        elif "@attribute" in line:
                                line = line.split(' ')
                                attrname = line[1]
                                attrtype = line[2][:-1]
                                attr.append((attrname, attrtype))
                
                new_data = ArffData(name, *attr)
                num_attr = len(attr)
                for line in arff_fp:
                        vals = line.split(',')
                        vals[-1] = vals[-1][:-1] #      remove newline
                        assert len(vals) is num_attr, "Not enough values in data point"
                        vals = map(lambda x: int(x), vals)
                        new_data.add_point(tuple(vals))

        return new_data



if __name__ == "__main__":
        main(sys.argv[1], sys.argv[2:])
