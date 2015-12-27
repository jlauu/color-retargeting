from __future__ import print_function
import sys
from math import sqrt

class Edge:
    def __init__(self, fdo, n1, n2, eqlen):
        self.fdo = fdo
        self.n1 = n1
        self.n2 = n2
        self.eqlen = eqlen

    def applySpringForces(self):
        f12 = [ r - l for l,r in zip(self.n1.p, self.n2.p) ]
        f12 = self.fdo.normalize(*f12)
        f12 = [ f * self._dLength() * self.fdo.getSpringConst() for f in f12]
        self.n2.f = [ a + b for a, b in zip(f12, self.n2.f) ]
        self.n1.f = [ a - b for a, b in zip(f12, self.n1.f) ]

    def _dLength(self):
        l = self.fdo.dist(self.n1.p, self.n2.p)
        return self.eqlen - l
        

class Node:
    def __init__(self, fdo, p, i, mass=1):
        self.fdo = fdo
        self.m = mass
        self.i = i
        self.p = p
        self.v = [ 0 for x in range(self.fdo.dims) ]
        self.zeroForce()

    def zeroForce(self):
        self.f = [ 0 for x in range(self.fdo.dims) ]

    def applyCoulombForceTo(self, other):
        f12 = [ r - l for l,r in zip(self.p, other.p) ]
        f12 = self.fdo.normalize(*f12)

        r = self.fdo.dist(self.p, other.p)
        r = max(r, self.fdo.getZeroDist())

        # mass * const / r^2
        other.f = [ f + fon * (self.m * self.fdo.getCoulombConst() / (r*r)) for f, fon in zip(other.f, f12)]


    def update(self, t):
        self.f = [ x * self.fdo.getDampConst() for x in self.f ]
        accel = [ x / self.m for x in self.f ]
        
        # vt
        vv = [ v * t for v in self.v ]
        
        # .5a^2
        aa = [ .5 * t * t * a for a in accel ]

        # p = p + vt + .5at^2
        self.p = [ p + v + a for p,v,a in zip(self.p, vv, aa) ]
        
        # v = v + a*t
        self.v = [ v + a*t for v,a in zip(self.v, accel)]

    def calcKE(self):
        return .5 * self.m * sum([x*x for x in self.v])

class FDO:
    # maybe all these should be @property
    # but static methods can be overridden by more interesting
    # derived FDO classes
    @staticmethod
    def getSpringConst():
        return 2 
    @staticmethod
    def getCoulombConst():
        return .2
    @staticmethod
    def getDampConst():
        return .8
    @staticmethod
    def getTimeStep():
        return .01
    @staticmethod
    def getCutoffKE():
        return 1000
    @staticmethod
    def getZeroDist():
        return 1

    @staticmethod
    def normalize(*vector):
        mag = FDO.mag(*vector)
        return [ v/mag for v in vector ]

    @staticmethod
    def mag(*vector):
        return FDO.dist([0 for i in range(len(vector))], vector)

    @staticmethod
    def dist(a, b):
        d = 0
        for l,r in zip(a,b):
            d += pow(r - l, 2)
        return sqrt(d)

    def __init__(self, dimensions):
        self.dims  = dimensions
        self._nodes = list()
        self._edges = list()
        self.size  = 0
        self.totalKE = 0

    def addNode(self, *point):
        if len(point) is not self.dims: return
        try:
            p = [ float(f) for f in point ]
            n = Node(self, p, self.size)
            self._nodes.append(n)
            self.size += 1
        except ValueError:
            print("Bad node format, not added", file=sys.stderr)
        return n

    def addSpring(self, n1, n2, eqlen=None):
        e = Edge(self, n1, n2, eqlen if eqlen is not None else self.dist(n1.p,n2.p))
        self._edges.append(e)

    def zeroNodeForces(self):
        for n in self._nodes:
            n.zeroForce()

    def applyForces(self):

        # attraction forces
        for n1 in self._nodes:
            for n2 in self._nodes:
                if n1.i is not n2.i:
                    n1.applyCoulombForceTo(n2)

        # spring forces
        for e in self._edges:
            e.applySpringForces()


    def _step(self, t=None):
        if t is None: t = FDO.getTimeStep()
        
        self.zeroNodeForces()
        self.applyForces()

        for n in self._nodes:
            n.update(t)
            self.totalKE += n.calcKE()

    def run(self, iterations=None, timestep=None):
        i = 0
        self.totalKE = 0
        iters = 50 if iterations is None else iterations
        t = self.getTimeStep() if timestep is None else timestep
        while (i < iters or self.totalKE < self.getCutoffKE()):
            self._step(t)
            i += 1

    def nodes(self):
        for n in self._nodes:
            yield n.p

    def print(self):
        for n in self.nodes():
            print(n)

