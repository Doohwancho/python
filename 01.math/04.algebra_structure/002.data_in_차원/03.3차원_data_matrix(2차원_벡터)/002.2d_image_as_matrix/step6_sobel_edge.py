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

# convolve
def convolve(matrix, kernel):
    if not matrix or not matrix[0] or not kernel or not kernel[0]: return []
    img_rows, img_cols = len(matrix), len(matrix[0])
    kernel_rows, kernel_cols = len(kernel), len(kernel[0])
    
    # 'valid' 컨볼루션
    output_rows = img_rows - kernel_rows + 1
    output_cols = img_cols - kernel_cols + 1
    if output_rows <= 0 or output_cols <= 0: return []
        
    output_matrix = create_empty_matrix(output_rows, output_cols)
    for r_out in range(output_rows):
        for c_out in range(output_cols):
            current_sum = 0
            for kr in range(kernel_rows):
                for kc in range(kernel_cols):
                    current_sum += matrix[r_out + kr][c_out + kc] * kernel[kr][kc]
            # 클리핑 (0-255) - 컨볼루션 결과는 음수나 255 초과 가능
            output_matrix[r_out][c_out] = min(max(int(current_sum), 0), 255)
    return output_matrix

# kernels
sobel_x_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobel_y_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
laplacian_kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
prewitt_x_kernel = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
prewitt_y_kernel = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]


# apply_sobel
def apply_sobel_or_prewitt(matrix, kernel_x, kernel_y):
    gx = convolve(matrix, kernel_x)
    gy = convolve(matrix, kernel_y)
    if not gx or not gy or len(gx) != len(gy) or (gx and gx[0] and gy and gy[0] and len(gx[0]) != len(gy[0])):
        print("Error in Gx/Gy convolution results.")
        return []
    
    rows, cols = len(gx), len(gx[0])
    magnitude_matrix = create_empty_matrix(rows, cols)
    for r in range(rows):
        for c in range(cols):
            magnitude = math.sqrt(gx[r][c]**2 + gy[r][c]**2)
            magnitude_matrix[r][c] = min(max(int(magnitude), 0), 255)
    return magnitude_matrix
# --- END OF COPIED FUNCTIONS ---


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

print_matrix(original_matrix, "Original 10x10 Matrix")
visualize_matrix(original_matrix, "Original Image")

# 5. 외곽선 감지
# Sobel (결과 이미지 크기가 커널 크기만큼 줄어듦. 10x10에 3x3 커널이면 8x8 결과)
sobel_edges_matrix = apply_sobel_or_prewitt(original_matrix, sobel_x_kernel, sobel_y_kernel)
if sobel_edges_matrix:
    print_matrix(sobel_edges_matrix, "Sobel Edges Matrix")
    visualize_matrix(sobel_edges_matrix, "Sobel Edges")
else:
    print("Sobel edge detection failed (e.g., image too small for kernel).")

