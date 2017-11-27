from simplexnoise import SimplexNoise
import unittest


class SimplexNoiseTest(unittest.TestCase):
    def setUp(self):
        self.noise = SimplexNoise()
        test = self.noise.get_value_2D(1.3, 5.3)
        print(test)

    def tearDown(self):
        self.noise = None

    # Test values against expected range
    def test_correct_range_1D(self):
        for i in range(1, 1000):
            with self.subTest(i=i):
                float_i = i / 100
                result = self.noise.get_value_1D(float_i)
                self.assertTrue(-1.0 <= result <= 1.0, "Noise value at" + str(float_i) +
                                " is not between -1.0 and 1.0.")

    # Test values against expected range (2D)
    def test_correct_range_2D(self):
        for x in range(1, 100):
            for y in range(1, 100):
                i = (x * 100) + y
                with self.subTest(i=i):
                    float_x = x / 100
                    float_y = y / 100
                    result = self.noise.get_value_2D(float_x, float_y)
                    print(str(result))
                    self.assertTrue(-1.0 <= result <= 1.0, "Noise value at" +
                                    str(float_x) + "," + str(float_y) +
                                    " is not between -1.0 and 1.0.")


if __name__ == '__main__':
    unittest.main()
