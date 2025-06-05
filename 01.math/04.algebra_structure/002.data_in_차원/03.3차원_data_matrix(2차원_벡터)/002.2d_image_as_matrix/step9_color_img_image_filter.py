from PIL import Image
import matplotlib.pyplot as plt
import numpy as np # NumPy는 행렬 연산 및 패딩에 편리하지만, 순수 Python으로도 구현 가능합니다.
                   # 여기서는 명시적인 루프를 위해 순수 Python 리스트를 주로 사용하되,
                   # 시각화 데이터 준비에만 살짝 활용하거나, 순수 리스트로 처리합니다.
import time

# --- 사용자 제공 함수 (약간 수정/활용) ---
def print_small_matrix(matrix, label="Matrix", precision=0):
    """작은 행렬(예: 3x3 패치 또는 커널)을 보기 좋게 출력합니다."""
    print(f"\n{label}:")
    if not matrix or not isinstance(matrix, list) or not isinstance(matrix[0], list):
        print(f"  Invalid matrix format: {matrix}")
        return

    # 각 숫자를 일정한 너비로 포맷팅하기 위함
    col_widths = [0] * len(matrix[0])
    for row in matrix:
        for i, val in enumerate(row):
            fmt_val = f"{val:.{precision}f}" if isinstance(val, float) else str(val)
            col_widths[i] = max(col_widths[i], len(fmt_val))

    for row in matrix:
        formatted_row = []
        for i, val in enumerate(row):
            fmt_val = f"{val:.{precision}f}" if isinstance(val, float) else str(val)
            formatted_row.append(fmt_val.rjust(col_widths[i]))
        print(f"  [{' '.join(formatted_row)}]")


def load_color_image_to_rgb_matrices(image_path='pepe_10_pixel.png'):
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        print("기본 10x10 컬러 이미지를 생성합니다 (무지개 패턴).")
        width, height = 10, 10
        matrix_r = [[(x*25) % 256 for x in range(width)] for y in range(height)]
        matrix_g = [[(y*25) % 256 for x in range(width)] for y in range(height)]
        matrix_b = [[((x+y)*20) % 256 for x in range(width)] for y in range(height)]
        return matrix_r, matrix_g, matrix_b, width, height

    width, height = img.size
    # if width != 10 or height != 10: # 필요시 크기 경고
    # print(f"Warning: Image size is {width}x{height}, not 10x10.")

    matrix_r = [[0 for _ in range(width)] for _ in range(height)]
    matrix_g = [[0 for _ in range(width)] for _ in range(height)]
    matrix_b = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            r_val, g_val, b_val = img.getpixel((x, y))
            matrix_r[y][x] = r_val
            matrix_g[y][x] = g_val
            matrix_b[y][x] = b_val
    return matrix_r, matrix_g, matrix_b, width, height

def combine_rgb_matrices_for_display(r_m, g_m, b_m, height, width):
    """R, G, B 행렬을 시각화를 위한 M x N x 3 구조로 결합 (값 클램핑 포함)."""
    display_img = [[[0,0,0] for _ in range(width)] for _ in range(height)]
    for r_idx in range(height):
        for c_idx in range(width):
            display_img[r_idx][c_idx] = [
                max(0, min(255, int(round(r_m[r_idx][c_idx])))),
                max(0, min(255, int(round(g_m[r_idx][c_idx])))),
                max(0, min(255, int(round(b_m[r_idx][c_idx]))))
            ]
    return display_img

# --- 컨볼루션 관련 함수 ---
def pad_matrix_channel(channel_matrix, padding_width, padding_value=0):
    """단일 채널 행렬에 패딩을 추가합니다."""
    height = len(channel_matrix)
    width = len(channel_matrix[0])
    
    new_height = height + 2 * padding_width
    new_width = width + 2 * padding_width
    
    padded_matrix = [[padding_value for _ in range(new_width)] for _ in range(new_height)]
    
    for r_idx in range(height):
        for c_idx in range(width):
            padded_matrix[r_idx + padding_width][c_idx + padding_width] = channel_matrix[r_idx][c_idx]
            
    return padded_matrix

def apply_convolution_step(padded_channel_patch, kernel):
    """3x3 패치와 3x3 커널 간의 컨볼루션(원소별 곱셈 후 합산)을 수행합니다."""
    k_height = len(kernel)
    k_width = len(kernel[0])
    
    multiplied_patch = [[0 for _ in range(k_width)] for _ in range(k_height)]
    output_value = 0
    
    for r_k in range(k_height):
        for c_k in range(k_width):
            multiplied_value = padded_channel_patch[r_k][c_k] * kernel[r_k][c_k]
            multiplied_patch[r_k][c_k] = multiplied_value
            output_value += multiplied_value
            
    return output_value, multiplied_patch

