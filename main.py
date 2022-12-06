import time
from math import ceil
from random import seed, randint
from typing import Set, Tuple

seed(10)


class BitNumberException(Exception):
    def __init__(self, text):
        self.text = text


class BitNumber:

    def __init__(self, binary_number: str):
        self.__int_number = int(0)

        for bit in binary_number:
            self.__int_number = (self.__int_number << 1)
            if bit == '1':
                self.__int_number |= 1
            elif bit == '0':
                continue
            else:
                raise BitNumberException('BitNumber format error')

        self.__len = len(binary_number)

    def swap(self, i: int, j: int) -> None:
        # TODO: i != j
        self.__int_number ^= (1 << i | 1 << j)

    def cut_off(self, m: int) -> None:
        self.__int_number = (self.__int_number >> m + 1) << m + 1

    def i_concatenate(self, i: int) -> None:
        self.__int_number = ((self.__int_number >> (len(self) - i)) << i) | \
               (self.__int_number & ((1 << i) - 1))

    def center_cut(self, i: int) -> None:
        self.__int_number = (self.__int_number >> i) & ((1 << (len(self) - (i * 2))) - 1)

    def bits_xor(self) -> int:
        buff = self.__int_number
        while (bl := buff.bit_length()) != 1 and buff != 0:
            bl //= 2
            t = buff & ((1 << bl) - 1)
            buff = t ^ (buff >> bl)

        return buff

    def rounded_move_left(self, i: int) -> None:
        self.rounded_move_right(self.__len - i)

    def rounded_move_right(self, i: int) -> None:
        self.__int_number = ((self.__int_number & ((1 << i) - 1)) << (self.__len - i)) | \
               (self.__int_number >> i)

    def __iter__(self):
        self.__buff_bit_number = self.__int_number
        self.__bit_count = len(bin(self.__buff_bit_number)[2:])
        return self.__next__()

    def __next__(self) -> int:
        while self.__bit_count:
            self.__bit_count -= 1
            number = self.__buff_bit_number & 1
            self.__buff_bit_number = self.__buff_bit_number >> 1
            yield number
        return

    def __getitem__(self, k: int) -> int:
        return (self.__int_number >> k) & 1

    def __setitem__(self, position: int, value: int) -> None:
        self.__int_number ^= ((self[position]^value & 1) << position)

    def __rshift__(self, k: int) -> None:
        self.__int_number >>= k

    def __rmod__(self, value):
        return value % self.__int_number

    def __len__(self) -> int:
        return len(bin(self.__int_number)) - 2

    def __repr__(self) -> str:
        return bin(self.__int_number)

    def __str__(self) -> str:
        return bin(self.__int_number)


def prime_divisors(number: int) -> set[tuple[int, int]]:
    divisors_pair = set()
    divisors = set()

    sq_split = int(number ** 0.5) + 1

    for test_divisor in range(1, sq_split):
        if test_divisor not in divisors and number % test_divisor == 0:
            if ferma(test_divisor):
                divisors.add(test_divisor)
                divisors.add(number // test_divisor)
                divisors_pair.add((test_divisor, number // test_divisor))

    return divisors_pair


def ferma(number: int) -> bool:
    if number % 2 == 0:
        return False

    for iteration in range(100):
        a = randint(2, int((number ** 0.5)) + 1)
        if gcd(a, number) != 1:
            return False
        if mod_pow(a, BitNumber(bin(number - 1)[2:]), number) != 1:
            return False

    return True


def solovei(number: int, k: int = 5) -> bool:
    if number % 2 == 0:
        return False

    for test_number_index in range(k):
        random_witness = randint(2, number - 1)

        if gcd(number, random_witness) != 1:
            return False

        if mod_pow(random_witness, BitNumber(bin(int((number-1)/2))[2:]), number) \
                != (ceil(random_witness/number) % number):
            return False

    return True


def gcd(a: int, b: int):
    if b == 0:
        return a
    return gcd(b, a % b)


def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x


def mod_pow(number: int, degree: BitNumber, module: int = 1) -> int:
    c = 1
    for bit in degree:
        if bit:
            c = (c * number) % module
        number = (number ** 2) % module

    return c


class RSA:
    def __init__(self, p: int = 0, q: int = 0, gen_range: int = 10000):

        if not p or not q:
            self.p = self.gen_primary(gen_range)

            while True:
                tmp = self.gen_primary(gen_range)
                if self.p != tmp:
                    self.q = tmp
                    break
        else:
            self.p = p
            self.q = q

        self.n = self.q * self.p
        self.__phi = (self.q - 1) * (self.p - 1)

        self.e = self.e_gen()
        self.d = self.d_gen()

    def e_gen(self) -> int:
        while True:
            self.e = randint(1, self.__phi)
            if gcd(self.e, self.__phi) == 1:
                break
        return self.e

    def d_gen(self) -> int:
        g, x, y = gcd_extended(self.e, self.__phi)
        if g != 1:
            raise Exception('Error')
        return x % self.__phi

    @staticmethod
    def gen_primary(numbers_range: int) -> int:

        primary_numbers_bit_compression = BitNumber("0")  # (n-1)/2 => 2,3,...,n = primes

        for number in range(3, numbers_range, 2):
            if not primary_numbers_bit_compression[round((number - 1) / 2)]:
                for test_number in range(number ** 2 - 2, numbers_range, 2):
                    if (not (primary_numbers_bit_compression[round((test_number - 1) / 2)])) \
                            and test_number % number == 0:
                        primary_numbers_bit_compression[round((test_number - 1) / 2)] = 1

        numbers = [index*2 + 1 for index, bit in enumerate(primary_numbers_bit_compression) if bit == 0]

        return numbers[randint(0, len(numbers))]


def main():
    # bit = BitNumber('0')
    #
    # print(bin(bit.set_bit(3)))
    # print(bin(bit.get_bit(1)))
    # print(bin(bit.rounded_move_right(5)))

    # rsa = RSA(gen_range=10000)
    #
    # # start = time.time()
    # # rsa.gen_primary(100000)
    # # end = time.time()
    # # print(end-start)
    #
    # print(f'e = {rsa.e}\nn = {rsa.n}\nd = {rsa.d}\nn = {rsa.n}\np = {rsa.p}\nq = {rsa.q}')
    # #
    # candidates = prime_divisors(rsa.n)
    # #
    # print(candidates)
    # #
    # for candidate in candidates:
    #     if candidate[0] == 1 or candidate[1] == 1:
    #         continue
    #
    #     test_rsa = RSA(candidate[0], candidate[1])
    #     test_rsa.e = rsa.e
    #     test_rsa.d = test_rsa.d_gen()
    #
    #     if rsa.e == test_rsa.e:
    #         print(f'FIND: \nd={test_rsa.d}, n={test_rsa.n}')

    print(ferma(67902031))
    print(solovei(67902031))

    # print(mod_pow(2396638, BitNumber(bin(int((2424713-1)/2))[2:]), 2424713))

    # print(gcd(7, 7))


if __name__ == '__main__':
    main()
