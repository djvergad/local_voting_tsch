#!/usr/bin/python3
'''
\brief Plots timelines and topology figures from collected simulation data.

\author Thomas Watteyne <watteyne@eecs.berkeley.edu>
\author Kazushi Muraoka <k-muraoka@eecs.berkeley.edu>
\author Nicola Accettura <nicola.accettura@eecs.berkeley.edu>
\author Xavier Vilajosana <xvilajosana@eecs.berkeley.edu>
'''

import os
import re
import glob
import pprint

import numpy
import scipy
import scipy.stats

import matplotlib.pyplot

#============================ defines =========================================

DATADIR       = '.'
PREFIX        = os.path.basename(os.getcwd()).split('_',1)[-1]
CONFINT       = 0.95

COLORS_TH     = {
    'Shared':          'black',
    'All':          'red',
    'None':          'cyan',
    'otf_1':          'darkturquoise',
    'otf_4':          'magenta',
    'otf_10':         'blue',
    'eotf_0':         'lime',
    'eotf_1':         'gray',
    'eotf_4':         'green',
    'eotf_10':        'cyan',
    'local_voting':   'red' ,
    'local_voting_z': 'black',
}

LINESTYLE_TH       = {
    0:        '-',
    1:        '--',
    4:        '-.',
    'NA':        '-.',
    10:       ':',
}

ECOLORS_TH         = {
    'Shared':          'black',
    'All':          'red',
    'None':         'cyan',
    'otf_0':          'darkmagenta',
    'otf_1':          'darkturquoise',
    'otf_4':          'magenta',
    'otf_10':         'blue',
    'eotf_0':         'lime',
    'eotf_1':         'gray',
    'eotf_4':         'green',
    'eotf_10':        'cyan',
    'local_voting':   'red' ,
    'local_voting_z': 'black',
}
COLORS_PERIOD      = {
    'NA':     'red',
    1:        'blue',
    10:       'green',
    60:       'black',
}

LINESTYLE_PERIOD   = {
    'NA':     '--',
    1:        '--',
    10:       '-.',
    60:       ':',
}

FILLSTYLES_ALG = {
    'otf':    '',
    'local_voting': '/',
}

ECOLORS_PERIOD     = {
    'NA':     'red',
    1:        'blue',
    10:       'green',
    60:       'magenta',
}

pp = pprint.PrettyPrinter(indent=4)

#============================ helpers =========================================

def binDataFiles():
    '''
    bin the data files according to the otfThreshold and pkPeriod.

    Returns a dictionary of format:
    {
        (otfThreshold,pkPeriod): [
            filepath,
            filepath,
            filepath,
        ]
    }
    '''
    infilepaths    = glob.glob(os.path.join(DATADIR,'**','*.dat'))

    dataBins       = {}
    for infilepath in infilepaths:
        with open(infilepath,'r') as f:
            for line in f:
                if not line.startswith('## ') or not line.strip():
                    continue
                m = re.search('lvMessageFreq_([^_/]+)',infilepath)
                if m:
                    freq      = m.group(1)
                # numPacketsBurst
                m = re.search('numPacketsBurst_([^_]+)',infilepath)
                if m:
                    numPacketsBurst  = int(m.group(1))

            if (freq,numPacketsBurst) not in dataBins:
                dataBins[(freq,numPacketsBurst)] = []
            dataBins[(freq,numPacketsBurst)] += [infilepath]

    # print "OUTPUT: %s" % output
    print("THE BINS ARE {}".format(list(dataBins.keys())))
    return dataBins

def gatherPerRunData(infilepaths,elemName):

    valuesPerRun = {}
    for infilepath in infilepaths:

        # print
        print('Parsing {0} for {1}...'.format(infilepath,elemName), end=' ')

        # find col_elemName, col_runNum, cpuID
        col_elemName    = None
        col_runNum      = None
        cpuID           = None
        with open(infilepath,'r') as f:
            for line in f:
                if line.startswith('# '):
                    # col_elemName, col_runNum
                    elems        = re.sub(' +',' ',line[2:]).split()
                    numcols      = len(elems)
                    col_elemName = elems.index(elemName)
                    col_runNum   = elems.index('runNum')
                    break

                if line.startswith('## '):
                    # cpuID
                    m = re.search('cpuID\s+=\s+([0-9]+)',line)
                    if m:
                        cpuID = int(m.group(1))
        assert col_elemName!=None
        assert col_runNum!=None
        assert cpuID!=None

        # parse data
        with open(infilepath,'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                m       = re.search('\s+'.join(['([\.0-9-]+)']*numcols),line.strip())
                runNum  = int(m.group(col_runNum+1))
                try:
                    elem         = float(m.group(col_elemName+1))
                except:
                    try:
                        elem     =   int(m.group(col_elemName+1))
                    except:
                        elem     =       m.group(col_elemName+1)

                if (cpuID,runNum) not in valuesPerRun:
                    valuesPerRun[cpuID,runNum] = []
                valuesPerRun[cpuID,runNum] += [elem]

        # print
        print('done.')

    return valuesPerRun

def gatherPerCycleData(infilepaths,elemName):

    valuesPerCycle = {}
    for infilepath in infilepaths:

        # print
        print('Parsing {0} for {1}...'.format(infilepath,elemName), end=' ')

        # find colnumelem, colnumcycle
        with open(infilepath,'r') as f:
            for line in f:
                if line.startswith('# '):
                    elems        = re.sub(' +',' ',line[2:]).split()
                    numcols      = len(elems)
                    colnumelem   = elems.index(elemName)
                    colnumcycle  = elems.index('cycle')
                    break

        assert colnumelem
        assert colnumcycle

        # parse data

        with open(infilepath,'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                reStr = '\s+'.join(['([\.0-9-]+)']*numcols)
                # print(f'reStr = {reStr}')
                # print(f'line = {line}')
                m       = re.search(reStr, line.strip())
                if not m:
                     print(f'line={line} m= {m}, re= {re}')
                cycle   = int(m.group(colnumcycle+1))
                # print(f'cycle= {cycle}')
                
                try:
                    elem         = float(m.group(colnumelem+1))
                except:
                    try:
                        elem     =   int(m.group(colnumelem+1))
                    except:
                        elem     =       m.group(colnumelem+1)

                if cycle not in valuesPerCycle:
                    valuesPerCycle[cycle] = []
                valuesPerCycle[cycle] += [elem]

        # print
        print('done.')

    return valuesPerCycle

def calcMeanConfInt(vals):
    assert type(vals)==list
    for val in vals:
        assert type(val) in [int,float,numpy.float64]

    a         = 1.0*numpy.array(vals)
    se        = scipy.stats.sem(a)
    m         = numpy.mean(a)
    confint   = se * scipy.stats.t._ppf((1+CONFINT)/2., len(a)-1)

    return (m,confint)

def getSlotDuration(dataBins):
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        for filepath in filepaths:
            with open(filepath,'r') as f:
                for line in f:
                    if line.startswith('## '):
                        m = re.search('slotDuration\s+=\s+([\.0-9]+)',line)
                        if m:
                            return float(m.group(1))

def getNumPacketsBurst(plotData):
    return set([numPacketsBurst for (freq,numPacketsBurst) in list(plotData.keys()) ])
    
def getFreqs(plotData):
    return set([freq for (freq,numPacketsBurst) in list(plotData.keys()) ])


#============================ plotters ========================================

def plot_vs_time(plotData,ymin=None,ymax=None,ylabel=None,filename=None,doPlot=True,withError=True):

    prettyp   = False

    #===== format data

    # calculate mean and confidence interval
    for ((freq), perCycleData) in list(plotData.items()):
        for cycle in list(perCycleData.keys()):
            (m,confint) = calcMeanConfInt(perCycleData[cycle])
            perCycleData[cycle] = {
                'mean':      m,
                'confint':   confint,
            }

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: {'mean': 12, 'confint':12},
    #         1: {'mean': 12, 'confint':12},
    #     }
    # }

    # arrange to be plotted
    for ((freq), perCycleData) in list(plotData.items()):
        x     = sorted(perCycleData.keys())
        y     = [perCycleData[i]['mean']    for i in x]
        yerr  = [perCycleData[i]['confint'] for i in x] if withError else [ 0 for i in x]
        assert len(x)==len(y)==len(yerr)

        plotData[(freq)] = {
            'x':        x,
            'y':        y,
            'yerr':     yerr,
        }

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         'x':      [ 0, 1, 2, 3, 4, 5, 6],
    #         'y':      [12,12,12,12,12,12,12],
    #         'yerr':   [12,12,12,12,12,12,12],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('arrange to be plotted'))
            f.write(pp.pformat(plotData))

    if not doPlot:
        return plotData

    #===== plot

    freqs           = []
    for (freq) in list(plotData.keys()):
        freqs      += [freq]
    freqs           = sorted(list(set(freqs)))


    # fig = matplotlib.pyplot.figure()
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 6), dpi=400, facecolor='w', edgecolor='k')

    allaxes = []
        # ax = fig.add_axes([0.10, 0.10, 0.85, 0.85])
     #   ax.set_xlim(xmin=0,xmax=600)
