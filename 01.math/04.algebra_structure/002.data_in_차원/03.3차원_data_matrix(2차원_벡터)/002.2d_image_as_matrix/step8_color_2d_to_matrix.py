from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np # NumPy를 사용하면 채널 결합 등이 편리합니다.

# 기존 print_matrix 함수는 그대로 사용 가능 (채널별 행렬 출력 시)
def print_matrix(matrix, label="Matrix"):
    print(f"\n{label}:")
    if not matrix or not matrix[0]:
        print("Empty or invalid matrix.")
        return
    max_val_len = 0
    is_float = False
    for r in matrix:
        for val_tuple in r: # val_tuple could be (R,G,B) or a single value
            if isinstance(val_tuple, tuple): # For list of list of tuples
                for val in val_tuple:
                    max_val_len = max(max_val_len, len(str(int(val))))
                    if isinstance(val, float): is_float = True
            else: # For list of list of numbers (single channel)
                max_val_len = max(max_val_len, len(str(int(val_tuple))))
                if isinstance(val_tuple, float): is_float = True

    format_str = f"{{:{max_val_len+1}.0f}}" if is_float else f"{{:{max_val_len+1}}}"

    for row_idx, row_data in enumerate(matrix):
        # Check if it's a matrix of tuples (RGB) or numbers (single channel)
        if row_data and isinstance(row_data[0], tuple): # RGB matrix
            # This printing can be very verbose for RGB.
            # Consider printing R, G, B matrices separately if needed for debugging.
            # For now, let's just indicate it's an RGB row.
            print(f"Row {row_idx}: {row_data[:3]}...") # Print first few pixels of the row
        else: # Single channel matrix
            print(' '.join(format_str.format(val) for val in row_data))


def load_color_image_to_rgb_matrices(image_path='pepe_10_pixel.png'):
    """컬러 이미지를 로드하여 R, G, B 채널별 2D 행렬(리스트의 리스트)로 분리하여 반환합니다."""
    try:
        img = Image.open(image_path).convert('RGB') # 'RGB'로 변환
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        # 대체용 10x10 컬러 이미지 생성 (예: 빨간색)
        print("Creating a default 10x10 red image matrix.")
        rows, cols = 10, 10
        matrix_r = [[255 for _ in range(cols)] for _ in range(rows)]
        matrix_g = [[0 for _ in range(cols)] for _ in range(rows)]
        matrix_b = [[0 for _ in range(cols)] for _ in range(rows)]
        return matrix_r, matrix_g, matrix_b, width, height

    width, height = img.size
    # if width != 10 or height != 10: # 필요시 크기 경고
    #     print(f"Warning: Image size is {width}x{height}, not 10x10.")

    matrix_r = [[0 for _ in range(width)] for _ in range(height)]
    matrix_g = [[0 for _ in range(width)] for _ in range(height)]
    matrix_b = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            matrix_r[y][x] = r
            matrix_g[y][x] = g
            matrix_b[y][x] = b

    return matrix_r, matrix_g, matrix_b, width, height

def visualize_color_matrices(matrix_r, matrix_g, matrix_b, title="Color Image"):
    """R, G, B 행렬들을 합쳐 컬러 이미지로 시각화합니다."""
    if not matrix_r or not matrix_g or not matrix_b:
        print(f"Cannot visualize empty matrices for {title}")
        return

    height = len(matrix_r)
    width = len(matrix_r[0])

    # Matplotlib의 imshow는 (height, width, 3) 형태의 배열을 기대합니다.
    # 또는 (리스트의 리스트의 [R,G,B] 튜플/리스트) 형태
    # NumPy를 사용하면 변환이 더 쉽지만, 순수 Python 리스트로도 가능합니다.

    # 순수 Python 리스트로 M x N x 3 구조 만들기
    combined_image_data = []
    for y in range(height):
        row_pixels = []
        for x in range(width):
            # 값들이 0-255 범위 내에 있도록 보장 (정수형)
            r = max(0, min(255, int(round(matrix_r[y][x]))))
            g = max(0, min(255, int(round(matrix_g[y][x]))))
            b = max(0, min(255, int(round(matrix_b[y][x]))))
            row_pixels.append([r, g, b])
        combined_image_data.append(row_pixels)

    # NumPy를 사용한다면:
    # combined_array = np.stack([
    #     np.array(matrix_r, dtype=np.uint8),
    #     np.array(matrix_g, dtype=np.uint8),
    #     np.array(matrix_b, dtype=np.uint8)
    # ], axis=-1) # (height, width, 3)
    # plt.imshow(combined_array)


    # Matplotlib는 0-1 범위의 float 또는 0-255 범위의 uint8을 선호합니다.
    # 위에서 int로 변환했으므로, imshow가 적절히 처리합니다.
    # 만약 float 값이라면 0-1로 정규화하거나, imshow가 처리할 수 있도록 uint8로 변환해야 합니다.
    # 여기서는 이미 0-255 범위의 정수라고 가정합니다.
    plt.imshow(combined_image_data)
    plt.title(title)
    # 컬러 이미지에는 컬러바가 큰 의미 없을 수 있으나, 필요시 추가
    # plt.colorbar()
    if width <= 20 and height <= 20 :
        plt.xticks(range(width))
        plt.yticks(range(height))
    plt.show()

