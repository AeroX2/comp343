#!/bin/env python3

import re
import sys
import subprocess
from math import log,sqrt,ceil
from multiprocessing import Pool

def string2decimal(string):
    t = "";
    v = [];
    for i in enumerate(string):
        v.append(ord(i[1]));

    #print(v);
    r = 0;
    for i in enumerate(v):
        r += i[1]*pow(128,len(v)-i[0]-1)
    return r;

def decimal2string(decimal):
    output = [];
    while (decimal > 0):
        decimal, r = divmod(decimal, 128)
        output.insert(0,r);
    #print(output)
    for i in enumerate(output):
        if (i[1] >= 32):
            output[i[0]] = chr(i[1])
        else:
            return None;
    return ''.join(output);

def hash_internal(string, d=-1):
    if (d == -1):
        d = string2decimal(string);

    n1 = d >> t-1
    n2 = d & ~(-1 << t-1)
    a = pow(alpha, n1, p)
    b = pow(beta, n2, p)
    return (a * b) % p, a, b, n1, n2, d;

def hash(string, d=-1):
    abp, a, b, n1, n2, d = hash_internal(string,d=d); 
    print("     D: %d" % d);
    print("     A: %d" % a);
    print("     B: %d" % b);
    print("    n1: %d" % n1);
    print("    n2: %d" % n2);
    print("String: %s" % string.strip());
    print("  Hash: %s" % abp);
    print()

def shanks(y, a, n):
    """ Shanks' baby-step giant-step for finding discrete logarithms 
        of form : a^x mod n = y, solve for x
    """
    print(y,a,n)
    #sys.stdout.flush()

    output = subprocess.run(["./discrete", str(y), str(a), str(n)], stdout=subprocess.PIPE);
    return int(output.stdout)

def helper(powers):
    final = []

    if powers:
        power = powers[0][0]
        max_count = powers[0][1]
    else:
        return [(1,1)]

    for count in range(max_count+1):
        blob = helper(powers[1:])
        for tmp in blob:
            a = tmp[0]*pow(power, count)
            b = tmp[1]*pow(power, (max_count-count))
            final.append((a,b))
    return final

def get_pairs(factors):
    powers = []
    for factor in set(factors):
        powers.append((factor, factors.count(factor)))
    return helper(powers);

def find_factors(n):
    i = 2;
    factors = []
    while n > i*i:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors;

def process(pair):
    a = pair[0];
    b = pair[1];

    n1 = 0;
    if (a != 1):
        n1 = shanks(a,alpha,p);

    n2 = 0;
    if (b != 1):
        n2 = shanks(b,beta,p);

    global big;
    d = n1 * big;
    d += n2 - (d % big);

    if (n2 > big):
        print("Invalid n2", n2);
    elif (d // big != n1):
        print("Invalid n1", d // big, n1);
    elif (d % big != n2):
        print("Invalid n2", d % big, n2);
    else:
        print("D found", d);
        string = decimal2string(d);
        if (string is not None):
            return string
        #return d;
    return None;

def find_conflicts(string):
    abp, a, b, n1, n2, d = hash_internal(string);
    factors = find_factors(a*b);

    global big;
    big = pow(2,t-1);

    pairs = get_pairs(factors);
    for pair in pairs:
        yield process(pair);
    #return Pool().map(process, pairs)

t = 56
p = 47687490304404143
alpha = 8691170756970600
beta = 36184489036644108

#t = 32
#p = 2180082167
#alpha = 485539736
#beta = 329746418

potentials = []
winners = []

string = input("String: ")
conflicts = find_conflicts(string)
for conflict in conflicts:
    if conflict is None:
        continue;
    if conflict == string:
        print("Conflict is the same")
        continue;
    a, _, _, _, _, _ = hash_internal(conflict);
    b, _, _, _, _, _ = hash_internal(string);
    if (a == b):
        if not re.match(r'^[^\W0-9_]+$', conflict):
            print("Partial winner", conflict)
            potentials.append(conflict);
            continue;
        print("We have a WINNER!!!, DING DING DING")
        print(conflict)
        #sys.stdout.flush()
        winners.append(conflict);

hash(string)
if potentials:
    print("Potentials");
for potential in potentials:
    hash(potential)

if winners:
    print("WINNERS!!!");
for winner in winners:
    hash(winner)

#Brute force method
#f = open('words.txt', 'r')
#i = 0;
#for line in f:
#    line = line.strip()
#    if (hash(line) == magic):
#        print("Holy shit");
#        print(line);
#        break;
#    i+=1
#    if (i % 10000 == 0):
#        i = 0;
#        print(line);