#        ax.set_ylim(ymin=ymin,ymax=ymax)
    plots = []
    legends = []
    for f in freqs:
        for ((freq), data) in list(plotData.items()):
            if freq==f:
                t = freq
                plots += [
                    ax.errorbar(
                        x        = data['x'],
                        y        = data['y'],
                        yerr     = data['yerr'] if withError else None,
                        color    = COLORS_TH[t],
                        ls       = LINESTYLE_TH[0],
                        ecolor   = ECOLORS_TH[t],
                    )
                ]
                legends += ( [ freq ] )

    legendPlots = tuple(plots)
    allaxes += [ax]

    # add x label

#        for ax in allaxes[1:]:
#            ax.get_xaxis().set_visible(False)
    allaxes[0].set_xlabel('time (slotframe cycles)')

        # add y label
    allaxes[int(len(allaxes)/2)].set_ylabel(ylabel)

    # add legend
    legendText = tuple(legends)

    ax.legend( legendPlots, legendText, loc="best", prop={'size':10})

    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_{1}.png'.format(PREFIX, filename)))
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_{1}.eps'.format(PREFIX, filename)))
    matplotlib.pyplot.close('all')

def plot_vs_threshold(plotData,ymin,ymax,ylabel,filename,legend_position='best',logy=False):

    prettyp   = False

    #===== format data

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('initial data'))
            f.write(pp.pformat(plotData))

    # collapse all cycles
    for ((freq,numPacketsBurst),perCycleData) in list(plotData.items()):
        temp = []
        for (k,v) in list(perCycleData.items()):
            temp += v

        plotData[(freq,numPacketsBurst)] = temp

    # plotData = {
    #     (otfThreshold,pkPeriod) = [
    #         cycle0_run0,
    #         cycle0_run1,
    #         ...,
    #         cycle1_run0,
    #         cycle1_run1,
    #         ...,
    #     ]
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('collapse all cycles'))
            f.write(pp.pformat(plotData))

    # calculate mean and confidence interval
    for ((freq,numPacketsBurst),perCycleData) in list(plotData.items()):
        (m,confint) = (0,0.0001)
        try:
            (m,confint) = calcMeanConfInt(perCycleData)
        except AssertionError:
            pass
        plotData[(freq,numPacketsBurst)] = {
            'mean':      m,
            'confint':   confint,
        }

    # plotData = {
    #     (otfThreshold,pkPeriod) = {'mean': 12, 'confint':12},
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('calculate mean and confidence interval'))
            f.write(pp.pformat(plotData))

    freqs           = []
    numPacketsBursts       = []
    for (freq,numPacketsBurst) in list(plotData.keys()):
        freqs      += [freq]
        numPacketsBursts  += [numPacketsBurst]
    freqs           = sorted(list(set(freqs)))
    numPacketsBursts       = sorted(list(set(numPacketsBursts)), reverse=True)

#    fig = matplotlib.pyplot.figure()
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 6), dpi=400, facecolor='w', edgecolor='k')
    # fig, ax = matplotlib.pyplot.subplots(figsize=(12, 9), dpi=400, facecolor='w', edgecolor='k')
    # matplotlib.pyplot.ylim(ymin=ymin,ymax=ymax)
    ax.set_xlabel('Parameters: ' + ('freq' if len(numPacketsBursts) == 1 else '(freq, numPacketsBurst))'))
    ax.set_ylabel(ylabel)
    bars = []
    legends = []
    offset = 0
    x = []
    for freq in freqs:
        for numPacketsBurst in numPacketsBursts:

            d = {}
            for ((pkFreq, pkNumPacketsBurst),data) in list(plotData.items()):
                if freq == pkFreq and numPacketsBurst == pkNumPacketsBurst:
                    d[freq,numPacketsBurst] = data

            x     = sorted(d.keys())
            tics  = [i+.25+offset for i in range(len(x))]
            y     = [d[k]['mean'] for k in x]
            yerr  = [d[k]['confint'] for k in x]

            t     = freq

            bars += [ax.bar(tics, y, 0.9 / (len(x) + 4), color= COLORS_TH[t], edgecolor=COLORS_TH[t], ecolor='black', yerr=yerr)]
            legends += [ '{}, thr={}'.format(freq,numPacketsBurst) ] if len(numPacketsBursts) > 0 else [ freq ]
            offset += 1.3 / (len(x) + 6)

    print("bars: {}, legends: {}".format(bars, legends))
    if (len(bars) == 0 and len(legends) == 0) or len(bars) != len(legends):
        return

    ax.set_xticks( [i+.25+offset/2 for i in range(len(x))])
    ax.set_xticklabels([(b) if len(numPacketsBursts) == 1 else (p,b) for (b,p) in x])
    ax.legend( bars, legends, loc=legend_position, prop={'size':10})

    if logy:
        ax.set_yscale('log')

