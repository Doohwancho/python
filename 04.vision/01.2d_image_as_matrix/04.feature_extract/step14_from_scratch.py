import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# --- 1. 이미지 로드 및 전처리 함수 ---
def load_and_preprocess_image(image_path='cat.jpg', size=(64, 64)):
    """이미지를 불러와 흑백 NumPy 배열로 변환합니다."""
    try:
        img = Image.open(image_path).convert('L') # 'L' = 흑백 모드
        img = img.resize(size)
        # 이미지 데이터를 0-1 사이로 정규화 (선택 사항이지만 일반적)
        return np.array(img) / 255.0
    except FileNotFoundError:
        print(f"에러: '{image_path}' 파일을 찾을 수 없습니다.")
        return None

# --- 2. From Scratch 핵심 연산 함수 ---
def apply_relu(feature_map):
    """ReLU 활성화 함수를 적용합니다."""
    # NumPy의 maximum 함수를 사용해 0보다 작은 값을 모두 0으로 만듦
    return np.maximum(0, feature_map)

def convolve_2d(image, kernel, padding=1, stride=1):
    """
    단일 입력 채널과 단일 커널에 대한 2D 컨볼루션 연산을 수행합니다.
    """
    # 1. 패딩 적용
    if padding > 0:
        image_padded = np.pad(image, pad_width=padding, mode='constant', constant_values=0)
    else:
        image_padded = image

    # 2. 출력 피처 맵 크기 계산
    k_h, k_w = kernel.shape
    img_h, img_w = image.shape
    out_h = (img_h - k_h + 2 * padding) // stride + 1
    out_w = (img_w - k_w + 2 * padding) // stride + 1
    
    output_map = np.zeros((out_h, out_w))

    # 3. 컨볼루션 연산 (슬라이딩 윈도우)
    for y in range(out_h):
        for x in range(out_w):
            # 윈도우(패치) 추출
            patch = image_padded[y*stride : y*stride + k_h, x*stride : x*stride + k_w]
            # Element-wise 곱셈 후 합산
            output_map[y, x] = (patch * kernel).sum()
            
    return output_map

def apply_conv_layer(input_maps, kernels, padding=1, stride=1):
    """
    하나의 컨볼루션 레이어 전체를 적용합니다.
    (입력 맵 여러 개 -> 여러 개의 커널 -> 출력 맵 여러 개)
    """
    num_output_kernels = kernels.shape[0]
    num_input_channels = input_maps.shape[0]
    
    # 첫 번째 커널의 결과로부터 출력 크기를 결정
    sample_output = convolve_2d(input_maps[0], kernels[0, 0], padding, stride)
    output_height, output_width = sample_output.shape
    
    # 최종 출력 피처 맵들 초기화
    output_maps = np.zeros((num_output_kernels, output_height, output_width))

    # 각 출력 커널(필터)에 대해 반복
    for k_idx in range(num_output_kernels):
        # 해당 커널이 처리해야 할 모든 입력 채널에 대해 컨볼루션 수행 후 합산
        # 이것이 PyTorch의 nn.Conv2d가 내부적으로 하는 핵심 작업입니다.
        total_conv_result = np.zeros((output_height, output_width))
        for c_idx in range(num_input_channels):
            image_channel = input_maps[c_idx]
            kernel_channel = kernels[k_idx, c_idx]
            total_conv_result += convolve_2d(image_channel, kernel_channel, padding, stride)
        output_maps[k_idx] = total_conv_result
        
    return output_maps


# --- 3. 시각화 함수 (이전과 거의 동일) ---
def visualize_feature_maps(feature_maps, title):
    """주어진 특징 맵들을 그리드 형태로 시각화합니다."""
    num_feature_maps = feature_maps.shape[0]
    grid_size = int(np.ceil(np.sqrt(num_feature_maps)))
    
    fig, axes = plt.subplots(grid_size, grid_size, figsize=(8, 8))
    fig.suptitle(title, fontsize=16)
    axes = axes.flatten()

    for i in range(num_feature_maps):
        ax = axes[i]
        ax.imshow(feature_maps[i], cmap='gray')
        ax.set_title(f'Filter {i+1}')
        ax.axis('off')

    for j in range(num_feature_maps, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.show()

# --- 4. 메인 실행 ---
if __name__ == "__main__":
    # 이미지 로드
    image = load_and_preprocess_image('cat.jpg')
    if image is None:
        exit()
        
    # 모델에 입력하기 위해 채널 및 배치 차원 추가: (높이, 너비) -> (1, 1, 높이, 너비)
    image_tensor_like = image[np.newaxis, np.newaxis, :, :]
    print(f"입력 이미지 배열 크기: {image_tensor_like.shape}")
    
    # --- Conv1 실행 ---
    # PyTorch의 nn.Conv2d(1, 8, 3)을 모방: 8개의 3x3 커널 (입력 채널 1개)
    np.random.seed(0) # 결과를 재현 가능하게 하기 위함
    conv1_kernels = np.random.randn(8, 1, 3, 3) # (출력채널, 입력채널, 커널높이, 커널너비)
    
    print("\n[1단계] From-scratch Conv1 연산을 수행합니다...")
    features_conv1 = apply_conv_layer(image_tensor_like[0], conv1_kernels)
    features_conv1_relu = apply_relu(features_conv1)
    visualize_feature_maps(features_conv1_relu, "Layer 1: From Scratch (Conv1 + ReLU)")

    # --- Conv2 실행 ---
    # PyTorch의 nn.Conv2d(8, 16, 3)을 모방: 16개의 3x3 커널 (입력 채널 8개)
    conv2_kernels = np.random.randn(16, 8, 3, 3) # (출력채널, 입력채널, 커널높이, 커널너비)
    
    print("\n[2단계] From-scratch Conv2 연산을 수행합니다...")
    # Conv1의 출력이 Conv2의 입력으로 들어감
    features_conv2 = apply_conv_layer(features_conv1_relu, conv2_kernels)
    features_conv2_relu = apply_relu(features_conv2)
    visualize_feature_maps(features_conv2_relu, "Layer 2: From Scratch (Conv2 + ReLU)")
    
    print("\n시각화 완료!")