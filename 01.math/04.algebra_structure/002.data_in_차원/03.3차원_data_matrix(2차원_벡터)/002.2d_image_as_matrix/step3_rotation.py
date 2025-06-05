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

# rotate_image
def rotate_image(matrix, angle_degrees):
    if not matrix or not matrix[0]: return []
    rows, cols = len(matrix), len(matrix[0])
    rads = math.radians(angle_degrees)
    cos_theta, sin_theta = math.cos(rads), math.sin(rads)
    center_x, center_y = cols / 2 - 0.5, rows / 2 - 0.5 # 픽셀 중심을 (0,0)이 아닌 (0.5,0.5)로 고려
    
    rotated_matrix = create_empty_matrix(rows, cols, 0)

    for r_new in range(rows):
        for c_new in range(cols):
            # 결과 픽셀의 중심을 이미지 중심으로 이동
            x_temp = c_new - center_x
            y_temp = r_new - center_y
            
            # 역회전 적용하여 원본 좌표 계산
            c_orig = (x_temp * cos_theta + y_temp * sin_theta) + center_x
            r_orig = (-x_temp * sin_theta + y_temp * cos_theta) + center_y
            
            # Nearest Neighbor Interpolation
            r_o_int, c_o_int = int(round(r_orig)), int(round(c_orig))
            
            if 0 <= r_o_int < rows and 0 <= c_o_int < cols:
                rotated_matrix[r_new][c_new] = matrix[r_o_int][c_o_int]
    return rotated_matrix

# --- Main Execution ---
# 0. (선택사항) 테스트용 10x10 이미지 직접 생성 (PNG 파일이 없을 경우)
def create_test_pattern_matrix(size=10):
    matrix = create_empty_matrix(size, size)
    for r in range(size):
        for c in range(size):
            if (r + c) % 2 == 0 : # 간단한 패턴
                 matrix[r][c] = 200 # 밝은 회색
            if r == c or r == size - 1 - c: # 대각선
                matrix[r][c] = 50 # 어두운 회색
            if r == 0 or c == 0 or r == size-1 or c == size -1: # 테두리
                matrix[r][c] = 100
    # 중앙에 더 밝은 사각형
    center_start = size // 2 - 1
    center_end = size // 2 + 1
    for r in range(center_start, center_end +1):
        for c in range(center_start, center_end+1):
            if 0 <= r < size and 0 <= c < size:
                matrix[r][c] = 250
    return matrix

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

# 2. 회전
rotated_matrix_45 = rotate_image(original_matrix, 0) # 원본 
print_matrix(rotated_matrix_45, "original  Matrix")
visualize_matrix(rotated_matrix_45, "Rotated 0 deg")

rotated_matrix_45 = rotate_image(original_matrix, 45) # 45도 회전
print_matrix(rotated_matrix_45, "Rotated 45 deg Matrix")
visualize_matrix(rotated_matrix_45, "Rotated 45 deg")

rotated_matrix_90 = rotate_image(original_matrix, 90) # 90도 회전
print_matrix(rotated_matrix_90, "Rotated 90 deg Matrix")
visualize_matrix(rotated_matrix_90, "Rotated 90 deg")

