
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import subprocess
import sys
import copy
from scipy import interpolate

from backend import *
from visualizationConfiguration import * 
from visConfIntervals import * 
import time



backend = Backend(*sys.argv[1:])









def visualize():
    """
    Generic visualization iteration.
    """
    global visualizer


    #
    # Prepare the plot environment
    bk = backend.Z
    amountPlots = len(bk)
    if amountPlots == 0: return
    visualizer.prepare(amountPlots)


    # 
    # Plot all plots relevant to the current configuration
    ke = copy.deepcopy(list(bk.keys())) #< everything that used to be there will be there.
    for plti, i in enumerate(ke[:amountPlots]):

        if i == "multiquery.intervals":
            #print("[INFO]\ttriggered", i)
            visualizer.plot(plti, i, bk[i])

        else:
            pass
            #print("[INFO]\tIgnored", i)




def walk(multithreaded=True):
    if multithreaded: 
        backend.start()
    while True:

        visualize()
        nn = time.time()
        nnn = nn
        while nnn - nn < 1 and False:
            nnn = time.time()
            begin = nnn - 6
            if len(visualizer.subplots) >= 2 and len(visualizer.subplots[1]) >= 1:
                visualizer.subplots[1][0].set_xlim([begin, nnn])
            #plt.xlim([begin, nnn])
            plt.pause(.01)



#visualizer = VisConf()
visualizer = VisConfIntervals()
walk()








