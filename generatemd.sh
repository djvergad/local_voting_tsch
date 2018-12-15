#!/bin/bash

cat << 'EOF'
Local Voting TSCH
=================

Implementation of the Local Voting algorithm in the 6TiSCH Simulator, and some
simulation results. Comparison of Local Voting with OTF, thresholds 0,1,4,10,
1,2, and 3 parents, 100 buffer size, and 5 25 50 80 packets per burst.

You can find eps and png figures of the results in folder bin/simData/

Some indicative results:

Table of Contents
=================

[TOC]

Aggregated Values vs parameters
===============================

EOF

buf=(100 100 100 100)
par=(3   3   3   3)
pkt=(80  50  25  5)


for metric in time_all_root max_latency latency chargeConsumedPerRecv chargeConsumed reliability max_txQueueFill txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain
do
    printf '### %s\n' "$metric"
    printf '![%s](bin/simData/%s_vs_threshold_buf_100.png)\n' "$metric" "$metric"
    printf "\n"
done

printf 'Some indicative scenarios\n'
printf '===================\n'
printf "\n"


for i in 0 1 2 3
do
    printf 'Scenario parents: %d, packets: %s\n' "${par[i]}" "${pkt[i]}"
    printf -- '------------------------------\n'

    for metric in appGenerated_cum appReachesDagroot_cum appReachesDagroot chargeConsumed latency numRxCells txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain
    do
        printf '### %s\n' "$metric" 
        printf '![%s](bin/simData/%s_vs_time_buf_%d_par_%d_pkt_%d.png)\n' "$metric" "$metric" "${buf[$i]}" "${par[$i]}" "$pkt"
        printf "\n"
    done
done
 
cat << 'EOF'

Code Organization
-----------------

* `bin/`: the script for you to run
* `SimEngine/`: the simulator
    * `Mote.py`: Models a 6TiSCH mote running the different standards listed above.
    * `Propagation.py`: Wireless propagation model.
    * `SimEngine.py`: Event-driven simulation engine at the core of this simulator.
    * `SimSettings.py`: Data store for all simulation settings.
    * `SimStats.py`: Periodically collects statistics and writes those to a file.
    * `Topology.py`: creates a topology of the motes in the network.
* `SimGui/`: the graphical user interface to the simulator

Issues and bugs
---------------

* Report at https://bitbucket.org/6tsch/simulator/issues
EOF
