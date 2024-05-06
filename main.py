import os
import time

from rdflib import Graph
from rdflib_hdt import HDTStore, optimize_sparql

global M100
global M300

global GraphM100
global GraphM300

def init():
    optimize_sparql()

    global M100
    global M300

    global GraphM100
    global GraphM300

    start100 = time.time()
    M100 = HDTStore("datasets/watdiv.100M.hdt")
    end100 = time.time()

    time100 = end100 - start100

    print(f"\nLoaded watdive 100M in {time100} seconds\n")

    start300 = time.time()
    M300 = HDTStore("datasets/watdiv.300M.hdt")
    end300 = time.time()

    time300 = end300 - start300

    print(f"\nLoaded watdiv 300M in {time300} seconds\n")

    GraphM100 = Graph(store=M100)
    GraphM300 = Graph(store=M300)

def runQueries():
    global M100
    global M300

    global GraphM100
    global GraphM300

    M100Times = {}
    M300Times = {}

    directory = "./queries/M100"
    for queryFile in os.listdir(directory):
        f = os.path.join(directory, queryFile)

        if os.path.isfile(f):
            query = ""

            with open(f, 'r') as qfile:
                qTemp = qfile.readlines()
                for line in qTemp:
                    line = line.replace('\t', ' ')
                    query += line

            startQuery100 = time.time()
            results = GraphM100.query(query)
            for result in results:
                pass
            endQuery100 = time.time()

            queryTime100 = endQuery100 - startQuery100

            M100Times[queryFile] = queryTime100

    directory = "./queries/M300"
    for queryFile in os.listdir(directory):
        f = os.path.join(directory, queryFile)

        if os.path.isfile(f):
            query = ""

            with open(f, 'r') as qfile:
                qTemp = qfile.readlines()
                for line in qTemp:
                    line = line.replace('\t', ' ')
                    query += line

            startQuery300 = time.time()
            results = GraphM300.query(query)
            for result in results:
                pass
            endQuery300 = time.time()

            queryTime300 = endQuery300 - startQuery300

            M300Times[queryFile] = queryTime300

    return (M100Times, M300Times)


            

                

if __name__ == "__main__":
    init()
    M100Times, M300Times = runQueries()

    M100Times = dict(sorted(M100Times.items()))
    M300Times = dict(sorted(M300Times.items()))

    for name, queryTime in M100Times.items():
        print(name + " " + str(queryTime * 1000))

    for name, queryTime in M300Times.items():
        print(name + " " + str(queryTime * 1000))