#            matplotlib.pyplot.errorbar(
#                x        = x,
#                y        = y,
#                yerr     = yerr,
#
#                color    = COLORS_TH[threshold],
#                ls       = LINESTYLE_TH[algorithm=='otf'],
#                ecolor   = ECOLORS_TH[threshold],
#                label    = '{}, thr={}'.format(algorithm,threshold)
#            )
#    matplotlib.pyplot.legend(prop={'size':10})
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_{1}.png'.format(PREFIX, filename)))
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_{1}.eps'.format(PREFIX, filename)))

    matplotlib.pyplot.close('all')

#----- txQueueFill

def gather_per_cycle_data(dataBins, parameter, factor=1.0):

    prettyp   = False

    # gather raw data
    plotData  = {}
    for ((freq, nunPacketsBurst),filepaths) in list(dataBins.items()):
        plotData[(freq, nunPacketsBurst)] = gatherPerCycleData(filepaths,parameter)

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw data'))
            f.write(pp.pformat(plotData))

     # Multiply by factor
    for ((freq, nunPacketsBurst),perCycleData) in list(plotData.items()):
        for cycle in list(perCycleData.keys()):
            perCycleData[cycle] = [ factor * val for val in perCycleData[cycle] ]

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('convert slots to seconds'))
            f.write(pp.pformat(plotData))

    return plotData


def plot_txQueueFill_vs_time(dataBins):

    plotData  = gather_per_cycle_data(dataBins, 'txQueueFill')

    for n in getNumPacketsBurst(plotData):
        plot_vs_time(
            plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
            ymin     = 0,
            ymax     = 50,
            ylabel   = 'txQueueFill',
            filename = 'txQueueFill_vs_time_pkt_{}'.format(n),
            withError = False,
        )

def plot_appReachesDagroot_vs_time(dataBins):

    plotData  = gather_per_cycle_data(dataBins, 'appReachesDagroot')

    for n in getNumPacketsBurst(plotData):
        plot_vs_time(
            plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
            ymin     = 0,
            ymax     = 50,
            ylabel   = 'appReachesDagroot',
            filename = 'appReachesDagroot_vs_time_pkt_{}'.format(n),
            withError = False,
        )

def plot_load_vs_threshold(dataBins):
    for label in ['LoadAllG', 'LoadAllJain', 'LoadCongG', 'LoadCongJain']:
        plotData  = gather_ave_data(dataBins, label)

        #ymax = { 1: 2.5, 5: 15, 25: 40 }


        plot_vs_threshold(
            plotData = plotData,
            ymin=0,
            ymax=130,
            ylabel=label,
            filename='{}_vs_threshold_buf_100'.format(label),
            legend_position='lower left'
        )


def plot_load_vs_time(dataBins):
#    for label in ['LoadAllAvgWithZero', 'LoadAllG', 'LoadAllJain', 'LoadAllMax', 'LoadAllMin',
#                  'LoadCong5Avg', 'LoadCong5AvgWithZero', 'LoadCong5G', 'LoadCong5Jain', 'LoadCong5Max', 'LoadCong5Min',
#                  'LoadCongAvg', 'LoadCongAvgWithZero', 'LoadCongG', 'LoadCongJain', 'LoadCongMax', 'LoadCongMin']:
    for label in ['LoadAllG', 'LoadAllJain', 'LoadCongG', 'LoadCongJain']:
        print("Loading label {}".format(label))
        plotData = gather_per_cycle_data(dataBins, label)

        for b in getBufferSizes(plotData):
            for p in getParentSizes(plotData):
                for n in getNumPacketsBurst(plotData):
                    for pe in getPkPeriods(plotData):
                        plot_vs_time(
                            plotData=dict(
                                ((th, per, alg), data) for (th, per, alg, par, buf, pkt), data in list(plotData.items()) if
                                buf == b and par == p and pkt == n and per == pe),
                            ymin=0,
                            ymax=1000,
                            ylabel=label,
                            filename='{}_vs_time_buf_{}_par_{}_pkt_{}'.format(label,b,p,n) + ('_per_{}'.format(pe) if len(getPkPeriods(plotData)) > 1 else ''),
                            withError=False,
                        )


def plot_numRxCells_vs_time(dataBins):

    plotData  = gather_per_cycle_data(dataBins, 'numRxCells')

    for n in getNumPacketsBurst(plotData):
        plot_vs_time(
            plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
            ymin     = 0,
            ymax     = 1000,
            ylabel   = 'numRxCells',
            filename = 'numRxCells_vs_time_pkt_{}'.format(n),
            withError = False,
        )

def plot_chargeConsumed_vs_time(dataBins):

    plotData  = gather_per_cycle_data(dataBins, 'chargeConsumed', 1e-5)

    for n in getNumPacketsBurst(plotData):
        plot_vs_time(
            plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
            ymin     = 0,
            ymax     = 7,
            ylabel   = 'chargeConsumed x1e5',
            filename = 'chargeConsumed_vs_time_pkt_{}'.format(n),
            withError = False,
        )

#===== latency

def gather_latency_data(dataBins):

    prettyp   = False

    # gather raw data
    plotData  = {}
    for ((freq, nunPacketsBurst),filepaths) in list(dataBins.items()):
        plotData[(freq, nunPacketsBurst)] = gatherPerCycleData(filepaths,'aveLatency')

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw data'))
            f.write(pp.pformat(plotData))

    # convert slots to seconds
    slotDuration = getSlotDuration(dataBins)
    for ((freq, nunPacketsBurst),perCycleData) in list(plotData.items()):
        for cycle in list(perCycleData.keys()):
            perCycleData[cycle] = [d*slotDuration for d in perCycleData[cycle]]

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('convert slots to seconds'))
            f.write(pp.pformat(plotData))

    # filter out 0 values
    for ((freq, nunPacketsBurst),perCycleData) in list(plotData.items()):
        for cycle in list(perCycleData.keys()):
            i=0
            while i<len(perCycleData[cycle]):
                if perCycleData[cycle][i]==0:
                    del perCycleData[cycle][i]
                else:
                    i += 1

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         cycle0: [run0,run1, ...],
    #         cycle1: [run0,run1, ...],
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('filter out 0 values'))
            f.write(pp.pformat(plotData))

    return plotData

