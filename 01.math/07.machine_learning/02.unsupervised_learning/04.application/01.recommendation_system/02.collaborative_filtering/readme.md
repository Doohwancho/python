# what 
jupyter notebook에 코드 흐름 순서 이해 해보자 

## step1) data gathering 

1. .csv에서 post/user/view 데이터 불러오기

## step2) preprocessing

2. post에서 카테고리가 A | B | C 이렇게 묶여있는걸 individual row로 변환(전처리)
3. merge(user, post)
    - 어떤 유저가 어떤 포스트를 언제 썼고, 그 포스트의 제목, 카테고리 등 정보가 있다.

## step3-1) user-to-user collaborative filtering approach

### 4-0. what 
1. 유저마다, 각 카테고리별로 거기에 속하는 posts를 몇개나 봤나 카운트 해서,
2. 각 유저 대비 235개 카테고리 별 posts 클릭 수 column을 235차원 벡터 삼아서,
3. 벡터 유사도를 cos theta 각도로 측정해서, 유사도가 높은 유저를 찾아
4. 그 유사한 유저가 본 최근 category를 추천한다. 


- Creating a matrix with users as rows and categories as columns. `[user_id, category_id]` -> `[88, 235]`

### 4-1. 유저 & 카테고리 매트릭스 만들기
```python
user_mat = [[] for i in range(len(users))]
for i in range(len(users)):
    for j in range(len(categories)):
        value = len(main[(main["user_id"]==users[i]) & (main["category"]==categories[j])])
        user_mat[i].append(value)
```

88 x 235 크기의 매트릭스를 만든다.\
각 셀은 "해당 유저가 해당 카테고리를 몇 번 클릭했는지"를 나타냅니다.\
예를들어 4 3 3 3 2 0 0...는 첫번째 유저가:

첫번째 카테고리를 4번 클릭\
두번째 카테고리를 3번 클릭\
세번째 카테고리를 3번 클릭... 했다는 뜻입니다


### 4-2. 희소 메트릭스로 변환 
```python
user_mat = csr_matrix(user_mat)

(0, 0)	4
(0, 1)	3
(0, 2)	3
(0, 3)	3
(0, 4)	2
(0, 11)	1
(0, 25)	2
(0, 26)	2
(0, 27)	2
(0, 32)	1
(0, 33)	2
(0, 34)	1
(0, 35)	1
(0, 48)	1
(0, 88)	1
(0, 89)	1
(0, 90)	1
(0, 91)	1
(0, 93)	1
(1, 0)	3
(1, 1)	3
(1, 2)	3
(1, 3)	3
(1, 4)	4
(1, 18)	2
:	:
```
대부분의 값이 0인 매트릭스를 효율적으로 저장하기 위해 변환합니다


### 4-3. 최근접 이웃 모델 설정
```python
model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=15)
```
matrix가 user x category 형태인데,\
행 = user:88명\
열 = category: 235개\

각 유저를 235차원 벡터로 보고 코사인 유사도를 측정한다.\
코사인 유사도란, 모든 벡터가 (0,0)에서 출발한다고 할 때,\
그 사이각 \theta를 측정하고, 그 값이 얼마나 서로 가까운지 측정,\
가까우면 서로 유사한 것.

예를 들어 유저 벡터가 이렇다면:\
```
유저1: [4,3,3,3,2,0,0,...]  # 235개의 카테고리에 대한 클릭 수
유저2: [3,4,3,2,1,0,0,...]
유저3: [0,0,0,0,0,5,4,...]
```

코사인 유사도는 이 벡터들 간의 각도를 계산합니다:

- 유저1과 유저2는 비슷한 카테고리를 비슷한 비율로 클릭했으므로 각도가 작음 → 높은 유사도
- 유저1과 유저3은 전혀 다른 카테고리를 클릭했으므로 각도가 큼 → 낮은 유사도

가장 유사한 15명을 찾는 부분:
```python
distances, indices = model.kneighbors(data[index], 15)
```

이 코드는:

타겟 유저의 벡터와 다른 모든 유저 벡터 사이의 코사인 유사도를 계산
유사도가 가장 높은 상위 15명을 선택

