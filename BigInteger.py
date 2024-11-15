class BigInteger:
    def __init__(self, String = "0"):
        self._array = []
        self._import(String)
        self.sign = True
        self._sign_process(String)
    def get(self):
        return self._array
    def _import(self, String="0"):
        self._array = [char for char in String]
        return self._array
    def _sign_process(self,String):
        if String[0] == "-":
            self.sign = False
            self._array = [int(char) for char in String[1:]]
            # print("Your number is negetive")
        else:
            self.sign = True
            self._array = [int(char) for char in String]
            # print("Your number is positive")


    def add(self, other):
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


        temp_obj = BigInteger()
        temp_obj._array = result
        result.reverse()
        temp_obj._array_rev = result
        return temp_obj

    def subtract(self, other):
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

        temp_obj = BigInteger()
        temp_obj._array = result
        result.reverse()
        temp_obj._array_rev = result
        return temp_obj

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


obj1 = BigInteger("-100")
# obj2 = BigInteger("200")
# obj3 = obj1.add(obj2)
# obj4 = obj1.subtract(obj2)
#
# print(obj3.get())
# print(obj4.get())


