from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import time
import math

# --- 유틸리티 함수 (이전 코드 재사용) ---
def load_image_to_numpy_array(image_path='pepe_10_pixel.png'):
    try:
        img = Image.open(image_path).convert('RGB')
        return np.array(img), img.width, img.height
    except FileNotFoundError:
        print(f"Error: 이미지 파일 '{image_path}'을(를) 찾을 수 없습니다.")
        print("기본 10x10 컬러 이미지를 생성합니다 (무지개 패턴).")
        width, height = 10, 10
        r = np.array([[(x * 25) % 256 for x in range(width)] for y in range(height)])
        g = np.array([[(y * 25) % 256 for x in range(width)] for y in range(height)])
        b = np.array([[((x + y) * 20) % 256 for x in range(width)] for y in range(height)])
        default_img = np.stack([r, g, b], axis=-1)
        return default_img, width, height

# --- 변환 시각화 함수 ---
def visualize_transformation_step_by_step(src_img, M, pause_duration=0.1):
    """
    주어진 변환 행렬 M을 사용하여 기하학적 변환을 단계별로 시각화합니다.
    """
    src_height, src_width, _ = src_img.shape
    out_height, out_width = src_height, src_width # 출력 이미지 크기는 입력과 동일하게 가정

    # 출력 이미지를 검은색으로 초기화
    out_img = np.zeros_like(src_img)

    # 역변환 행렬 계산 (핵심!)
    try:
        M_inv = np.linalg.inv(M)
    except np.linalg.LinAlgError:
        print("에러: 변환 행렬의 역행렬을 계산할 수 없습니다. (Singular matrix)")
        return

    # Matplotlib 인터랙티브 모드 설정
    plt.ion()
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].set_title("원본 이미지")
    axes[0].imshow(src_img)
    axes[1].set_title("변환 중인 이미지")

    print("="*50)
    print("기하학적 변환 시작 (역매핑 방식)")
    print("출력 픽셀 -> 역변환 -> 입력 좌표 -> 값 가져오기")
    print("="*50)

    # 출력 이미지의 모든 픽셀 (u, v)를 순회
    for v in range(out_height): # y 좌표 (행)
        for u in range(out_width): # x 좌표 (열)
            
            # 1. 출력 좌표 벡터 생성 (동차 좌표계)
            dest_vec = np.array([u, v, 1])

            # 2. 역변환 행렬을 곱하여 원본 좌표 계산
            src_vec = M_inv @ dest_vec
            
            # 동차 좌표를 일반 좌표로 변환
            x, y = src_vec[0], src_vec[1]

            print(f"\n--- 처리 중인 출력 픽셀: (u,v) = ({u}, {v}) ---")
            print(f"  - 역변환 계산: M_inv @ [{u}, {v}, 1] => 원본좌표 (x,y) = ({x:.2f}, {y:.2f})")

            # 3. 보간법 (Interpolation) - 여기서는 최근접 이웃 보간법 사용
            src_x = int(round(x))
            src_y = int(round(y))
            
            print(f"  - 보간법 (최근접 이웃): ({x:.2f}, {y:.2f}) -> ({src_x}, {src_y})")

            # 4. 원본 이미지의 경계 내에 있는지 확인
            pixel_color = [0, 0, 0] # 경계 밖은 검은색
            if 0 <= src_x < src_width and 0 <= src_y < src_height:
                pixel_color = src_img[src_y, src_x]
                print(f"  - 값 가져오기: 원본({src_x}, {src_y})의 색상 {pixel_color}를 가져옴")
            else:
                print(f"  - 원본 이미지 범위 밖임. 검은색으로 처리.")

            # 5. 출력 이미지에 픽셀 값 채우기
            out_img[v, u] = pixel_color

            # --- 시각화 업데이트 ---
            axes[1].imshow(out_img)

            # 강조 표시용 사각형
            # 이전 사각형 제거
            if hasattr(fig, 'highlight_dest'): fig.highlight_dest.remove()
            if hasattr(fig, 'highlight_src'): fig.highlight_src.remove()
            
            # 출력 픽셀 위치 강조 (노란색)
            rect_dest = plt.Rectangle((u - 0.5, v - 0.5), 1, 1, lw=2, ec='yellow', fc='none')
            fig.highlight_dest = axes[1].add_patch(rect_dest)
            
            # 역매핑된 원본 픽셀 위치 강조 (라임색)
            rect_src = plt.Rectangle((src_x - 0.5, src_y - 0.5), 1, 1, lw=2, ec='lime', fc='none')
            fig.highlight_src = axes[0].add_patch(rect_src)
            
            fig.canvas.draw()
            plt.pause(pause_duration)

    # 최종 정리
    if hasattr(fig, 'highlight_dest'): fig.highlight_dest.remove()
    if hasattr(fig, 'highlight_src'): fig.highlight_src.remove()
    axes[1].set_title("변환 완료")
    fig.canvas.draw()
    plt.ioff()
    print("\n" + "="*50 + "\n변환 완료!\n" + "="*50)
    plt.show()