따라서 이 코드는 User-User Collaborative Filtering입니다:

Item-Item CF는 비슷한 아이템을 찾는 반면
이 코드는 비슷한 유저를 찾고 그 유저들이 좋아한 컨텐츠를 추천

예시:
1. 타겟유저: Visual Arts(4회), Graphic Design(3회) 클릭
2. 비슷한유저1: Visual Arts(3회), Graphic Design(4회), Fashion Design(2회) 클릭
3. 비슷한유저2: Visual Arts(5회), Graphic Design(2회), Watercolours(3회) 클릭
4. → 타겟유저에게 Fashion Design, Watercolours를 추천


cosine 유사도를 사용해서\
brute force로 (모든 경우의 수를 다 계산해서)\
가장 비슷한 15명의 이웃을 찾는 모델을 만듭니다


### 4-4. 추천 함수 
```python
def recommender(user_id, data=user_mat, model=model):
    model.fit(data)
    index = users.index(user_id)
    current_user = main[main['user_id']==user_id]
    distances, indices = model.kneighbors(data[index], 15)
    recomendation = []
    for i in indices[0]:
        user = main[main['user_id']==users[i]]
        for i in user['category'].unique():
            if i not in current_user['category'].unique():
                recomendation.append(i)
    return recomendation
```

입력된 user_id에 대해:

그 유저와 가장 비슷한 15명을 찾고\
그 15명이 본 카테고리 중에서\
입력된 유저가 아직 안 본 카테고리들을 추천해줍니다


### 4-5. 실제 추첨 결과
```python 
recommender(users[0])[:10]

['Fashion Portfoilio',
 'Fashion Design',
 'Watercolours',
 'Drawings',
 'Sketch Video',
 'Political Science',
 'Colonialism In India',
 'Legal Studies',
 'Labor Law',
 'Banking']
```


- nearest neighbor로 찾는데, neighbor 갯수는 15개고, 알고리즘은 brute-force 


## step3-2) hybrid 방식: content-based filtering + collaborative filtering
- content-based filtering approach 에 아이템 별 분석한 후에, collaborative 방식에 유저간 유사도 비교 추가


### 5-1. 먼저, content-based filtering -> 아이템 분석함 
- 행:카테고리  [열: posts(232개)] 1,0 matrix 만듬
- 카테고리별: 컬럼은 posts임. 
- 해당 카테고리에 속하는 post는 1, 안속하는 post면 0. 으로 해서,
- rows는 카테고리, columns는 모든 posts 232개로 함. 

```python
item_profiles = {}
for i in categories:
    item_profiles.update({i:[]})
    for j in posts:
        item_profiles[i].append(1) if i in list(main[main['post_id']==j]['category'].unique()) else item_profiles[i].append(0)    
```


ex)\
'Visual Arts' 카테고리에 속하는 post는 1, 안속하는 post면 0.
232개 posts에 대해서 다 함 
```
'Visual Arts': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```



### 5-2. 유저별로 클릭한 포스트 별 가중치 계산

```python
user_profiles = {}
# Filling the user_profiles
for i in users:
    # step1) 유저 별 데이터 수집: 특정 유저가 본 모든 카테고리와 포스트 목록을 가져옵니다
    # 행은 유저임
    user_profiles.update({i:[]})
    # 해당 유저의 정보를 main에서 가져옴 
    current_user = main[main['user_id']==i]
    # 해당 유저가 본 모든 유니크한 카테고리를 리스트로 뽑음 
    current_user_categories = list(current_user['category'].unique())
    # 해당 유저가 본 모든 유니크한 posts를 리스트로 뽑음 
    current_user_post = list(current_user['post_id'].unique())
    
    # step2) 카테고리의 가중치를 계산 
    category_weight = {}
    # 행: 유저, 열: posts 갯수 232개
    result_vector = np.array([0 for i in range(len(posts))])
    # 유저가 본 카테고리를 돌면서, 
    for j in current_user_categories:
        category_weight.update({j:0})
        # 각 카테고리가 몇 번 나타났는지 카운트
        for k in list(current_user['category']):
            if j==k:
                category_weight[j]+=1
        # 전체 본 포스트 수로 나누어 정규화
        category_weight[j] = category_weight[j]/len(current_user_post)
        # Now we have calculated our weights, Now we will calculate user-profile
        result_vector = result_vector+ (category_weight[j]*item_profiles[j])
        # 예시) 유저가 총 10개의 포스트를 봤고
        # 그 중 'Business' 카테고리가 4번 나왔다면
        # Business의 가중치는 4/10 = 0.4가 됩니다
    user_profiles[i] = result_vector/len(current_user_post)
```

