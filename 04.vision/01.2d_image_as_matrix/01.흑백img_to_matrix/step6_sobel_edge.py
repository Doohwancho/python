from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np
import time

# --- 이미지 로드 함수 (사용자 제공 코드 활용) ---
def load_image_to_matrix(image_path='pepe_10_pixel.png'):
    """이미지를 로드하여 흑백(Grayscale) 2D 행렬로 변환하여 반환합니다."""
    try:
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print(f"Error: 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        print("기본 10x10 흑백 패턴 이미지를 생성합니다.")
        width, height = 10, 10
        matrix = [[(r + c) * 15 for c in range(width)] for r in range(height)]
        return matrix, width, height

    width, height = img.size
    grayscale_matrix = [[img.getpixel((x, y)) for x in range(width)] for y in range(height)]
    return grayscale_matrix, width, height

# --- 헬퍼 함수 (출력 및 패딩) ---
def print_small_matrix(matrix, label="Matrix", precision=0):
    """작은 행렬(예: 3x3 패치 또는 커널)을 보기 좋게 출력합니다."""
    print(f"\n{label}:")
    if not matrix or not isinstance(matrix[0], list):
        print(f"  Invalid matrix: {matrix}")
        return

    col_widths = [0] * len(matrix[0])
    for row in matrix:
        for i, val in enumerate(row):
            fmt_val = f"{val:.{precision}f}" if isinstance(val, float) else str(val)
            col_widths[i] = max(col_widths[i], len(fmt_val))

    for row in matrix:
        formatted_row = [f"{val:.{precision}f}".rjust(col_widths[i]) if isinstance(val, float) else str(val).rjust(col_widths[i]) for i, val in enumerate(row)]
        print(f"  [{' '.join(formatted_row)}]")

def pad_matrix(matrix, padding_width=1, padding_value=0):
    """단일 채널 행렬에 패딩을 추가합니다."""
    if not matrix: return []
    height, width = len(matrix), len(matrix[0])
    new_height, new_width = height + 2 * padding_width, width + 2 * padding_width
    padded_matrix = [[padding_value for _ in range(new_width)] for _ in range(new_height)]
    
    for r in range(height):
        for c in range(width):
            padded_matrix[r + padding_width][c + padding_width] = matrix[r][c]
    return padded_matrix

def apply_convolution_to_patch(patch, kernel):
    """3x3 패치와 3x3 커널 간의 컨볼루션을 수행하고 결과 값과 중간 계산 행렬을 반환합니다."""
    output_value = 0
    multiplied_patch = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for r in range(3):
        for c in range(3):
            multiplied_value = patch[r][c] * kernel[r][c]
            multiplied_patch[r][c] = multiplied_value
            output_value += multiplied_value
    return output_value, multiplied_patch

# --- 메인 연출 함수: Sobel 엣지 검출 단계별 시각화 ---
def apply_sobel_step_by_step(image_matrix, pause_duration=0.3):
    """Sobel 엣지 검출을 단계별로 적용하고 콘솔과 이미지로 연출합니다."""
    height, width = len(image_matrix), len(image_matrix[0])
    sobel_x_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    
    padded_img = pad_matrix(image_matrix)
    
    # 최종 결과 및 중간 계산 결과(Gx, Gy)를 저장할 행렬들
    magnitude_matrix = [[0 for _ in range(width)] for _ in range(height)]
    gx_matrix = [[0 for _ in range(width)] for _ in range(height)]
    gy_matrix = [[0 for _ in range(width)] for _ in range(height)]

    # Matplotlib 인터랙티브 시각화 설정
    plt.ion()
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    # 원본 이미지 표시
    axes[0].imshow(image_matrix, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title("원본 이미지")

    print("="*60)
    print("Sobel 엣지 검출 시작! (픽셀별 Gx, Gy, 최종 Magnitude 계산)")
    print("="*60)

    for r_out in range(height):
        for c_out in range(width):
            print(f"\n--- 출력 픽셀 ({r_out}, {c_out}) 계산 시작 ---")
            
            # 현재 커널과 겹치는 3x3 이미지 패치 추출
            patch = [row[c_out:c_out+3] for row in padded_img[r_out:r_out+3]]
            print_small_matrix(patch, f"입력 패치 @ ({r_out},{c_out})")

            # 1. Gx 계산
            gx_val, gx_mult = apply_convolution_to_patch(patch, sobel_x_kernel)
            gx_matrix[r_out][c_out] = gx_val
            print_small_matrix(sobel_x_kernel, "Sobel X 커널")
            print_small_matrix(gx_mult, "패치 * Gx 커널", precision=1)
            print(f"-> Gx 값: {gx_val:.2f}")

            # 2. Gy 계산
            gy_val, gy_mult = apply_convolution_to_patch(patch, sobel_y_kernel)
            gy_matrix[r_out][c_out] = gy_val
            print_small_matrix(sobel_y_kernel, "Sobel Y 커널")
            print_small_matrix(gy_mult, "패치 * Gy 커널", precision=1)
            print(f"-> Gy 값: {gy_val:.2f}")

            # 3. 최종 Magnitude 계산
            magnitude = math.sqrt(gx_val**2 + gy_val**2)
            final_magnitude_val = max(0, min(255, int(round(magnitude))))
            magnitude_matrix[r_out][c_out] = final_magnitude_val
            print(f"\n-> 최종 Magnitude = sqrt({gx_val:.1f}² + {gy_val:.1f}²) = {magnitude:.2f} -> {final_magnitude_val}")

            # 4. 시각화 업데이트
            for i, (matrix, title) in enumerate([
                (gx_matrix, f"Gx 계산 중..."),
                (gy_matrix, f"Gy 계산 중..."),
                (magnitude_matrix, f"Magnitude 계산 중...")
            ], 1):
                ax = axes[i]
                ax.clear()
                # Gx, Gy는 음수, 양수 범위를 가지므로 vmin/vmax 없이 표시하여 상대적 차이를 봄
                if i < 3:
                    ax.imshow(matrix, cmap='gray')
                else: # Magnitude는 0~255
                    ax.imshow(matrix, cmap='gray', vmin=0, vmax=255)
                ax.set_title(title)

            # 현재 처리 중인 픽셀 위치 강조
            rect = plt.Rectangle((c_out - 0.5, r_out - 0.5), 1, 1, 
                                 linewidth=2, edgecolor='lime', facecolor='none')
            axes[0].add_patch(rect) # 원본 이미지에 표시
            
            fig.canvas.draw()
            plt.pause(pause_duration)
            
            if rect: rect.remove() # 이전 강조 표시 제거

    # 최종 결과 표시
    axes[1].set_title("Gx 최종 결과")
    axes[2].set_title("Gy 최종 결과")
    axes[3].set_title("Sobel Magnitude 최종 결과")
    fig.canvas.draw()
    plt.ioff()
    print("\n" + "="*60)
    print("Sobel 엣지 검출 완료!")
    print("="*60)
    plt.show()

# --- 메인 실행 ---
if __name__ == "__main__":
    # 1. 흑백 이미지 로드
    original_matrix, img_h, img_w = load_image_to_matrix('pepe_10_pixel.png')

    # 2. 원본 이미지 시각화 (확인용)
    # visualize_matrix(original_matrix, "Original Grayscale Image")

    # 3. Sobel 엣지 검출 단계별 시각화 실행
    # pause_duration을 줄이면 더 빠르게 진행됩니다 (예: 0.1)
    apply_sobel_step_by_step(original_matrix, pause_duration=0.2)