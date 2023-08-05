import unittest
import lifelib

class TestOtherRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        lifelib.load_rules('b36s23', 'g3b3s23', 'r7b65t95s65t114', 'g11b3s23', force_compile=True)

    def setUp(self):

        self.sess = lifelib.load_rules('b36s23', 'g3b3s23', 'r7b65t95s65t114', 'g11b3s23')

    def test_multistate_apgcode(self):

        lt = self.sess.lifetree(memory=1000, n_layers=8)
        apgcode = 'xp32_ss2gzw11_wsfm76cg_x86668_wke2024_ws6i1_x1'
        rro = lt.pattern(apgcode, 'g11b3s23')
        self.assertEqual(rro.apgcode, apgcode)

        rrorle = lt.pattern('''x = 8, y = 7, rule = 23/3/11
4.B$2.2AEC$.2A3ED$ABCHJHE$.2AB.2HF$2.AJ2.G$7.J!''', 'g11b3s23')

        self.assertEqual(rrorle.apgcode, apgcode)

    def test_highlife(self):

        lt = self.sess.lifetree(memory=1000, n_layers=1)
        rep = lt.pattern('3o$o2bo$o3bo$bo2bo$2b3o!', 'b36s23')
        self.assertEqual(rep[12 * (2 ** 40 - 1)].population, 12 * (2 ** 40))
        self.assertEqual(rep[12 * (2 ** 40)].population, 24)

    def test_generations(self):

        lt = self.sess.lifetree(memory=1000, n_layers=2)
        p54soup = lt.pattern('''oobbooobooobooob$
bobbboooobooobbo$
bbbbobobbooobobo$
oboboboooobooboo$
obbbobbboobooobo$
bobobbboobbboobb$
ooooooobobooboob$
bboooboooobobboo$
boooobobbooobbbb$
bbbobbobobboboob$
oooboboobooboooo$
boobobbooobooobb$
obobbobbobbbbbbo$
oobbbbbbbbbooobo$
bbbboboobbooboob$
bbbbooobobobbboo!''', 'g3b3s23')
        self.assertEqual(p54soup.oscar(verbose=False)['period'], 54)

        x = p54soup.population
        self.assertEqual(p54soup[30, 7], 0)
        p54soup[30, 7] = 2
        self.assertEqual(p54soup[30, 7], 2)
        self.assertEqual(p54soup.population, x + 1)

        try:
            import numpy as np
        except ImportError:
            return

        coords = np.array([[0, 1], [2, 3], [4, 5], [-6, 69], [73, -48]], dtype=np.int64)
        values = np.array([1, 0, 2, 1, 2], dtype=np.int64)

        p54soup[coords] = values
        values2 = p54soup[coords]

        print(values)
        print(values2)

        self.assertEqual(np.all(values == values2), True)

    def test_largerthanlife(self):

        lt = self.sess.lifetree(memory=1000, n_layers=1)
        rrosoup = lt.pattern('''booobbbboobboooo$
bbooobooobobbobo$
bboobboobooobboo$
oobobobobbbooboo$
booooobboboooobo$
booboboboobooooo$
obboooobbbbbobbo$
oooooooobobboobb$
obbbbbobbbbboobb$
bobobboooooobobb$
bbbbobbbbooobboo$
bobobbbobbobboob$
obbobbbboobbobbb$
bobobbooooooooob$
oobobboooboobboo$
bboboobbobbbbobb!''', 'r7b65t95s65t114')
        self.assertEqual(rrosoup.oscar(verbose=False)['period'], 552)

if __name__ == '__main__':
    unittest.main()
