from PIL import Image

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

# 추출된 matrix 시각화 (간단한 텍스트 기반)
print("Original Image Matrix (10x10):")
for row in image_matrix:
    # 숫자를 간격 맞춰 출력 (예: 3자리 정수)
    print(' '.join(f"{val:3}" for val in row))