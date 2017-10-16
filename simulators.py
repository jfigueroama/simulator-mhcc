from pyrsistent import m, pmap, v, pvector
from datetime import datetime, time
import math

def simulate_meter_moc(context):
    return context.set('value', context['value'] + 1)

def meter_new_context():
    context = m(
        value       = 0,                # the consumption value (watts)
        rnd_changep = 0,                # 0-1. Explained above
        rnd_sign    = 0,                # 1 if > 0.5 else -1
        rnd_change  = 0,                # value between min_change and max_change
        min_value   = 0,                # lower bound of value
        max_value   = 9000,             # upper bound of value
        min_change  = 5,                # minimum value change (watts)
        max_change  = 200,              # maximum value change (watts)
        change_rate = 0.8,              # 0-1, changes will occur
                                        #    if rnd_changep <= change_rate
        dt          = None #datetime.now()    # current moment. Not needed now.

    )
    return context




def update_meter_context(context, rndchangep, rndsign, rndchange):
    return context.set('rnd_changep', rndchangep).set('rnd_sign', rndsign).set('rnd_change', rndchange)

# Return a randomly updated meter context.
# It receives the context and the random generator.
def rand_meter_context(context, rnd):
    return update_meter_context(context,
                                rnd.random(),
                                rnd.random(),
                                rnd.randint(context['min_change'],
                                            context['max_change']))

# To simulate a meter we use a "house" with different appliances. Each of them
# has a probability to be on during certian moments of the day.
# The house information does not change, but the current appliances status have
# to change.
# The final consumption is the sum of the watts used by the appliances turned on
# during the checking.
#
# meter_new_context().set('rnd_changep', 1).set('rnd_sign', 0).set('rnd_change', 100)
#
def simulate_linear_meter(context):
    changep = context['change_rate'] >= context['rnd_changep']
    
    if changep:
        operator = 1 if (context['rnd_sign'] > 0.5) else -1
        ovalue   = context['value']
        cvalue   = ovalue + (context['rnd_change'] * operator)
        dvalue   = cvalue if ((cvalue < context['max_value'] 
                               and cvalue > context['min_value']) 
                              or cvalue == context['min_value'] 
                              or cvalue == context['max_value']) else ovalue

        return context.set('value', dvalue)
    else:
        return context

#####################################
#####################################
# POV

def simulate_pv_moc(context):
    return context.set('value', context['value'] + 1)


def pv_new_context():
    context = m(
        value       = 0,                # the consumption value (in kW)
        rnd_changep = 0,                #
        rnd_change  = 0,                #

        curve_start = None,             # start time of the curve increase.

        amplitude   = 3.25,             # amplitude * sin(x / divisor)
        divisor     = 4.4,              #   

        max_change  = 0.2,              # maximum value (watts)
        change_rate = 0.8,              # 0-1, changes will occur
                                        #       if change_rate >= rnd_changep
        dt          = None #datetime.now()    # current moment

    )
    return context

def update_pv_change(ctx, change):
    nchange = change % ctx['max_change']
    return ctx.set('rnd_change', nchange)

def is_pv_context_ok(ctx):
    issomenone = (ctx['curve_start'] is None)
    return (not issomenone)

def time2dec(ti):
    if (ti is None):
        return 0
    else:
        return ti.hour + (100*ti.minute / 6000)

# sin based approximation
# The formula y=amplitude*sin((x+ added)/divisor) is usted to create a similar curve.
# This function creates the ideal value.
def pv_sba(ctx):
    if is_pv_context_ok(ctx):
        power = 0
        ctime = time(ctx['dt'].hour,
                     ctx['dt'].minute,
                     ctx['dt'].second)
        cval  = time2dec(ctime)

        if (ctime >= ctx['curve_start']):
            # Simulation of the main curve
            cinit = time2dec(ctx['curve_start'])
            x     = cval - cinit
            power = ctx['amplitude'] * math.sin(x / ctx['divisor'])

        return power

    else:
        return 0


# This simuation uses a point based approximation (pba) to 
def simulate_pv(spvfn, ctx):
    changep = ctx['change_rate'] >= ctx['rnd_changep']
    
    if changep:
        ovalue   = spvfn(ctx)
        cvalue   = ovalue - ctx['rnd_change']
        
        if (cvalue >= 0):
            return ctx.set('value', cvalue)
        
    return ctx
