from simplexnoise import SimplexNoise
import unittest


class SimplexNoiseTest(unittest.TestCase):
    def setUp(self):
        self.noise = SimplexNoise()

    def tearDown(self):
        self.noise = None

    # Test values against expected range
    def test_correct_range(self):
        for i in range(1, 10000):
            with self.subTest(i=i):
                float_i = i / 100
                result = self.noise.get_value(float_i)
                self.assertTrue(-1.0 <= result <= 1.0, "Noise value at" + str(float_i) +
                                " is not between -1.0 and 1.0.")


if __name__ == '__main__':
    unittest.main()
