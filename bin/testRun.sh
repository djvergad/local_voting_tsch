#!/bin/bash
# ./runSimOneCPU.py --numRuns=1 --numCyclesPerRun=100 --numChans 1 --pkPeriod 0.3 --pkPeriodVar 0.3 --otfHousekeepingPeriod 1 | tee tmp.out
# python runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100 --numChans 3 --pkPeriod 0.5 --pkPeriodVar 0 --otfHousekeepingPeriod 1 | tee tmp.out
python -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100  --numPacketsBurst 25 --burstTimestamp 20 --pkPeriod 16 --otfThreshold 0 --buffer 100 --parents=1 --scheduler none --algorithm otf | tee tmp.out
