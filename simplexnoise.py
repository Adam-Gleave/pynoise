import math


# Simplex noise creation class
class SimplexNoise:
    # Permutation table

    # Use this to hash a number to a random integer between 0 and 255.
    # Numbers in this array are a randomly organised set
    __permutations = [
        216, 117, 91, 54, 101, 12, 189, 9, 211, 14, 73, 94, 24, 89, 231, 63,
        58, 5, 41, 124, 68, 204, 82, 210, 195, 202, 142, 109, 72, 32, 165, 11,
        60, 214, 2, 74, 193, 118, 217, 213, 92, 105, 158, 227, 20, 138, 70,
        113, 241, 244, 86, 203, 76, 128, 154, 229, 110, 181, 21, 137, 35, 168,
        174, 65, 239, 31, 8, 160, 95, 120, 219, 156, 192, 220, 57, 207, 38,
        75, 77, 39, 159, 25, 246, 235, 240, 221, 133, 85, 3, 106, 43, 200, 17,
        228, 232, 248, 42, 163, 141, 50, 209, 27, 152, 34, 253, 230, 36, 126,
        22, 186, 129, 116, 13, 7, 236, 171, 224, 103, 67, 164, 18, 98, 100,
        135, 108, 97, 81, 234, 212, 222, 4, 150, 166, 84, 1, 251, 206, 201,
        49, 61, 180, 96, 170, 6, 226, 161, 173, 225, 140, 190, 208, 119, 198,
        78, 245, 71, 199, 172, 250, 93, 87, 153, 134, 10, 254, 162, 238, 188,
        79, 15, 194, 196, 46, 62, 115, 182, 184, 66, 52, 104, 37, 205, 45, 16,
        218, 243, 197, 29, 23, 111, 144, 59, 223, 176, 136, 185, 127, 132, 83,
        255, 114, 88, 187, 191, 125, 122, 90, 107, 139, 51, 47, 145, 143, 53,
        99, 123, 28, 233, 215, 56, 130, 157, 131, 148, 80, 64, 55, 249, 48,
        177, 33, 252, 242, 179, 44, 237, 19, 112, 146, 102, 149, 178, 26, 151,
        30, 147, 167, 175, 121, 155, 69, 0, 183, 40, 169, 247
    ]

    # Helper function
    # Hash a number using permutations table
    def __hash(self, n):
        n = n % 255

        return self.__permutations[n]

    # Helper function
    # Compute gradient vector from a 1D coordinate
    def __grad(self, n, x):
        # Obtain lower 4 bits of hash
        h = int(n) & 0x0F
        # Gradient value between 1.0 and 8.0
        grad = 1 + (h & 7)

        # Set a random sign to gradient
        if (h & 8) != 0:
            grad = 0 - grad

        # Multiply gradient with distance from corner
        return grad * x

    # Entrance function
    # 1D simplex noise
    def get_value(self, x):
        # Get "corners" of coordinate (nearest integers)
        c0 = math.floor(x)
        c1 = c0 + 1

        # Get distances from coordinate to corners
        x0 = x - c0
        x1 = x0 - 1

        # Calculate corner contributions
        temp0 = 1 - (x0 * x0)
        temp0 = temp0 * temp0
        cont0 = temp0 * temp0 * self.__grad(self.__hash(c0), x0)

        temp1 = 1 - (x1 * x1)
        temp1 = temp1 * temp1
        cont1 = temp1 * temp1 * self.__grad(self.__hash(c1), x1)

        # Max value +/- 2.53125
        # Scale to within [-1, +1]
        return 0.395 * (cont0 + cont1)
