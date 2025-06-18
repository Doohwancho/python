from PIL import Image
import matplotlib.pyplot as plt
import numpy as np # 시각화 시 틱 설정 등에 편리

# --- 이미지 로드 및 시각화 함수 ---

def load_image_as_grayscale_matrix(image_path='pepe_10_pixel.png'):
    """이미지를 로드하여 흑백(Grayscale) 2D 행렬(리스트의 리스트)로 변환하여 반환합니다."""
    try:
        # 이미지를 열고 'L' 모드(Grayscale)로 변환
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print(f"Error: 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        print("기본 10x10 흑백 패턴 이미지를 생성합니다.")
        width, height = 10, 10
        # 간단한 대각선 패턴 생성
        matrix = [[0 for _ in range(width)] for _ in range(height)]
        for r_idx in range(height):
            for c_idx in range(width):
                if r_idx < height // 2:
                    matrix[r_idx][c_idx] = 50  # 상단은 어둡게
                else:
                    matrix[r_idx][c_idx] = 200 # 하단은 밝게
                if r_idx == c_idx : # 대각선은 더 밝거나 어둡게
                    matrix[r_idx][c_idx] = 120 if r_idx < height // 2 else 250
        return matrix, width, height

    width, height = img.size
    # if width != 10 or height != 10: # 필요시 크기 경고
    #     print(f"Warning: Image size is {width}x{height}, not 10x10.")

    grayscale_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y_idx in range(height):
        for x_idx in range(width):
            grayscale_matrix[y_idx][x_idx] = img.getpixel((x_idx, y_idx))
            
    return grayscale_matrix, width, height

def visualize_grayscale_matrix(matrix, title="Image", ax=None, width=10, height=10):
    """단일 흑백(Grayscale) 행렬을 시각화합니다."""
    if ax is None:
        fig, ax_new = plt.subplots()
        ax_new.imshow(matrix, cmap='gray', vmin=0, vmax=255)
        ax_new.set_title(title)
        if width <= 20 and height <= 20: # 작은 이미지용 틱
            ax_new.set_xticks(np.arange(0, width, 1))
            ax_new.set_yticks(np.arange(0, height, 1))
            ax_new.grid(which="major", color="lightgray", linestyle='-', linewidth=0.5)
        plt.show()
    else:
        ax.imshow(matrix, cmap='gray', vmin=0, vmax=255)
        ax.set_title(title)
        if width <= 20 and height <= 20:
            ax.set_xticks(np.arange(0, width, 1))
            ax.set_yticks(np.arange(0, height, 1))
            ax.grid(which="major", color="lightgray", linestyle='-', linewidth=0.5)

# --- 이진화 함수 ---

def binarize_image_fixed_threshold(image_matrix, threshold_value, height, width, max_val=255):
    """주어진 임계값을 사용하여 흑백 이미지를 이진화합니다."""
    binarized_matrix = [[0 for _ in range(width)] for _ in range(height)]
    
    print(f"\n이진화 적용 중... 임계값: {threshold_value}")
    print("픽셀 값 | > 임계값? | 결과 값")
    print("---------------------------------")

    for r_idx in range(height):
        for c_idx in range(width):
            pixel_val = image_matrix[r_idx][c_idx]
            is_above_threshold = pixel_val > threshold_value
            
            if is_above_threshold:
                binarized_matrix[r_idx][c_idx] = max_val
            else:
                binarized_matrix[r_idx][c_idx] = 0
            
            # 처음 몇 개 픽셀에 대해서만 상세 정보 출력 (콘솔이 너무 길어지는 것을 방지)
            if r_idx < 2 and c_idx < 3: # 예: 처음 2행, 3열까지만 상세 출력
                 print(f"{pixel_val:7d} | {str(is_above_threshold):10s} | {binarized_matrix[r_idx][c_idx]:7d}")
            elif r_idx == 2 and c_idx == 0:
                 print("... (이후 픽셀들은 유사하게 처리됨) ...")

    return binarized_matrix

# --- 메인 실행 ---
if __name__ == "__main__":
    # 1. 흑백 이미지 로드
    # 실제 10x10 이미지 파일명으로 변경하세요. (예: 'pepe_10_pixel.png')
    # 파일이 없으면 load_image_as_grayscale_matrix 함수 내에서 기본 이미지를 생성합니다.
    image_filename = 'pepe_10_pixel.png' 
    grayscale_img_matrix, img_height, img_width = load_image_as_grayscale_matrix(image_filename)

    # 2. 이진화를 위한 임계값 설정
    # 이 값은 이미지에 따라 조절해야 합니다.
    # 간단하게 이미지 픽셀 값들의 평균을 임계값으로 사용해볼 수 있습니다.
    if grayscale_img_matrix: # 이미지가 성공적으로 로드되었거나 생성되었는지 확인
        all_pixels = [pixel for row in grayscale_img_matrix for pixel in row]
        if all_pixels: # 픽셀이 있는지 확인
            # 평균값 계산 시 정수 나눗셈을 피하기 위해 float으로 변환 후 계산
            threshold = sum(all_pixels) / len(all_pixels) if len(all_pixels) > 0 else 127
            print(f"계산된 평균 임계값 (예시): {threshold:.2f}")
        else:
            threshold = 127 # 기본값
            print(f"픽셀이 없어 기본 임계값 사용: {threshold}")
        
        # 실제 적용할 임계값 (정수로 사용하거나, 위 평균값을 그대로 사용해도 됨)
        # 여기서는 고정된 값을 사용하거나, 계산된 평균을 사용해봅시다.
        # fixed_threshold = 100
        fixed_threshold = int(round(threshold)) # 계산된 평균값을 반올림하여 사용
        print(f"실제 적용될 임계값: {fixed_threshold}")

        # 3. 이진화 적용
        binarized_img_matrix = binarize_image_fixed_threshold(grayscale_img_matrix, 
                                                              fixed_threshold, 
                                                              img_height, img_width)

        # 4. 원본 흑백 이미지와 이진화된 이미지 시각화
        fig, axes = plt.subplots(1, 2, figsize=(10, 5)) # 1x2 그리드로 이미지 표시
        
        visualize_grayscale_matrix(grayscale_img_matrix, "원본 흑백 이미지", ax=axes[0], width=img_width, height=img_height)
        visualize_grayscale_matrix(binarized_img_matrix, f"이진화 이미지 (임계값: {fixed_threshold})", ax=axes[1], width=img_width, height=img_height)
        
        plt.tight_layout()
        plt.show()

        print("\n--- 이진화 실습 완료 ---")
        print("\n참고: 오츄(Otsu)의 이진화나 적응형 임계값(Adaptive Thresholding) 같은 자동 임계값 결정 방법도 있습니다.")
        print("이런 방법들은 이미지의 특성에 맞춰 더 적절한 임계값을 찾아주며, OpenCV 같은 라이브러리에서 쉽게 사용할 수 있습니다.")

    else:
        print("이미지 매트릭스가 비어있어 이진화를 진행할 수 없습니다.")