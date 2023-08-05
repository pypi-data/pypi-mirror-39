import unittest
from discrete_model import parse_smbionet_output_file, InfluenceGraph, DiscreteModel


class Test(unittest.TestCase):
    def test_mucus_operon_v3(self):
        model1, model2 = parse_smbionet_output_file('resources/mucusOperonV3.out')
        graph = InfluenceGraph()
        graph.add_variable('operon', 0, 2)
        graph.add_variable('mucuB', 0, 1)
        graph.add_regulation('free', 'operon', '(not(mucuB>=1))')
        graph.add_regulation('alg', 'operon', '(operon>=1)')
        graph.add_regulation('prod', 'mucuB', '(operon>=1)')

        expected_model1 = DiscreteModel(graph)
        expected_model1.set_variable_state('K_operon', 0)
        expected_model1.set_variable_state('K_operon+alg', 2)
        expected_model1.set_variable_state('K_operon+free', 0)
        expected_model1.set_variable_state('K_operon+alg+free', 2)
        expected_model1.set_variable_state('K_mucuB', 0)
        expected_model1.set_variable_state('K_mucuB+prod', 1)

        expected_model2 = DiscreteModel(graph)
        expected_model2.set_variable_state('K_operon', 0)
        expected_model2.set_variable_state('K_operon+alg', 2)
        expected_model2.set_variable_state('K_operon+free', 1, 2)
        expected_model2.set_variable_state('K_operon+alg+free', 2)
        expected_model2.set_variable_state('K_mucuB', 0)
        expected_model2.set_variable_state('K_mucuB+prod', 1)

        self.assertEqual(expected_model1, model1)
        self.assertEqual(expected_model2, model2)


if __name__ == '__main__':
    unittest.main()
