"""
Johnny Lau

Summary: kNN clustering module.

"""
import math
from random import choice

class ClusterKMeans:
        def __init__(self, raw, k):
                self.raw = raw
                self.size = len(raw.data)
                #self.ranges = self.calc_ranges(raw)
                self.data = dict.fromkeys(self.raw.data, 0)
                self.reset(k)

        def init_centers(self, k):
                self.centers = [choice(self.raw.data) for x in range(k)]

        def print_centers(self):
                print("Centers: ")
                for center in self.centers:
                        print(center)

        def assign_points(self):
                for point in self.data:
                        dist = None
                        for k, c in enumerate(self.centers):
                                new_dist = sqr_dist(point, c)
                                if dist is None: dist = new_dist
                                #print ("%dth center: %s has sqr dist %s to point: %s" % (k, c, new_dist, point))
                                if new_dist <= dist:
                                        #print ("%f vs %f pick:" %(dist, new_dist))
                                        dist = new_dist
                                        self.data[point] = k
                                #print("Center#%d: %s with dist %f" % (k, c, dist))

        def reset(self, k):
                self.init_centers(k)
                #  initialize empty hash: point -> index of center
                #self.print_centers()
                self.assign_points()
                #print("Quality: ", self.calc_quality())

        def iterate(self):
                num_attr = len(self.raw.attr)
                #  initialize list of [summed point, total elements] pairs
                new_centers = [ [[0]*num_attr,0] for x in self.centers]
                #new_centers = [map(lambda x: [(0,)*num_attr, 0], self.centers)
                for point, k in self.data.items():
                        new_centers[k][1] += 1 # number of terms
                        new_centers[k][0] = sum_points(new_centers[k][0], point)
                new_centers = list(map(mean_helper, new_centers))
                #print ('new centers: ', new_centers)
                self.centers = new_centers
                self.assign_points()
                #self.print_centers()
                #print("Quality: ",self.calc_quality())

        def calc_quality(self):
                quality = 0.0
                for point, k in self.data.items():
                        quality += sqr_dist(point, self.centers[k])
                return quality


"""
                HELPER FUNCTIONS
"""

def sqr_dist(pt_x, pt_y):
        #assert len(pt_x) == len(pt_y), "Data points must be in the same dimension"
        squares = []
        num_attr = len(pt_x)
#        return sum([math.pow(pt_x[i] - pt_y[i], 2) for i in range(num_attr)])
        for i in range(len(pt_x)):
                squares.append(math.pow(pt_x[i] - pt_y[i],2))

        return sum(squares)

def distance(pt_x, pt_y):
        return math.sqrt(sqr_dist(pt_x,pt_y))
                
def sum_points(pt_x, pt_y):
        assert len(pt_x) == len(pt_y), "Data points must be in the same dimension"
        new_pt = tuple()
        for i in range(len(pt_x)):
                new_pt += (pt_x[i] + pt_y[i],)
        return new_pt

def mean_helper(mean_pairs):
        num_terms = mean_pairs[1]
        # prevent divison by 0
        if num_terms is 0: 
                num_terms = 1.0
        else:
                num_terms = float(num_terms)
        point = mean_pairs[0]
        return [ sum/num_terms for sum in point]
        #return tuple(map(lambda sum: sum/num_terms, point))