def create_transformation_matrix(angle_deg=0, scale_x=1.0, scale_y=1.0, tx=0, ty=0, shear_x=0):
    """다양한 변환을 조합하여 3x3 아핀 변환 행렬을 생성합니다."""
    # 중심점 기준 회전을 위해 이동 -> 회전 -> 역이동을 하지만, 여기서는 원점 기준
    theta = math.radians(angle_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)

    # 각 변환에 대한 행렬 생성
    T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]]) # 이동
    R = np.array([[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]]) # 회전
    Sc = np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]]) # 크기
    Sh = np.array([[1, shear_x, 0], [0, 1, 0], [0, 0, 1]]) # 전단
    
    # 행렬 곱셈 순서: 크기 -> 전단 -> 회전 -> 이동
    # M = T @ R @ Sh @ Sc
    # 더 직관적인 순서: 이동 @ 회전 @ 전단 @ 스케일
    M = T.dot(R.dot(Sh.dot(Sc)))
    return M

# --- 메인 실행 ---
if __name__ == "__main__":
    src_image, width, height = load_image_to_numpy_array('pepe_10_pixel.png')
    
    # --- 변환 종류 선택 ---
    
    # 1. 강체 변환 (Rigid): 30도 회전 + 우측으로 2칸, 아래로 1칸 이동
    print("\n--- 예제 1: 강체 변환 (회전 + 이동) ---")
    M_rigid = create_transformation_matrix(angle_deg=30, tx=2, ty=1)
    # visualize_transformation_step_by_step(src_image, M_rigid, pause_duration=0.01)

    # 2. 유사 변환 (Similarity): 30도 회전 + 0.7배 균일 축소 + 이동
    print("\n--- 예제 2: 유사 변환 (회전 + 균일 크기 + 이동) ---")
    M_similarity = create_transformation_matrix(angle_deg=30, scale_x=0.7, scale_y=0.7, tx=2, ty=2)
    # visualize_transformation_step_by_step(src_image, M_similarity, pause_duration=0.01)

    # 3. 아핀 변환 (Affine): 회전 + 비균일 축소 + 찌그러트리기(전단)
    print("\n--- 예제 3: 아핀 변환 (회전 + 비균일 크기 + 전단) ---")
    M_affine = create_transformation_matrix(angle_deg=20, scale_x=1.2, scale_y=0.8, shear_x=0.3, tx=1, ty=1)
    visualize_transformation_step_by_step(src_image, M_affine, pause_duration=0.01)
    
    # 참고: 원근 변환은 3x3 행렬의 마지막 행이 [0, 0, 1]이 아니므로 별도의 계산이 필요하여
    # 이 코드에서는 아핀 변환까지만 다룹니다. OpenCV의 getPerspectiveTransform 함수를 사용하면
    # 4개의 점 매핑으로 원근 변환 행렬을 쉽게 얻을 수 있습니다.