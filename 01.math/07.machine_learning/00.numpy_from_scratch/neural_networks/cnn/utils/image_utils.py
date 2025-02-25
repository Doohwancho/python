import numpy as np
from PIL import Image

def load_image(image_path, target_size=(28, 28)):
    """
    이미지 파일 읽어서 CNN 입력으로 변환하는거임 ㅋㅋ
    
    Args:
        image_path: 이미지 경로
        target_size: 리사이즈할 크기 (기본값 MNIST 크기)
    
    Returns:
        numpy array: shape (1, 1, height, width) - 흑백 이미지
        또는 shape (1, 3, height, width) - RGB 이미지
    """
    # 이미지 로드
    img = Image.open(image_path)
    
    # 타겟 사이즈로 리사이즈
    img = img.resize(target_size)
    
    # numpy 배열로 변환
    img_array = np.array(img)
    
    # 채널 먼저 오게 변환 (HWC -> CHW)
    if len(img_array.shape) == 3:  # RGB 이미지
        img_array = img_array.transpose(2, 0, 1)
    else:  # 흑백 이미지
        img_array = img_array[np.newaxis, :, :]
    
    # 배치 차원 추가 & 정규화
    img_array = img_array[np.newaxis, :, :, :] / 255.0
    
    return img_array

# 사용 예시:
"""
# 이미지 로드해서 CNN에 넣기
image_path = "test_image.jpg"
x = load_image(image_path)
output = model.forward(NDArray(x))

# 예측 결과 출력
predicted_class = np.argmax(output)
print(f"예측 클래스: {predicted_class} ㅋㅋ")
"""
