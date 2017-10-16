#!/usr/bin/env python3.5

import argparse
import pika
from datetime import datetime, time
import random
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from pyrsistent import m, pmap
from functools import partial
import os.path

from simulators import simulate_pv, pv_new_context, update_pv_change, simulate_pv, pv_sba
import utils

QUEUE="simulator-mhcc"

###################################




def pvsimulator(fname, qu):
    ctx = pv_new_context().set('curve_start', time(7,0))
    print("Started simulator")
    
    if not os.path.isfile(fname):
        utils.write_headers(fname)
        print("Created file " + fname)

    try:
        while True:
            body   = qu.get()
            consup = int(body)
            dt     = datetime.now()
            ctx    = (update_pv_change(ctx, random.random())
                      .set('rnd_changep', random.random())
                      .set('dt', dt))
            ctx    = simulate_pv(pv_sba, ctx)
            power  = ctx['value']

            print("Processing consumption and pv value: "
                  + body + ", " + str(power))
            utils.write_result(fname, consup, power, dt)

    except Exception as e:
        print(e)
        print("Finished pvsimulator")


def pvs_stopped(fut):
    print("Finished pvsimulator")

def msg_callback(qu, ch, method, properties, body):
    rbody = body.decode('UTF-8')
    #print("Received value " + rbody)
    qu.put(rbody)

def msg_handler(qu):
    try:
        pars = pika.ConnectionParameters(host='localhost')
        conn = pika.BlockingConnection(pars)
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE)
        ch.basic_consume(partial(msg_callback, qu), queue=QUEUE, no_ack=True)

        ch.start_consuming()
        
        conn.close()

    except Exception as e:
        conn.close()

def mhs_stopped(fut):
    print(fut)

##########################
if __name__ == "__main__":
    desc   = "PV Simulator"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', metavar='fname', type=str,
                        nargs='?', help='file to store the simulation data.',
                        default="data_simulation.txt")
    args       = parser.parse_args()

    ex         = ThreadPoolExecutor(max_workers=2)
    msgs       = Queue()

    pv_future  = ex.submit(pvsimulator, args.f, msgs) # Save and print received data
    mhs_future = ex.submit(msg_handler, msgs)     # Manage the channel
    pv_future.add_done_callback(pvs_stopped)
    mhs_future.add_done_callback(mhs_stopped)
