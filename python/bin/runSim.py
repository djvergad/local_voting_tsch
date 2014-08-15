#!/usr/bin/python
'''
\author Thomas Watteyne <watteyne@eecs.berkeley.edu>    
\author Xavier Vilajosana <xvilajosana@eecs.berkeley.edu>
\author Kazushi Muraoka <k-muraoka@eecs.berkeley.edu>
\author Nicola Accettura <nicola.accettura@eecs.berkeley.edu>
'''

#============================ adjust path =====================================

import os
import sys
if __name__=='__main__':
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..'))

#============================ logging =========================================

import logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('BatchSim')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

#============================ imports =========================================

import time
import itertools
import logging.config
import argparse

from SimEngine     import SimEngine,   \
                          SimSettings, \
                          Propagation
from SimGui        import SimGui

#============================ defines =========================================

#============================ body ============================================

def parseCliOptions():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument( '--squareSide',
        dest       = 'squareSide',
        nargs      = '+',
        type       = float,
        default    = 1.000,
        help       = 'Length of the side of the square area the motes are deployed in, in km.',
    )
    
    parser.add_argument( '--numMotes',
        dest       = 'numMotes',
        nargs      = '+',
        type       = int,
        default    = [20, 40],
        help       = 'Number of simulated motes.',
    )
    
    parser.add_argument( '--numChans',
        dest       = 'numChans',
        nargs      = '+',
        type       = int,
        default    = 16,
        help       = 'Number of frequency channels (between 1 and 16).',
    )
    
    parser.add_argument( '--slotDuration',
        dest       = 'slotDuration',
        nargs      = '+',
        type       = float,
        default    = 0.010,
        help       = 'Duration of a TSCH timeslot, in seconds.',
    )
    
    parser.add_argument( '--slotframeLength',
        dest       = 'slotframeLength',
        nargs      = '+',
        type       = int,
        default    = 101,
        help       = 'Number of timeslots in a slotframe.',
    )
    
    parser.add_argument( '--pkPeriod',
        dest       = 'pkPeriod',
        nargs      = '+',
        type       = float,
        default    = 10,
        help       = 'Average period (is s) between two packets generated by a mote.',
    )
    
    parser.add_argument( '--pkPeriodVar',
        dest       = 'pkPeriodVar',
        nargs      = '+',
        type       = float,
        default    = 0.2,
        help       = 'Variability percentage of the traffic, in [0..1[. Use 0 for CBR traffic.',
    )
    
    parser.add_argument( '--otfThreshold',
        dest       = 'otfThreshold',
        nargs      = '+',
        type       = int,
        default    = [0, 10],
        help       = 'OTF threshold, in cells.',
    )
    
    parser.add_argument( '--numCyclesPerRun',
        dest       = 'numCyclesPerRun',
        nargs      = 1,
        type       = int,
        default    = 10,
        help       = 'Duration of one simulation run, in slotframe cycle.',
    )
    
    parser.add_argument( '--numRuns',
        dest       = 'numRuns',
        nargs      = 1,
        type       = int,
        default    = 3, 
        help       = 'Number of simulation runs per each configurations.',
    )
    
    parser.add_argument('--gui',
        dest       = 'gui',
        action     = 'store_true',
        default    = False,
        help       = 'Display the GUI during execution.',
    )
    
    options        = parser.parse_args()
    
    return options.__dict__

def main():
    # initialize logging
    logging.config.fileConfig('logging.conf')
    
    # parse CLI options
    options            = parseCliOptions()
    
    # start the GUI
    if options['gui']:
        gui            = SimGui.SimGui()
    
    # compute all the simulation parameter combinations
    combinationKeys    = sorted([k for (k,v) in options.items() if type(v)==list])
    simParams          = []
    for p in itertools.product(*[options[k] for k in combinationKeys]):
        simParam = {}
        for (k,v) in zip(combinationKeys,p):
            simParam[k] = v
        for (k,v) in options.items():
            if k not in simParam:
                simParam[k] = v
        simParams      += [simParam]
    print '{0} parameter combinations to run'.format(len(simParams))
    
    # run a simulation for each set of simParams
    for simParam in simParams:
        
        # record start time
        startTime = time.time()
        
        # run the simulation runs
        for runNum in xrange(simParam['numRuns']):
            
            # log
            print('run {0}/{1}, start'.format(runNum+1,simParam['numRuns']))
            
            # create singletons
            settings         = SimSettings.SimSettings(**simParam)
            settings.setStartTime(startTime)
            settings.setCombinationKeys(combinationKeys)
            propagation      = Propagation.Propagation()
            simengine        = SimEngine.SimEngine(runNum) # starts this simulation
            
            # wait for simulation to end
            simengine.join()
            
            # destroy singletons
            simengine.destroy()
            propagation.destroy()
            settings.destroy()
            
            # log
            print('run {0}/{1}, end'.format(runNum+1,simParam['numRuns']))

#============================ main ============================================

if __name__=="__main__":
    main()