from typing import List, Tuple

from main import BitNumber

start_permutation = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
                     62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
                     57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
                     61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

end_permutation = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
                   38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
                   36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
                   34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

r_box = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

checker_bits = [8, 16, 24, 32, 40, 48, 56, 64]

compression_key_swap = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
                        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

shift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

p_box = [14, 17, 11, 24, 1, 5, 3, 28,
         15, 6, 21, 10, 23, 19, 12, 4,
         26, 8, 16, 7, 27, 20, 13, 2,
         41, 52, 31, 37, 47, 55, 30, 40,
         51, 45, 33, 48, 44, 49, 39, 56,
         34, 53, 46, 42, 50, 36, 29, 32]

p_box_excluding = [32, 1, 2, 3, 4, 5,
                   4, 5, 6, 7, 8, 9,
                   8, 9, 10, 11, 12, 13,
                   12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21,
                   20, 21, 22, 23, 24, 25,
                   24, 25, 26, 27, 28, 29,
                   28, 29, 30, 31, 32, 1]

p_box_existing = [16, 7, 20, 21, 29, 12, 28, 17,
                  1, 15, 23, 26, 5, 18, 31, 10,
                  2, 8, 24, 14, 32, 27, 3, 9,
                  19, 13, 30, 6, 22, 11, 4, 25]

s_box = [
    [
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
    ],
    [
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
    ],
    [
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
    ],
    [
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
    ],
    [
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
    ],
    [
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
    ],
    [
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
    ],
    [
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
    ],
]


class DES:

    def __init__(self, key: str):
        self.key = BitNumber('')
        for symbol in bytes(key, 'utf-8'):
            self.key = self.key + BitNumber(bin(symbol)[2:])

        self.__round_keys = [key for key in self.__gen_round_key()]

    def encrypt(self, block):
        block = self.__permutation(block, start_permutation)

        LB = block[:32]
        RB = block[32:]

        for key in self.__round_keys:
            RB, LB = LB, (LB ^ self.__des_fun(RB, key))

        RB, LB = LB, RB

        block = self.__permutation(LB + RB, end_permutation)

        return block

    def decrypt(self, block):
        block = self.__permutation(block, start_permutation)

        for key in self.__round_keys[::-1]:
            LB = block[:32]
            RB = block[32:]

            RB, LB = LB, (RB ^ self.__des_fun(LB, key))

        RB, LB = LB, RB

        block = self.__permutation(LB + RB, end_permutation)

        return block

    def __des_fun(self, half_block: BitNumber, round_key: BitNumber):
        excluded_block = self.__permutation(half_block, p_box_excluding)

        excluded_block = excluded_block ^ round_key

        b_keys = [excluded_block[6 * index: 6 * (index + 1)] for index in range(7)]

        b_block = BitNumber('')

        for b_key in b_keys:
            m = BitNumber(bin(b_key[0])[2:]) + BitNumber(bin(b_key[5])[2:])
            l = b_key[1:5]

            b_block = b_block + BitNumber(bin(s_box[0][int(m) * 15 + int(l)])[2:])

        return self.__permutation(b_block, p_box_existing)

    def __gen_round_key(self):
        permutated_key = self.__permutation(self.key, compression_key_swap)

        for round in range(16):
            C0 = permutated_key[28:]
            D0 = permutated_key[:28]

            C0.rounded_move_left(shift[round])
            D0.rounded_move_left(shift[round])

            permutated_key = C0 + D0

            yield self.__permutation(permutated_key, p_box)

        return

    @staticmethod
    def __permutation(block: BitNumber, bit_map: List[int]) -> BitNumber:
        buff = BitNumber('')

        if len(block) != len(bit_map):
            assert 'Error'

        for index, bit_map_place in enumerate(bit_map):
            buff[index] = block[(bit_map_place - 1)]
        return buff

    @staticmethod
    def block_split(block: List[int]) -> Tuple[List[int], List[int]]:
        return block[:32], block[32:]


if __name__ == '__main__':
    des = DES(b'AABB0910'.decode('utf-8'))

    block = '123456ABCD'

    bin_block = BitNumber('')

    for symbol in bytes(block, 'utf-8'):
        bin_block = bin_block + BitNumber(bin(int(symbol))[2:])

    enc_block = des.encrypt(bin_block)

    print(bin_block)
    print(enc_block)
    print(des.decrypt(enc_block))