def plot_latency_vs_time(dataBins):

    plotData  = gather_latency_data(dataBins)

    for n in getNumPacketsBurst(plotData):
        plot_vs_time(
            plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
            ymin     = 0,
            ymax     = 18,
            ylabel   = 'end-to-end latency (s)',
            filename = 'latency_vs_time_pkt_{}'.format(n),
            withError = False,
        )

def plot_latency_vs_threshold(dataBins):
    print("plotata1 {}".format(list(dataBins.keys())))
    plotData  = gather_ave_data(dataBins, 'aveLatency', 'appReachesDagroot')

# ymax = { 1: 2.5, 5: 15, 25: 40 }


    print("plotata {}".format(list(plotData.keys())))
    plot_vs_threshold(
        plotData = plotData,
        ymin=0,
        ymax=130,
        ylabel='average end-to-end latency (s)',
        filename='latency_vs_threshold_buf_100'
    )

def plot_txQueueFill_vs_threshold(dataBins):
    plotData = gather_ave_data(dataBins, 'txQueueFill')

    plot_vs_threshold(
        plotData = plotData,
        ymin=0,
        ymax=40,
        ylabel='average queue size (packets)',
        filename='txQueueFill_vs_threshold_buf_100'
    )

def plot_max_txQueueFill_vs_threshold(dataBins):
    plotData = gather_max_data(dataBins, 'txQueueFill')

    plot_vs_threshold(
        plotData = plotData,
        ymin=0,
        ymax=40,
        ylabel='max avg queue size (packets)',
        filename='max_txQueueFill_vs_threshold_buf_100'
    )

def plot_ave_q_delay_vs_threshold(dataBins):

    plotData  = gather_ave_data(dataBins, 'aveQueueDelay', ['appReachesDagroot', 'appRelayed'])

    plot_vs_threshold(
        plotData = plotData,
        ymin       = 0,
        ymax       = 100,
        ylabel     = 'average queue delay (s)',
        filename   = 'queue_delay_vs_threshold_buf_100'
    )

def gather_max_data(dataBins, label):
    plotData  = {}
    unit_factor = getSlotDuration(dataBins) if label in ['aveLatency', 'aveQueueDelay'] else 1e-5 if label == 'chargeConsumed' else 0.02 if label == 'txQueueFill' else 1
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        perCycle = gatherPerCycleData(filepaths, label)

        max_values = [ 0 for i in perCycle[0]]
        # print "file: {}, percyle: {}, {}".format(filepaths,perCycle,(freq,numPacketsBurst))
        for k,v in list(perCycle.items()):
            for run,value in enumerate(v):
                lat = unit_factor * value
                if lat > max_values[run]:
                    max_values[run] = lat
            # print k,len(v)
        # print "max_{}: {}".format(label,max_values)

        plotData[(freq,numPacketsBurst)] = {0: max_values}

    return plotData

def gather_ave_data(dataBins, label, count_label=None):
    plotData  = {}
    unit_factor = getSlotDuration(dataBins) if label in ['aveLatency', 'aveQueueDelay'] else 0.02 if label == 'txQueueFill' else 1
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        perCycle = gatherPerCycleData(filepaths, label)

        perCycle_count = {}
        if count_label:
            if type(count_label)==list:
                perCycle_count = [gatherPerCycleData(filepaths, cl) for cl in count_label]
            else:
                perCycle_count = [gatherPerCycleData(filepaths, count_label)]


#        print "perCyple: {}\n\n, count: {}\n\n".format(perCycle, perCycle_count)

        sum_values = [ 0 for i in perCycle[0]]
        count_values = [ 0 for i in perCycle[0]]

        for k,v in list(perCycle.items()):
            for run,value in enumerate(v):
                lat = unit_factor * value
                if count_label:
                    sum_values[run] += sum([ pcc[k][run] * lat for pcc in perCycle_count ])
                    count_values[run] += sum([ pcc[k][run] for pcc in perCycle_count ])
                else:
                    sum_values[run] += lat
                    count_values[run] += 1


#        values += [ perCycle_count[k] * unit_factor * v_i /sum_perCycle_count for v_i in v]

        plotData[(freq,numPacketsBurst)] = {0: [ v / count_values[run] if count_values[run]>0 else 0 for run,v in enumerate(sum_values) ]  }

    return plotData

def gather_sum_data(dataBins, label):
    plotData  = {}
    unit_factor = getSlotDuration(dataBins) if label in ['aveLatency', 'aveQueueDelay']  else 1
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        perCycle = gatherPerCycleData(filepaths, label)

        sum_values = [ 0 for i in perCycle[0]]

        for k,v in list(perCycle.items()):
            for run,value in enumerate(v):
                lat = unit_factor * value
                sum_values[run] += lat

        plotData[(freq,numPacketsBurst)] = {0: [ v for run,v in enumerate(sum_values) ]  }

    return plotData


def plot_max_latency_vs_threshold(dataBins):

    plotData  = gather_max_data(dataBins, 'aveLatency')

    plot_vs_threshold(
        plotData = plotData,
        ymin       = 0,
        ymax       = 100,
        ylabel     = 'max end-to-end latency (s)',
        filename   = 'max_latency_vs_threshold_buf_100'
    )


def plot_max_queue_delay_vs_threshold(dataBins):

    plotData  = gather_max_data(dataBins, 'aveQueueDelay')

    plot_vs_threshold(
        plotData= plotData,
        ymin       = 0,
        ymax       = 100,
        ylabel     = 'max queue delay (s)',
        filename   = 'max_queue_delay_vs_threshold_buf_100'
    )

def plot_chargeConsumed_vs_threshold(dataBins):

    charge  = gather_max_data(dataBins, 'chargeConsumed')

    plot_vs_threshold(
        plotData= charge,
        ymin       = 0,
        ymax       = 20,
        ylabel     = 'charge consumed x1e5',
        filename   = 'chargeConsumed_vs_threshold_buf_100',
        # legend_position='lower right'
    )

    work = gather_sum_data(dataBins, 'appReachesDagroot')

    charge_per_packet = {}

    for (freq, pkt), data in list(work.items()):
        charge_per_packet[(freq, pkt)] = { 0: [ c / w if w > 0 else None for w, c in zip(data[0], charge[(freq, pkt)][0]) ]}

    print("Charge: ", charge)
    print("Work: ", work)
    print("charge_per_packet: ", charge_per_packet)

    plot_vs_threshold(
        plotData= charge_per_packet,
        ymin       = 0,
        ymax       = 0.08,
        ylabel     = 'charge consumed/packet received x1e5',
        filename   = 'chargeConsumedPerRecv_vs_threshold_buf_100',
        logy = True
    )