# --- 메인 시각화 및 연산 함수 ---
def convolve_and_visualize_steps(r_orig, g_orig, b_orig, kernel, pause_duration=0.5):
    """컬러 이미지에 컨볼루션을 단계별로 적용하고 시각화합니다."""
    height = len(r_orig)
    width = len(r_orig[0])
    k_height = len(kernel)
    k_width = len(kernel[0])

    if k_height % 2 == 0 or k_width % 2 == 0:
        print("Error: 커널 크기는 홀수여야 합니다 (예: 3x3).")
        return

    padding_width = k_height // 2 # 3x3 커널의 경우 1

    # 각 채널 패딩
    r_padded = pad_matrix_channel(r_orig, padding_width)
    g_padded = pad_matrix_channel(g_orig, padding_width)
    b_padded = pad_matrix_channel(b_orig, padding_width)

    # 결과 이미지 채널 초기화 (0으로)
    r_out = [[0 for _ in range(width)] for _ in range(height)]
    g_out = [[0 for _ in range(width)] for _ in range(height)]
    b_out = [[0 for _ in range(width)] for _ in range(height)]

    # Matplotlib 인터랙티브 모드 켜기
    plt.ion()
    fig, axes = plt.subplots(1, 2, figsize=(10, 5)) # 원본과 처리 중인 이미지

    # 원본 이미지 표시 (한 번만)
    original_display_img = combine_rgb_matrices_for_display(r_orig, g_orig, b_orig, height, width)
    axes[0].imshow(original_display_img)
    axes[0].set_title("원본 이미지")
    axes[0].set_xticks(np.arange(-.5, width, 1), minor=True) # 그리드 선을 위한 틱
    axes[0].set_yticks(np.arange(-.5, height, 1), minor=True)
    axes[0].grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    axes[0].tick_params(which="minor", size=0)
    axes[0].set_xticks(np.arange(0, width, 1 if width <=10 else 2)) # 주 틱
    axes[0].set_yticks(np.arange(0, height, 1 if height <=10 else 2))


    print("="*50)
    print("컨볼루션 연산 시작!")
    print_small_matrix(kernel, "사용 커널", precision=2)
    print("="*50)

    for r_idx_out in range(height): # 결과 이미지의 행
        for c_idx_out in range(width): # 결과 이미지의 열
            print(f"\n--- 현재 처리 중인 출력 픽셀: ({r_idx_out}, {c_idx_out}) ---")

            # 현재 커널이 겹치는 패딩된 이미지의 3x3 패치 추출
            # r_idx_out, c_idx_out이 패딩된 이미지에서 패치의 좌상단 모서리가 됨
            patch_r = [row[c_idx_out : c_idx_out + k_width] for row in r_padded[r_idx_out : r_idx_out + k_height]]
            patch_g = [row[c_idx_out : c_idx_out + k_width] for row in g_padded[r_idx_out : r_idx_out + k_height]]
            patch_b = [row[c_idx_out : c_idx_out + k_width] for row in b_padded[r_idx_out : r_idx_out + k_height]]

            # R 채널 연산 및 출력
            val_r, mult_r = apply_convolution_step(patch_r, kernel)
            r_out[r_idx_out][c_idx_out] = val_r
            print_small_matrix(patch_r, f"R 채널 입력 패치 @ ({r_idx_out},{c_idx_out})")
            print_small_matrix(mult_r, "R 채널: 패치 * 커널 결과", precision=1)
            print(f"R 채널 결과 값 @ ({r_idx_out},{c_idx_out}): {val_r:.2f} -> {max(0,min(255,int(round(val_r))))}")

            # G 채널 연산 및 출력
            val_g, mult_g = apply_convolution_step(patch_g, kernel)
            g_out[r_idx_out][c_idx_out] = val_g
            print_small_matrix(patch_g, f"G 채널 입력 패치 @ ({r_idx_out},{c_idx_out})")
            print_small_matrix(mult_g, "G 채널: 패치 * 커널 결과", precision=1)
            print(f"G 채널 결과 값 @ ({r_idx_out},{c_idx_out}): {val_g:.2f} -> {max(0,min(255,int(round(val_g))))}")

            # B 채널 연산 및 출력
            val_b, mult_b = apply_convolution_step(patch_b, kernel)
            b_out[r_idx_out][c_idx_out] = val_b
            print_small_matrix(patch_b, f"B 채널 입력 패치 @ ({r_idx_out},{c_idx_out})")
            print_small_matrix(mult_b, "B 채널: 패치 * 커널 결과", precision=1)
            print(f"B 채널 결과 값 @ ({r_idx_out},{c_idx_out}): {val_b:.2f} -> {max(0,min(255,int(round(val_b))))}")

            # 현재까지 처리된 결과 이미지 시각화
            current_display_img = combine_rgb_matrices_for_display(r_out, g_out, b_out, height, width)
            axes[1].clear() # 이전 그림 지우기
            axes[1].imshow(current_display_img)
            axes[1].set_title(f"처리 중... ({r_idx_out}, {c_idx_out}) 완료")
            axes[1].set_xticks(np.arange(-.5, width, 1), minor=True)
            axes[1].set_yticks(np.arange(-.5, height, 1), minor=True)
            axes[1].grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
            axes[1].tick_params(which="minor", size=0)
            axes[1].set_xticks(np.arange(0, width, 1 if width <=10 else 2))
            axes[1].set_yticks(np.arange(0, height, 1 if height <=10 else 2))


            # 현재 처리 중인 픽셀 위치를 원본 이미지에도 표시 (선택 사항)
            # 현재 커널의 중심이 (r_idx_out, c_idx_out)이므로, 원본 이미지에 해당 픽셀을 강조
            rect = plt.Rectangle((c_idx_out - 0.5, r_idx_out - 0.5), 1, 1, 
                                 linewidth=2, edgecolor='lime', facecolor='none', 
                                 transform=axes[0].transData) # 원본 이미지 좌표계 사용
            
            # 이전 강조 표시 제거 및 새 강조 표시 추가
            if hasattr(fig, 'highlight_rect_orig'):
                fig.highlight_rect_orig.remove()
            fig.highlight_rect_orig = rect
            axes[0].add_patch(rect)
            
            # 현재 커널 영역을 처리 중인 이미지에도 표시 (선택 사항)
            # 결과 이미지의 (r_idx_out, c_idx_out) 픽셀이 방금 계산됨
            rect_out = plt.Rectangle((c_idx_out - 0.5, r_idx_out - 0.5), 1, 1,
                                     linewidth=2, edgecolor='yellow', facecolor='none',
                                     transform=axes[1].transData)
            if hasattr(fig, 'highlight_rect_out'):
                fig.highlight_rect_out.remove()
            fig.highlight_rect_out = rect_out
            axes[1].add_patch(rect_out)


            plt.tight_layout()
            fig.canvas.draw()
            plt.pause(pause_duration)
            
            if r_idx_out == height -1 and c_idx_out == width -1:
                print("\n최종 결과 값으로 클램핑 중...")
            else:
                time.sleep(0.05) # 너무 많은 콘솔 출력을 위한 약간의 딜레이

    if hasattr(fig, 'highlight_rect_orig'): fig.highlight_rect_orig.remove()
    if hasattr(fig, 'highlight_rect_out'): fig.highlight_rect_out.remove()
    
    axes[1].set_title("최종 결과 이미지")
    fig.canvas.draw()
    plt.ioff() # 인터랙티브 모드 끄기
    print("="*50)
    print("컨볼루션 연산 완료!")
    print("="*50)
    plt.show() # 최종 결과 보여주고 유지

    return r_out, g_out, b_out