이 유저id에 대한 모든 포스트에 대한 숫자가 이렇게 나옴 

예시)
1. 유저가 총 10개의 포스트를 봤고
2. 그 중 'Business' 카테고리가 4번 나왔다면
3. Business의 가중치는 4/10 = 0.4가 됩니다
4. 근데 포스트 7,8이 둘다 'Business' 카테고리에 속해있으면, 둘 다 똑같은 가중치 부여됨 

```
print(user_profiles['5df49b32cc709107827fb3c7'])

232
[0.12396694 0.         0.         0.         0.00826446 0.00826446
 0.         0.00826446 0.00826446 0.         0.         0.
 0.         0.         0.         0.         0.         0.04132231
 0.         0.15702479 0.         0.00826446 0.09090909 0.02479339
 0.03305785 0.         0.         0.02479339 0.01652893 0.01652893
 0.01652893 0.01652893 0.         0.05785124 0.07438017 0.
 0.00826446 0.         0.         0.         0.         0.
 0.08264463 0.         0.01652893 0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.04132231 0.04132231 0.         0.00826446
 0.         0.         0.         0.02479339 0.00826446 0.
 0.07438017 0.         0.         0.03305785 0.         0.
 0.         0.         0.09917355 0.         0.09917355 0.
 0.         0.03305785 0.03305785 0.         0.         0.02479339
 0.02479339 0.         0.         0.         0.         0.03305785
 0.02479339 0.12396694 0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.01652893 0.03305785 0.         0.         0.         0.
 0.03305785 0.         0.04958678 0.03305785 0.04958678 0.
 0.         0.         0.         0.         0.01652893 0.
 0.         0.         0.         0.         0.05785124 0.04958678
 0.         0.         0.         0.         0.04958678 0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.05785124 0.         0.         0.         0.         0.
 0.         0.         0.02479339 0.         0.         0.
 0.04132231 0.         0.         0.         0.         0.
 0.         0.         0.         0.         0.         0.
 0.         0.         0.02479339 0.         0.         0.02479339
 0.         0.         0.         0.         0.         0.
 0.09917355 0.         0.         0.00826446 0.         0.
 0.         0.01652893 0.         0.        ]
```

### 5-3. 추천 함수
위에 유저간 모든 post에 대해서 카테고리 중요도/가중치 계산했잖아?\
그걸 각 유저마다 1개의 벡터로 삼아서,\
각 벡터의 유사도를 계산함.\
젤 가까운 벡터의 유저의 카테고리 추천하는 것

유저간 유사도 계산 후 가장 유사한 유저의 카테고리 추천한다는 점에서 
Collaborative Filter approach이다.

