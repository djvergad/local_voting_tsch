#!/bin/bash
# ./runSimOneCPU.py --numRuns=1 --numCyclesPerRun=100 --numChans 1 --pkPeriod 0.3 --pkPeriodVar 0.3 --otfHousekeepingPeriod 1 | tee tmp.out
# python -u runSimOneCPU.py --cpuID=1 --numRuns=1 --pkPeriod=0.1 --buffer=100 --algorithm=local_voting_z --parents=1 --scheduler=deBras --simDataDir=single | tee tmp.out
# python2 -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --numPacketsBurst 80 --algorithm local_voting_z --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs | tee tmp.out
# python3 -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numRadios=1 --numCyclesPerRun=600 --algorithm=eotf --numPacketsBurst 5 --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 100 --parents=1 --scheduler deBras --simDataDir testOutputs | tee tmp.out
# python3 -m cProfile -o output.pstats runSimOneCPU.py


# python3 -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numRadios=1 --numCyclesPerRun=600 --algorithm=eotf --numPacketsBurst 5 --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 100 --parents=1 --scheduler deBras --simDataDir testOutputs | tee tmp.out

### bursts
# python3 -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100 --algorithm='eotf' --numPacketsBurst 25 --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 600 --scheduler deBras --simDataDir testOutputs | tee tmp.out &
# python3 -u runSimOneCPU.py --cpuID 15 --numRuns=1 --numCyclesPerRun=100 --algorithm='local_voting_z' --numPacketsBurst 80 --burstTimestamp 20 --pkPeriod 16 --otfThreshold 10 --buffer 600 --scheduler deBras --simDataDir testOutputs5 | tee tmp.out &

### steady
# python3 -u runSimOneCPU.py --cpuID 1 --numRuns=1 --numCyclesPerRun=100 --algorithm=eotf --pkPeriod 0.8 --otfThreshold 10 --buffer 600 --scheduler deBras --simDataDir testOutputs | tee tmp.out &
# ./runSimOneCPU.py --cpuID 2 --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --pkPeriod 0.8 --otfThreshold 10 --buffer 600 --scheduler deBras --simDataDir testOutputs2 | tee tmp.out &



python2 -u runSimOneCPU.py --seed 4 --cpuID 4 --lvMessageFreq None --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --pkPeriod 0.1 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs_over &
python2 -u runSimOneCPU.py --seed 4 --cpuID 4 --lvMessageFreq Shared --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --pkPeriod 0.1 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs_over &
python2 -u runSimOneCPU.py --seed 4 --cpuID 4 --lvMessageFreq All  --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --pkPeriod 0.1 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs_over &

# python2 -u runSimOneCPU.py --seed 2 --lvMessageFreq 6top --cpuID 2 --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --algorithm local_voting_z --pkPeriod 0.1 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs_over &
# python2 -u runSimOneCPU.py --seed 3 --lvMessageFreq 6top --cpuID 3 --numRuns=1 --numCyclesPerRun=100 --algorithm=local_voting_z --algorithm local_voting_z --pkPeriod 0.1 --otfThreshold 10 --buffer 100 --parents=3 --scheduler deBras --simDataDir testOutputs_over &


wait
