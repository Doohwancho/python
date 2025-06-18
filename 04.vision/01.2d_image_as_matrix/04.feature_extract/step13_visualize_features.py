import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 1. 간단한 CNN 모델 정의
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 첫 번째 컨볼루션 레이어
        # 입력 채널 1개(흑백), 출력 채널 8개(8개의 특징 추출), 커널 크기 3x3
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1)
        
        # 두 번째 컨볼루션 레이어
        # 입력 채널 8개, 출력 채널 16개(16개의 더 복잡한 특징 추출)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1)

    def forward(self, x):
        # 이 함수는 전체 모델 실행용이지만, 여기서는 각 레이어를 단계별로 실행할 것입니다.
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        return x

# 2. 특징 맵 시각화 함수
def visualize_feature_maps(feature_maps, title):
    """주어진 특징 맵들을 그리드 형태로 시각화합니다."""
    
    # 계산 그래프로부터 분리하고 CPU로 이동
    feature_maps = feature_maps.detach().cpu()
    
    # 특징 맵의 개수 (채널 수)
    num_feature_maps = feature_maps.shape[1]
    
    # 그리드 크기 계산 (예: 16개면 4x4 그리드)
    grid_size = int(np.ceil(np.sqrt(num_feature_maps)))
    
    fig, axes = plt.subplots(grid_size, grid_size, figsize=(8, 8))
    fig.suptitle(title, fontsize=16)
    
    # 불필요한 축 제거를 위해 1D 배열로 변환
    axes = axes.flatten()

    for i in range(num_feature_maps):
        # i번째 특징 맵 가져오기
        feature_map = feature_maps[0, i, :, :]
        ax = axes[i]
        ax.imshow(feature_map.numpy(), cmap='gray') # 흑백으로 표시
        ax.set_title(f'Filter {i+1}')
        ax.axis('off')

    # 남는 빈 subplot 숨기기
    for j in range(num_feature_maps, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.92) # suptitle과 겹치지 않게 조정
    plt.show()


# --- 메인 실행 ---
if __name__ == "__main__":
    # 3. 이미지 로드 및 전처리
    try:
        # 이미지를 불러와서 64x64 크기, 흑백으로 변환
        img = Image.open('cat.jpg').convert('L') # 'L'은 흑백 모드
    except FileNotFoundError:
        print("에러: 'cat.jpg' 파일을 찾을 수 없습니다. 코드와 같은 폴더에 넣어주세요.")
        exit()

    # 이미지를 파이토치 텐서로 변환하는 파이프라인
    preprocess = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.5], std=[0.5]) # 필요시 정규화
    ])
    
    # 전처리 적용 및 모델 입력에 맞게 차원 추가 (배치 차원)
    # 모델은 (배치크기, 채널, 높이, 너비) 형태의 입력을 기대함
    img_tensor = preprocess(img).unsqueeze(0) # [1, 1, 64, 64] 크기가 됨
    print(f"입력 이미지 텐서 크기: {img_tensor.shape}")

    # 4. 모델 생성 및 특징 추출 실행
    model = SimpleCNN()
    
    # --- 첫 번째 레이어 통과 및 시각화 ---
    print("\n[1단계] 첫 번째 Conv 레이어를 통과시켜 저수준 특징을 추출합니다...")
    features_conv1 = model.conv1(img_tensor)
    # ReLU 활성화 함수를 통과시켜 특징을 더 명확하게 만듦
    features_conv1_relu = torch.relu(features_conv1)
    visualize_feature_maps(features_conv1_relu, "Layer 1: Feature Maps (Conv1 + ReLU)")
    
    # --- 두 번째 레이어 통과 및 시각화 ---
    print("\n[2단계] 첫 번째 특징들을 입력으로 받아 두 번째 Conv 레이어를 통과시킵니다...")
    features_conv2 = model.conv2(features_conv1_relu)
    features_conv2_relu = torch.relu(features_conv2)
    visualize_feature_maps(features_conv2_relu, "Layer 2: Feature Maps (Conv2 + ReLU)")

    print("\n시각화 완료!")