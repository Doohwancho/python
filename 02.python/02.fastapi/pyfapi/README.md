# A. what 
CRUD app using fastapi + mongodb\
+ jwt auth feature

## a-1. techstacks 
- **[FastAPI](https://fastapi.tiangolo.com/)**: web framework for python 
  Python 3.6+ based on standard Python type hints.
- **[MongoDB](https://www.mongodb.com/)**: A NoSQL database for storing user data.
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI web server implementation for Python. (.py를 돌려주는 fastapi에 응답을 http response로 바꿔줌)
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: data validation lib for python
  Python.
- **[Motor](https://motor.readthedocs.io/en/stable/)**: async connector to mongodb
- **[Beanie](https://beanie-odm.dev/)**: mongodb버전의 orm 인가 봄
- **[Docker](https://www.docker.com/)**: 
- **[Oauth2](https://fastapi.tiangolo.com/tutorial/security)**: OAuth2 with Password (and hashing), Bearer with JWT
  tokens.


## a-2. project 이해

### a-2-1. RESTful api docs
http://localhost:8000/api/v1/docs

### a-2-2. mongodb
프로젝트 시작 시, 기본 collections 2개 user_role과 app_user에 \
admin user 만들어주는 코드가 \
user_migration.py

```
show dbs
use app (database 이름이 "app"으로 생성됨.)

app> show collections
app_role
app_user
app> db.app_user.find()
[
  {
    _id: ObjectId('67ece1e695c0fbebbed9c895'),
    user_id: '47ba11c9-76d3-452c-a5cd-f4b7aec5459a',
    username: 'admin',
    first_name: 'Admin',
    last_name: 'User',
    email: 'admin@localhost.com',
    hashed_password: '$2b$12$j1VVCvevM4muJmDE3fdcl.RD1pZypYZTLfKszXIbTsukfi.ntaOHG',
    is_active: true,
    roles: [ 'admin' ],
    created_by: 'system',
    created_date: ISODate('2025-04-02T07:06:14.456Z'),
    last_updated_by: 'system',
    last_updated_date: ISODate('2025-04-02T07:06:14.456Z'),
    age: null
  }
]
app> db.app_role.find()
[
  { _id: ObjectId('67ece1e595c0fbebbed9c893'), name: 'admin' },
  { _id: ObjectId('67ece1e595c0fbebbed9c894'), name: 'user' }
]
app>
```

### a-2-3. schemas (pydantic lib)
http://localhost:8000/api/v1/docs 에 하단부 보면 스키마 나온다. 

pydantic library(data validation lib)로 class 만들면, 얘로 데이터 검증한다. 

example)
```py
from pydantic import BaseModel


class LoginVM(BaseModel):
    """Login schema for authentication"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "plain-text-password"
            }
        }
```

command + shift + f 로 스키마가가 각각 어떤 파일에 있는지 보자.

### a-2-4. motor로 connect to mongodb
app/conf/env/db_config.py에서 init_db() 봐봐 
```py
client = AsyncIOMotorClient(mongodb_uri)
```


### a-2-5. beanie로 orm마냥 entity 정의 

ex. user_entity.py
```py
from datetime import datetime

from beanie import Document
from pydantic import EmailStr


class User(Document):
    user_id: str | None = None
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str | None = None
    is_active: bool | None = None
    roles: list[str] | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    last_updated_by: str | None = None
    last_updated_date: datetime | None = None
    age: int | None = None
```



# B. how 

## b-1. how to setup?

### step1) 먼저 파이선 3.10 이상 버전으로 세팅 
```
asdf local python 3.11.5 (3.10버전 이상이면 무관)
```

### step2) virtual env setting 
```
python3 -m venv venv
source venv/bin/activate
```

### step3) download requirements.txt into virtual env
```
pip install -r requirements.txt
```

### step4) .env setting 
```
cp .env.default .env.dev
cp .env.default .env.prod
```

### step5) mongodb setting
goal: .env.dev에 적힌대로 mongodb에 database 만들어줘야 함 

```.env.dev
DB_DATABASE_NAME="pyfapi"
DB_HOST="127.0.0.1"
DB_PORT="27017"
DB_USERNAME="root"
DB_PASSWORD="root123"
```

오해하면 안되는게, 실제로 mongodb에는 "app"이라는 이름으로 db가 만들어짐. pyfapi가 아니라. 


#### step5-1) download mongodb on mac m1
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/

#### step5-2) mongodb 접속
```
brew services start mongodb-community

mongosh
```

#### step5-3) create root user 
```
test> use admin
switched to db admin
admin> db.createUser(
...   {
...     user: "root",
...     pwd: "root123",
...     roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
...   }
... )
{ ok: 1 }
admin>
```

#### step5-4) db 생성
```
admin> use pyfapi
switched to db pyfapi
pyfapi>
```

#### step5-5) restart mongodb
```
brew services restart mongodb-community
```


### step6) 실행 
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env.dev

http://0.0.0.0:8000
```


### step7) mongodb에 저장된 유저 확인
```
use app 

app> db.app_user.find()
[
  {
    _id: ObjectId('67ece1e695c0fbebbed9c895'),
    user_id: '47ba11c9-76d3-452c-a5cd-f4b7aec5459a',
    username: 'admin',
    first_name: 'Admin',
    last_name: 'User',
    email: 'admin@localhost.com',
    hashed_password: '$2b$12$j1VVCvevM4muJmDE3fdcl.RD1pZypYZTLfKszXIbTsukfi.ntaOHG',
    is_active: true,
    roles: [ 'admin' ],
    created_by: 'system',
    created_date: ISODate('2025-04-02T07:06:14.456Z'),
    last_updated_by: 'system',
    last_updated_date: ISODate('2025-04-02T07:06:14.456Z'),
    age: null
  }
]
app> db.app_role.find()
[
  { _id: ObjectId('67ece1e595c0fbebbed9c893'), name: 'admin' },
  { _id: ObjectId('67ece1e595c0fbebbed9c894'), name: 'user' }
]
```

### step8) 어떤 api list가 있는지 보기 
```
http://localhost:8000/api/v1/docs
http://localhost:8000/api/v1/redoc
```

### step9) login해서 access token 받기

access token 안받고 

```
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

그러면 access token을 받음 
```
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJ1c2VyX2lkIjoiNDdiYTExYzktNzZkMy00NTJjLWE1Y2QtZjRiN2FlYzU0NTlhIiwiZW1haWwiOiJhZG1pbkBsb2NhbGhvc3QuY29tIiwiZXhwIjoxNzQ4NzY1MDQyfQ._5F819265j6zZHZR9Q_Y1F6uJE4X4dNDSEE5-LWMyw8","token_type":"bearer"}%
```

### step10) access token 첨부해서 http request 보내기

ex1) 내가 로그인한 유저의 정보로 가져오기 
```
curl -X GET "http://127.0.0.1:8000/api/v1/account/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJ1c2VyX2lkIjoiNDdiYTExYzktNzZkMy00NTJjLWE1Y2QtZjRiN2FlYzU0NTlhIiwiZW1haWwiOiJhZG1pbkBsb2NhbGhvc3QuY29tIiwiZXhwIjoxNzQ4NzY1MDQyfQ._5F819265j6zZHZR9Q_Y1F6uJE4X4dNDSEE5-LWMyw8"
```

result
```
{"user_id":"47ba11c9-76d3-452c-a5cd-f4b7aec5459a","sub":"admin","email":"admin@localhost.com","scopes":["admin"],"exp":1748765042.0,"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJ1c2VyX2lkIjoiNDdiYTExYzktNzZkMy00NTJjLWE1Y2QtZjRiN2FlYzU0NTlhIiwiZW1haWwiOiJhZG1pbkBsb2NhbGhvc3QuY29tIiwiZXhwIjoxNzQ4NzY1MDQyfQ._5F819265j6zZHZR9Q_Y1F6uJE4X4dNDSEE5-LWMyw8"}%
```

ex2) 모든 사용자의 정보 가져오기 
```
curl -X GET "http://127.0.0.1:8000/api/v1/users" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJ1c2VyX2lkIjoiNDdiYTExYzktNzZkMy00NTJjLWE1Y2QtZjRiN2FlYzU0NTlhIiwiZW1haWwiOiJhZG1pbkBsb2NhbGhvc3QuY29tIiwiZXhwIjoxNzQ4NzY1MDQyfQ._5F819265j6zZHZR9Q_Y1F6uJE4X4dNDSEE5-LWMyw8"

[{"user_id":"47ba11c9-76d3-452c-a5cd-f4b7aec5459a","username":"admin","first_name":"Admin","last_name":"User","email":"admin@localhost.com","is_active":true,"roles":["admin"],"created_by":"system","created_date":"2025-04-02T07:06:14.456000","last_updated_by":"system","last_updated_date":"2025-04-02T07:06:14.456000"}]%
```


### step11) home page 접속 
```
http://localhost:8000/
```