def gather_time_all_reached(dataBins):
    plotData  = {}
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        perCycle = gatherPerCycleData(filepaths,'appReachesDagroot')

        lastnonzero = [ 1000 for i in perCycle[0]]
        # print "file: {}, percyle: {}, {}".format(filepaths,perCycle,(freq,numPacketsBurst))
        for k,v in list(perCycle.items()):
            for run,value in enumerate(v):
                if value != 0:
                    lastnonzero[run] = k
            # print k,len(v)
#        print "lastnonzero: {}".format(lastnonzero)

        plotData[(freq,numPacketsBurst)] = {0: lastnonzero}

    return plotData


def plot_time_all_reached_vs_threshold(dataBins):

    plotData  = gather_time_all_reached(dataBins)

    plot_vs_threshold(
        plotData=plotData,
        ymin       = 60,
        ymax       = 100,
        ylabel     = 'time for last packet to reach root',
        filename   = 'time_all_root_vs_threshold_buf_100',
        legend_position='lower right'
    )



#===== numCells

def gather_numCells_data(dataBins):

    prettyp   = False

    # gather raw data
    plotData  = {}
    for ((otfThreshold,pkPeriod,algorithm),filepaths) in list(dataBins.items()):
        plotData[(otfThreshold,pkPeriod)] = gatherPerCycleData(filepaths,'numTxCells')

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw data'))
            f.write(pp.pformat(plotData))

    return plotData

def plot_numCells_vs_time(dataBins):

    plotData  = gather_numCells_data(dataBins)

    plot_vs_time(
        plotData = plotData,
        ymin     = 0,
        ymax     = 200,
        ylabel   = 'number of scheduled cells',
        filename = 'numCells_vs_time',
        withError=False
    )

def plot_numCells_vs_threshold(dataBins):

    plotData  = gather_numCells_data(dataBins)

    plot_vs_threshold(
        plotData   = plotData,
        ymin       = 0,
        ymax       = 600,
        ylabel     = 'number of scheduled cells',
        filename   = 'numCells_vs_threshold',
    )

def plot_numCells_otfActivity_vs_time(dataBins):

    plotData  = gather_numCells_data(dataBins)

    plotDataNumCells = plot_vs_time(
        plotData   = plotData,
        doPlot     = False,
    )

    (otfAddData,otfRemoveData) = plot_otfActivity_vs_time(
        dataBins   = dataBins,
        doPlot     = False,
    )

    #===== plot

    allaxes = []
    pkPeriods           = []
    otfThresholds       = []
    for (otfThreshold,pkPeriod) in list(plotDataNumCells.keys()):
        pkPeriods      += [pkPeriod]
        otfThresholds  += [otfThreshold]
    pkPeriods           = sorted(list(set(pkPeriods)))
    otfThresholds       = sorted(list(set(otfThresholds)), reverse=True)

    fig = matplotlib.pyplot.figure(figsize=(8, 6), dpi=400, facecolor='w', edgecolor='k')

    #=== otfActivity

    def plotForEachPkPeriodOtfActivity(ax,plotData,pkPeriod_p):
        plots = []
        for th in otfThresholds:
            for ((otfThreshold,pkPeriod),data) in list(plotData.items()):
                if otfThreshold==th and pkPeriod==pkPeriod_p:
                    plots += [
                        ax.errorbar(
                            x        = data['x'],
                            y        = data['y'],
                            yerr     = data['yerr'],
                            color    = COLORS_TH[th],
                            ls       = LINESTYLE_TH[th],
                            ecolor   = ECOLORS_TH[th],
                        )
                    ]
        return tuple(plots)

    def maxY(plotData):
        returnVal = []
        for ((otfThreshold,pkPeriod),data) in list(plotData.items()):
            returnVal += data['y']
        return max(returnVal)

    # plot axis
    ax = fig.add_axes([0.12, 0.54, 0.85, 0.40])
    # ax.set_xlim(xmin= 0,xmax=600)
    ax.set_ylim(ymin=-4,ymax=8)
    ax.annotate(
        'max. value {0:.0f}'.format(maxY(otfAddData)),
        xy=(10, 7.9),
        xycoords='data',
        xytext=(22, 4),
        textcoords='data',
        arrowprops=dict(arrowstyle="->",facecolor='black'),
        horizontalalignment='right',
        verticalalignment='top',
    )
    ax.annotate(
        'add cells',
        xytext=(50,0.2),
        xy    =(50,3.8),
        xycoords='data',
        textcoords='data',
        arrowprops=dict(arrowstyle="->",facecolor='black'),
        horizontalalignment='center',
        verticalalignment='bottom',
    )
    ax.annotate(
        'remove cells',
        xytext=(50,-0.2),
        xy    =(50,-3.8),
        xycoords='data',
        textcoords='data',
        arrowprops=dict(arrowstyle="->",facecolor='black'),
        horizontalalignment='center',
        verticalalignment='top',
    )
    plotForEachPkPeriodOtfActivity(ax,otfAddData,pkPeriod)
    plotForEachPkPeriodOtfActivity(ax,otfRemoveData,pkPeriod)
    allaxes += [ax]

    # add x/y labels
    ax.set_xticks([])
    ax.set_ylabel('num. add/remove OTF\noperations per cycle')

    #=== numCells

    # plot axis
    ax = fig.add_axes([0.12, 0.14, 0.85, 0.40])
    # ax.set_xlim(xmin=0,xmax=600)
    ax.set_ylim(ymin=0,ymax=199)
    plots = []
    for th in otfThresholds:
        for ((otfThreshold,pkPeriod),data) in list(plotDataNumCells.items()):
            if otfThreshold==th:
                plots += [
                    ax.errorbar(
                        x        = data['x'],
                        y        = data['y'],
                        yerr     = data['yerr'],
                        color    = COLORS_TH[th],
                        ls       = LINESTYLE_TH[th],
                        ecolor   = ECOLORS_TH[th],
                    )
                ]
    legendPlots = tuple(plots)

    # add x/y labels
    ax.set_xlabel('time (slotframe cycles)')
    ax.set_ylabel('number of\nscheduled cells')
    ax.annotate(
        'first burst\n(5 packets per node)',
        xy=(20, 120),
        xycoords='data',
        xytext=(20, 35),
        textcoords='data',
        arrowprops=dict(arrowstyle="->",facecolor='black'),
        horizontalalignment='center',
        verticalalignment='center',
    )
    ax.annotate(
        'second burst\n(5 packets per node)',
        xy=(60, 120),
        xycoords='data',
        xytext=(60, 35),
        textcoords='data',
        arrowprops=dict(arrowstyle="->",facecolor='black'),
        horizontalalignment='center',
        verticalalignment='center',
    )

    #=== legend

    legendText = tuple(['OTF threshold {0} cells'.format(t) for t in otfThresholds])
    fig.legend(
        legendPlots,
        legendText,
        'upper right',
        prop={'size':11},
    )

    allaxes += [ax]

    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_numCells_otfActivity_vs_time.png'.format(PREFIX)))
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_numCells_otfActivity_vs_time.eps'.format(PREFIX)))
    matplotlib.pyplot.close('all')

