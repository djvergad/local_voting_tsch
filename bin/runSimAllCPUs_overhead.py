#!/usr/bin/env python2
'''
\brief Start batch of simulations concurrently.
Workload is distributed equally among CPU cores.
\author Thomas Watteyne <watteyne@eecs.berkeley.edu>
'''

import os
import time
import math
import multiprocessing
import fileinput

MIN_TOTAL_RUNRUNS = 2 # 500 # 94 # 500
algos = [('local_voting_z','None'), ('local_voting_z','Shared'), ('local_voting_z','All')]


def runOneSim(params):
    (cpuID,numRuns) = params
    command     = []
    # command     = ['ssh {0} "cd $PWD;'.format(host)]
    command    = ['python2 runSimOneCPU.py']
    command    += ['--numRuns {0}'.format(numRuns)]
    command    += ['--cpuID {0}'.format(cpuID)]
#     command    += ['--numPacketsBurst {0}'.format(0)]
#    command    += ['--parents {0}'.format(3)]
 #   command    += ['--burstTimestamp {0}'.format(None)]
    command    += ['--pkPeriod {0}'.format('0.1')]# 0.1 0.2 0.4')]
    command    += ['--buffer {0}'.format(100)]

    algo = algos[cpuID % len(algos)]
    command    += ['--algorithm {0}'.format(algo[0])] # eotf otf local_voting local_voting_z
#     command    += ['--otfThreshold {0}'.format(algo[1])]
    command    += ['--lvMessageFreq={0}'.format(algo[1])]
#    command    += ['--parents {0}'.format(1)]
    command    += ['--scheduler {0}'.format('deBras')] # deBras, none
    command    += ['--simDataDir {0}'.format('simData_overhead')] # deBras, none
#     command    += ['--seed {0}'.format(1024)] # deBras, none

    # command    += ['--numChans {0}'.format(1)]
    # command    += ['"']
    #command    += ['&']
    command     = ' '.join(command)
    print "Executing command '{0}'".format(command)
    os.system(command)

def printProgress(num_cpus):
    while True:
        time.sleep(1)
        output     = []
        for cpu in range(num_cpus):
            with open('cpu{0}.templog'.format(cpu),'r') as f:
                output += ['[cpu {0}] {1}'.format(cpu,f.read())]
        allDone = True
        for line in output:
            if line.count('ended')==0:
                allDone = False
        output = '\n'.join(output)
        # os.system('clear')
        # print output
        with open('progress.txt', 'w') as f:
            f.write(output)

        if allDone:
            break
    for cpu in range(num_cpus):
        os.remove('cpu{0}.templog'.format(cpu))

def buildSshParams():
    result = []
    i = 0
    for line in fileinput.input():
        (cores,host)=line.rstrip().split("/")
        cores = int(cores) if len(cores) > 0 else 0
        print "We read {0} {1}".format(cores, host)
        for j in range(int(cores)):
            result.append(host)
    return result


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # ssh_params = buildSshParams()
    # print "The ssh params are {0}".format(ssh_params)
    # num_cpus = len(ssh_params) # multiprocessing.cpu_count()
    num_cpus = max(min(multiprocessing.cpu_count(), len(algos)* MIN_TOTAL_RUNRUNS), len(algos))
    runsPerCpu =  int(math.ceil(float(MIN_TOTAL_RUNRUNS)/float(num_cpus)*float(len(algos))))
    pool = multiprocessing.Pool(num_cpus)
    pool.map_async(runOneSim,[(i,runsPerCpu) for i in range(num_cpus)])
    printProgress(num_cpus)
    raw_input("Done. Press Enter to close.")
