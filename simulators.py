from pyrsistent import m, pmap, v


"""
context for simulate_consume
{"

"""

def meter_new_context():
    return m(value=0)


def simulate_meter_moc(context):
    return context.set('value', context['value'] + 1)




def simulate_pv_moc(context):
    return context.set('value', context['value'] + 1)