# --- 컬러 이미지 행렬 연산 예제 ---

def scale_channel(channel_matrix, scale_factor):
    """단일 색상 채널 행렬의 모든 값에 스칼라를 곱합니다 (밝기 조절)."""
    if not channel_matrix: return []
    height = len(channel_matrix)
    width = len(channel_matrix[0])
    scaled_channel = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            scaled_value = channel_matrix[y][x] * scale_factor
            # 결과값을 0-255 범위로 클램핑
            scaled_channel[y][x] = max(0, min(255, int(round(scaled_value))))
    return scaled_channel

def swap_rb_channels(r_matrix, g_matrix, b_matrix):
    """R 채널과 B 채널을 서로 바꿉니다."""
    # 실제로는 행렬 자체가 바뀌는 것이 아니라, 새로운 행렬 세트를 반환합니다.
    # R 값들이 새 B 행렬로, B 값들이 새 R 행렬로 갑니다. G는 그대로.
    return b_matrix, g_matrix, r_matrix # 매우 간단한 예시!

def color_to_grayscale_matrix(r_matrix, g_matrix, b_matrix):
    """R, G, B 채널을 사용하여 흑백(grayscale) 행렬을 생성합니다."""
    if not r_matrix or not g_matrix or not b_matrix: return []
    height = len(r_matrix)
    width = len(r_matrix[0])
    grayscale_matrix = [[0 for _ in range(width)] for _ in range(height)]

    # 표준 가중치: Y = 0.299R + 0.587G + 0.114B
    for y in range(height):
        for x in range(width):
            gray_value = (0.299 * r_matrix[y][x] +
                          0.587 * g_matrix[y][x] +
                          0.114 * b_matrix[y][x])
            grayscale_matrix[y][x] = max(0, min(255, int(round(gray_value))))
    return grayscale_matrix

# --- 메인 실행 부분 ---

# 1. 컬러 이미지 로드
# 실제 10x10 컬러 이미지 파일 경로로 변경하세요 (예: 'pepe_10_pixel_color.png')
# 파일이 없다면, load_color_image_to_rgb_matrices 함수 내에서 기본 빨간색 이미지가 생성됩니다.
file_path = 'pepe_10_pixel.png'
try:
    r_orig, g_orig, b_orig, width, height = load_color_image_to_rgb_matrices(file_path)
except FileNotFoundError: # 함수 내부에서 FileNotFoundError 처리하므로 실제로는 여기 도달 안 함
    print(f"{file_path}을(를) 찾을 수 없어 프로그램을 종료합니다.")
    exit()


print_matrix(r_orig, f"Original Red Channel ({width}x{height})")
# print_matrix(g_orig, "Original Green Channel") # 필요시 출력
# print_matrix(b_orig, "Original Blue Channel") # 필요시 출력
visualize_color_matrices(r_orig, g_orig, b_orig, "Original Color Image")


# 2. 예제 연산: Red 채널 밝기 1.5배 증가
r_scaled = scale_channel(r_orig, 1.5)
g_scaled = g_orig # Green 채널은 그대로
b_scaled = b_orig # Blue 채널은 그대로
visualize_color_matrices(r_scaled, g_scaled, b_scaled, "Red Channel Scaled x1.5")


# 3. 예제 연산: R 채널과 B 채널 교환
r_swapped, g_swapped, b_swapped = swap_rb_channels(r_orig, g_orig, b_orig)
visualize_color_matrices(r_swapped, g_swapped, b_swapped, "Red & Blue Channels Swapped")


# 4. 예제 연산: 컬러를 흑백으로 변환
grayscale_from_color = color_to_grayscale_matrix(r_orig, g_orig, b_orig)
# 흑백 이미지는 기존 visualize_matrix 함수(cmap='gray' 사용)로 보는 것이 더 적절할 수 있습니다.
# 여기서는 RGB 모든 채널에 같은 흑백 값을 넣어 컬러 시각화 함수로 보겠습니다.
visualize_color_matrices(grayscale_from_color,
                         grayscale_from_color,
                         grayscale_from_color,
                         "Grayscale from Color (viewed as RGB)")

# 만약 흑백 전용 시각화 함수를 사용한다면:
# (이전에 제공된 visualize_matrix 함수를 사용)
def visualize_grayscale_matrix(matrix, title="Grayscale Image"):
    if not matrix or not matrix[0]:
        print(f"Cannot visualize empty matrix for {title}")
        return
    plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
    plt.title(title)
    plt.colorbar()
    height = len(matrix)
    width = len(matrix[0])
    if width <= 20 and height <= 20 :
        plt.xticks(range(width))
        plt.yticks(range(height))
    plt.show()

print_matrix(grayscale_from_color, "Grayscale Matrix calculated from Color")
visualize_grayscale_matrix(grayscale_from_color, "Grayscale from Color (Grayscale View)")

print("\n--- 컬러 이미지 처리 예제 완료 ---")