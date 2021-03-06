# simulator-mhcc
A simulator in Python.

## Architecture
The simulators are pure functions defined in the `simulators.py` file.

There are two ways to run the simulator: a quick script and two simulators of the complete environment.

The quick script called `gendata.py` creates data for a complete day with 2 second intervals. It does not require RabbitMQ.

The script called `meter.py` generates a power consumption value and send it to a RabbitQM queue which name is fixed for this exercise. The number of seconds to generate power values can be customized with the -s parameter.

The script called `simulator.py` takes a power consumption value from a RabbitMQ queue and generates the pv power value. Both values are stored plus some calculations. The name of the file can be customized using the -f parameter.

The pv simulator use 2 futures to 1) hold the consuming loop of the rabbit channel, and 2) process the received  power consumption value.

The pv power value is calculated using a `sin` function `(amplitude * sin(x / divisor))`. I think the best estimation can be done using a neural network trained with real data. I used the `sin` function to keep it simple and due to the lack of real data.

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
4. Check the data many times:
```bash
cat data.txt
```

### Quick data generator
You can create the sample file of a complete day (from 00:00:00 to 00:00:00) with 2sec lecture intervals:
```bash
python3.5 gendata.py > data.txt
```

## Data representation
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
## Credits
José Figueroa Martínez