#===== otfActivity

def plot_otfActivity_vs_time(dataBins,doPlot=True):

    prettyp   = False

    # gather raw add/remove data
    otfAddData     = {}
    otfRemoveData  = {}
    for ((otfThreshold,pkPeriod),filepaths) in list(dataBins.items()):
        otfAddData[   (otfThreshold,pkPeriod)] = gatherPerCycleData(filepaths,'otfAdd')
        otfRemoveData[(otfThreshold,pkPeriod)] = gatherPerCycleData(filepaths,'otfRemove')

    # otfAddData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }
    # otfRemoveData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw add/remove data'))
            f.write(pp.pformat(otfAddData))
            f.write(pp.pformat(otfRemoveData))

    #===== format data

    # calculate mean and confidence interval
    for ((otfThreshold,pkPeriod),perCycleData) in list(otfAddData.items()):
        for cycle in list(perCycleData.keys()):
            (m,confint) = calcMeanConfInt(perCycleData[cycle])
            perCycleData[cycle] = {
                'mean':      m,
                'confint':   confint,
            }
    for ((otfThreshold,pkPeriod),perCycleData) in list(otfRemoveData.items()):
        for cycle in list(perCycleData.keys()):
            (m,confint) = calcMeanConfInt(perCycleData[cycle])
            perCycleData[cycle] = {
                'mean':      -m,
                'confint':   confint,
            }

    # otfAddData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: {'mean': 12, 'confint':12},
    #         1: {'mean': 12, 'confint':12},
    #     }
    # }
    # otfRemoveData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: {'mean': 12, 'confint':12},
    #         1: {'mean': 12, 'confint':12},
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('calculate mean and confidence interval'))
            f.write(pp.pformat(otfAddData))
            f.write(pp.pformat(otfRemoveData))

    # arrange to be plotted
    for ((otfThreshold,pkPeriod),perCycleData) in list(otfAddData.items()):
        x     = sorted(perCycleData.keys())
        y     = [perCycleData[i]['mean']    for i in x]
        yerr  = [perCycleData[i]['confint'] for i in x]
        assert len(x)==len(y)==len(yerr)

        otfAddData[(otfThreshold,pkPeriod)] = {
            'x':        x,
            'y':        y,
            'yerr':     yerr,
        }
    for ((otfThreshold,pkPeriod),perCycleData) in list(otfRemoveData.items()):
        x     = sorted(perCycleData.keys())
        y     = [perCycleData[i]['mean']    for i in x]
        yerr  = [perCycleData[i]['confint'] for i in x]
        assert len(x)==len(y)==len(yerr)

        otfRemoveData[(otfThreshold,pkPeriod)] = {
            'x':        x,
            'y':        y,
            'yerr':     yerr,
        }

    # otfAddData = {
    #     (otfThreshold,pkPeriod) = {
    #         'x':      [ 0, 1, 2, 3, 4, 5, 6],
    #         'y':      [12,12,12,12,12,12,12],
    #         'yerr':   [12,12,12,12,12,12,12],
    #     }
    # }
    # otfRemoveData = {
    #     (otfThreshold,pkPeriod) = {
    #         'x':      [ 0, 1, 2, 3, 4, 5, 6],
    #         'y':      [12,12,12,12,12,12,12],
    #         'yerr':   [12,12,12,12,12,12,12],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('arrange to be plotted'))
            f.write(pp.pformat(otfAddData))
            f.write(pp.pformat(otfRemoveData))

    if not doPlot:
        return (otfAddData,otfRemoveData)

    pkPeriods           = []
    otfThresholds       = []
    for (otfThreshold,pkPeriod) in list(otfAddData.keys()):
        pkPeriods      += [pkPeriod]
        otfThresholds  += [otfThreshold]
    pkPeriods           = sorted(list(set(pkPeriods)))
    otfThresholds       = sorted(list(set(otfThresholds)), reverse=True)

    #===== plot

    fig = matplotlib.pyplot.figure(figsize=(8, 6), dpi=400, facecolor='w', edgecolor='k')

    def plotForEachPkPeriod(ax,plotData,pkPeriod_p):
        #ax.set_xlim(xmin=poi,xmax=poi)
        #ax.set_ylim(ymin=0,ymax=50)
        if pkPeriod_p!='NA':
            ax.text(1,70,'packet period {0}s'.format(pkPeriod_p))
        plots = []
        for th in otfThresholds:
            for ((otfThreshold,pkPeriod),data) in list(plotData.items()):
                if otfThreshold==th and pkPeriod==pkPeriod_p:
                    plots += [
                        ax.errorbar(
                            x        = data['x'],
                            y        = data['y'],
                            yerr     = data['yerr'],
                            color    = COLORS_TH[th],
                            ls       = LINESTYLE_TH[th],
                            ecolor   = ECOLORS_TH[th],
                        )
                    ]
        return tuple(plots)

    # plot axis
    allaxes = []
    subplotHeight = 0.85/len(pkPeriods)
    for (plotIdx,pkPeriod) in enumerate(pkPeriods):
        ax = fig.add_axes([0.12, 0.10+plotIdx*subplotHeight, 0.85, subplotHeight])
        legendPlots = plotForEachPkPeriod(ax,otfAddData,pkPeriod)
        legendPlots = plotForEachPkPeriod(ax,otfRemoveData,pkPeriod)
        allaxes += [ax]

    # add x label
    for ax in allaxes[1:]:
        ax.get_xaxis().set_visible(False)
    allaxes[0].set_xlabel('time (slotframe cycles)')

    # add y label
    allaxes[int(len(allaxes)/2)].set_ylabel('number of add/remove OTF\noperations per cycle')

    # add legend
    legendText = tuple(['OTF threshold {0} cells'.format(t) for t in otfThresholds])
    fig.legend(
        legendPlots,
        legendText,
        'upper right',
        prop={'size':8},
    )

    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_otfActivity_vs_time.png'.format(PREFIX)))
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_otfActivity_vs_time.eps'.format(PREFIX)))
    matplotlib.pyplot.close('all')

