class BigInteger:
    def __init__(self, input=None):
        match input:
            case _ if isinstance(input, str):
                # print("String")
                string_val = input
            case _ if isinstance(input, int):
                string_val = str(input)
                # print("Integer")
            case _ if isinstance(input, list):
                string_val = ''.join(map(str, input))
                # print("List")
            case _:
                string_val = "0"
                print("Unknown type")
        self._array = []
        self._import(string_val)
        self.sign = True
        self._sign_init(string_val)

    def get(self):
        if self.sign:
            return self._array
        else:
            self._array.insert(0, "-")
            return self._array
    def _import(self, String="0"):
        self._array = [char for char in String]
        return self._array
    def _sign_init(self,String):
        if String[0] == "-":
            self.sign = False
            self._array = [int(char) for char in String[1:]]
            # print("Your number is negetive")
        else:
            self.sign = True
            self._array = [int(char) for char in String]
            # print("Your number is positive")
    def _sign_process(self,sign1,sign2,other):
        # + / +
        if sign1 and sign2:
            return self.add_process(other)
        # + / -
        elif sign1 and not sign2:
            return self.sub_process(other)
        # - / -
        elif (not sign1) and (not sign2):
            obj = self.add_process(other)
            obj.sign = False
            return obj
        # - / +
        if (not sign1) and (sign2):
            return other.sub_process(self)


    def add(self,other):
        return self._sign_process(self.sign,other.sign, other)
    def subtract(self,other):
        return self._sign_process(self.sign, not other.sign, other)

    def add_process(self, other):
        self._array_rev = list(reversed(self._array))
        other._array_rev = list(reversed(other._array))


        if len(self._array_rev) < len(other._array_rev):
            larger_rev, smaller_rev = other._array_rev, self._array_rev
        else:
            larger_rev, smaller_rev = self._array_rev, other._array_rev

        carry = 0
        result = []

        for i in range(len(larger_rev)):
            # Add corresponding digits along with carry
            total = larger_rev[i] + (smaller_rev[i] if i < len(smaller_rev) else 0) + carry
            result.append(total % 10)
            carry = total // 10

        if carry:
            result.append(carry)

        result.reverse()
        temp_obj = BigInteger(result)
        return temp_obj

    def sub_process(self, other):
        self._array_rev = list(reversed(self._array))
        other._array_rev = list(reversed(other._array))


        # Check if we need to swap `self` and `other` to get a positive result
        if len(self._array_rev) < len(other._array_rev) or (
                len(self._array_rev) == len(other._array_rev) and self._array_rev < other._array_rev
        ):
            larger_rev, smaller_rev = other._array_rev, self._array_rev
            negative_result = True
        else:
            larger_rev, smaller_rev = self._array_rev, other._array_rev
            negative_result = False

        result = []
        borrow = 0

        for i in range(len(larger_rev)):
            # Subtract with borrowing if needed
            digit_self = larger_rev[i]
            digit_other = smaller_rev[i] if i < len(smaller_rev) else 0
            total = digit_self - digit_other - borrow

            if total < 0:
                total += 10
                borrow = 1
            else:
                borrow = 0

            result.append(total)


        # Remove leading zeros in the result
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        if negative_result:
            result.append('-')
        result.reverse()
        temp_obj = BigInteger(result)
        return temp_obj

    def multiply(self, other):
        self._array_rev = list(reversed(self._array))
        other._array_rev = list(reversed(other._array))

        result = [0] * (len(self._array_rev) + len(other._array_rev))

        for i in range(len(self._array_rev)):
            for j in range(len(other._array_rev)):
                result[i + j] += self._array_rev[i] * other._array_rev[j]
                result[i + j + 1] += result[i + j] // 10
                result[i + j] %= 10

        while len(result) > 1 and result[-1] == 0:
            result.pop()

        result.reverse()

        temp_obj = BigInteger(result)

        if self.sign != other.sign:
            temp_obj.sign = False

        return temp_obj

    def karatsuba_multiply(self, other):
        # Convert arrays to numbers for easier calculation
        def list_to_number(lst):
            return int(''.join(map(str, lst)))

        def number_to_list(num):
            return [int(digit) for digit in str(num)]

        # Base case for recursion
        if len(self._array) == 1 or len(other._array) == 1:
            return self.multiply(other)

        n = max(len(self._array), len(other._array))
        m = n // 2

        # Split the numbers
        high1 = list_to_number(self._array[:-m]) if len(self._array) > m else 0
        low1 = list_to_number(self._array[-m:])
        high2 = list_to_number(other._array[:-m]) if len(other._array) > m else 0
        low2 = list_to_number(other._array[-m:])

        # Create BigInteger objects for high and low parts
        high1_big = BigInteger(high1)
        low1_big = BigInteger(low1)
        high2_big = BigInteger(high2)
        low2_big = BigInteger(low2)

        # Recursive Karatsuba calls
        z0 = low1_big.karatsuba_multiply(low2_big)  # low1 * low2
        z2 = high1_big.karatsuba_multiply(high2_big)  # high1 * high2
        z1 = (low1_big.add(high1_big)).karatsuba_multiply(low2_big.add(high2_big))  # (low1 + high1) * (low2 + high2)
        z1 = z1.subtract(z0).subtract(z2)  # Subtract z0 and z2 from z1

        # Combine results: z2 * 10^(2*m) + z1 * 10^m + z0
        result = z2.left_shift(2 * m).add(z1.left_shift(m)).add(z0)

        # Adjust the sign of the result
        result.sign = (self.sign == other.sign)

        return result

    def left_shift(self, n):
        if self._array == [0]:  # if number is zero, no shift changes anything
            return self

        self._array.extend([0] * n)
        self._array_rev = list(reversed(self._array))
        return self

    def left_shift(self, n):
        if self._array == [0]:
            return self
        self._array.extend([0] * n)
        self._array_rev = list(reversed(self._array))
        return self

    def right_shift(self, n):
        if len(self._array) > n:
            self._array = self._array[:-n]
        else:
            self._array = [0]  # Set to zero if we shift more than the number of digits
        self._array_rev = list(reversed(self._array))
        return self

obj1 = BigInteger(400)
obj2 = BigInteger("200")
obj3 = obj1.karatsuba_multiply(obj2)
# obj4 = obj1.subtract(obj2)
#
print(obj3.get())
# print(obj4.get())


