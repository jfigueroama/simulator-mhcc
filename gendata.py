#!/usr/bin/env python3.5

import random
from datetime import datetime, time
from pyrsistent import m, pmap
import simulators
import utils

from simulators import meter_new_context, pv_new_context, update_meter_context, update_pv_change, simulate_linear_meter, simulate_pv, pv_sba, rand_meter_context

random.seed()

def main():
    meter  = meter_new_context()
    pv     = pv_new_context().set('curve_start', time(7,0))
    dt     = datetime.now()

    utils.print_headers()
    for hour in range(0, 24):
        for minute in range(0, 60):
            for second in filter(lambda x: x % 2 == 0, range(0,60)):
                dt    = dt.replace(dt.year, dt.month, dt.day, hour, minute, second)
                ti    = time(hour, minute, second)
                
                meter = rand_meter_context(meter, random)
                pv    = (update_pv_change(pv, random.random())
                         .set('rnd_changep', random.random())
                         .set('dt', dt))

                meter = simulate_linear_meter(meter)
                pv    = simulate_pv(pv_sba, pv)
                
                utils.print_result(meter['value'], pv['value'], dt)


if __name__ == "__main__":
    main()


