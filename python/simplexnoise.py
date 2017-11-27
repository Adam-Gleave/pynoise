import math


# Simplex noise creation class
class SimplexNoise:
    # Permutation table
    # Use this to hash a number to a random integer between 0 and 255.
    # Numbers in this array are a randomly organised set
    __PERMUTATIONS = [
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
        n = n % 0xFF

        return self.__PERMUTATIONS[n]

    # Skewing factors to translate co-ordinates into simplex space
    __FACTOR2D_A = 0.5 * (math.sqrt(3.0) - 1.0)
    __FACTOR2D_B = (3.0 - math.sqrt(3.0)) / 6.0

    """
    --------------------------- Vector functions ------------------------------
    
    Interpolating gradient values requires obtaining the dot (scalar) product.
    This is usually a slow process, but since the gradient vectors we are
    dealing only contains 0, 1, or -1, we can replace these functions with our
    own.
    
    ---------------------------------------------------------------------------    
    """

    # Return the dot product of two 2D vectors
    def __dot2d(self, vector, x, y):
        return vector[0] * x + vector[1] * y

    """ 
    --------------------- Gradient functions and tables -----------------------
    
    In order to compute the noise value of a point, we must find the value of 
    an interpolation function between pseudorandom gradient values of all 
    neighbouring grid vertices. These are not fully random, or patterns would 
    not be repeatable given identical input.
    
    These helper functions provide the means of determining these gradients 
    given aspecific grid-point co-ordinate, and the gradient of the function at
    a given distance from this grid-point (the noise lookup value).
    
    ---------------------------------------------------------------------------
    """

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

    # 3D gradient table
    # Use this to obtain a gradient from a given index value generated in a
    # pseudorandom manner from 3D co-ordinates
    __GRADS3D = [
        (1, 1, 0), (-1, 1, 0), (1, - 1, 0), (-1, -1, 0),
        (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
        (0, 1, 1), (0, - 1, 1), (0, 1, -1), (0, -1, -1)
    ]

    """
    ----------------------------- Noise functions -----------------------------
    
    These public functions allow the user of the SimplexNoise class to look up
    a value retrieved from the noise function at any given co-ordinate.
    
    ---------------------------------------------------------------------------
    """

    # 1D simplex noise
    def get_value_1D(self, x):
        # Get "corners" of co-ordinate (nearest integers)
        c0 = math.floor(x)
        c1 = c0 + 1

        # Get distances from co-ordinate to corners
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

    # 2D simplex noise
    def get_value_2D(self, x, y):
        cont0, cont1, cont2 = 0.0, 0.0, 0.0

        # Skew the input space to translate to simplex cell space
        # Hairy factor for 2D
        simplex = (x + y) * self.__FACTOR2D_A
        i = math.floor(x + simplex)
        j = math.floor(y + simplex)

        k = (i + j) * self.__FACTOR2D_B

        # Un-skew cell origin to standard space
        origin_x = i - k
        origin_y = j - k

        # Get distances from origin to co-ordinate
        x0 = x - origin_x
        y0 = y - origin_y

        # Determine which simplex the co-ordinate lies within
        # In 2D space, the simplex is an equilateral triangle
        # There are two (skewed) simplices in each 2D cell

        # Obtain offsets for middle (second) corner in skewed (simplex) sapce
        if x0 > y0:
            i1 = 1
            j1 = 0
        else:
            i1 = 0
            j1 = 1

        # Obtain offsets for middle (second) corner in standard space
        x1 = x0 - i1 + self.__FACTOR2D_B
        y1 = y0 - i1 + self.__FACTOR2D_B
        # Obtain offsets for last corner in standard space
        x2 = x0 - 1.0 + 2.0 * self.__FACTOR2D_B
        y2 = y0 - 1.0 + 2.0 * self.__FACTOR2D_B

        # Obtain an index into the gradient array at each simplex corner
        # Wrap at 8 so as to not go out of bounds
        ii = i & 255
        jj = j & 255
        grad0 = self.__hash(ii + self.__hash(jj)) % 12
        grad1 = self.__hash(ii + i1 + self.__hash(jj + j1)) % 12
        grad2 = self.__hash(ii + 1 + self.__hash(jj + 1)) % 12

        # Calculate corner contributions
        temp0 = 0.5 - x0 * x0 - y0 * y0

        if temp0 < 0:
            cont0 = 0
        else:
            temp0 = temp0 * temp0
            gv = self.__GRADS3D[grad0]
            cont0 = temp0 * temp0 * self.__dot2d(gv, x0, y0)

        temp1 = 0.5 - x1 * x1 - y1 * y1

        if temp1 < 0:
            cont1 = 0.0
        else:
            temp1 = temp1 * temp1
            gv = self.__GRADS3D[grad1]
            cont1 = temp1 * temp1 * self.__dot2d(gv, x1, y1)

        temp2 = 0.5 - x2 * x2 - y2 * y2

        if temp2 < 0:
            cont2 = 0.0
        else:
            temp2 = temp2 * temp2
            gv = self.__GRADS3D[grad2]
            cont2 = temp2 * temp2 * self.__dot2d(gv, x2, y2)

        # Return the sum of all contributions, scaled to fit within [-1, 1]
        return 70 * (cont0 + cont1 + cont2)