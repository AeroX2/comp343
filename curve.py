#!/bin/env python3

from math import sqrt

class Curve:
    def __init__(self, a, b, p):
        self.a = a;
        self.b = b;
        self.p = p;

    def invmod(self, x):
        if x % self.p == 0:
            raise ZeroDivisionError("Impossible inverse")
        return pow(x, self.p-2, self.p);

    def valid(self, p):
        return (p[1]**2 - (p[0]**3 + self.a*p[0] + self.b)) % self.p == 0

    def add(self, p1, p2):
        x1,y1 = p1
        x2,y2 = p2

        if x1 == None:
            return p2
        if x2 == None:
            return p1

        if x1 == x2 and y1 == y2:
            if ((2*y1) == 0):
                return (None,None)
            halflife = (3*pow(x1,2,self.p)+self.a) * self.invmod(2*y1)
        else:
            if ((x2-x1) == 0):
                return (None,None)
            halflife = (y2-y1) * self.invmod(x2-x1)

        x = (pow(halflife,2,self.p) - x1 - x2) % self.p;
        y = (halflife*(x1-x) - y1) % self.p;

        assert self.valid((x,y))
        return (x,y)

    def mul(self, p, n):
        r = (None, None);
        while n:
            if (n & 1):
                r = self.add(r,p)
            p = self.add(p,p)
            n >>= 1
        return r

    def order(self, p):
        i = 0;
        r = p;
        while r is not None:
            if (i & 1):
                r = self.add(r,p)
            p = self.add(p,p)
            i<<=1
        return i
    
    def lowest_x(self):
        x = 1;
        y = sqrt((x**3 + self.a*x + self.b) % self.p)
        y = sqrt((pow(x,3,self.p) + (self.a%self.p*x%self.p)%self.p + self.b%self.p) % self.p)
        while (y >= self.p/2):
            y = sqrt((x**3 + self.a*x + self.b) % self.p)
            y = sqrt((pow(x,3,self.p) + (self.a%self.p*x%self.p)%self.p + self.b%self.p) % self.p)
            x += 1
        return x,y;

    def highest_x(self):
        x = self.p-1;
        y = sqrt((x**3 + self.a*x + self.b) % self.p)
        while (y <= self.p/2):
            y = sqrt((pow(x,3,self.p) + (self.a%self.p*x%self.p)%self.p + self.b%self.p) % self.p)
            x -= 1
        return x,y;


    
p = 786831054276193
a = 692921120522918
b = 725362064236058
E = Curve(a,b,p)

print(E.lowest_x());
print(E.highest_x());

#P =                [98787801814401, 518250957953530] is a point on E of order 786831073953473
#test = (E.add(      (98787801814401, 518250957953530), (98787801814401, 518250957953530)))
#print(test)
#test = (E.add(test, (98787801814401, 518250957953530)))
#print(test)
#test = (E.add(test, (98787801814401, 518250957953530)))
#print(test)
#print(E.mul((98787801814401, 518250957953530), 547))
#print(E.mul((98787801814401, 518250957953530), 786831073953473))
#print(E.order((98787801814401, 518250957953530)))


