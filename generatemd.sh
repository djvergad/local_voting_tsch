#!/bin/bash

buf=(100 100 100 100 100 100)
par=(1 1 1 2 3 3)
pkt=(80 50 25 25 25 5)

printf 'Table of Contents\n'
printf '=================\n\n'

printf '1. [Aggregated results](#aggr)\n'

for i in 0 1 2 3 4 5
do
  printf '%d. [Scenario parents: %d, packets: %s](#sec_%d)\n' "$((i + 2))" "${par[i]}" "${pkt[i]}" "$i"
done
printf "\n"


printf 'Aggregated Values vs parameters <a name="aggr"></a>\n'
printf '===============================\n'
printf "\n"

for metric in time_all_root max_latency latency chargeConsumedPerRecv chargeConsumed reliability max_txQueueFill txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain
do
    printf '### %s\n' "$metric"
    printf '![%s](bin/simData/%s_vs_threshold_buf_100.png)\n' "$metric" "$metric"
    printf "\n"
done

printf 'Some indicative scenarios\n'
printf '===================\n'
printf "\n"


for i in 0 1 2 3 4 5
do
    printf 'Scenario parents: %d, packets: %s <a name="sec_%d"></a>\n' "${par[i]}" "${pkt[i]}" "$i"
    printf -- '------------------------------\n'

    for metric in appGenerated_cum appReachesDagroot_cum appReachesDagroot chargeConsumed latency numRxCells txQueueFill LoadAllG LoadAllJain LoadCongG LoadCongJain
    do
        printf '### %s\n' "$metric" 
        printf '![%s](bin/simData/%s_vs_time_buf_%d_par_%d_pkt_%d.png)\n' "$metric" "$metric" "${buf[$i]}" "${par[$i]}" "$pkt"
        printf "\n"
    done
done
 
