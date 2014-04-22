from collections import defaultdict

def apriori_simple(counts,minsupport,dataset):


    #very inefficient implementation
    #no actually, impossibly slow implementation
    valid = set(k for k,v in counts.items() if (v >=minsupport))
    dataset = [[el for el in ds if (el in valid)] for ds in dataset]
    dataset = [frozenset(ds) for ds in dataset if len(ds) > 1]

    #frozenset is immutable so elements can be used as dictionary
    #or as element in another set
    itemsets = [frozenset([v]) for v in valid]

    allsets = [itemsets]
    newsets = []
    for j in range(16):
        print ("increment:")
        print (j)
        for i,ell in enumerate(itemsets):
            print (i)
            print (ell)
            for v_ in valid:
                if v_ not in ell:
                    newset = (ell|set([v_]))
                    c_newset = 0
                    for d in dataset:
                        if set(d).issuperset(newset) :
                            c_newset +=1
                    if c_newset > minsupport:
                        newsets.append(newset)
                        print ("added c_newset")
        allsets.append(newsets)
        itemsets = (newsets)
    return allsets
    