# --- 메인 실행 ---
if __name__ == "__main__":
    # 1. 컬러 이미지 로드 (파일이 없으면 기본 패턴 생성)
    # 실제 10x10 컬러 이미지 파일 경로 (예: 'pepe_10_pixel_color.png')
    # 직접 만드시거나, 인터넷에서 작은 아이콘을 10x10으로 줄여서 사용하세요.
    r_channel_orig, g_channel_orig, b_channel_orig, img_w, img_h = load_color_image_to_rgb_matrices('pepe_10_pixel.png')

    # 2. 사용할 3x3 커널 정의
    # 예1: 간단한 블러(평균) 커널 (값을 1/9로 하면 정규화된 블러)
    # kernel_blur = [[1/9, 1/9, 1/9],
    #                [1/9, 1/9, 1/9],
    #                [1/9, 1/9, 1/9]]
    
    # 예2: 샤프닝 커널
    kernel_sharpen = [[ 0, -1,  0],
                      [-1,  5, -1],
                      [ 0, -1,  0]]

    # 예3: 간단한 엣지 검출 (수평선)
    # kernel_edge_h = [[-1, -1, -1],
    #                  [ 0,  0,  0],
    #                  [ 1,  1,  1]]

    selected_kernel = kernel_sharpen # 사용할 커널 선택

    # 3. 컨볼루션 단계별 시각화 실행
    # pause_duration을 줄이면 더 빠르게 진행됩니다 (예: 0.1)
    # 너무 많은 콘솔 출력으로 느릴 수 있으니, 실제 사용 시에는 print문 일부를 주석처리할 수 있습니다.
    r_final, g_final, b_final = convolve_and_visualize_steps(
        r_channel_orig, g_channel_orig, b_channel_orig,
        selected_kernel,
        pause_duration=0.2 # 각 스텝 후 대기 시간(초)
    )

    print("\n최종 R 채널 결과 (클램핑 전 값 일부):")
    for r in range(min(3, img_h)): print([f"{x:.1f}" for x in r_final[r][:min(5,img_w)]])
    # 최종 결과 이미지는 convolve_and_visualize_steps 함수 마지막에 plt.show()로 표시됩니다.