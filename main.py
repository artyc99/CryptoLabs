from random import seed, randint
from typing import Set, Tuple

seed(10)

class Bit:

    def __init__(self, binary_number: str):
        self.__binary_number = binary_number
        self.__int_number = int(0)

        for bit in self.__binary_number:
            self.__int_number = (self.__int_number << 1)
            if bit == '1':
                self.__int_number |= 1

    def get_bit(self, k: int):
        return (self.__int_number >> k) & 1

    def set_bit(self, k: int):
        return self.__int_number ^ (1 << k)

    def swap(self, i: int, j: int):
        # TODO: i != j
        return self.__int_number ^ (1 << i | 1 << j)

    def cut_off(self, m: int):
        return (self.__int_number >> m + 1) << m + 1

    def i_concatinate(self, i: int):
        return ((self.__int_number >> (len(self) - i)) << i) | \
               (self.__int_number & ((1 << i) - 1))

    def center_cut(self, i: int):
        return (self.__int_number >> i) & ((1 << (len(self) - (i * 2))) - 1)

    def bits_xor(self):
        buff = self.__int_number
        while (bl := buff.bit_length()) != 1 and buff != 0:
            bl //= 2
            t = buff & ((1 << bl) - 1)
            buff = t ^ (buff >> bl)

        return buff

    def rounded_move_left(self, i: int):
        # Тоже самое что сдвиг вправо просто проще а коэф сдвига = длинна минус сдвиг вправо
        return self.rounded_move_right(len(self) - i)
        # return (((self.__int_number & ((1 << (len(self) - i)) - 1)) << i) |
        #         ((self.__int_number & (((1 << i) - 1) << (len(self) - i))) >> (len(self) - i)))

    def rounded_move_right(self, i: int):
        return ((self.__int_number & ((1 << i) - 1)) << (len(self) - i)) | \
               (self.__int_number >> i)

    def __len__(self):
        return len(bin(self.__int_number)) - 2

    def __repr__(self):
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

    if number == 2:
        return True

    for iteration in range(100):
        a = randint(2, int((number ** 0.5)) + 1)
        if gcd(a, number) != 1:
            return False
        if ((a ** (number - 1)) % number) != 1:
            return False

    return True


def gcd(a: int, b: int):
    if b == 0:
        return a
    return gcd(b, a % b)

# long long mul(long long a, long long b, long long m){
# 	if(b==1)
# 		return a;
# 	if(b%2==0){
# 		long long t = mul(a, b/2, m);
# 		return (2 * t) % m;
# 	}
# 	return (mul(a, b-1, m) + a) % m;
# }
#
# long long pows(long long a, long long b, long long m){
# 	if(b==0)
# 		return 1;
# 	if(b%2==0){
# 		long long t = pows(a, b/2, m);
# 		return mul(t , t, m) % m;
# 	}
# 	return ( mul(pows(a, b-1, m) , a, m)) % m;
# }


class RSA:
    def __init__(self, p: int, q: int):
        self.__p = p
        self.__q = q
        self.n = self.__q * self.__p
        self.__n_cut = (self.__q - 1) * (self.__p - 1)

        self.d = 0

    def d_gen(self, start: int, end: int) -> None:
        while True:
            new_d = randint(start, end)
            if gcd(new_d, self.__n_cut) == 1:
                self.d = new_d
                break


def main():
    # bit = Bit('11011111')
    #
    # print(bit)
    # # print(bin(bit.get_bit(1)))
    # print(bin(bit.rounded_move_right(5)))

    rsa = RSA(51893, 39679)
    rsa.d_gen(2, 100000)

    print(f'd = {rsa.d}\nn = {rsa.n}')

    candidates = prime_divisors(rsa.n)

    print(candidates)

    for candidate in candidates:
        new_rsa = RSA(candidate[0], candidate[1])
        new_rsa.d_gen(2, 100000)
        print(f'find d = {new_rsa.d}')
        if rsa.d == new_rsa.d:
            print(f'find d = {new_rsa.d}')
            break

    print(gcd(7, 7))


if __name__ == '__main__':
    main()
