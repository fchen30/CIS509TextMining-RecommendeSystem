# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 10:29:32 2016

@author: hina
"""
print ()

import networkx
from operator import itemgetter
from networkx import algorithms
import matplotlib.pyplot
import math
from itertools import islice

# definie class similarity
class similarity:
    
    # Class instantiation 
    def __init__ (self, ratingP, ratingQ):
        self.ratings1 = ratingP
        self.ratings2 = ratingQ

    # Minkowski Distance between two vectors
    def minkowksi(self, r):
    
        # calcualte minkowski distance
        distance = 0       
        for k in (set(self.ratings1.keys()) & set(self.ratings2.keys())):
            p = self.ratings1[k]
            q = self.ratings2[k]
            distance += pow(abs(p - q), r)
    
        # return value of minkowski distance
        return pow(distance,1/r)

    # Pearson Correlation between two vectors
    def pearson(self):
        
        sumpq = 0
        sump = 0
        sumq = 0
        sump2 = 0
        sumq2 = 0
        n = 0

        # calcualte pearson correlation using the computationally efficient form        
        for k in (set(self.ratings1.keys()) & set(self.ratings2.keys())):
            n += 1
            p = self.ratings1[k]
            q = self.ratings2[k]
            sumpq += p * q
            sump += p
            sumq += q
            sump2 += pow(p, 2)
            sumq2 += pow(q, 2)
    
        # error check for n==0 condition
        if n == 0:
            print (">>> pearson debug: n=0; returning -2 correlation!")
            return -2    

        # calcualte nr and dr for pearson correlation
        nr = (sumpq - (sump * sumq) / n)
        dr = (math.sqrt(sump2 - pow(sump, 2) / n) * 
                        math.sqrt(sumq2 - pow(sumq, 2) / n))
        
        # error check for dr==0 condition
        if dr == 0:
            print (">>> pearson debug: denominator=0; returning -2 correlation!")
            return -2

        # return value of pearson correlation coefficient        
        return nr / dr




# read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating'] = float(cell[8].strip())
    MetaData['DegreeCentrality'] = int(cell[9].strip())
    MetaData['ClusteringCoeff'] = float(cell[10].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()
#print ("Number of Nodes:")
#print (copurchaseGraph.number_of_nodes())
#print ()
#
#print ("Number of Edges:")
#print (copurchaseGraph.number_of_edges())
#print ()



## plot the weighted graph
#pos=networkx.spring_layout(G)
#matplotlib.pyplot.figure(figsize=(10,10))
#networkx.draw_networkx_nodes(G,pos,node_size=1500)
#networkx.draw_networkx_labels(G,pos,font_size=20)
#edgewidth = [ d['weight'] for (u,v,d) in G.edges(data=True)]
#networkx.draw_networkx_edges(G,pos,edge_color=edgewidth,width=edgewidth)
#edgelabel = networkx.get_edge_attributes(G,'weight')
#networkx.draw_networkx_edge_labels(G,pos,edge_labels=edgelabel,font_size=20)
#matplotlib.pyplot.axis('off')
#matplotlib.pyplot.savefig("graph.png") 
#matplotlib.pyplot.show()
# now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
asin = '0805047905'

# create variables 
newBookList={}
ratingDistances = []
bookSortedDistances = []
pearsonScore=[]  
kNNBookList = {}
relatedList=[]
# example code to start looking at metadata associated with this book
print ("ASIN = ", asin) 
print ("Title = ", amazonBooks[asin]['Title'])
print ("SalesRank = ", amazonBooks[asin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[asin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[asin]['AvgRating'])
#print ("DegreeCentrality = ", amazonBooks[asin]['DegreeCentrality'])
#print ("ClusteringCoeff = ", amazonBooks[asin]['ClusteringCoeff'])
#print ("Dijkstra Shortest Path from node A to node D:")

ego = networkx.ego_graph(copurchaseGraph, asin, radius=1)
#print ("Ego Network:", 
#       "Nodes =", ego.number_of_nodes(), 
#        "Edges =", ego.number_of_edges())

# How close the similarity you want 
threshold = 0.25
egotrim = networkx.Graph()
for n1, n2, e in ego.edges(data=True):
    if e['weight'] >= threshold and n1 == asin:
        egotrim.add_edge(n1,n2,e)

#check if the program can find edges for the apointed book with the current threshold value, if not, exit the program
if egotrim.number_of_edges()>=1:
    relatedList=[x[1] for x in egotrim.edges()]
else:
    print("The threshold is too high, there is no connected node")
    

  


if relatedList == []:
    print("Pease lower your threshold and try again")
else:
    for item in relatedList:
        for key in amazonBooks:
            if item == key:
                newBookList[key]= {'SalesRank': amazonBooks[key]['SalesRank'], 'TotalReviews': amazonBooks[key]['TotalReviews'], 'AvgRating': amazonBooks[key]['AvgRating']}
        
    

apointedBook = {'SalesRank': amazonBooks[asin]['SalesRank'], 'TotalReviews': amazonBooks[asin]['TotalReviews'], 'AvgRating': amazonBooks[asin]['AvgRating']}

#print(apointedBook)
#print(newBookList)
        
# find the euclidean distance between apointedbook's ratings, and each of the other book's ratings.
# use a for loop to get at the other users and their ratings
# use the similarity class to caclulate the euclidean distance between book ratings.



for i in sorted(newBookList.keys()):
#    tup1 = ()
    
    X=similarity(apointedBook, newBookList[i])
    tup1=(i,round(X.minkowksi(2),2))
    ratingDistances.append(tup1)
    tup1 = ()


# sort list of tuples by lowest distance to highest distance.
# assign sorted list to variable ratingSortedDistances.



bookSortedDistances = sorted(ratingDistances, key=lambda x:x[1])
# apointedbook's NN is the book at the 0th position of the sorted list.

k=3
bookKNN = list(islice(bookSortedDistances,k))

# the closest three books of the apointed book

for item in bookKNN:
    for key in amazonBooks:
        if item[0] == key:
            kNNBookList[key]= {'SalesRank': amazonBooks[key]['SalesRank'], 'TotalReviews': amazonBooks[key]['TotalReviews'], 'AvgRating': amazonBooks[key]['AvgRating']}

# check for pearson coorlation
    
for i in sorted(kNNBookList.keys()):
#    tup2 = ()
    
    X=similarity(apointedBook, kNNBookList[i])
    #computer and normalize pearson correlation
    tup2=(i,round((X.pearson()+1)/2,2))
    pearsonScore.append(tup2)
    tup2 = ()  

#dr = 0
#for item in pearsonScore:
#    dr +=item[1]
#
#weight = []
#
#for item in pearsonScore:
#    tup3=(item[0],round(item[1]/dr,2))
#    weight.append(tup3)
#    tup3=()
#
#print(weight)

#predictBook = {}


#only recommend books with certain similarity 
pearsonThreshold = 0.9
if relatedList==[]:
     print()
else:
    
    print ()
    print ("Recommendations:")
    print ("--------------------------------------------------------------")
    for item in pearsonScore:
        if item[1]>=pearsonThreshold:
            print("Title ", amazonBooks[item[0]]['Title']+'\n'+"TotalReviews", amazonBooks[item[0]]['TotalReviews'],'\n'+"Avg Rating ",amazonBooks[item[0]]['AvgRating'],'\n'+"Pearson Coorelation ",item[1])
            print()