def gather_sumOtfActivity_data(dataBins):

    prettyp   = False

    # gather raw add/remove data
    otfAddData     = {}
    otfRemoveData  = {}
    for ((otfThreshold,pkPeriod),filepaths) in list(dataBins.items()):
        otfAddData[   (otfThreshold,pkPeriod)] = gatherPerCycleData(filepaths,'otfAdd')
        otfRemoveData[(otfThreshold,pkPeriod)] = gatherPerCycleData(filepaths,'otfRemove')

    # otfAddData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }
    # otfRemoveData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }

    assert sorted(otfAddData.keys())==sorted(otfRemoveData.keys())
    for otfpk in list(otfAddData.keys()):
        assert sorted(otfAddData[otfpk].keys())==sorted(otfRemoveData[otfpk].keys())

    # sum up number of add/remove operations

    plotData = {}
    for otfpk in list(otfAddData.keys()):
        plotData[otfpk] = {}
        for cycle in list(otfAddData[otfpk].keys()):
            plotData[otfpk][cycle] = [sum(x) for x in zip(otfAddData[otfpk][cycle],otfRemoveData[otfpk][cycle])]

    # plotData = {
    #     (otfThreshold,pkPeriod) = {
    #         0: [12,12,12,12,12,12,12,12,12],
    #         1: [12,12,12,12,12,0,0,0,0],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw data'))
            f.write(pp.pformat(plotData))

    return plotData

def plot_otfActivity_vs_threshold(dataBins):

    plotData  = gather_sumOtfActivity_data(dataBins)

    plot_vs_threshold(
        plotData   = plotData,
        ymin       = 0,
        ymax       = 25,
        ylabel     = 'number of add/remove OTF operations per cycle',
        filename   = 'otfActivity_vs_threshold',
    )


#===== reliability

def plot_reliability_vs_time(dataBins):

    prettyp = True

    #===== gather data

    for val_str in 'appGenerated', 'appReachesDagroot', 'txQueueFill':

        # gather raw add/remove data
        plotData    = {}
        for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
            plotData[(freq,numPacketsBurst)] = {
                i: list(k) for i,k in enumerate(
                    zip(*list(gatherPerRunData(filepaths, val_str).values()))
                )
            }

        for n in getNumPacketsBurst(plotData):
            plot_vs_time(
                plotData = dict(((freq),data) for (freq,pkt),data in list(plotData.items()) if pkt == n),
                ymin     = 0,
                ymax     = 50,
                ylabel   = val_str,
                filename = val_str + '_vs_time_pkt_{}'.format(n),
                withError = False,
            )

        plotDataCum = {}
        for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
            plotDataCum[(freq,numPacketsBurst)] = {
                i: list(k) for i,k in enumerate(
                   zip(*list(map(numpy.cumsum,
                            list(gatherPerRunData(filepaths, val_str).values()))))
                )
            }

        for n in getNumPacketsBurst(plotData):
            plot_vs_time(
                plotData = dict(((freq),data) for (freq,pkt),data in list(plotDataCum.items()) if pkt == n),
                ymin     = 0,
                ymax     = 10000,
                ylabel   = val_str,
                filename = val_str + '_cum_vs_time_pkt_{}'.format(n),
                withError = False,
            )

def plot_reliability_vs_threshold(dataBins):

    prettyp = True

    #===== gather data

    # gather raw add/remove data
    appGeneratedData    = {}
    appReachedData      = {}
    txQueueFillData     = {}
    for ((freq,numPacketsBurst),filepaths) in list(dataBins.items()):
        appGeneratedData[(freq,numPacketsBurst)]=gatherPerRunData(filepaths,'appGenerated')
        appReachedData[  (freq,numPacketsBurst)]=gatherPerRunData(filepaths,'appReachesDagroot')
        txQueueFillData[ (freq,numPacketsBurst)]=gatherPerRunData(filepaths,'txQueueFill')

    # appGeneratedData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): [12,12,12,12,12,12,12,12,12],
    #         (cpuID,runNum): [12,12,12,12,12,0,0,0,0],
    #     }
    # }
    # appReachedData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): [12,12,12,12,12,12,12,12,12],
    #         (cpuID,runNum): [12,12,12,12,12,0,0,0,0],
    #     }
    # }
    # txQueueFillData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): [12,12,12,12,12,12,12,12,12],
    #         (cpuID,runNum): [12,12,12,12,12,0,0,0,0],
    #     }
    # }

    if prettyp:
        with open('templog.txt','w') as f:
            f.write('\n============ {0}\n'.format('gather raw add/remove data'))
            f.write('appGeneratedData={0}'.format(pp.pformat(appGeneratedData)))
            f.write('appReachedData={0}'.format(pp.pformat(appReachedData)))
            f.write('txQueueFillData={0}'.format(pp.pformat(txQueueFillData)))

    #===== format data

    # sum up appGeneratedData
    for ((freq,numPacketsBurst),perRunData) in list(appGeneratedData.items()):
        for cpuID_runNum in list(perRunData.keys()):
            perRunData[cpuID_runNum] = sum(perRunData[cpuID_runNum])
    # sum up appReachedData
    for ((freq,numPacketsBurst),perRunData) in list(appReachedData.items()):
        for cpuID_runNum in list(perRunData.keys()):
            perRunData[cpuID_runNum] = sum(perRunData[cpuID_runNum])
    # get last of txQueueFillData
    for ((freq,numPacketsBurst),perRunData) in list(txQueueFillData.items()):
        for cpuID_runNum in list(perRunData.keys()):
            perRunData[cpuID_runNum] = perRunData[cpuID_runNum][-1]

    # appGeneratedData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): sum_over_all_cycles,
    #         (cpuID,runNum): sum_over_all_cycles,
    #     }
    # }
    # appReachedData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): sum_over_all_cycles,
    #         (cpuID,runNum): sum_over_all_cycles,
    #     }
    # }
    # txQueueFillData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): value_last_cycles,
    #         (cpuID,runNum): value_last_cycles,
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('format data'))
            f.write('\nappGeneratedData={0}'.format(pp.pformat(appGeneratedData)))
            f.write('\nappReachedData={0}'.format(pp.pformat(appReachedData)))
            f.write('\ntxQueueFillData={0}'.format(pp.pformat(txQueueFillData)))

    #===== calculate the end-to-end reliability for each runNum

    reliabilityData = {}
    for otfThreshold_pkPeriod in list(appReachedData.keys()):
        reliabilityData[otfThreshold_pkPeriod] = {}
        for cpuID_runNum in appReachedData[otfThreshold_pkPeriod]:
            g = float(appGeneratedData[otfThreshold_pkPeriod][cpuID_runNum])
            r = float(appReachedData[otfThreshold_pkPeriod][cpuID_runNum])
            # q = float(txQueueFillData[otfThreshold_pkPeriod][cpuID_runNum])
            # assert g>0
            if g > 0:
                reliability = r / g
            else:
                reliability = 0
                
            # reliability = (r+q)/g
    #         reliability = r / g
            assert reliability>=0
            assert reliability<=1
            reliabilityData[otfThreshold_pkPeriod][cpuID_runNum] = reliability

    # reliabilityData = {
    #     (otfThreshold,pkPeriod) = {
    #         (cpuID,runNum): 0.9558,
    #         (cpuID,runNum): 1.0000,
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('calculate the end-to-end reliability for each cycle'))
            f.write('reliabilityData={0}'.format(pp.pformat(reliabilityData)))

    # calculate the end-to-end reliability per (otfThreshold,pkPeriod)
    for otfThreshold_pkPeriod in list(reliabilityData.keys()):
        vals = list(reliabilityData[otfThreshold_pkPeriod].values())
        (m,confint) = calcMeanConfInt(vals)
        reliabilityData[otfThreshold_pkPeriod] = {
            'mean':      m,
            'confint':   confint,
        }

    # reliabilityData = {
    #     (otfThreshold,pkPeriod) = {
    #         'mean': 12,
    #         'confint':12,
    #     }
    # }

    if prettyp:
        with open('templog.txt','a') as f:
            f.write('\n============ {0}\n'.format('calculate the end-to-end reliability per (otfThreshold,pkPeriod)'))
            f.write('reliabilityData={0}'.format(pp.pformat(reliabilityData)))

    pkPeriods           = []
    otfThresholds       = []
    algorithms          = []
    parent_sizes        = []
    buffer_sizes        = []
    for (freq,numPacketsBurst) in list(reliabilityData.keys()):
        pkPeriods      += [pkPeriod]
        otfThresholds  += [otfThreshold]
        algorithms     += [algorithm]
        parent_sizes   += [parent_size]
        buffer_sizes   += [buffer_size]
    pkPeriods           = sorted(list(set(pkPeriods)))
    otfThresholds       = sorted(list(set(otfThresholds)), reverse=True)
    algorithms          = sorted(list(set(algorithms)))
    parent_sizes        = sorted(list(set(parent_sizes)))
    buffer_sizes        = sorted(list(set(buffer_sizes)))
    numPacketsBursts    = sorted(list(getNumPacketsBurst(reliabilityData)))

     #===== plot

    # ymin = {1: 0.94, 5: 0.80, 25: 0.20}
    #for pkt in numPacketsBursts:
    fig, ax = matplotlib.pyplot.subplots(figsize=(8, 6), dpi=400, facecolor='w', edgecolor='k')
    # matplotlib.pyplot.ylim(ymin=ymin,ymax=ymax)
    matplotlib.pyplot.ylim(ymin=0.40,ymax=1.015)
