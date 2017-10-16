#!/usr/bin/env python3.5

import argparse
import pika
import time
import random
from pyrsistent import m, pmap
import simulators
import utils

QUEUE="simulator-mhcc"

def main(conf):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    ch = conn.channel()
    ch.queue_declare(queue=QUEUE)
    
    context = simulators.meter_new_context()

    while True:
        time.sleep(conf["sleep"])
        context = simulators.simulate_meter_moc(context)
        #time.time()
        print(context)


#    ch.basic_publish(exchange='',
#                      routing_key='simulator-mhcc',
#                      body='Hello World!')
#    print(" [x] Sent 'Hello World!'")
    conn.close()


if __name__ == "__main__":
    main({"sleep": 2})
    print("simulador-meter")


