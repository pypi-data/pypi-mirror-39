import unittest
from discrete_model import parse_smbionet_output_file, InfluenceGraph, DiscreteModel


class Test(unittest.TestCase):
    def test_process_activation(self):
        model1, _ = parse_smbionet_output_file('resources/mucusOperonV3.out')
        free = model1.influence_graph.find_process_by_name('free')
        self.assertTrue(free.is_active(mucuB=0))

    def test_find_transition(self):
        model1, model2 = parse_smbionet_output_file('resources/mucusOperonV3.out')
        operon = model1.influence_graph.find_variable_by_name('operon')
        free = model1.influence_graph.find_process_by_name('free')
        alg = model1.influence_graph.find_process_by_name('alg')
        transition = model1.find_transition(operon, (alg, free))
        self.assertEqual((2,), transition.states)
    
        transition = model2.find_transition(operon, (free,))
        self.assertEqual((1, 2), transition.states)


    def test_mucus_operon_v3(self):
        model1, model2 = parse_smbionet_output_file('resources/mucusOperonV3.out')
        graph = InfluenceGraph()
        graph.add_variable('operon', 0, 2)
        graph.add_variable('mucuB', 0, 1)
        graph.add_process('free', '(not(mucuB>=1))', 'operon')
        graph.add_process('alg', '(operon>=1)', 'operon')
        graph.add_process('prod', '(operon>=1)', 'mucuB')

        expected_model1 = DiscreteModel(graph)
        expected_model1.add_transition('operon', (), (0,))
        expected_model1.add_transition('operon', ('alg',), (2,))
        expected_model1.add_transition('operon', ('free',), (0,))
        expected_model1.add_transition('operon', ('alg', 'free'), (2,))
        expected_model1.add_transition('mucuB', (), (0,))
        expected_model1.add_transition('mucuB', ('prod',), (1,))

        expected_model2 = DiscreteModel(graph)
        expected_model2.add_transition('operon', (), (0,))
        expected_model2.add_transition('operon', ('alg',), (2,))
        expected_model2.add_transition('operon', ('free',), (1, 2))
        expected_model2.add_transition('operon' , ('alg', 'free'), (2,))
        expected_model2.add_transition('mucuB', (), (0,))
        expected_model2.add_transition('mucuB', ('prod',), (1,))

        self.assertEqual(expected_model1, model1)
        self.assertEqual(expected_model2, model2)


if __name__ == '__main__':
    unittest.main()
