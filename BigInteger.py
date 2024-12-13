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
        z0 = low1_big.karatsuba_multiply(low2_big)  # low1 * low2 (b * d)
        z2 = high1_big.karatsuba_multiply(high2_big)  # high1 * high2 (a * c)

        # (low1 + high1) * (low2 + high2) | (a + b) (c + d)
        z1 = (low1_big.add(high1_big)).karatsuba_multiply(low2_big.add(high2_big))

        z1 = z1.subtract(z0).subtract(z2)  # Subtract z0 and z2 from z1

        # Combine results: z2 * 10^(2*m) + z1 * 10^m + z0
        result = z2.left_shift(2 * m).add(z1.left_shift(m)).add(z0)

        # Adjust the sign of the result
        result.sign = (self.sign == other.sign)

        return result

    def divide(self, other):
        # Handle sign of the result
        result_sign = self.sign == other.sign

        dividend = self._array[:]  # Copy of the dividend(Maghsoom)
        divisor = other._array[:]  # Copy of the divisor(Maghsoom alayh)

        result = []
        remainder = []

        for digit in dividend:
            remainder.append(digit)  # Append the current digit to the remainder
            # Remove leading zeros in the remainder
            while len(remainder) > 1 and remainder[0] == 0:
                remainder.pop(0)

            remainder_value = int(''.join(map(str, remainder)))
            divisor_value = int(''.join(map(str, divisor)))

            # Determine how many times the divisor fits into the remainder
            quotient_digit = remainder_value // divisor_value
            result.append(quotient_digit)

            # Update the remainder
            remainder_value -= quotient_digit * divisor_value
            remainder = list(map(int, str(remainder_value)))

        result.reverse()
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        result.reverse()

        # Convert result to BigInteger
        result_obj = BigInteger(result)
        result_obj.sign = result_sign

        return result_obj

    def factorial(cls,n):
        temp = BigInteger(1)
        for i in range(1,n+1):
            temp = temp.karatsuba_multiply(BigInteger(i))
        return temp


    def pow(self,number):

        temp = BigInteger(1)
        base = self

        while number > 0:
            if number % 2 == 1:
                temp = temp.multiply(base)
            base = base.multiply(base)
            number //= 2
        return temp
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





obj1 = BigInteger("3")
obj2 = BigInteger("4")

result_add = obj1.add(obj2)
print("Addition Result:", result_add.get())

result_sub = obj1.subtract(obj2)
print("Subtraction Result:", result_sub.get())

result_mul = obj1.multiply(obj2)
print("Multiplication Result:", result_mul.get())

result_karatsuba = obj1.karatsuba_multiply(obj2)
print("Karatsuba Multiplication Result:", result_karatsuba.get())

result_div = obj2.divide(obj1)
print("Division Result:", result_div.get())

result_pow = obj1.pow(5)
print("Power Result (obj1^3):", result_pow.get())

result_fact = BigInteger.factorial(BigInteger,5)
print("Factorial Result (5!):", result_fact.get())





