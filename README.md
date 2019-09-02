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





# Uniform Traffic
## Aggregated Values vs parameters
### time_all_root
![time_all_root](bin/simData_steady/steady_time_all_root_vs_threshold_buf_100.png)

### max_latency
![max_latency](bin/simData_steady/steady_max_latency_vs_threshold_buf_100.png)

### latency
![latency](bin/simData_steady/steady_latency_vs_threshold_buf_100.png)

### chargeConsumedPerRecv
![chargeConsumedPerRecv](bin/simData_steady/steady_chargeConsumedPerRecv_vs_threshold_buf_100.png)

### chargeConsumed
![chargeConsumed](bin/simData_steady/steady_chargeConsumed_vs_threshold_buf_100.png)

### reliability
![reliability](bin/simData_steady/steady_reliability_vs_threshold_buf_100.png)

### max_txQueueFill
![max_txQueueFill](bin/simData_steady/steady_max_txQueueFill_vs_threshold_buf_100.png)

### txQueueFill
![txQueueFill](bin/simData_steady/steady_txQueueFill_vs_threshold_buf_100.png)

### LoadAllG
![LoadAllG](bin/simData_steady/steady_LoadAllG_vs_threshold_buf_100.png)

### LoadAllJain
![LoadAllJain](bin/simData_steady/steady_LoadAllJain_vs_threshold_buf_100.png)

### LoadCongG
![LoadCongG](bin/simData_steady/steady_LoadCongG_vs_threshold_buf_100.png)

### LoadCongJain
![LoadCongJain](bin/simData_steady/steady_LoadCongJain_vs_threshold_buf_100.png)

## Some indicative scenarios

