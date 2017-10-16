# simulator-mhcc
A simulator in Python.

## Architecture
The simulators are pure functions defined in the `simulators.py` file.

There are two ways to run the simulator: a quick script and a simulator of the complete environment.

The quick script called `gendata.py` creates data for a complete day with 2 second intervals. It does not require RabbitMQ.

The script called `simulator.py` is a complete environment that generates a power consumption value, send it to the pv simulator through RabbitMQ and then the pv simulator generates and store the generated data plus some calculations.

Both simulators are called from the `simulator.py` and run inside futures.

## Requirements

The complete simulator requires a localhost RabbitMQ server plus some python libraries:
* pika
* pyrsistent

## Usage

1. Please make sure you have a RabbitMQ server running in your localhost.
2. Run the meter simulator script in one terminal:
```bash
python3 meter.py -s 2
```
3. Run the simulator script in another terminal:
```bash
python3 simulator.py -f data.txt
```
4. Check the data:
```bash
cat data.txt
```


### Quick data generator
You can create the sample file of a complete day (from 00:00:00 to 00:00:00) with 2sec lecture intervals:
```bash
python3.5 gendata.py > data.txt
```


### Data representation
Each column represents:
* captured-at: Moment of capture.
* consumption: Simulated power consumption (watts).
* pvpower: Simulated power generated by a PV (kilo watts).
* consumption+pvpower(W): Sum of the generated values (watts).
* consumption-pvpower(W): Difference of the generated values (watts).


```
captured-at consumption(W)  pvpower(kW) consumption+pvpower(W)  consumption-pvpower(W)
2017-10-16T08:00:00:    453 0.6213883323197676  1074.3883323197676  -168.38833231976764
```

