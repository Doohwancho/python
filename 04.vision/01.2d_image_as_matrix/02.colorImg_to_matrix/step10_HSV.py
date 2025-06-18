from PIL import Image
import matplotlib.pyplot as plt
import numpy as np # 시각화 시 데이터 변환에 편리
import colorsys # RGB <-> HSV 변환을 위해 표준 라이브러리 colorsys 사용

# --- 이미지 로드 및 시각화 함수 (이전 코드 재활용 및 수정) ---

def load_color_image_to_rgb_matrices(image_path='pepe_10_pixel.png'):
    """컬러 이미지를 로드하여 R, G, B 채널별 2D 행렬(리스트의 리스트)로 분리하여 반환합니다."""
    try:
        img = Image.open(image_path).convert('RGB') # 'RGB'로 변환
    except FileNotFoundError:
        print(f"Error: 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        print("기본 10x10 컬러 이미지를 생성합니다 (무지개 패턴).")
        width, height = 10, 10
        matrix_r = [[(x*20 + y*5) % 256 for x in range(width)] for y in range(height)]
        matrix_g = [[(y*20 + x*5) % 256 for x in range(width)] for y in range(height)]
        matrix_b = [[((x+y)*15 + 50) % 256 for x in range(width)] for y in range(height)]
        return matrix_r, matrix_g, matrix_b, width, height

    width, height = img.size
    # if width != 10 or height != 10: # 필요시 크기 경고
    # print(f"Warning: Image size is {width}x{height}, not 10x10.")

    matrix_r = [[0 for _ in range(width)] for _ in range(height)]
    matrix_g = [[0 for _ in range(width)] for _ in range(height)]
    matrix_b = [[0 for _ in range(width)] for _ in range(height)]

    for y_idx in range(height):
        for x_idx in range(width):
            r_val, g_val, b_val = img.getpixel((x_idx, y_idx))
            matrix_r[y_idx][x_idx] = r_val
            matrix_g[y_idx][x_idx] = g_val
            matrix_b[y_idx][x_idx] = b_val
    return matrix_r, matrix_g, matrix_b, width, height

def combine_rgb_matrices_for_display(r_m, g_m, b_m, height, width):
    """R, G, B 행렬을 시각화를 위한 M x N x 3 구조로 결합 (0-255 값 클램핑 포함)."""
    display_img = [[[0,0,0] for _ in range(width)] for _ in range(height)]
    for r_idx in range(height):
        for c_idx in range(width):
            display_img[r_idx][c_idx] = [
                max(0, min(255, int(round(r_m[r_idx][c_idx])))),
                max(0, min(255, int(round(g_m[r_idx][c_idx])))),
                max(0, min(255, int(round(b_m[r_idx][c_idx]))))
            ]
    return display_img

def visualize_image_matrix(image_data_rgb_format, title="Image", ax=None):
    """M x N x 3 형태의 이미지 데이터를 시각화합니다."""
    if ax is None:
        fig, ax_new = plt.subplots()
        ax_new.imshow(image_data_rgb_format)
        ax_new.set_title(title)
        if len(image_data_rgb_format) <= 20 and len(image_data_rgb_format[0]) <= 20 : # 작은 이미지용 틱
            ax_new.set_xticks(np.arange(0, len(image_data_rgb_format[0]), 1))
            ax_new.set_yticks(np.arange(0, len(image_data_rgb_format), 1))
            ax_new.grid(which="major", color="gray", linestyle='-', linewidth=0.5)
        plt.show()
    else:
        ax.imshow(image_data_rgb_format)
        ax.set_title(title)
        if len(image_data_rgb_format) <= 20 and len(image_data_rgb_format[0]) <= 20 :
            ax.set_xticks(np.arange(0, len(image_data_rgb_format[0]), 1))
            ax.set_yticks(np.arange(0, len(image_data_rgb_format), 1))
            ax.grid(which="major", color="gray", linestyle='-', linewidth=0.5)


# --- RGB <-> HSV 변환 함수 ---

def convert_rgb_to_hsv_matrices(r_matrix, g_matrix, b_matrix, height, width):
    """RGB 채널 행렬들을 HSV 채널 행렬들로 변환합니다 (값 범위 0.0 ~ 1.0)."""
    h_matrix = [[0.0 for _ in range(width)] for _ in range(height)]
    s_matrix = [[0.0 for _ in range(width)] for _ in range(height)]
    v_matrix = [[0.0 for _ in range(width)] for _ in range(height)]

    for r_idx in range(height):
        for c_idx in range(width):
            # colorsys는 R,G,B 값을 0.0~1.0 범위로 받음
            r_norm = r_matrix[r_idx][c_idx] / 255.0
            g_norm = g_matrix[r_idx][c_idx] / 255.0
            b_norm = b_matrix[r_idx][c_idx] / 255.0
            
            h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
            
            h_matrix[r_idx][c_idx] = h
            s_matrix[r_idx][c_idx] = s
            v_matrix[r_idx][c_idx] = v
            
    return h_matrix, s_matrix, v_matrix

def convert_hsv_to_rgb_matrices(h_matrix, s_matrix, v_matrix, height, width):
    """HSV 채널 행렬들을 RGB 채널 행렬들로 변환합니다 (값 범위 0 ~ 255)."""
    r_matrix_new = [[0 for _ in range(width)] for _ in range(height)]
    g_matrix_new = [[0 for _ in range(width)] for _ in range(height)]
    b_matrix_new = [[0 for _ in range(width)] for _ in range(height)]

    for r_idx in range(height):
        for c_idx in range(width):
            h = h_matrix[r_idx][c_idx]
            s = s_matrix[r_idx][c_idx]
            v = v_matrix[r_idx][c_idx]
            
            r_norm, g_norm, b_norm = colorsys.hsv_to_rgb(h, s, v)
            
            # 다시 0~255 범위로 스케일링
            r_matrix_new[r_idx][c_idx] = int(round(r_norm * 255.0))
            g_matrix_new[r_idx][c_idx] = int(round(g_norm * 255.0))
            b_matrix_new[r_idx][c_idx] = int(round(b_norm * 255.0))
            
    return r_matrix_new, g_matrix_new, b_matrix_new

# --- HSV 공간에서 효과 적용 함수 ---

def modify_hue(h_matrix_orig, height, width, shift_amount):
    """Hue 채널 값을 주어진 양만큼 이동시킵니다 (0.0 ~ 1.0 범위, 순환)."""
    h_matrix_mod = [[0.0 for _ in range(width)] for _ in range(height)]
    for r_idx in range(height):
        for c_idx in range(width):
            new_hue = (h_matrix_orig[r_idx][c_idx] + shift_amount) % 1.0
            h_matrix_mod[r_idx][c_idx] = new_hue
    return h_matrix_mod

def modify_saturation(s_matrix_orig, height, width, scale_factor):
    """Saturation 채널 값을 주어진 비율로 조절합니다 (0.0 ~ 1.0 범위로 클램핑)."""
    s_matrix_mod = [[0.0 for _ in range(width)] for _ in range(height)]
    for r_idx in range(height):
        for c_idx in range(width):
            new_sat = s_matrix_orig[r_idx][c_idx] * scale_factor
            s_matrix_mod[r_idx][c_idx] = max(0.0, min(1.0, new_sat)) # 0.0~1.0 사이로 클램핑
    return s_matrix_mod

def modify_value(v_matrix_orig, height, width, scale_factor):
    """Value 채널 값을 주어진 비율로 조절합니다 (0.0 ~ 1.0 범위로 클램핑)."""
    v_matrix_mod = [[0.0 for _ in range(width)] for _ in range(height)]
    for r_idx in range(height):
        for c_idx in range(width):
            new_val = v_matrix_orig[r_idx][c_idx] * scale_factor
            v_matrix_mod[r_idx][c_idx] = max(0.0, min(1.0, new_val)) # 0.0~1.0 사이로 클램핑
    return v_matrix_mod

# --- 메인 실행 ---
if __name__ == "__main__":
    # 1. 컬러 이미지 로드
    # 실제 10x10 컬러 이미지 파일명으로 변경하세요. (예: 'pepe_10_pixel_color.png')
    # 파일이 없으면 load_color_image_to_rgb_matrices 함수 내에서 기본 이미지를 생성합니다.
    image_filename = 'pepe_10_pixel.png'
    r_orig, g_orig, b_orig, img_height, img_width = load_color_image_to_rgb_matrices(image_filename)

    # 원본 이미지 데이터 (시각화용)
    original_image_display_data = combine_rgb_matrices_for_display(r_orig, g_orig, b_orig, img_height, img_width)

    # 2. RGB -> HSV 변환
    print("RGB를 HSV로 변환 중...")
    h_channel, s_channel, v_channel = convert_rgb_to_hsv_matrices(r_orig, g_orig, b_orig, img_height, img_width)

    # 3. HSV 공간에서 효과 적용 및 결과 시각화
    fig, axes = plt.subplots(2, 2, figsize=(10, 10)) # 2x2 그리드로 이미지 표시
    axes_flat = axes.flatten() # 사용하기 쉽게 1차원 배열로

    visualize_image_matrix(original_image_display_data, "원본 이미지", ax=axes_flat[0])

    # 효과 1: Hue 변경 (색조 이동)
    print("Hue 변경 효과 적용 중...")
    hue_shift = 0.33 # 예: 1/3 정도 색상환 이동 (0.0 ~ 1.0)
    h_mod_hue = modify_hue(h_channel, img_height, img_width, hue_shift)
    r_hue_mod, g_hue_mod, b_hue_mod = convert_hsv_to_rgb_matrices(h_mod_hue, s_channel, v_channel, img_height, img_width)
    hue_modified_display_data = combine_rgb_matrices_for_display(r_hue_mod, g_hue_mod, b_hue_mod, img_height, img_width)
    visualize_image_matrix(hue_modified_display_data, f"Hue +{hue_shift:.2f} 변경", ax=axes_flat[1])

    # 효과 2: Saturation 변경 (채도 조절)
    print("Saturation 변경 효과 적용 중...")
    saturation_scale = 1.8 # 예: 채도 80% 증가
    s_mod_sat = modify_saturation(s_channel, img_height, img_width, saturation_scale)
    r_sat_mod, g_sat_mod, b_sat_mod = convert_hsv_to_rgb_matrices(h_channel, s_mod_sat, v_channel, img_height, img_width) # 원본 H, V 사용
    saturation_modified_display_data = combine_rgb_matrices_for_display(r_sat_mod, g_sat_mod, b_sat_mod, img_height, img_width)
    visualize_image_matrix(saturation_modified_display_data, f"Saturation x{saturation_scale:.1f}", ax=axes_flat[2])

    # 효과 3: Value 변경 (명도 조절)
    print("Value 변경 효과 적용 중...")
    value_scale = 0.7 # 예: 명도 30% 감소
    v_mod_val = modify_value(v_channel, img_height, img_width, value_scale)
    r_val_mod, g_val_mod, b_val_mod = convert_hsv_to_rgb_matrices(h_channel, s_channel, v_mod_val, img_height, img_width) # 원본 H, S 사용
    value_modified_display_data = combine_rgb_matrices_for_display(r_val_mod, g_val_mod, b_val_mod, img_height, img_width)
    visualize_image_matrix(value_modified_display_data, f"Value x{value_scale:.1f}", ax=axes_flat[3])
    
    plt.tight_layout()
    plt.show()

    print("\n--- HSV 효과 적용 및 시각화 완료 ---")