```python
from sklearn.metrics.pairwise import cosine_similarity


# 유저 ID를 입력하면 그 유저에게 맞는 포스트를 추천해주는 함수
def recommender1(user_id, user_profiles = user_profiles, item_profiles=item_profiles):
    # step1) 각 카테고리와 유저의 취향이 얼마나 비슷한지 계산합니다
    # 예를들어, 유저가 'Business' 글을 많이 봤다면 'Business' 카테고리와의 유사도가 높게 나옵니다.
    # 반면 'Art' 글을 전혀 안 봤다면 유사도가 낮게 나옵니다
    # 유사도 구하는건 cos theta 각도가 얼마나 서로 가까운지로 계산
    similarity = {}
    for i in item_profiles:
        similarity.update({i:cosine_similarity(user_profiles[user_id].reshape(1, -1), item_profiles[i].reshape(1, -1))})

    # step2) 해당 유저와 가장 유사도가 높은 카테고리 순서대로 정렬한다.
    # 예: [(Business, 0.9), (Finance, 0.8), (Art, 0.1)]
    sorted_similarity = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    
    
    # step3) 유저별로 어떤 post를 봤는지 리스트로 뽑는다. 
    user_posts = list(main[main['user_id']==user_id]['post_id'].unique())

    # displaying users viewed posts and categories
    print("해당 유저가 본 posts들:{}".format(user_posts))
    print("")
    print("해당 유저가 본 category들:{}".format(list(main[main['user_id']==user_id]['category'].unique())))
    print("")
    
    # step4) create recomendation list ([카테고리: post])
    # 유저가 아직 안 본 포스트 중에서
    # 유사도가 높은 카테고리의 포스트를 추천 목록에 추가합니다 (20개 찰때까지)
    recommendations = []
    for i in sorted_similarity:
        category_posts = list(main[main['category']==i[0]]['post_id'].unique()) #카테고리별 posts들
        for j in category_posts:
            if j not in user_posts: # 유저가 아직 안 본 포스트 중에서
                recommendations.append([i[0], j]) # 유사도가 높은 카테고리의 포스트를 추천 목록에 추가합니다
        # we will recommend top 20 posts to the user
        if len(recommendations)==20:
            break
    for i in recommendations:
        print(i)
```

결과 
```python
recommender1(users[1]);

['Illustration', '5ec7aafbec493f4a26558857']
['Illustration', '5ec7ad1aec493f4a26558869']
['Illustration', '5ec7abfdec493f4a26558860']
['Illustration', '5e5b59cbd701ab08af792b90']
['Illustration', '5dbc622a99cbb90e4339c7f6']
['Illustration', '5e2d516fc85ab714a7da66dd']
['Illustration', '5e9895e8a3258347b42f2ba7']
['Illustration', '5e979637a3258347b42f2b1e']
['Illustration', '5e4ba3a9f5561b1994c8e392']
['Illustration', '5e5bb3eed701ab08af792bfa']
['Visual Arts', '5ed2378276027d35905cc6b5']
['Visual Arts', '5e2d4737c85ab714a7da66d9']
['Visual Arts', '5ecb7567eaff6b0c3a58a4cf']
['Visual Arts', '5e5b59cbd701ab08af792b90']
['Visual Arts', '5e7a0d85cfc8b713f5ac7d77']
['Visual Arts', '5e2d4d63c85ab714a7da66db']
['Visual Arts', '5dbc622a99cbb90e4339c7f6']
['Visual Arts', '5eb1551e10426255a7aaa003']
['Visual Arts', '5eb158d410426255a7aaa011']
['Visual Arts', '5eb153ca10426255a7aa9fff']
['Visual Arts', '5e2d516fc85ab714a7da66dd']
['Visual Arts', '5e7f39a3a3258347b42f2151']
['Visual Arts', '5e94bf78a3258347b42f2925']
['Visual Arts', '5e94452ea3258347b42f282a']
['Visual Arts', '5e81c257a3258347b42f22f0']
['Visual Arts', '5e5bb3eed701ab08af792bfa']
['Graphic Design', '5e1029f22a37d20505da2a79']
['Graphic Design', '5ecb7567eaff6b0c3a58a4cf']
['Graphic Design', '5e5b59cbd701ab08af792b90']
['Graphic Design', '5e2d4d63c85ab714a7da66db']
['Graphic Design', '5dbc622a99cbb90e4339c7f6']
['Graphic Design', '5e2d516fc85ab714a7da66dd']
['Graphic Design', '5da745b6019399436815c4cd']
['Graphic Design', '5e81c257a3258347b42f22f0']
['Graphic Design', '5e81bf2fa3258347b42f2244']
['Graphic Design', '5e5bb3eed701ab08af792bfa']
['Artistic design', '5ed0007a76027d35905cc0ea']
['Artistic design', '5e2d4737c85ab714a7da66d9']
: :
```