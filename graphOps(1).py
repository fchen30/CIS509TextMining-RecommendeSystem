# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 20:56:56 2017

@author: hina
"""

import networkx

asin = '0805047905'

# read the copurchase graph
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# get degree centrality of given asin
dcl = networkx.degree(copurchaseGraph)
dc = dcl[asin]
print ("Degree Centrality:", dc)

# get ego network of given asin at depth 1
ego = networkx.ego_graph(copurchaseGraph, asin, radius=1)
print ("Ego Network:", 
       "Nodes =", ego.number_of_nodes(), 
        "Edges =", ego.number_of_edges())

# get clustering coefficient of given asin
cc = networkx.average_clustering(ego)
print ("Clustering Coefficient:", round(cc,2))
        
# get one-hop neighbors of given asin
ngbs = ego.neighbors(asin)
print ("Number of one-hop neighbors:", len(ngbs))
#print (ngbs)

# use island method on ego network
threshold = 0.90
egotrim = networkx.Graph()
for n1, n2, e in ego.edges(data=True):
    if e['weight'] >= threshold:
        egotrim.add_edge(n1,n2,e)
print ("Trimmed Ego Network:", 
       "Threshold=", threshold,
       "Nodes =", egotrim.number_of_nodes(), 
        "Edges =", egotrim.number_of_edges())