#    matplotlib.pyplot.xlabel('Parameters, (buffer,parents)')
    ax.set_ylabel('end-to-end reliability')
    ax.set_xlabel('Parameters: (packets per burst, num of parents)' if len(pkPeriods) == 1 else '(num of parents, pkPeriod)')
    bars = []
    legends = []
    offset = 0
    x = []
    for algorithm in algorithms:
        for threshold in otfThresholds:

            if algorithm in ['local_voting','local_voting_z'] and threshold != 10:
                continue

            d = {}
            for ((otfThreshold,pkPeriod,pkAlgorithm,parent_size,buffer_size,numPacketsBurst),data) in list(reliabilityData.items()):
                if otfThreshold == threshold and pkAlgorithm == algorithm and buffer_size == 100:
                    d[numPacketsBurst,parent_size,pkPeriod] = data

            x     = sorted(d.keys())
            tics  = [i+.25+offset for i in range(len(x))]
            y     = [d[k]['mean'] for k in x]
            yerr  = [d[k]['confint'] for k in x]
            t     = "{0}_{1}".format(algorithm,threshold) if algorithm in ['otf', 'eotf'] else algorithm
            bars += [ax.bar(tics, y, 0.9 / (len(x) + 4), color= COLORS_TH[t], edgecolor=COLORS_TH[t], ecolor='black', yerr=yerr)]
            legends += [ '{}, thr={}'.format(algorithm,threshold) if algorithm in ['otf','eotf'] else algorithm ]
            offset += 1.3 / (len(x) + 6)

    ax.set_xticks( [i+.25+offset/2 for i in range(len(x))])
    ax.set_xticklabels([(b,p) if len(pkPeriods) == 1 else (p,pe) for (b,pe,p) in x])
    ax.legend( bars, legends, loc="lower left", prop={'size':10})

##===== plot

#    fig = matplotlib.pyplot.figure()
#    matplotlib.pyplot.ylim(ymin=0.94,ymax=1.015)
#    matplotlib.pyplot.xlabel('OTF threshold (cells)')
#    matplotlib.pyplot.ylabel('end-to-end reliability')
#    for period in pkPeriods:

#       d = {}
#       for ((otfThreshold,pkPeriod),data) in reliabilityData.items():
#           if pkPeriod==period:
#               d[otfThreshold] = data
#       x     = sorted(d.keys())
#       y     = [d[k]['mean'] for k in x]
#       yerr  = [d[k]['confint'] for k in x]
#
#       matplotlib.pyplot.errorbar(
#           x        = x,
#           y        = y,
#           yerr     = yerr,
#           color    = COLORS_PERIOD[period],
#           ls       = LINESTYLE_PERIOD[period],
#           ecolor   = ECOLORS_PERIOD[period],
#           label    = 'packet period {0}s'.format(period)
#       )
#    matplotlib.pyplot.legend(prop={'size':10})
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_reliability_vs_threshold_buf_100.png'.format(PREFIX)))
    matplotlib.pyplot.savefig(os.path.join(DATADIR,'{0}_reliability_vs_threshold_buf_100.eps'.format(PREFIX)))
    matplotlib.pyplot.close('all')

#============================ main ============================================

def main():

    dataBins = binDataFiles()

    plot_time_all_reached_vs_threshold(dataBins)
    plot_max_latency_vs_threshold(dataBins)
    plot_latency_vs_threshold(dataBins)
    plot_latency_vs_time(dataBins) ### Good for 25,1

    plot_numRxCells_vs_time(dataBins)

#    plot_chargeConsumed_vs_threshold(dataBins)
    plot_chargeConsumed_vs_time(dataBins)


    # plot_reliability_vs_threshold(dataBins)
    plot_reliability_vs_time(dataBins)
    plot_txQueueFill_vs_threshold(dataBins)
    plot_max_txQueueFill_vs_threshold(dataBins)

    # plot_load_vs_threshold(dataBins)
    # plot_load_vs_time(dataBins)

if __name__=="__main__":
    main()
