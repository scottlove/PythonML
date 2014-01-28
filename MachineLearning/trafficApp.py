import scipy as sp
import matplotlib.pyplot as plt

def myScatterPlot (x,y,title,x_label,y_label,x_ticks,x_tickLabels):
    plt.scatter(x,y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(x_ticks,x_tickLabels)
    plt.autoscale
    plt.grid()
    plt.show()

def plotWebTraffic (x,y,numWeeks,f1):
    title = "Web traffic over the last month"
    x_label = "Time"
    y_label = "Hits/hour"
    #list of strings week 0 ...week 10
    x_tickLabels = ['week %i'%w for w in range(numWeeks)]
    #10 tick marks spaced at 1 week intervals
    x_ticks = [w*7*24 for w in range(numWeeks)]
    #myScatterPlot(x,y,title,x_label,y_label,x_ticks,x_tickLabels)
    plt.scatter(x,y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(x_ticks,x_tickLabels)
    plt.autoscale
    plt.grid()
    #plt.show()
    fx = sp.linspace(0,x[-1],1000)
    plt.plot(fx,f1(fx),linewidth=4)
    plt.legend(["d%u" % f1.order], loc="upper left")
    plt.show()





data = sp.genfromtxt("c:/temp/web_traffic.tsv",delimiter = "\t")

#split the data into two arrays
x = data[:,0]
y = data[:,1]

#this notation removes any rows where y does not exist
#cleaning the data
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

#get bestfit using 1st order line
#set full = False to only get model parameters.
fp1,residuals, rank, sv, recond = sp.polyfit(x,y,1,full=True)
#build model function based of best fit
f1= sp.poly1d(fp1)
plotWebTraffic(x,y,5,f1)












