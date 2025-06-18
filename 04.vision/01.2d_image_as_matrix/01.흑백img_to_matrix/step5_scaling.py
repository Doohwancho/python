from PIL import Image
import math
import matplotlib.pyplot as plt # 시각화용 라이브러리

# --- Helper Functions ---
def create_empty_matrix(rows, cols, default_value=0):
    return [[default_value for _ in range(cols)] for _ in range(rows)]

def print_matrix(matrix, label="Matrix"):
    print(f"\n{label}:")
    if not matrix or not matrix[0]:
        print("Empty or invalid matrix.")
        return
    for row in matrix:
        print(' '.join(f"{val:5.0f}" if isinstance(val, float) else f"{val:3}" for val in row))

def visualize_matrix(matrix, title="Image"):
    if not matrix or not matrix[0]:
        print(f"Cannot visualize empty matrix for {title}")
        return
    plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
    plt.title(title)
    plt.colorbar()
    # Ensure integer ticks if matrix is small
    if matrix and matrix[0] and len(matrix[0]) <= 20 and len(matrix) <=20 :
        plt.xticks(range(len(matrix[0])))
        plt.yticks(range(len(matrix)))
    plt.show()


# scale_image
def scale_image(matrix, scale_x, scale_y):
    if not matrix or not matrix[0]: return []
    original_rows, original_cols = len(matrix), len(matrix[0])
    new_rows, new_cols = int(original_rows * scale_y), int(original_cols * scale_x)
    if new_rows == 0 or new_cols == 0: return [[]]
    
    scaled_matrix = create_empty_matrix(new_rows, new_cols)
    for r_new in range(new_rows):
        for c_new in range(new_cols):
            r_orig = r_new / scale_y
            c_orig = c_new / scale_x
            r_o_int = min(int(r_orig), original_rows - 1)
            c_o_int = min(int(c_orig), original_cols - 1)
            scaled_matrix[r_new][c_new] = matrix[r_o_int][c_o_int]
    return scaled_matrix


def load_image_to_matrix():
    # 1. 이미지 로드 (예: '10x10_black.png')
    try:
        img = Image.open('pepe_10_pixel.png').convert('L') # 'L'은 그레이스케일로 변환
    except FileNotFoundError:
        print("Error: Image file not found. Make sure 'your_10x10_image.png' exists.")
        exit()

    # 2. 이미지 크기 확인
    width, height = img.size
    if width != 10 or height != 10:
        print(f"Warning: Image size is {width}x{height}, not 10x10.")

    # 3. 픽셀 데이터를 matrix (리스트의 리스트)로 추출
    image_matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel_value = img.getpixel((x, y))
            # 검은색은 0, 흰색은 255. 필요시 0~1 사이로 정규화 가능
            row.append(pixel_value)
        image_matrix.append(row)

    return image_matrix

# 1. 이미지 로드 또는 테스트 매트릭스 생성
# image_file = 'your_10x10_image.png' # 실제 10x10 이미지 파일 경로
original_matrix = load_image_to_matrix()
# original_matrix = create_test_pattern_matrix(10) # PNG 대신 테스트 패턴 사용

# print_matrix(original_matrix, "Original 10x10 Matrix")
# visualize_matrix(original_matrix, "Original Image")

# 4. 스케일링
# 10x10은 너무 작아서 스케일링 결과가 잘 안보일 수 있음.
scaled_up_matrix = scale_image(original_matrix, 1.0, 1.0) # original 
print_matrix(scaled_up_matrix, "original Matrix")
visualize_matrix(scaled_up_matrix, "original")

scaled_up_matrix = scale_image(original_matrix, 1.5, 1.5) # 1.5배 확대 (결과: 15x15)
print_matrix(scaled_up_matrix, "Scaled Up 1.5x Matrix")
visualize_matrix(scaled_up_matrix, "Scaled Up 1.5x (Nearest Neighbor)")

scaled_down_matrix = scale_image(original_matrix, 0.7, 0.7) # 0.7배 축소 (결과: 7x7)
print_matrix(scaled_down_matrix, "Scaled Down 0.7x Matrix")
visualize_matrix(scaled_down_matrix, "Scaled Down 0.7x (Nearest Neighbor)")