## Scenario parents: 3, average inter-packet period: 0.1
### appGenerated
![appGenerated](bin/simData_steady/steady_appGenerated_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_steady/steady_appReachesDagroot_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_steady/steady_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### latency
![latency](bin/simData_steady/steady_latency_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### txQueueFill
![txQueueFill](bin/simData_steady/steady_txQueueFill_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### txQueueFill_cum
![txQueueFill_cum](bin/simData_steady/steady_txQueueFill_cum_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### numRxCells
![numRxCells](bin/simData_steady/steady_numRxCells_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### chargeConsumed
![chargeConsumed](bin/simData_steady/steady_chargeConsumed_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### LoadAllG
![LoadAllG](bin/simData_steady/steady_LoadAllG_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### LoadAllJain
![LoadAllJain](bin/simData_steady/steady_LoadAllJain_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### LoadCongG
![LoadCongG](bin/simData_steady/steady_LoadCongG_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

### LoadCongJain
![LoadCongJain](bin/simData_steady/steady_LoadCongJain_vs_time_buf_100_par_3_pkt_1_per_0.1.png)

## Scenario parents: 3, average inter-packet period: 0.2
### appGenerated
![appGenerated](bin/simData_steady/steady_appGenerated_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_steady/steady_appReachesDagroot_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_steady/steady_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### latency
![latency](bin/simData_steady/steady_latency_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### txQueueFill
![txQueueFill](bin/simData_steady/steady_txQueueFill_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### txQueueFill_cum
![txQueueFill_cum](bin/simData_steady/steady_txQueueFill_cum_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### numRxCells
![numRxCells](bin/simData_steady/steady_numRxCells_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### chargeConsumed
![chargeConsumed](bin/simData_steady/steady_chargeConsumed_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### LoadAllG
![LoadAllG](bin/simData_steady/steady_LoadAllG_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### LoadAllJain
![LoadAllJain](bin/simData_steady/steady_LoadAllJain_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### LoadCongG
![LoadCongG](bin/simData_steady/steady_LoadCongG_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

### LoadCongJain
![LoadCongJain](bin/simData_steady/steady_LoadCongJain_vs_time_buf_100_par_3_pkt_1_per_0.2.png)

## Scenario parents: 3, average inter-packet period: 0.4
### appGenerated
![appGenerated](bin/simData_steady/steady_appGenerated_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_steady/steady_appReachesDagroot_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_steady/steady_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### latency
![latency](bin/simData_steady/steady_latency_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### txQueueFill
![txQueueFill](bin/simData_steady/steady_txQueueFill_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### txQueueFill_cum
![txQueueFill_cum](bin/simData_steady/steady_txQueueFill_cum_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### numRxCells
![numRxCells](bin/simData_steady/steady_numRxCells_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### chargeConsumed
![chargeConsumed](bin/simData_steady/steady_chargeConsumed_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### LoadAllG
![LoadAllG](bin/simData_steady/steady_LoadAllG_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### LoadAllJain
![LoadAllJain](bin/simData_steady/steady_LoadAllJain_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### LoadCongG
![LoadCongG](bin/simData_steady/steady_LoadCongG_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

### LoadCongJain
![LoadCongJain](bin/simData_steady/steady_LoadCongJain_vs_time_buf_100_par_3_pkt_1_per_0.4.png)

# Bursty Traffic
## Aggregated Values vs parameters
### time_all_root
![time_all_root](bin/simData_bursts/bursts_time_all_root_vs_threshold_buf_100.png)

### max_latency
![max_latency](bin/simData_bursts/bursts_max_latency_vs_threshold_buf_100.png)

### latency
![latency](bin/simData_bursts/bursts_latency_vs_threshold_buf_100.png)

### chargeConsumedPerRecv
![chargeConsumedPerRecv](bin/simData_bursts/bursts_chargeConsumedPerRecv_vs_threshold_buf_100.png)

### chargeConsumed
![chargeConsumed](bin/simData_bursts/bursts_chargeConsumed_vs_threshold_buf_100.png)

### reliability
![reliability](bin/simData_bursts/bursts_reliability_vs_threshold_buf_100.png)

### max_txQueueFill
![max_txQueueFill](bin/simData_bursts/bursts_max_txQueueFill_vs_threshold_buf_100.png)

### txQueueFill
![txQueueFill](bin/simData_bursts/bursts_txQueueFill_vs_threshold_buf_100.png)

### LoadAllG
![LoadAllG](bin/simData_bursts/bursts_LoadAllG_vs_threshold_buf_100.png)

### LoadAllJain
![LoadAllJain](bin/simData_bursts/bursts_LoadAllJain_vs_threshold_buf_100.png)

### LoadCongG
![LoadCongG](bin/simData_bursts/bursts_LoadCongG_vs_threshold_buf_100.png)

### LoadCongJain
![LoadCongJain](bin/simData_bursts/bursts_LoadCongJain_vs_threshold_buf_100.png)

## Some indicative scenarios

## Scenario parents: 3, packets: 80
### appGenerated_cum
![appGenerated_cum](bin/simData_bursts/bursts_appGenerated_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_bursts/bursts_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_bursts/bursts_appReachesDagroot_vs_time_buf_100_par_3_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData_bursts/bursts_chargeConsumed_vs_time_buf_100_par_3_pkt_80.png)

### latency
![latency](bin/simData_bursts/bursts_latency_vs_time_buf_100_par_3_pkt_80.png)

### numRxCells
![numRxCells](bin/simData_bursts/bursts_numRxCells_vs_time_buf_100_par_3_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData_bursts/bursts_txQueueFill_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData_bursts/bursts_LoadAllG_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData_bursts/bursts_LoadAllJain_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData_bursts/bursts_LoadCongG_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData_bursts/bursts_LoadCongJain_vs_time_buf_100_par_3_pkt_80.png)

## Scenario parents: 3, packets: 50
### appGenerated_cum
![appGenerated_cum](bin/simData_bursts/bursts_appGenerated_cum_vs_time_buf_100_par_3_pkt_50.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_bursts/bursts_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_50.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_bursts/bursts_appReachesDagroot_vs_time_buf_100_par_3_pkt_50.png)

### chargeConsumed
![chargeConsumed](bin/simData_bursts/bursts_chargeConsumed_vs_time_buf_100_par_3_pkt_50.png)

### latency
![latency](bin/simData_bursts/bursts_latency_vs_time_buf_100_par_3_pkt_50.png)

### numRxCells
![numRxCells](bin/simData_bursts/bursts_numRxCells_vs_time_buf_100_par_3_pkt_50.png)

### txQueueFill
![txQueueFill](bin/simData_bursts/bursts_txQueueFill_vs_time_buf_100_par_3_pkt_50.png)

### LoadAllG
![LoadAllG](bin/simData_bursts/bursts_LoadAllG_vs_time_buf_100_par_3_pkt_50.png)

### LoadAllJain
![LoadAllJain](bin/simData_bursts/bursts_LoadAllJain_vs_time_buf_100_par_3_pkt_50.png)

### LoadCongG
![LoadCongG](bin/simData_bursts/bursts_LoadCongG_vs_time_buf_100_par_3_pkt_50.png)

### LoadCongJain
![LoadCongJain](bin/simData_bursts/bursts_LoadCongJain_vs_time_buf_100_par_3_pkt_50.png)

## Scenario parents: 3, packets: 25
### appGenerated_cum
![appGenerated_cum](bin/simData_bursts/bursts_appGenerated_cum_vs_time_buf_100_par_3_pkt_25.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_bursts/bursts_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_25.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_bursts/bursts_appReachesDagroot_vs_time_buf_100_par_3_pkt_25.png)

### chargeConsumed
![chargeConsumed](bin/simData_bursts/bursts_chargeConsumed_vs_time_buf_100_par_3_pkt_25.png)

### latency
![latency](bin/simData_bursts/bursts_latency_vs_time_buf_100_par_3_pkt_25.png)

### numRxCells
![numRxCells](bin/simData_bursts/bursts_numRxCells_vs_time_buf_100_par_3_pkt_25.png)

### txQueueFill
![txQueueFill](bin/simData_bursts/bursts_txQueueFill_vs_time_buf_100_par_3_pkt_25.png)

### LoadAllG
![LoadAllG](bin/simData_bursts/bursts_LoadAllG_vs_time_buf_100_par_3_pkt_25.png)

### LoadAllJain
![LoadAllJain](bin/simData_bursts/bursts_LoadAllJain_vs_time_buf_100_par_3_pkt_25.png)

### LoadCongG
![LoadCongG](bin/simData_bursts/bursts_LoadCongG_vs_time_buf_100_par_3_pkt_25.png)

### LoadCongJain
![LoadCongJain](bin/simData_bursts/bursts_LoadCongJain_vs_time_buf_100_par_3_pkt_25.png)

## Scenario parents: 3, packets: 5
### appGenerated_cum
![appGenerated_cum](bin/simData_bursts/bursts_appGenerated_cum_vs_time_buf_100_par_3_pkt_5.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData_bursts/bursts_appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_5.png)

### appReachesDagroot
![appReachesDagroot](bin/simData_bursts/bursts_appReachesDagroot_vs_time_buf_100_par_3_pkt_5.png)

### chargeConsumed
![chargeConsumed](bin/simData_bursts/bursts_chargeConsumed_vs_time_buf_100_par_3_pkt_5.png)

### latency
![latency](bin/simData_bursts/bursts_latency_vs_time_buf_100_par_3_pkt_5.png)

### numRxCells
![numRxCells](bin/simData_bursts/bursts_numRxCells_vs_time_buf_100_par_3_pkt_5.png)

### txQueueFill
![txQueueFill](bin/simData_bursts/bursts_txQueueFill_vs_time_buf_100_par_3_pkt_5.png)

### LoadAllG
![LoadAllG](bin/simData_bursts/bursts_LoadAllG_vs_time_buf_100_par_3_pkt_5.png)

### LoadAllJain
![LoadAllJain](bin/simData_bursts/bursts_LoadAllJain_vs_time_buf_100_par_3_pkt_5.png)

### LoadCongG
![LoadCongG](bin/simData_bursts/bursts_LoadCongG_vs_time_buf_100_par_3_pkt_5.png)

### LoadCongJain
![LoadCongJain](bin/simData_bursts/bursts_LoadCongJain_vs_time_buf_100_par_3_pkt_5.png)


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

