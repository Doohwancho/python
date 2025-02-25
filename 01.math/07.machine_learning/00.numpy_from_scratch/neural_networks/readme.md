---\
history of neural network 


1. Perceptron (1957)
    - 최초의 인공신경망 모델
    - Frank Rosenblatt가 개발
    - 단순한 이진 분류만 가능
    - XOR 문제를 풀지 못하는 한계
2. MLP(multi layer perceptrons, 1960s - 1980s)
    - Hidden layer 도입으로 XOR 문제 해결
    - Backpropagation 알고리즘 개발
    - 기본적인 패턴 인식 가능
    - 하지만 학습이 어렵고 느림
3. CNN(1989, LeNet)
    - MLP 앞단에 feature extraction 기능이 추가된거 
    - Yann LeCun이 개발한 LeNet 등장
    - 이미지 처리에 많이 썼었음 2017년도까지
    - Convolution과 Pooling 개념 도입
    - 2012년 AlexNet으로 실제 성능 입증
4. RNN (1990s)
    - MLP에 "메모리" 기능이 추가된 것. (문장 처리할 때 이전 단어 기억하는거 생각하면 됨 ㅇㅇ)
    - 시퀀스 데이터 처리를 위한 구조
    - 시간적 의존성 학습 가능
    - Vanishing gradient 문제 존재
    - NLP 태스크에 주로 사용
    - text/audio/시계열 데이터 같은 sequential data 처리에 많이 썼음 2017년도까지(그러다가 transformer에게 대체 당하긴 했지만....)
    - m1에서 training하는데 몇분~수십분 걸림 
5. LSTM (1997)
    - LSTM은 RNN에 "장기기억" 추가한거임. (더 오래 기억할 수 있게 gate들 달아놓음)
    - RNN의 vanishing gradient 문제 해결
    - 긴 시퀀스 학습 가능
    - Gate 메커니즘 도입
    - 현대 시퀀스 모델의 기초 
    - m1에서 training하는데 수십분 ~ 몇시간 걸림 
    - 이 이상 GAN부터는 로컬에서 돌리는 생각 포기하는게 좋음 ㅇㅇ 
6. GAN (2014)
    - "경쟁" 기능 추가된거임. Generator랑 Discriminator가 서로 싸움 ㅋㅋ
    - ex. Generator: "가짜 이미지 만들기 ㄱㄱ"
    -     Discriminator: "이거 가짜네 ㅋㅋ"
    -     Generator: "ㅅㅂ 더 잘 만들어야겠네"
    - 이런식으로 서로 발전하면서 성능 올라감 ㄹㅇ
    - Ian Goodfellow가 제안
    - 생성자와 판별자의 적대적 학습
    - 이미지 생성 능력 획기적 향상
    - Deep fake의 기술적 기반
7. Transformer (2017)
    - "주의집중(Attention)" 기능 추가됨
    - RNN: 앞에서부터 차례로 처리
    - Transformer: 한번에 다 보고 중요한거 찾음 (입력의 모든 부분을 한번에 보면서 중요도 계산)
    - 병렬처리도 가능해서 개빠름 ㅇㅇ
    - "Attention is all you need" 논문
    - Self-attention 메커니즘 도입
    - 병렬 처리 가능
    - 현대 대규모 언어 모델의 기반
8. BERT (2018)
    - Transformer에 "양방향" 기능 추가
    - GPT: 앞에서부터 읽음, BERT: 앞뒤 다 보고 이해함 -> 문맥 이해 개잘됨 ㅋㅋ
    - Transformer 기반 양방향 언어 모델
    - Pre-training, Fine-tuning 패러다임 확립
    - NLP 태스크 성능 대폭 향상
9. GPT (2018-현재)
    - transformer + 거대한 스케일 
    - 파라미터 개많이 넣어서 일반적인 지능 생김 
    - BERT: 특정 태스크 잘함 
    - GPT: 거의 모든 태스크 다 함 ㄷㄷ
    - Transformer 기반 대규모 언어 모델
    - Zero/Few-shot learning 능력
    - 범용 AI 시스템으로 발전


---\
Optimization technique의 진보 


1. Activation Functions
    - Sigmoid → ReLU → LeakyReLU 등
        1. sigmoid 잘쓰다가 문제점 발견: 깊은 레이어에서 기울기가 증발함 
        2. 그래서 ReLU로 바꿨더니 개잘됨. 음수를 다 0으로 만들어서 연산도 빠름 ㄹㅇ 
        3. LeakyReLU는 음수도 조금 살려둠 ㅇㅇ
    - Gradient vanishing 문제 해결
2. Regularization
    - Dropout: 랜덤으로 뉴런 몇개 꺼버림 ㅋㅋ
    - Batch Normalization: 정규화 해주는 레이어 추가한 것 
    - Layer Normalization: batch normalization이랑 좀 비슷한데 다름. transformer에서 많이 씀
3. Optimization
    - SGD → Momentum → Adam
        1. 걍 무식하게 내려감
        2. 이전 방향도 기억하면서 내려감(관성 있게 내려가서 local minimum 탈출 잘됨)
        3. adam은 성능 매우 좋음. 
    - Learning rate scheduling
        - 처음엔 크게크게 가다가 나중엔 미세조정 
    - Gradient clipping
        - 기울기 너무 크면 대충 잘라버림 ㅋㅋ
4. Architecture Search
    - ResNet의 Skip connection
        - 레이어 건너뛰어서 정보 전달함 ("야 이거 니가 처리 못하겠으면 나한테 패스해" 이런거임)
    - Inception의 Multi-scale processing
        - 여러 크기의 필터 동시에 씀
        - "야 이거 여러 관점에서 한번 봐봐" 이런거
    - AutoML과 NAS
        - AI가 AI 구조 찾아주는거임. 근데 컴퓨터 개많이 필요함 
