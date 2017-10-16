import unittest
from datetime import datetime, time
import simulators
from simulators import meter_new_context, simulate_linear_meter, update_meter_context


class TestSimulators(unittest.TestCase):
    def setUp(self):
        pass

    def test_update_meter_context(self):
        ctx = update_meter_context(meter_new_context(), 100, 200, 300)
        self.assertEqual(ctx['rnd_changep'], 100)
        self.assertEqual(ctx['rnd_sign'], 200)
        self.assertEqual(ctx['rnd_change'], 300)

    def test_simulate_linear_meter(self):
        ctx1  = meter_new_context()
        ctx2  = ctx1.set('value', 5000)
        self.assertEqual(simulate_linear_meter(update_meter_context(ctx1, 0, 1, 100))['value'], 100)
        self.assertEqual(simulate_linear_meter(update_meter_context(ctx1, 0, 0, 100))['value'], 0)
        self.assertEqual(simulate_linear_meter(update_meter_context(ctx1, 0, 1, 9001))['value'], 0)
        self.assertEqual(simulate_linear_meter(update_meter_context(ctx2, 0, 0, 4000))['value'], 1000)
        self.assertEqual(simulate_linear_meter(update_meter_context(ctx2, 1, 0, 4000))['value'], 5000)


    def test_time2dec(self):
        self.assertEqual(simulators.time2dec(time(12,30)), 12.5)
        self.assertEqual(simulators.time2dec(time(12,00)), 12.0)
        self.assertEqual(simulators.time2dec(time(12,45)), 12.75)

if __name__ == '__main__':
    unittest.main()
