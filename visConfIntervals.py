import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import random

from visualizationConfiguration import VisConf

import time


def tryParse(s):
    try:
        return int(s)
    except:
        return 1

def timelines(y, xstart, xstop, sp, color='b'):
    """Plot timelines at y from xstart to xstop with given color."""   
    sp.hlines(y, xstart, xstop, color, lw=2)

    sp.vlines(xstart, -1, 2, color, "--", lw=.08)
    sp.vlines(xstop, -1, 2, color, "--", lw=.08)


    sp.vlines(xstart, y+.1, y-0.1, color, lw=1)
    sp.vlines(xstop, y+.1, y-0.1, color, lw=1)




class VisConfIntervals(VisConf):

    def __init__(self):

        #matplotlib.rcParams['patch.edgecolor'] = 'FFFFFF'
        matplotlib.rcParams['axes.facecolor'] = 'FFFFFF'
        #matplotlib.rcParams['axes.edgecolor'] = 'AAAAAA'
        #matplotlib.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
        #matplotlib.rcParams['text.color'] = 'AAAAAA'
        #matplotlib.rcParams['xtick.alignment'] = 'top'
        #matplotlib.rcParams['ytick.alignment'] = 'center_baseline'
        #matplotlib.rcParams['xtick.direction'] = 'in'
        #matplotlib.rcParams['ytick.direction'] = 'in'
        #matplotlib.rcParams['ytick.color'] = 'AAAAAA'
        #matplotlib.rcParams['xtick.color'] = 'AAAAAA'
        #matplotlib.rcParams['xtick.color'] = 'FFFFFF'
        #matplotlib.rcParams['ytick.labelright'] = True
        matplotlib.rcParams['xtick.labelbottom'] = True
        #matplotlib.rcParams['xtick.labeltop'] = True
        matplotlib.rcParams['text.latex.preview'] = True

        matplotlib.rcParams['toolbar'] = 'None'
        self.ptt = [0, 0]
        self.last = 0

        self.namedict = {}

        




        self.subplots = [[]]
        self.szpp = 3 # <size per plot
        self.figure = plt.figure(figsize=(self.szpp, self.szpp*3), facecolor=[0,0,0,1])


    def prepare(self, amountPlots, plotsInCol=3):
        """
        Prepares the figure + subplots, returns its dimensions
        :param: amountPlots     the amount of topics that are already received.


        Sets:
        self.figure
        self.subplots

        :return:    rows, cols
        """
        self.rows = 3
        self.cols = 1
        if self.rows != len(self.subplots) or len(self.subplots) == 0 or self.cols != len(self.subplots[0]):
            # in case some plots already exists, close it
            plt.close("all") ## XXX: it might be a good idea to just close the old plot
                             #       for having multiple visuaizer configurations run
                             #       simultaneously
            # Initialize all figures and suplots, such that they are ready for being used in #plot
            self.figure = plt.figure(figsize=(5*3,self.szpp*self.rows), facecolor=[1,1,1,1])
            plt.subplots_adjust(0.01 / self.cols, 0.10 / self.rows, 1 - .02 / self.cols, 1-.10 / self.rows)
            self.subplots = [[plt.subplot(self.rows, self.cols, r*self.cols + c+1) for c in range(self.cols)] \
                for r in range(self.rows)]
            for s in self.subplots:
                for o in s:
                    o.axis("off")

            sp = self.subplots[0][0]
            img = matplotlib.image.imread("file.png")
            #sp.imshow(img, extent=[-2.56*5, 2.56*5, -1*5, 1*5], aspect=1)
            sp.imshow(img, interpolation='nearest')#, aspect='auto')

        return self.rows, self.cols


    def plot(self, plotNumber, plotTitle, content):
        """
        :plotNumber:
        """
        sp = self.subplots[1][0]
        name = ""

        now = 0

        for j in content:
            lkz = content[j][1]
            tkz = content[j][0]

            ctt = [lkz[-1][0], lkz[-1][3]]
            if ctt[0] != self.ptt[0] or ctt[1] != self.ptt[1]:
                divisor = 1000000000.
                now = max(now, lkz[-1,2]/divisor)
                #sp.clear()
                name = j if j else plotTitle
                
                #xfmt = matplotlib.dates.DateFormatter('%M:%S')
                #sp.xaxis.set_major_formatter(xfmtcolor)
                if not name in self.namedict:
                    #label, insert and generate color
                    color = np.array([random.random() * 1, random.random() * 1, random.random()])
                    self.namedict[name] = color
                    sp.scatter(lkz[:,1]/divisor, lkz[:,3], label="Optimal Fragment" if lkz[:,3][0]  == -1 else "Query " +  str(lkz[:,3][0]), c=color)
                else:
                    color = self.namedict[name]

                    sp.scatter(lkz[:,1]/divisor, lkz[:,3], c=color)

                if lkz[:,3][0] == -1:
                    sp.vlines(lkz[:,1]/divisor, -1, 2, color, linestyles='dotted', lw=.2)
                    #sp.vlines(xstop, y+.1, y-0.1, color, lw=1)

                timelines(lkz[:,3], lkz[:,0]/divisor, lkz[:,2]/divisor, sp, "black" if lkz[:,3][0] != -1 else color) 
                sp.tick_params(top=False, bottom=True, left=False, right=False, labelleft=False, labelbottom=True)
                sp.grid()
                #for spine in sp.spines.values():
                #   spine.set_visible(False)
                sp.grid()

                self.ptt = ctt


            
            if lkz.shape[0]:
                pass
                #print(tkz, lkz.shape, j)
                #
                # Should work with arbritrary awmount of parameters
                #y = lkz[:,3]
                #x = lkz[:,1:3]

                #x = np.hstack((lkz[:,0:2], np.ones(lkz.shape[0])[:,np.newaxis] * np.nan)).flatten()
                #y = np.ones(x.shape[0])  * (lkz[0,2] if lkz.shape[1] == 3 else tryParse(j))

                #sp.plot(x, y, label= name)
      
        if self.last and True:
            #for nn in np.arange(self.last, now, .1):
            val = 25
            #vls = (now - self.last) /(1.+np.exp(-np.arange(val)+val/2))
            vls = (now - self.last) *np.linspace(0, 1, val)
            #vls = (now - self.last)/2. /(1.+np.exp(-np.arange(val)+val/2)) + (now - self.last) / 2. * np.arange(val)/val
            for n in vls:
                #(nn - 25)**3 / 
                nn = self.last + n
                begin = nn - 6
                sp.set_xlim([begin, nn])
                plt.pause(.0001)
        self.last = now

        sp.legend(loc="upper left")
        sp.set_title(name)

        pass

