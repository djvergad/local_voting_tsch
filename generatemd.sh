#!/bin/bash

cat << 'EOF'
Local Voting TSCH
=================

Implementation of the Local Voting algorithm in the 6TiSCH Simulator, and some
simulation results.

Comparison of slot allocation algorithm Local Voting Z, Local Voting, OTF and E-OTF.

Results for bursty and uniform traffic.


You can find eps and png figures of the results in folder bin/simData_steady/ and 
bin/simData_bursts/

Some indicative results:

# Table of Contents


[TOC]





EOF

buf=(100 100 100 100)
par=(3   3   3   3)
pkt=(80  50  25  5)

rates=(0.1 0.2 0.4)

bar_metrics=(time_all_root max_latency latency chargeConsumedPerRecv chargeConsumed reliability max_txQueueFill txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain)
line_metrics=(appGenerated_cum appReachesDagroot_cum appReachesDagroot chargeConsumed latency numRxCells txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain)

printf '# Uniform Traffic\n'

printf '## Aggregated Values vs parameters\n'

for metric in "${bar_metrics[@]}"
do
    printf '### %s\n' "$metric"
    printf '![%s](bin/simData_steady/steady_%s_vs_threshold_buf_100.png)\n' "$metric" "$metric"
    printf "\n"
done

printf '## Some indicative scenarios\n'
printf "\n"


for i in 0 1 2
do
    printf '## Scenario parents: %s, average inter-packet period: %s\n' "${rates[i]}"

    for metric in "${line_metrics[@]}"
    do
        printf '### %s\n' "$metric" 
        printf '![%s](bin/simData_steady/steady_%s_vs_time_buf_%d_par_%d_pkt_1_per_%s.png)\n' "$metric" "$metric" "${buf[$i]}" "${par[$i]}" "${rates[$i]}"
        printf "\n"
    done
done

printf '# Bursty Traffic\n'

printf '## Aggregated Values vs parameters\n'

for metric in "${bar_metrics[@]}"
do
    printf '### %s\n' "$metric"
    printf '![%s](bin/simData_bursts/bursts_%s_vs_threshold_buf_100.png)\n' "$metric" "$metric"
    printf "\n"
done

printf '## Some indicative scenarios\n'
printf "\n"


for i in 0 1 2 3
do
    printf '## Scenario parents: %d, packets: %s\n' "${par[i]}" "${pkt[i]}"

    for metric in "${line_metrics[@]}"
    do
        printf '### %s\n' "$metric" 
        printf '![%s](bin/simData_bursts/bursts_%s_vs_time_buf_%d_par_%d_pkt_%d.png)\n' "$metric" "$metric" "${buf[$i]}" "${par[$i]}" "${pkt[$i]}"
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

EOF
