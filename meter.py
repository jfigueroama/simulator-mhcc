#!/usr/bin/env python
import argparse
import pika
import time
from pyrsistent import m, pmap
import random

from simulators import rand_meter_context, meter_new_context, simulate_linear_meter



QUEUE="simulator-mhcc"  # same QUÉÚÉ as in simulator.py

def main(seconds):
    try:
        para = pika.ConnectionParameters(host='localhost')
        conn = pika.BlockingConnection(para)
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE)
        context = meter_new_context()

        while True:
            time.sleep(seconds)
            context = simulate_linear_meter(rand_meter_context(context,random))
            print(context['value'])

            ch.basic_publish(exchange='',
                             routing_key=QUEUE,
                             body=str(context['value']))

        conn.close()
    except Exception as e:
        conn.close()


if __name__ == "__main__":
    desc = "Power Consumption Simulator"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-s', metavar='seconds', type=int, nargs='?',
                        default=2,
                        help='Will send generated values every desired seconds.')
    args = parser.parse_args()

    main(args.s)

