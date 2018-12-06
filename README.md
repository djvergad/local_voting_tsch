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

### time_all_root
![time_all_root](bin/simData/time_all_root_vs_threshold_buf_100.png)

### max_latency
![max_latency](bin/simData/max_latency_vs_threshold_buf_100.png)

### latency
![latency](bin/simData/latency_vs_threshold_buf_100.png)

### chargeConsumedPerRecv
![chargeConsumedPerRecv](bin/simData/chargeConsumedPerRecv_vs_threshold_buf_100.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_threshold_buf_100.png)

### reliability
![reliability](bin/simData/reliability_vs_threshold_buf_100.png)

### max_txQueueFill
![max_txQueueFill](bin/simData/max_txQueueFill_vs_threshold_buf_100.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_threshold_buf_100.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_threshold_buf_100.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_threshold_buf_100.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_threshold_buf_100.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_threshold_buf_100.png)

Some indicative scenarios
===================

Scenario parents: 1, packets: 80
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_1_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_1_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_1_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_1_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_1_pkt_80.png)

Scenario parents: 1, packets: 50
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_1_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_1_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_1_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_1_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_1_pkt_80.png)

Scenario parents: 1, packets: 25
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_1_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_1_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_1_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_1_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_1_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_1_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_1_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_1_pkt_80.png)

Scenario parents: 2, packets: 25
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_2_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_2_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_2_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_2_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_2_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_2_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_2_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_2_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_2_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_2_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_2_pkt_80.png)

Scenario parents: 3, packets: 25
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_3_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_3_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_3_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_3_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_3_pkt_80.png)

Scenario parents: 3, packets: 5
------------------------------
### appGenerated_cum
![appGenerated_cum](bin/simData/appGenerated_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot_cum
![appReachesDagroot_cum](bin/simData/appReachesDagroot_cum_vs_time_buf_100_par_3_pkt_80.png)

### appReachesDagroot
![appReachesDagroot](bin/simData/appReachesDagroot_vs_time_buf_100_par_3_pkt_80.png)

### chargeConsumed
![chargeConsumed](bin/simData/chargeConsumed_vs_time_buf_100_par_3_pkt_80.png)

### latency
![latency](bin/simData/latency_vs_time_buf_100_par_3_pkt_80.png)

### numRxCells
![numRxCells](bin/simData/numRxCells_vs_time_buf_100_par_3_pkt_80.png)

### txQueueFill
![txQueueFill](bin/simData/txQueueFill_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllG
![LoadAllG](bin/simData/LoadAllG_vs_time_buf_100_par_3_pkt_80.png)

### LoadAllJain
![LoadAllJain](bin/simData/LoadAllJain_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongG
![LoadCongG](bin/simData/LoadCongG_vs_time_buf_100_par_3_pkt_80.png)

### LoadCongJain
![LoadCongJain](bin/simData/LoadCongJain_vs_time_buf_100_par_3_pkt_80.png)


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
