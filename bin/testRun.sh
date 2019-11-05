#!/bin/bash
# ./runSimOneCPU.py --numRuns=1 --numCyclesPerRun=100 --numChans 1 --pkPeriod 0.3 --pkPeriodVar 0.3 --otfHousekeepingPeriod 1 | tee tmp.out
# python -u runSimOneCPU.py --cpuID=1 --numRuns=1 --pkPeriod=0.1 --buffer=100 --algorithm=local_voting_z --parents=1 --scheduler=deBras --simDataDir=single | tee tmp.out
python -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --numPacketsBurst 50 --algorithm local_voting_z --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs | tee tmp.out
