import unittest
from discrete_model import parse_smbionet_output_file, InfluenceGraph, DiscreteModel
from simu_net import Simulation, Result


class Test(unittest.TestCase):
    def test_mucus_operon_v3(self):
        model1, *_ = parse_smbionet_output_file('../ggea/resources/model2346.out')
        simulation = Simulation(model1)
        result = simulation.run()
        self.assertEqual(100, len(result.states))

    def test_day_night_cycle(self):
        model1, *_ = parse_smbionet_output_file('resources/day_night_cycle.out')
        simulation = Simulation(model1)
        simulation.steps = 5
        simulation.random.seed(0xff)
        result = simulation.run()
        expected = [
            {'G': 0, 'P': 1},
            {'G': 0, 'P': 0},
            {'G': 1, 'P': 0},
            {'G': 1, 'P': 1},
            {'G': 0, 'P': 1}
        ]
        for e, a in zip(expected, result.states):
            self.assertEqual(e, {v.name: s for v, s in a.items()})


if __name__ == '__main__':
    unittest.main()
