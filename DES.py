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


class DES:

    def __init__(self, key: str):
        self.key = BitNumber('')
        for symbol in bytes(key, 'utf-8'):
            self.key = self.key + BitNumber(bin(symbol)[2:])

        self.__round_keys = [rk for rk in self.__gen_round_key()]

    def

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


test = [int(number) for number in '0000000000000010000000000000000000000000000000000000000000000001']

if __name__ == '__main__':
    print(DES('rrrrrrrr'))
