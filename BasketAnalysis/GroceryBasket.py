from collections import defaultdict
import BasketAnalysis.Apriori as a

from itertools import chain
file = r"C:/Dev/Datasets/Retail/retail.dat"

# dataset is a two dim list, with one sublist of items for each cart
dataset = [[int(tok) for tok in line.strip().split()] for line in open(file)]
#get every 20th item
#list notation seq =[start:stop:step]
#doing this to make slow apriori implementation run
dataset = dataset[::20]


counts = defaultdict(int)

#chain allows iterating through all items in each cart as if
#they were in one list
for elem in chain(*dataset):
    counts[elem] += 1

ap = a.apriori_simple(counts,80,dataset)

print (ap.count())
print (ap)