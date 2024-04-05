import numpy as np
from collections import Counter
import heapq
import cv2


def ordered_dither(gray_image: np.ndarray, level: int = 4):
    def get_bayer_matrix(n: int):
        if n == 1:
            return np.array([[0]])
        else:
            m_n = get_bayer_matrix(n // 2)
            first = (n ** 2) * m_n
            second = (n ** 2) * m_n + 2
            third = (n ** 2) * m_n + 3
            fourth = (n ** 2) * m_n + 1
            first_col = np.concatenate((first, third), axis=0)
            second_col = np.concatenate((second, fourth), axis=0)
            return (1 / n ** 2) * np.concatenate((first_col, second_col), axis=1)

    n = 2 ** level
    dithered = gray_image.copy()
    bayer_matrix = get_bayer_matrix(n) * 256
    for x in range(dithered.shape[0]):
        i = x % n
        for y in range(dithered.shape[1]):
            j = y % n
            if dithered[x][y] > bayer_matrix[i][j]:
                dithered[x][y] = 255
            else:
                dithered[x][y] = 0

    return np.require(dithered, np.uint8, 'C'), dithered.shape[0], dithered.shape[1]


def huffman_encode(gray_image: np.ndarray):
    values = gray_image.flatten()
    pixel_count = Counter(values)
    p = np.array(list(pixel_count.values())) / len(values)
    entropy = -np.sum(p * np.log2(p))

    heap = [[weight, [symbol, '']] for symbol, weight in pixel_count.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lowest1 = heapq.heappop(heap)
        lowest2 = heapq.heappop(heap)
        for sym_code_pair in lowest1[1:]:
            sym_code_pair[1] = '0' + sym_code_pair[1]
        for sym_code_pair in lowest2[1:]:
            sym_code_pair[1] = '1' + sym_code_pair[1]
        heapq.heappush(heap, [lowest1[0] + lowest2[0]] + lowest1[1:] + lowest2[1:])
    tree = heapq.heappop(heap)
    huffman_tree = sorted(tree[1:], key=lambda pair: (len(pair[-1]), pair[0]))
    average_code_length = sum(len(code) * pixel_count[symbol] for symbol, code in huffman_tree) / tree[0]

    return entropy, average_code_length


def blur(image: np.ndarray):
    k = 4
    # blurred_image = np.zeros_like(image)
    # for i in range(k, image.shape[0] - k):
    #     for j in range(k, image.shape[1] - k):
    #         blurred_image[i, j] = np.average(image[i - k:i + k, j - k:j + k])

    blurred_image = cv2.GaussianBlur(image, (9, 9), 0)

    return blurred_image, blurred_image.shape[0], blurred_image.shape[1]
