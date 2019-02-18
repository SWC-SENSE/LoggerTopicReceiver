import matplotlib.pyplot as plt
import numpy as np
import matplotlib


def tryParse(s):
    try:
        return int(s)
    except:
        return 1



class VisConf:

    def __init__(self):

        #matplotlib.rcParams['patch.edgecolor'] = 'FFFFFF'
        matplotlib.rcParams['axes.facecolor'] = '000000'
        matplotlib.rcParams['axes.edgecolor'] = 'AAAAAA'
        #matplotlib.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']
        matplotlib.rcParams['text.color'] = 'AAAAAA'
        #matplotlib.rcParams['xtick.alignment'] = 'top'
        #matplotlib.rcParams['ytick.alignment'] = 'center_baseline'
        #matplotlib.rcParams['xtick.direction'] = 'in'
        #matplotlib.rcParams['ytick.direction'] = 'in'
        matplotlib.rcParams['ytick.color'] = 'AAAAAA'
        matplotlib.rcParams['xtick.color'] = 'AAAAAA'
        #matplotlib.rcParams['xtick.color'] = 'FFFFFF'
        #matplotlib.rcParams['ytick.labelright'] = True
        matplotlib.rcParams['xtick.labelbottom'] = True
        #matplotlib.rcParams['xtick.labeltop'] = True
        matplotlib.rcParams['text.latex.preview'] = True

        matplotlib.rcParams['toolbar'] = 'None'







        self.subplots = [[]]
        self.figure = plt.figure(figsize=(1, 1), facecolor=[0,0,0,1])


    def prepare(self, amountPlots, plotsInCol=3):
        """
        Prepares the figure + subplots, returns its dimensions
        :param: amountPlots     the amount of topics that are already received.


        Sets:
        self.figure
        self.subplots

        :return:    rows, cols
        """
        szpp = 3 # <size per plot
        self.rows = int(np.ceil(amountPlots / plotsInCol))
        self.cols = int(min(amountPlots, plotsInCol))
        if self.rows != len(self.subplots) or len(self.subplots) == 0 or self.cols != len(self.subplots[0]):
            # in case some plots already exists, close it
            plt.close("all") ## XXX: it might be a good idea to just close the old plot
                             #       for having multiple visuaizer configurations run
                             #       simultaneously
            # Initialize all figures and suplots, such that they are ready for being used in #plot
            self.figure = plt.figure(figsize=(szpp*self.cols,szpp*self.rows), facecolor=[0,0,0,1])
            plt.subplots_adjust(0.14 / self.cols, 0.10 / self.rows, 1 - .02 / self.cols, 1-.10 / self.rows)
            self.subplots = [[plt.subplot(self.rows, self.cols, r*self.cols + c+1) for c in range(self.cols)] \
                for r in range(self.rows)]

        return self.rows, self.cols


    def plot(self, plotNumber, plotTitle, content):
        """
        :plotNumber:
        """
        sp = self.subplots[int(np.floor(plotNumber / self.cols))][plotNumber % self.cols]
        sp.clear()
        name = ""

        for j in content:
            lkz = content[j][1]
            tkz = content[j][0]
            name = j if j else plotTitle
            
            if lkz.shape[0]:
           
                #
                # Should work with arbritrary awmount of parameters
                if tkz == "scatter" or tkz == "points" or tkz == "histogram":
                    x = lkz[:,0] if lkz.shape[1] > 1 else np.arange(lkz.shape[0])
                    yy = lkz[:,1:] if lkz.shape[1] > 1 else lkz[:,0:1]
                    yy = yy.T

                    sheep = yy.shape[0]#< everything that used to be there will be there.
                    titles=[]
                    if tkz == "histogram":
                        for en in range(lkz.T.shape[0]):
                            titles += [ "[" + str(en) + "]"]
                        sp.hist(lkz, label=titles)
                    else:
                        for en in range(sheep):
                            y = yy[en]
                            if tkz == "points":
                                sp.plot(x, y, 
                                        label= name + ("[" + str(en) + "]" if yy.shape[0] > 1 else ""))
                            else:
                                sp.plot(x, y,  
                                        label= name + ("[" + str(en) + "]" if yy.shape[0] > 1 else ""))


                
                elif tkz == "interval" :
                    assert(lkz.shape[1] == 2 or lkz.shape[1] == 3)
                    x = np.hstack((lkz[:,0:2], np.ones(lkz.shape[0])[:,np.newaxis] * np.nan)).flatten()
                    y = np.ones(x.shape[0])  * (lkz[0,2] if lkz.shape[1] == 3 else tryParse(j))

                    sp.plot(x, y, label= name)
                
        sp.legend()
        sp.set_title(name)

        pass

