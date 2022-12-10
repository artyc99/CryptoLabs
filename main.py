from math import ceil
from random import seed, randint, getrandbits

seed(10)


class BitNumberException(Exception):
    def __init__(self, text):
        self.text = text


class RabinException(Exception):
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

    @staticmethod
    def rand(bit_count: int = 256, odd: bool = True) -> int:
        number = getrandbits(bit_count - 1)

        if odd:
            number = (number << 1) | 1
        else:
            number = (number << 1) | getrandbits(1)

        return number

    def __add__(self, other):
        self.__len += len(other)
        return self.__class__(bin(self.__int_number << len(other) | int(other))[2:])

    def __int__(self):
        return self.__int_number

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

    def __getitem__(self, k: int):
        if isinstance(k, slice):
            return self.__class__(bin(self.__int_number)[2:][k.start:k.stop:k.step])
        else:
            return (self.__int_number >> k) & 1

    def __setitem__(self, position: int, value: int) -> None:
        if self.__len < position:
            self.__len = position + 1
        self.__int_number ^= ((self[position] ^ value & 1) << position)

    def __rshift__(self, k: int) -> None:
        self.__int_number >>= k

    def __rmod__(self, value):
        return value % self.__int_number

    def __len__(self) -> int:
        return self.__len

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


def ferma(number: int, k: int = 100) -> bool:
    if number % 2 == 0:
        return False
    if number == 3:
        return True

    random_witness_set = set()

    for iteration in range(k):
        random_witness = get_random_int(2, number - 1, random_witness_set)

        random_witness_set.add(random_witness)

        if mod_pow(random_witness, BitNumber(bin(number - 1)[2:]), number) != 1:
            return False

    return True


def solovei(number: int, k: int = 100) -> bool:
    if number % 2 == 0:
        return False
    if number == 3:
        return True

    random_witness_set = set()

    for test_number_index in range(k):
        random_witness = get_random_int(2, number - 1, random_witness_set)

        random_witness_set.add(random_witness)

        if mod_pow(random_witness, BitNumber(bin(int((number - 1) / 2))[2:]), number) \
                != jacobi(random_witness, number):
            return False

    return True


def rabin(number: int, k: int = 100):
    if number % 2 == 0:
        return False
    if number == 3:
        return True

    s, d = divider_search(number)
    random_witness_set = set()

    if s == 0 and d == 0:
        raise RabinException('Cannot find S and D')

    for test_number_index in range(k):
        random_witness = get_random_int(2, number - 1, random_witness_set)

        random_witness_set.add(random_witness)

        for s_index in range(s):
            test = mod_pow(random_witness, BitNumber(bin(2 ** s_index * d)[2:]), number)

            if test != 1 and test != number - 1:
                return False

    return True


def get_random_int(start: int, end: int, exclude: set) -> int:
    while True:
        number = randint(start, end)
        if number not in exclude and number % 2 != 0:
            return number


def jacobi(a: int, n: int) -> int:
    j = 1
    while a != 0:
        while a % 2 == 0:
            j *= pow(-1, (n * n - 1) / 8)
            a /= 2
        if not ((a - 3) % 4 or (n - 3) % 4):
            j = -j
        a, n = n, a
        a %= n
    return j


def divider_search(number: int):
    two_pow_divider = 2
    pow = 1
    div = 1
    mod = 0

    while two_pow_divider < number:
        mod = (number - 1) % two_pow_divider
        div = (number - 1) // two_pow_divider
        if mod == 0 and div & 1 == 1:
            return pow, div
        two_pow_divider <<= 1
        pow += 1

    return 0, 0


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
        number = (number * number) % module

    return c


class RSA:
    def __init__(self, p: int = 0, q: int = 0, gen_range: int = 10000):

        if not p or not q:
            self.p = self.gen_primary_resheto(gen_range)

            while True:
                tmp = self.gen_primary_resheto(gen_range)
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
    def gen_primary_resheto(numbers_range: int) -> int:

        primary_numbers_bit_compression = BitNumber("0")  # (n-1)/2 => 2,3,...,n = primes

        for number in range(3, numbers_range, 2):
            if not primary_numbers_bit_compression[round((number - 1) / 2)]:
                for test_number in range(number ** 2 - 2, numbers_range, 2):
                    if (not (primary_numbers_bit_compression[round((test_number - 1) / 2)])) \
                            and test_number % number == 0:
                        primary_numbers_bit_compression[round((test_number - 1) / 2)] = 1

        numbers = [index * 2 + 1 for index, bit in enumerate(primary_numbers_bit_compression) if bit == 0]

        return numbers[randint(0, len(numbers))]


def main():
    # bit = BitNumber('0')
    #
    # print(bin(bit.set_bit(3)))
    # print(bin(bit.get_bit(1)))
    # print(bin(bit.rounded_move_right(5)))

    rsa = RSA(gen_range=10000)

    # start = time.time()
    # rsa.gen_primary(100000)
    # end = time.time()
    # print(end-start)

    # print(f'e = {rsa.e}\nn = {rsa.n}\nd = {rsa.d}\nn = {rsa.n}\np = {rsa.p}\nq = {rsa.q}')
    #
    # text = 'ABC'
    #
    # print(f'Text: {text}')
    #
    # numbers = [byte for byte in bytes(text, 'utf-8')]
    #
    # print(numbers)
    #
    # encoded = [mod_pow(number, BitNumber(bin(rsa.e)[2:]), rsa.n) for number in numbers]
    #
    # print(encoded)
    #
    # decoded = [mod_pow(encod, BitNumber(bin(rsa.d)[2:]), rsa.n) for encod in encoded]
    #
    # print(decoded)

    d = BitNumber('1010')
    a = BitNumber('1010')
    c = d + a
    print(c)

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

    # print(solovei(BitNumber.rand(bit_count=16), k=100))
    # print(ferma(561, k=100))
    # print(solovei(561, k=100))
    # print(rabin(561, k=20))

    # count = 2

    # while count:
    #     random_int = BitNumber.rand(bit_count=8)
    #     print(random_int)
    #     test = rabin(random_int, k=50)
    #     if test:
    #         print(solovei(random_int, k=50))
    #         print(rabin(random_int, k=50))
    #         print(ferma(random_int, k=50))
    #         print(random_int, '\n\n')
    #         count -= 1

    # print(mod_pow(2396638, BitNumber(bin(int((2424713-1)/2))[2:]), 2424713))

    # print(gcd(7, 7))


if __name__ == '__main__':
    main()
