# A. Meta

## a. key to effectively learning
---
goal

build a vector map\
전체 다 100% 이해하는게 아니라, 중요부분 위주로 큰 그림 파악하는 것.\
요리로 비유하면 요리를 미리 다 해놓는게 아니라, 중요 부분만 반조리 해 놓고 저장해 놓는 것.\
개발로 치면 뼈대 library module을 여러개 수집해 놓는 것.

---
How

1. build core branch from core root
2. add a few core concepts to each branch
3. add details to each concepts, connect concepts with each other by relating

---
오해

1. you are an engineer, not researcher or scholar. you don't need details of what and why. you just need how and little bit of what & why just enough to understand concepts and twig a little
2. you're not trying to load every concepts of calculus/algebra/statistics to your brain. you only need ones used for machine learning.
3. collecting many math concept is only half of math skills. another half is to think in math for hours to solve problem.
4. ml engineer는 모델 개발을 하지 않는다. statistics/linear algebra보다 더 중요한건, 그 모델에 feed-in할 데이터를 이해하는 능력이라 applied statistics가 더 중요하다.
5. 수능수학, 문제집 풀듯이 어떤 방정식을 외우고 그 방정식에 빠진 부분에 대한 답을 패턴 매칭으로 찾는걸 연습하는게 아니다. 컨셉/본질 이해 후 real world problem 적용을 연습하는 것.
6. most people dont think simple enough. go all the way down to the most fundamental level, think of platonically perfect, ideal goal, and then think how to get there from the most fundamental level.
7. 그림 인쇄할 때, 프린트기처럼 초고해상도로 머리부터 순서대로 발끝까지 그리는게 아니라, 먼저 스케치로 큰 뭉텅이 그리고, 조금씩 윤곽을 잡으며 디테일을 채워나가는 식으로 배운다.
	- 수학배울 때, 처음부터 필수 방정식 암기 및 문제풀기 반복학습 위주로 하지 말고, 먼저 데카르트 좌표계에 visualize 해서 컨셉부터 이해한 후에, 방정식을 배우고, 관련 문제 풀기 및 증명


## b. key to effectively learning math

### 1. Q. how to build a vector map effectively?

1. knowledge tree에서 fundamental(most connected node)에서 출발 (ex. decartian coordinate) - first principle thinking
    - decartian coordinate
    - axiom on each subject을 염두, 배우는 모든 것이 이 원리에 모두 어긋나지 않는지 확인
2. platonian theoretically perfect, ideal goal을 염두해가며 거기에 필요한 지식을 top down으로 나열 (ex. transformer 배우는데 필요한 calculus/linear_algebra/statistics concepts 나열)
	- 지식의 우선순위를 선별하는 것. 각 과목의 모든 노드의 what/why/how를 depth 10까지 다 배우면 너무 비효율. 어짜피 안쓸 노드는 잠잘 떄 gc됨
    - ex. transformer (attention mechanism)
3. 각 과목의 뼈대, schema, branch from knowledge tree를 세움. visualize in 1 picture
4. goal에 필요한 지식 중점으로 fundamental로부터 빌드업을 bottom up 하는데, 그게 fundamental과 모두 연결되어야 함. 연결될 땐, axiomatic base rule에 모든게 어긋나지 않으면서 착착 쌓여야 함
5. 언어가 1개로 통일할 수록 좋다. normalization 해야 context switching에서 일어나는 cost가 없다.
	- html canvas w/ js over html + python matplotlib + r + etc
6. feedback speed가 빠를 수록 좋다 + accurate + visualization 일 수록 좋다. (claude3 토큰 리셋 시간 5시간)
7. accumulate in a sorted manner for easy read() and update() later for experimentation and adding to the knowledge tree(single source + 압축)
    - 학(개념): obsidian
    - 습(working code): github
        - single source이면 repo 옮길 때 context switching cost가 없다
8. 예측 based learning
    - textbook index 순차적으로 배우는게 아니라, 내 머릿속에서 내가 원하는 방향으로 예측하면서 + w/ ai로 배우기(일종의 공책 수학)
	- 점을 찍고 넓히는 방향이 ADHD도 배우기 좋은 학습방법


### 2. Q. how to 체화/습득 using vector map?

#### case1) 개념 학습방법
1. 수학적 능력은 수학개념, 패턴 습득도 있지만, 깊게 논리적 정합성을 깨지 않으면서 생각하는 것이다. 이를 위해 30분 ~ 1시간 짜리 증명(중요도 순 나열 from [proofwiki](https://proofwiki.org/wiki/Main_Page)), 누워서
    - proofwiki for 증명

#### case2) 체화, 습득 방법
2. challenges in project form(carefully level-designed by essential-ness)
	- level = prev_level + 1(ex. adding a feature or 약간 응용)
	- readme에 설명 달기(초딩도 이해하기 쉽게)
	- devide and conquer로 큰 프로젝트의 sub module 각개격파식도 좋다.



### 3. ml engineer job description for top-down 지식 우선순위 정렬
https://www.linkedin.com/jobs/search/?currentJobId=4021946798&distance=25.0&geoId=105149562&keywords=machine%20learning%20recommendation&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true


- transformer
	1. matrix multiplication
	2. softmax for encoding from vectors to probability 0~1
	3. gradients for optimization in multi-variable calculus: activation functions like ReLU

### 4. project list top down for deep learning - multi-layer-perceptron(MLP)
1. build single perceptron
2. build a loss function
3. gradient descent
4. activation function
5. back propagation
6. sum it up, build MLP



# B. Goal

build vector map of math for machine learning bottom up



# C. Subjects


a. number_theory\
b. geometry\
c. calculus\
d. algebra\
e. statistics\
f. physics\
g. machine_learning\
	1. sp(supervised_learning)
		1. reg(regression)
			1. linear_regression
			2. overfitting_and_regularization
			3. gradient_descent
		2. cls(classification)
			1. logistic_regression
			2. SVM
			3. decision_tree
			4. KNN
				1. recommendation_system
	2. us(unsupservised_learning)
		1. cl(clustering)
			1. k_means_clustering
		2. dr(dimension_reduction)
			1. PCA
		3. ad(anomaly_detection)
	3. rl(reinforcement_learning)
h. deep_learning\
i. information_theory\
j. algorithm




# D. Concepts


a-1. euler's formula on imaginary number :white_check_mark:\
a-2. 허수와 euler's formula를 이용한 2차원 벡터, object 회전 :white_check_mark:\
a-3. log & exponential function are inverse :white_check_mark:\
a-4. e :white_check_mark:

b-1. sin cos tan :white_check_mark:\
b-2. sin cos tan + sec csc cot :white_check_mark:\
b-3. sin cos tan + sec csc cot with animation :white_check_mark:\
b-4. perpendicular line to the point on circle :white_check_mark:\
b-5. fundamental trig model :white_check_mark:\
b-6. wave :white_check_mark:\
b-7. 푸리에변환 :white_check_mark:\
b-8. 푸리에변환으로 audio 유효 Hz(주파수) visualize :white_check_mark:\
b-9. 푸리에변환으로 image compression :white_check_mark:

g-ml-sp-cls-knn-rec-1.collaborative filtering approach :white_check_mark:
