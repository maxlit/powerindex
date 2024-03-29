import unittest
from powerindex import *
from math import exp as e, sin, sqrt
# python -m unittest discover project_directory '*_test.py'
# poetry run python -m unittest powerindex/testpowerindex.py 

class TestPowerIndex(unittest.TestCase):
    #cf=cf1+cf2
    def setUp(self):
        self.game=Game(6, [4, 3, 2])# http://www.ctl.ua.edu/math103/power/sspi_example.htm   result (S-S: 4/6,1/6,1/6
        self.ElectoralCollegeGame=Game(270,
                                       [54,33,32,25,23,22,21
                                        ,18,15,14,13,13,12,12]+
                                        [11]*4+[10]*2+[9]*2+[8]*6+[7]*3+[6]*2+[5]*4+[4]*6+[3]*8
                                        )

    def test__coeffs_of_general_GF_Banzhaf(self):
        game=Game(6, [1,3])
        coeffs=game._coeffs_of_general_GF("Banzhaf")
        correct_coeffs=[1,1,0,1,1]
        self.assertEqual(coeffs,correct_coeffs)
        
    def test__coeffs_of_general_GF_Shapley_Shubik(self):
        game=Game(2, [1,1])
        coeffs=game._coeffs_of_general_GF("ShapleyShubik")
        self.assertEqual(coeffs[0],[1,0,0])
        self.assertEqual(coeffs[1],[0,2])
        self.assertEqual(coeffs[2],[0,0])
        
    def test__coeffs_of_player_GF_Banzhaf(self):
        game=Game(6, [1,3])
        coeffs=[1,-3,2,-3,1]
        c=game._coeffs_of_player_GF(coeffs,2,"Banzhaf")
        correct_c=[1,-3,1,0]
        self.assertEqual(c,correct_c)
        
    def test__coeffs_of_player_GF_Shapley_Shubik(self):
        game=Game(2,[1,1])
        coeffs=game._coeffs_of_general_GF("ShapleyShubik")
        c=game._coeffs_of_player_GF(coeffs,1,"ShapleyShubik")
        #correct_c=[1,-3,1,0]
        self.assertEqual(c[0][0],1)
        self.assertEqual(c[1][1],1)
        self.assertEqual(c[1][0],0)
        self.assertEqual(c[0][1],0)

    def test_calc_banzhaf(self):
        # example from Game Theory and Strategy by Phillip D. Straffin:
        correct_banzhaf=[5/12.0,0.25,0.25,1/12.0]
        game=Game(6, [4, 3, 2, 1])
        game.calc_banzhaf()
        self.assertAlmostEqual(correct_banzhaf,game.banzhaf)

        # EEC 1958-1972
        # Germany, France, Italy, BeNiLux
        game=Game(6, [4, 4, 4, 2, 2, 1])
        game.calc_banzhaf()
        correct_banzhaf=[5/21.0,5/21.0,5/21.0,3/21.0,3/21.0,0]
        game.calc_banzhaf()
        self.assertAlmostEqual(correct_banzhaf,game.banzhaf)
        
    def test_calc_shapley_shubik(self):
        #game=Game(2,[1,1])
        #game.calc_shapley_shubik()
        # example from http://en.wikipedia.org/wiki/Shapley%E2%80%93Shubik_power_index
        game=Game(4,[3,2,1,1])
        game.calc_shapley_shubik()
        correct_dist=[0.5,1/6.0,1/6.0,1/6.0]
        for i in range(len(correct_dist)):
            self.assertAlmostEqual(game.shapley_shubik[i],correct_dist[i])

    def test_calc_contested_garment(self):
        # example from https://en.wikipedia.org/wiki/Contested_garment_rule
        correct_dist = {1: [100/3., 100/3., 100/3.],
                        2: [50, 75, 75],
                        3: [50, 100, 150],
                        4: [50, 125, 225],
                        5: [100/3.0 * 2, 100/3.*2 + 100, 100/3.0*2 + 200]
                        }
        claims = [100, 200, 300]
        for r in range(1, 6):
            q = r * 100
            game=Game(q, claims, absolute=True)
            game.calc_contested_garment()
            for i in range(len(correct_dist[r])):
                self.assertAlmostEqual(game.contested_garment[i],correct_dist[r][i])

    def test_calc_contested_garment_permutation(self):
        # example from https://en.wikipedia.org/wiki/Contested_garment_rule
        claims = [100, 200, 300]
        claims_ = [200, 100, 300]
        for r in range(2, 5):
            q = r * 100
            game = Game(q, claims, absolute=True)
            game.calc_contested_garment()
            game_ = Game(q, claims_, absolute=True)
            game_.calc_contested_garment()
            self.assertNotEqual(game.contested_garment[0], game_.contested_garment[0]) # this element was permutated
            self.assertAlmostEqual(game.contested_garment[2], game_.contested_garment[2]) # this element wasn't permuted
                
def main():
    unittest.main()

if __name__=='__main__':
    main()
