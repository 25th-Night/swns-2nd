# 📢 소셜 네트워크 서비스 개발 프로젝트 2차

### 🔔 참고
> 📌 <u>**[소셜 네트워크 서비스 개발 프로젝트 1차](https://github.com/likelion-backend-6th/TrackProject_1_ChoiSeonWoo)</u> repository** <br>
> 📌 <u>**[소셜 네트워크 서비스 개발 프로젝트 2차](https://github.com/likelion-backend-6th/TrackProject_2_ChoiSeonWoo)</u> repository** <br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; → `k8s` 작업부터 이어서 진행하기 위해 `미러링` 를 통해 기존 작업 코드 및 커밋 내역을 복제후 진행하였음을 참고해주세요.

<br>

## 🗒️ 프로젝트 개요
- Python, Django를 이용한 소셜 네트워크 서비스 애플리케이션 개발
- Django REST Framework, drf-spectacular를 이용한 백엔드 API 개발
- Docker를 이용한 컨테이너 형태로의 배포
- GitHub Actions를 이용한 CICD pipeline 구축
- Terraform을 이용한 IaC 구현
- NCloud에서 로드밸런서를 활용한 클라우드 방식의 배포

<br>

## 📖 프로젝트 주요 기능

### 0️⃣ 권한 및 정책

- 사용자 계정은 관리자와 일반 사용자로 구분되어 API에 대한 접근 권한이 부여됨.
- 관리자 계정은 모든 기능을 이용 가능.
- `팔로우`, `좋아요`를 제외한 나머지 데이터의 삭제 요청은 `is_active` 필드 값을 `False`로 변경하는 것으로 처리됨.

### 1️⃣ 유저

- JWT를 이용한 토큰 인증
- 사용자는 전체 혹은 나를 제외한 유저 목록 조회 가능
- 사용자는 나를 제외한 유저 목록 조회 시, 각 유저의 프로필 정보도 확인 가능
- 사용자는 내 정보 조회/수정/삭제 가능
- 사용자는 조건에 따른 유저 정보 검색 가능

### 2️⃣ 프로필

- 사용자는 전체 혹은 나를 제외한 프로필 목록 조회 가능
- 사용자는 전체 혹은 나를 제외한 프로필 목록 조회 시, 해당 프로필의 유저 정보도 확인 가능
- 사용자는 내 프로필 조회/생성/수정 가능
- 사용자는 프로필에 사진을 추가 가능
- 사용자는 조건에 따른 프로필 검색 가능

### 3️⃣ 팔로우

- 사용자는 다른 사용자를 `팔로우` 및 `언팔로우` 가능
- 사용자는 following (내가 `팔로우`한 사람들) 목록 확인 가능
- 사용자는 follower (나를 `팔로우`한 사람들) 목록 확인 가능
- 사용자는 `팔로우`한 사람들이 올린 게시글을 모아 볼 수 있음
- 사용자는 나를 제외한 유저 목록 조회 시, 해당 유저에 대한 `팔로우` 여부 확인 가능

### 4️⃣ 게시글
- 사용자는 전체 게시글 혹은 나를 제외한 유저의 게시글 목록 조회 가능
- 사용자는 본인의 게시글 조회/수정/삭제 가능
- 게시글 작성 시, `임시저장`/`공개` 상태 지정이 가능
- `임시저장` 상태의 게시글은 사용자 본인만 조회 가능
- 사용자는 본인이 작성한 게시글을 모아 볼 수 있음
- 사용자는 본인이 팔로우한 사람들의 게시글 모아보기 가능
- 사용자는 조건에 따른 게시글 검색 가능

### 5️⃣ 댓글
- 사용자는 특정 게시글에 달린 댓글 목록 조회 가능
- 사용자는 댓글 조회/생성/수정/삭제 가능
- 사용자는 본인이 작성한 댓글을 모아 볼 수 있음
- 사용자는 조건에 따른 댓글 검색 가능

### 6️⃣ 이미지
- 사용자는 게시글에 달린 이미지 목록 확인 가능
- 사용자는 게시글에 이미지를 조회/추가/삭제 가능
- 사용자는 본인이 업로드한 이미지를 모아보기 가능

### 7️⃣ 좋아요
- 사용자는 게시글에 `좋아요` 누르기/취소 가능
- 사용자는 댓글에 `좋아요` 누르기/취소 가능
- 사용자는 본인이 `좋아요` 누른 게시글을 모아보기 가능
- 사용자는 본인이 `좋아요` 누른 댓글을 모아보기 가능
- 게시글 혹은 댓글 조회 시, `좋아요` 수 확인 가능

<br>

## 🏤 Infra

### 🖥 GitHub Repository

**코드 및 버전 관리**

- 작업 환경 별 Branch 분리

| Branch | 용도                       | Merge to         |
|-------|--------------------------|------------------|
| `feat`  | 기능 개발 및 테스트              | `develop` branch |
| `develop` | 정상 동작 확인 및 버그 수정         |  `main` branch   |
| `main`  | 서비스 배포                   | -                |

<br>

### 🚥 GitHub Actions

**지속적 통합 (CI) 및 지속적 배포 (CD)를 구축**

**1️⃣ CI**

| 분류    | 설명                                                                  |
|-------|:--------------------------------------------------------------------|
| 조건    | `feature` 혹은 `fix` 브랜치로 push되었을 때                                   |
| 진행    | - 테스트 진행 <br> - 테스트 정상 완료 시 NCR로 docker image `build` & `push`      |
| 확인 대상 | - 모든 파일과 디렉토리 <br> - 단, `infra` 및 `script` 디렉토리 및 그 하위 파일과 디렉토리은 제외 |

**2️⃣ CD to staging**

| 분류    | 설명                                                                                                                                               |
|-------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| 조건    | - `feature` 브랜치에서 `develop` 브랜치로의 `Pull Request`가 완료되어 코드가 `merge` 되었을 때                                                                         |
| 진행    | - `staging` stage의 `django` 서버로 배포 <br> - 배포는 NCR docker image 를 통한 컨테이너 형태로 진행                                                                  |
| 확인 대상 | - 모든 파일과 디렉토리 <br> - 단, `docker` , `infra` , `script` 디렉토리 및 그 하위 파일과 디렉토리를 제외 <br> - .github/workflows 내 자기 자신(CD_dev.yaml)을 제외한 다른 워크플로우 파일 제외 |

**3️⃣ CI and CD to production**

| 분류    | 설명                                                                                                         |
|-------|:-----------------------------------------------------------------------------------------------------------|
| 조건    | - 새로운 버전이 Release되었을 때                                                                                     |
| 진행    | - NCR로 release 버전의 docker image `build` & `push` <br> - `prod` stage의 `django` 서버에 해당 버전의 docker image를 배포 |


<br>

### ⛵ Docker
**컨테이너화된 애플리케이션 이미지를 생성 및 관리**

- 이미지 버전 관리를 위하여 조건에 따라 `TIMESTAMP` Ver. 과 `latest` Ver. , `Release` Ver. 으로 docker image를 생성
- 생성된 이미지는 클라우드 환경(NCloud Container Registry)에 Push
- `staging` stage로의 배포 시 `Latest` Ver. 이미지를 사용하며, 롤백 혹은 로그 확인 시 `TIMESTAMP` Ver. 이미지를 사용
- `prod` stage로의 배포 시 `release` Ver. 이미지를 사용하며, 롤백 혹은 로그 확인 시에도 각 `release` Ver. 이미지를 사용

<br> 

### 💻 Terraform

**클라우드 환경에서 인프라를 코드로 관리 및 프로비저닝**

**Shared Module**
- AWS `S3` : S3 Object Storage 리소스 생성
- NCP `Network` : VPC, Subnet 리소스 생성
- NCP `Server` : Access Group, Network Interface, Init Script, Server 및 관련 리소스 생성
- NCP `LoadBalancer` : Target Group, LoadBalancer 및 관련 리소스 생성

**Child Module**
- `Staging` : `develop` 브랜치 에서 관리되는 코드를 사용하여 `스테이징` 환경의 클라우드 리소스를 배포
- `Prod` :  `main` 브랜치 에서 관리되는 코드를 사용하여 `프로덕션` 환경의 클라우드 리소스를 배포

<br>

### ⛅ AWS, NCP

**클라우드 리소스를 활용하여 애플리케이션 서비스를 SaaS 형태로 제공**


<br>

## 🪓 주요 설치 패키지/모듈

|    종류     |                이름                 |    버전    |
|:---------:|:---------------------------------:|:--------:|
| Language  |            **python**             |   3.11   |
| Framework |            **Django**             |  4.2.4   |
| Database  |          **PostgreSQL**           |    13    |
|  Library  |           **gunicorn**            |  21.2.0  |
|  Library  |        **psycopg2-binary**        |  2.9.7   |
|  Library  |      **djangorestframework**      |  3.14.0  |
|  Library  | **djangorestframework-simplejwt** |  5.3.0   |
|  Library  |      **drf-nested-routers**       |  0.93.4  |
|  Library  |        **drf-spectacular**        |  0.26.4  |
|  Library  |    **drf-spectacular-sidecar**    | 2023.9.1 |
|  Library  |             **boto3**             | 1.28.44  |
|  Library  |        **django-storages**        |   1.14   |
|  Library  |         **django-filter**         |   23.2   |
|  Library  |         **django-taggit**         |  4.0.0   |
|  Library  |            **Pillow**             |  10.0.0  |
|  Library  |             **Faker**             |  19.6.1  |

<br> 

## 📋 Database Schema

### 💾 User

| Column Name      | Data Type               | Constraint                                                       |
|------------------|-------------------------|------------------------------------------------------------------|
| **id**           | INTEGER                 | PRIMARY KEY                                                      |
| **email**        | VARCHAR(max_length=100) | UNIQUE , NOT NUL                                                 |
| **fullname**     | VARCHAR(max_length=30)  | NOT NULL                                                         |
| **phone**        | VARCHAR(max_length=30)  | UNIQUE,  NOT NULL                                                |
| **password**     | VARCHAR(max_length=100) |                                                                  |
| **is_admin**     | BOOLEAN                 | NOT NULL, DEFAULT : False                                        |
| **is_superuser** | BOOLEAN                 | NOT NULL, DEFAULT : False                                        |
| **is_active**    | BOOLEAN                 | NOT NULL, DEFAULT : True                                         |
| **last_login**   | DATETIME                | NULL                                                             |
| **created_at**   | DATETIME                | DEFAULT CURRENT_TIMESTAMP, NOT NULL                              |
| **updated_at**   | DATETIME                | DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP, NOT NULL |

### 💾 Profile

| Column Name    | Data Type               | Constraint                                                       |
|----------------|-------------------------|------------------------------------------------------------------|
| **id**         | INTEGER                 | PRIMARY KEY                                                      |
| **user**       | INTEGER                 | FOREIGN KEY REFERENCES User(user_id), NOT NULL                   |
| **nickname**   | VARCHAR(max_length=30)  | UNIQUE, NOT NULL                                                 |
| **birthday**   | DATE                    | NOT NULL                                                         |
| **image_url**  | VARCHAR(max_length=255) | NULL                                                             |
| **is_public**  | BOOLEAN                 | NOT NULL, DEFAULT : True                                         |
| **is_active**  | BOOLEAN                 | NOT NULL, DEFAULT : True                                         |
| **created_at** | DATETIME                | DEFAULT CURRENT_TIMESTAMP, NOT NULL                              |
| **updated_at** | DATETIME                | DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP, NOT NULL |

### 💾 Follow

| Column Name    | Data Type | Constraint                                     |
|----------------|-----------|------------------------------------------------|
| **id**         | INTEGER   | PRIMARY KEY                                    |
| **user_from**  | INTEGER   | FOREIGN KEY REFERENCES User(user_id), NOT NULL |
| **user_to**    | INTEGER   | FOREIGN KEY REFERENCES User(user_id), NOT NULL |
| **created_at** | DATETIME  | DEFAULT CURRENT_TIMESTAMP, NOT NULL            |

### 💾 Post

| Column Name    | Data Type               | Constraint                                                       |
|----------------|-------------------------|------------------------------------------------------------------|
| **id**         | INTEGER                 | PRIMARY KEY                                                      |
| **title**      | VARCHAR(max_length=250) | NOT NULL                                                         |                                                                  |
| **slug**       | VARCHAR(max_length=250) | UNIQUE, NOT NULL                                                 |
| **author**     | INTEGER                 | FOREIGN KEY REFERENCES User(user_id), NOT NULL                   |
| **body**       | TEXT                    | NOT NULL                                                         |
| **status**     | INTEGER                 | NOT NULL, DEFAULT : 0                                            |
| **is_active**  | BOOLEAN                 | NOT NULL, DEFAULT : True                                         |
| **publish**    | DATETIME                | DEFAULT CURRENT_TIMESTAMP,NOT NULL                               |
| **created_at** | DATETIME                | DEFAULT CURRENT_TIMESTAMP, NOT NULL                              |
| **updated_at** | DATETIME                | DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP, NOT NULL |

### 💾 Comment

| Column Name    | Data Type | Constraint                                                       |
|----------------|-----------|------------------------------------------------------------------|
| **id**         | INTEGER   | PRIMARY KEY                                                      |
| **body**       | TEXT      | NOT NULL                                                         |                                                                  |
| **post**       | INTEGER   | FOREIGN KEY REFERENCES Post(post_id), NOT NULL                   |
| **author**     | INTEGER   | FOREIGN KEY REFERENCES User(user_id), NOT NULL                   |
| **body**       | TEXT      | NOT NULL                                                         |
| **is_active**  | BOOLEAN   | NOT NULL, DEFAULT : True                                         |
| **created_at** | DATETIME  | DEFAULT CURRENT_TIMESTAMP, NOT NULL                              |
| **updated_at** | DATETIME  | DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP, NOT NULL |

### 💾 Image

| Column Name    | Data Type               | Constraint                                                       |
|----------------|-------------------------|------------------------------------------------------------------|
| **id**         | INTEGER                 | PRIMARY KEY                                                      |
| **name**       | VARCHAR(max_length=250) | NOT NULL                                                         |                                                                  |
| **post**       | INTEGER                 | FOREIGN KEY REFERENCES Post(post_id), NOT NULL                   |
| **author**     | INTEGER                 | FOREIGN KEY REFERENCES User(user_id), NOT NULL                   |
| **image_url**  | VARCHAR(max_length=255) | NULL                                                            |
| **is_active**  | BOOLEAN                 | NOT NULL, DEFAULT : True                                         |
| **created_at** | DATETIME                | DEFAULT CURRENT_TIMESTAMP, NOT NULL                              |

### 💾 Like

| Column Name         | Data Type | Constraint                                                     |
|---------------------|-----------|----------------------------------------------------------------|
| **id**              | INTEGER   | PRIMARY KEY                                                    |
| **content_type_id** | INTEGER   | FOREIGN KEY REFERENCES Content_type(content_type_id), NOT NULL |
| **object_id**       | INTEGER   | NOT NULL                                                       |
| **user**            | INTEGER   | FOREIGN KEY REFERENCES User(user_id), NOT NULL                 |
| **created_at**      | DATETIME  | DEFAULT CURRENT_TIMESTAMP, NOT NULL                            |

### 💾 Content_type

| Column Name   | Data Type                | Constraint  |
|---------------|--------------------------|-------------|
| **id**        | INTEGER                  | PRIMARY KEY |
| **app_label** | VARCHAR (max_length=100) | NOT NULL    |
| **model**     | VARCHAR (max_length=100) | NOT NULL    |

### 💾 Tag

| Column Name | Data Type                | Constraint  |
|-------------|--------------------------|-------------|
| **id**      | INTEGER                  | PRIMARY KEY |
| **name**    | VARCHAR (max_length=100) | NOT NULL    |
| **slug**    | VARCHAR (max_length=100) | NOT NULL    |

### 💾 Taggeditem

| Column Name         | Data Type | Constraint                                                     |
|---------------------|-----------|----------------------------------------------------------------|
| **id**              | INTEGER   | PRIMARY KEY                                                    |
| **object_id**       | INTEGER   | NOT NULL                                                       |
| **content_type_id** | INTEGER   | FOREIGN KEY REFERENCES Content_type(content_type_id), NOT NULL |
| **tag_id**          | INTEGER   | FOREIGN KEY REFERENCES Tag(tag_id), NOT NULL                   |

<br>

## 📅 ERD

![image](https://s3.ap-northeast-2.amazonaws.com/25th.night-project/TI/TrackProject_2_ChoiSeonWoo/ERD.png)

<br>

## API 명세서
> 하단 Notion 링크를 통해 접속하여 확인 가능

![API_docs](https://s3.ap-northeast-2.amazonaws.com/25th.night-project/TI/TrackProject_2_ChoiSeonWoo/API_docs.png)




<br>

## 배포 URL

### [🚧 `staging` Server URL](http://be-lb-staging-19620609-8d2472f463f7.kr.lb.naverncp.com/)

> [📜 `OpenAPI` URL](http://be-lb-staging-19620609-8d2472f463f7.kr.lb.naverncp.com/api/docs/)

### [🏳‍🌈 `production` Server URL](http://be-lb-prod-19620881-161af97c0c6e.kr.lb.naverncp.com/)

> [📜 `OpenAPI` URL](http://be-lb-prod-19620881-161af97c0c6e.kr.lb.naverncp.com/api/docs/)



<br>

## 📑 Check List

### 0️⃣0️⃣ DB & API설계

- [x]  DB 설계
- [x]  API 설계

### 0️⃣1️⃣ 초기 셋팅

- [x]  github 관련 설정
- [x]  가상환경 및 장고 설치
- [x]  프로젝트 및 주요 앱 생성
- [x]  `gunicorn` 설정
- [x]  `requirements.txt` 작성
- [x]  stage에 따른 설정 파일 분리
- [x]  환경변수 관련 디렉토리 및 파일 생성

### 0️⃣2️⃣ Docker 셋팅

- [x]  Dockerfile for Django - 작성
- [x]  관련 스크립트 파일 작성
- [x]  Django 프로젝트에서 psycopg2 사용 설정
- [x]  Dockerfile for nginx in ubuntu - 작성
- [x]  관련 스크립트 파일 작성
- [x]  docker-compose.yml for local 환경 - 작성
- [x]  local 환경에서 사용할 환경변수 파일 작성
- [x]  docker-compose.yml for test - 작성

### 0️⃣3️⃣ Terraform 셋팅

- [x]  디렉토리 및 파일 생성
- [x]  기본 모듈 : `network` 작성
- [x]  기본 모듈 : `server` 작성
- [x]  기본 모듈 : `loadBalancer` 작성
- [x]  서버 모듈 : `staging` 작성
- [x]  서버 모듈 : `prod` 작성
- [x]  배포 스크립트 작성
- [x]  SSH provider를 이용한 배포
- [x]  정상 생성 및 배포 확인

### 0️⃣4️⃣ CI/CD 셋팅

- [x]  github repository - Settings - Secrets and variables 설정
- [x]  github 환경 설정 - `branch protection rule`
- [x]  CI : feature 브랜치로 push 이벤트 발생 시
- [x]  CD : develop 브랜치로 PR이 완료 시 staging 서버로 배포
- [x]  CD : main 브랜치로 PR이 완료 시 prod 서버로 배포
- [x]  Django 앱 이미지 교체 (로컬/원격 환경 및 NCR)

### 0️⃣5️⃣ Model

- [x]  Profile 모델 생성
- [x]  Follow 모델 생성
- [x]  Post 모델 생성
- [x]  Admin site에 모델 등록
- [x]  로컬 환경에서 docker-compose로 테스트
- [x]  Post 모델에 대한 테스트 코드 작성

### 0️⃣6️⃣ User

- [x]  패키지 설치 및 셋팅 - DRF, DRF Spectacular 외
- [x]  회원가입 기능 구현
- [x]  회원가입 테스트
- [x]  로그인 기능 구현
- [x]  로그인 테스트
- [x]  유저 C/U/D 기능 구현
- [x]  유저 C/U/D 기능 테스트
- [x]  프로필 C/R/U/D 기능 구현
- [x]  프로필 C/R/U/D 기능 테스트
- [x]  팔로우 기능 구현
- [x]  팔로우 기능 테스트

### 0️⃣7️⃣ Post

- [x]  권한 확인 클래스 리팩토링
- [x]  게시글 C/R/U/D 기능 구현
- [x]  게시글 관련 테스트
- [x]  내가 작성한 게시글 모아보기 기능 구현
- [x]  해당 기능 테스트
- [x]  내가 팔로우한 유저의 게시글 모아보기 기능 구현
- [x]  해당 기능 테스트

### 0️⃣8️⃣ OpenAPI

- [x]  drf-spectacular 관련 라이브러리 설치
- [x]  OpenAPI Swagger 생성
- [x]  각 앱별 drf-spectacular 추가 설정

### 0️⃣9️⃣ Image

- [x]  NCloud Object Storage 생성
- [x]  `boto3` 라이브러리 설치 및 `Object Storage` 설정
- [x]  프로필 이미지 업로드 기능 추가
- [x]  프로필 이미지 기능 테스트
- [x]  AWS S3 버킷 생성
- [x]  `django-storages` 라이브러리 설치 및 `S3` 설정
- [x]  정적 파일 정상 서빙 확인
- [x]  Terraform 코드 수정

### 1️⃣0️⃣ Refactor

- [x]  Common - Permission 수정
- [x]  Users - Model 수정
- [x]  Users - Serializer 수정
- [x]  Users - View & Url 수정
- [x]  Posts - Model 수정
- [x]  Posts - Serializer 수정
- [x]  Posts - View & Url 수정
- [x]  Test 시나리오 작성
- [x]  Test Code 작성 및 실행

### 1️⃣1️⃣ Terraform (2)

- [x]  Terraform을 이용한 S3 버킷 생성 살펴보기
- [x]  AWS S3 버킷 생성을 위한 Terraform 코드 작업
- [x]  테스트용 Django 앱 및 S3 버킷 리소스 생성을 통한 테스트
- [x]  현재 프로젝트 내 Terraform 코드 작성
- [x]  Terraform으로 리소스 생성 및 확인

### 1️⃣2️⃣ DB 및 API 추가 설계

- [x]  추가 개발 기능 정의
- [x]  추가 테이블 정의
- [x]  ERD 작성
- [x]  추가 API 설계 및 명세서 작성
- [x]  테스트케이스 추가
- [x]  추가 기능 개발 전, 수정사항 확인 및 작업

### 1️⃣3️⃣ Comment

- [x]  모델 생성 및 마이그레이션 적용
- [x]  시리얼라이저 및 뷰 생성
- [x]  필터 생성 및 적용
- [x]  생성한 View의 URL 등록
- [x]  테스트코드 작성 및 확인

### 1️⃣4️⃣ Image(2)

- [x]  모델 생성 및 마이그레이션 적용
- [x]  이미지 업로드 모듈 수정
- [x]  시리얼라이저 및 뷰 생성
- [x]  생성한 View의 URL 등록
- [x]  테스트코드 작성 및 확인

### 1️⃣5️⃣ Like

- [x]  모델 생성 및 마이그레이션 적용
- [x]  시리얼라이저 및 뷰 생성
- [x]  생성한 View의 URL 등록
- [x]  테스트코드 작성 및 확인
- [x]  API 정리를 위한 추가 리팩토링
- [x]  좋아요 카운트를 위한 테이블 비정규화 및 시그널 추가

### 1️⃣6️⃣ OpenAPI (2)

- [x]  데이터 상태 필드 적용 및 테스트
- [x]  각 API별 스키마 설정 코드 작성
- [x]  view 함수 내 각 API에 스키마 설정 추가
- [x]  전체 로직 점검 및 코드 수정
- [x]  prod 환경 배포 관련 workflow 파일 수정

### 1️⃣7️⃣ Dummy Data

- [x]  유저 생성 코드 작성
- [x]  프로필 생성 코드 작성
- [x]  팔로우 생성 코드 작성
- [x]  게시글 생성 코드 작성
- [x]  댓글 생성 코드 작성
- [x]  이미지 생성 코드 작성
- [x]  좋아요 생성 코드 작성
- [x]  코드 실행 및 테스트

### 1️⃣8️⃣ k8s

- [x]  NCloud module 세분화 - `network` 모듈을 `vpc` 와 `subnet` 으로 분리
- [x]  `network` 모듈 분리에 따른 `loadBalancer` 모듈, `server` 모듈 수정
- [x]  `cluster` 모듈 작성
- [x]  `node_pool` 모듈 작성
- [x]  기존 `staging` stage,  `prod` stage 수정
- [x]  `k8s` stage 작성
- [x]  `Terraform Backend` 를 NCloud S3 Object Storage로 설정
- [x]  정상 동작 테스트
- [x]  로컬 환경에서의 사용 설정

### 1️⃣9️⃣ ArgoCD

- [x]  ArgoCD 설치
- [x]  `argocd-server` svc의 유형 변경
- [x]  비밀번호 확인 및 서버 접속

### 2️⃣0️⃣ Helm

- [x]  health check, version check API 작성
- [x]  Helm 설치
- [x]  Helm Chart 생성
- [x]  기타 파일 작성
- [x]  `values.yaml` 작성
- [x]  `Chart.yaml` 작성
- [x]  PostgreSQL 서버 생성을 위한 매니페스트 yaml 작성
- [x]  Django 서버 생성을 위한 매니페스트 yaml 작성

### 2️⃣1️⃣ ArgoCD를 통한 배포

- [x]  Github token 발급 및 secret 설정
- [x]  실시간 동기화를 위한 github webhook 설정
- [x]  환경별 환경변수 설정
- [x]  CI/CD workflow 수정
- [x]  ArgoCD에 repository 등록
- [x]  ArgoCD를 통한 환경별 배포

### 2️⃣2️⃣ Monitoring - Prometheus

- [x]  django-prometheus 설치 및 설정
- [x]  prometheus 설정
- [x]  docker-compose 파일에 prometheus 추가
- [x]  정상 동작 확인

### 2️⃣3️⃣ Monitoring - Grafana

- [x]  docker-compose에 grafana 앱 추가 코드 작성
- [x]  grafana 실행 및 prometheus 설정, 정상 동작 확인


<br>

## 📌 Notion

### 🏠 1차 진행 관련
- [00. (📺 PLAN) DB & API 설계](https://www.notion.so/browneyed/00-DB-API-2e7c2be0ed3b447cae64c1113a50f4ee?pvs=4)
- [01. (🏗 SETTING) 초기 셋팅](https://www.notion.so/browneyed/01-81b4ca5fab734a14b1e50bfe56b307ec?pvs=4)
- [02. (🏰 INFRA) Docker 셋팅](https://www.notion.so/browneyed/02-Docker-54acd08e87744d1bb7edf096ce365e19?pvs=4)
- [03. (🏰 INFRA) Terraform 셋팅](https://notion.so/1bc02cc29f784493be1a104edf900f9f)
- [04. (🏗 SETTING) CI/CD 셋팅](https://notion.so/d4c0eef1aa734e3ca7aa3b7f23836902)
- [05. (👑 FEATURE) Model](https://notion.so/06deff565c354917afc045f67113a1c4)
- [06. (👑 FEATURE) User](https://notion.so/37b6c92d79074e2b8284a809fb3e6cd8)
- [07. (❓❗ Q&A) Github Actions](https://notion.so/fd8c3a72303e4502bbe99aa52b7483e9)
- [08. (🐞 BUG) Docker & CI/CD](https://notion.so/9a2d41b6042b466f90af5fe3589786a5)
- [09. (🐞 BUG) Model](https://notion.so/fe769e41e06e43ce9e90348c67c81187)
- [10. (👑 FEATURE) Post](https://notion.so/d3ec4bc1f1654d0797794085918721ef)
- [11. (👑 FEATURE) OpenAPI](https://notion.so/820a1c6a6da34d9d89495378a0531799)
- [12. (👑 FEATURE) IMAGE](https://notion.so/2d88d0e5590d46368c817d08c3967b20)
- [13. (❓❗ Q&A) TestCode - Mocking](https://notion.so/de18bc5d422441859743351103a21aca)

### 🕍 2차 진행 관련
- [14. (🏗 SETTING) 2차 프로젝트 준비](https://notion.so/9d5e7351a3d1459d8ab962f031586793)
- [15. (❓❗ Q&A) Mocking (2)](https://notion.so/28565c259b02432687e46b71704a9735)
- [16. (🐞 BUG) TestCode - Mocking](https://notion.so/ba4877b4c33e49909e28de18ab313dcb)
- [17. (👑 FEATURE) Refactor](https://notion.so/3b5063b7350c4950bea326f0e0e13da2)
- [18. (🏰 INFRA) Terraform - AWS S3](https://notion.so/fd6008e863ca447c87de28bf04c6f20a)
- [19. (📺 PLAN) DB 및 API 추가 설계](https://notion.so/198d2b2898354246aa12c73ddc88fd22)
- [20. (👑 FEATURE) Comment](https://notion.so/c7e4103eb94343968a56c2d1786beb6e)
- [21. (👑 FEATURE) Image (2)](https://notion.so/efbef538b8b44bb9acbe287c9a863a08)
- [22. (👑 FEATURE) Like](https://notion.so/c20221b942ba4f3f9ed152598cedc846)
- [23. (👑 FEATURE) OpenAPI (2)](https://notion.so/f8c2e921a4ab43be8160655b42ea184d)
- [24. (👑 FEATURE) Dummy Data](https://notion.so/a17ba1431a884e69949086d51cc3fdf2)
- [25. (🏰 INFRA) k8s](https://notion.so/bc750741aeb34a298f8e2bd1efd9f80e)
- [26. (📮 ETC) repository mirror](https://notion.so/605df01a70144df3afa7a6c49c6bfdb6)
- [27. (🏰 INFRA) ArgoCD](https://notion.so/5578b6558a90455f8614a782ebbeace9)
- [28. (🏰 INFRA) Helm](https://notion.so/550a72f1cff64215b11ac03c3801a1e3)
- [29. (🏰 INFRA) ArgoCD를 통한 배포](https://notion.so/5b59fa957f1b4ead9ac7215f2aa1e6c3)
- [30. (🏰 INFRA) Prometheus](https://notion.so/7e0fc316cd2c409e83da6c35b1470142)
- [31. (🏰 INFRA) Grafana](https://notion.so/1d78ca43b3ec4f63b0c061595f3100ff)

<br>


## 📠 Porting Manual

**아래 내용이 이미 준비된 상황을 가정으로 작성되었습니다.**

> - NCloud 및 AWS에 가입된 계정 존재
> - NCloud에서 Administrator 권한이 부여된 Sub Account/서비스 계정이 존재
> - AWS에서 Administrator 권한이 부여된 IAM 서비스 계정이 존재
> - NCloud Container Registry에 생성한 Registry가 존재 


### 1. 아래 문서를 참고하여 `NCLOUD Object Storage` 버킷과  생성

- [NCloud Object Storage 버킷 생성](https://www.notion.so/browneyed/12-Image-2d88d0e5590d46368c817d08c3967b20?pvs=4#618e69a5cf6f4d0db92de94bb8a786a2)
  - Terraform에서 NCloud Object Storage 리소스 생성을 지원하지 않아 수동으로 생성 (2023.09 기준)

### 2. git clone 후 아래 순서대로 진행

> `staging` 서버 환경 구축만을 기준으로 작성


**a.`.envs` 폴더 하위에 `prod` 폴더 생성 후, 해당 폴더 하위에 `prod` 파일 생성**

```bash
# NCloud -------------------------------
NCP_ACCESS_KEY=<NCloud Sub Account 계정의 Access Key>
NCP_SECRET_KEY=<NCloud Sub Account 계정의 Secret Key>
NCP_S3_ENDPOINT_URL=https://kr.object.ncloudstorage.com
NCP_S3_REGION_NAME=kr-standard
NCP_S3_BUCKET_NAME=<NCloud Object Storage에서 생성한 버킷 이름>
# AWS ----------------------------------
AWS_ACCESS_KEY_ID=<AWS IAM 계정의 Access Key>
AWS_SECRET_ACCESS_KEY=<AWS IAM 계정의 Access Key>
AWS_REGION=ap-northeast-2
AWS_STORAGE_BUCKET_NAME="<name>-<env>" # infra/AWS/modules/s3/staging/main.tf 참고
```

**b. docker image 생성 및 NCloud Container Registry 로그인 후 push**

- NCloud Container Registry 로그인

```bash
docker login <Sub Account Id>.kr.ncr.nturss.com
```
- Django 앱 이미지 생성

```bash
docker build -t <Sub Account Id>.kr.ncr.nturss.com/<이미지태그>:latest -f docker/Dockerfile_dj .
```

- 생성한 이미지를 NCloud Container Registry 로그인

```bash
docker push <Sub Account Id>.kr.ncr.nturss.com/<이미지태그>:latest
```

**c. https://djecrety.ir/ 접속 → `Generate` 클릭 > `Django Secret Key` 가 자동 복사됨**

- 어딘가에 붙여넣기 하여 보관해둘 것

**d. `infra/NCP/stage/staging` 폴더 내에 `terraform.tfvars` 파일 생성 및 작성**

```bash
# --------------------------------------------
# Remote Server Account Info
username="<원격서버 접속시 사용할 계정의 사용자명>"
password="<원격서버 접속시 사용할 계정의 비밀번호>"
# --------------------------------------------
# DB Info
postgres_db="<PostgreSQL db 서버 이름>"
postgres_user="<PostgreSQL db 계정 사용자명>"
postgres_password="<PostgreSQL db 계정 비밀번호>"
postgres_volume="<PostgreSQL db에 사용할 Volume명>"
db_container_name="<PostgreSQL db 컨테이너명>"
# --------------------------------------------
# Django Info
django_settings_module="config.settings.staging"
django_secret_key="'<a에서 생성한 Django Secret Key 삽입>'"
django_container_name="<Django 앱 컨테이너명>"
# --------------------------------------------
# NCP Info
ncr_host="browneyed.kr.ncr.ntruss.com"
ncr_image="swns:latest"
ncp_access_key="<NCloud Sub Account 계정의 Access Key>"
ncp_secret_key="<NCloud Sub Account 계정의 Secret Key>"
ncp_lb_domain="lb-init-domain.com"
ncp_s3_endpoint_url="https://kr.object.ncloudstorage.com"
ncp_s3_region_name="kr-standard"
ncp_s3_bucket_name="<NCloud Object Storage에서 생성한 버킷 이름>"
# --------------------------------------------
# AWS Info
aws_access_key_id="<AWS IAM 계정의 Access Key>"
aws_secret_access_key="<AWS IAM 계정의 Access Key>"
aws_region="ap-northeast-2"
aws_storage_bucket_name="<'a'에서 지정한 AWS_STORAGE_BUCKET_NAME>"
```

**e. Terraform 명령어를 실행하여 인프라 구축**

- AWS 리소스 생성

```bash
cd infra/NCP/stage/staging
```

```bash
terraform init
```

```bash
terraform apply
```

- NCP 리소스 생성

```bash
cd ../../../..
cd infra/NCP/stage/staging
```

```bash
terraform init
```

```bash
terraform apply
```

- `init script` 관련 에러 발생 시, 터미널에서 아래의 명령어 실행 후 `terraform apply` 재시도

> 줄바꿈 관련 캐리지리턴 제거 명령어

```bash
sed -i 's/\r//g' ../../script/set_be_server.sh
sed -i 's/\r//g' ../../script/set_db_server.sh
```


**f. `terraform apply` 의 결과로, 터미널 창에 아래와 같이 출력됨**

- AWS

```bash
Changes to Outputs:
  + bucket_bucket_regional_dns = "<버킷명>.s3.ap-northeast-2.amazonaws.com"
```

- NCP

```bash
Changes to Outputs:
  + be_lb_domain = "<Load Balancer 주소>"
  + be_public_ip = "<Django 서버 Host 주소>"
  + db_public_ip = "<PostgreSQL DB 서버 Host 주소>"
```


**g. ssh 를 이용하여 Django 서버에 원격 접속**

> `<원격서버 접속시 사용할 계정 정보>` 는 위에서 `d`에서 지정한 데이터들을 사용

```bash
ssh <원격서버 접속시 사용할 계정의 사용자명>@<Django 서버 Host 주소>
```

```bash
<원격서버 접속시 사용할 계정의 비밀번호> 입력 후 Enter
```

**h. `.env` 파일 내 `NCP_LB_DOMAIN` 내용 수정**

> 실제 서비스에서는 도메인이 이미 지정되어 있으므로 불필요한 과정

- `f` 에서 확인한 `Load Balancer 주소`로 지정

```bash
vi .env
```

```bash
NCP_LB_DOMAIN=<Load Balancer 주소>
```

**i. 변경된 환경변수 적용**

- `.env` 파일 리로드 및 해당 내용을 `.bash_aliases` 에도 적용하기 위해 아래 명령어 실행

```bash
source ~/.bash_aliases
```

**j. 실행 중인 Django 앱 컨테이너 중지 및 삭제 후 재실행**

- 이미 `alias` 가 `.bash_aliases` 파일 내에 지정되어 있어음

```bash
# django 컨테이너 중지 및 컨테이너 삭제
dstrm
```

```bash
# 환경변수를 반영하여 django 컨테이너 실행
drerun
```

**k. `f` 에서 확인한 `Load Balancer 주소`로 접속**

- 정상 접속 됨을 확인 가능

<br>

## 📚 테스트용 Dummy Data 생성

### 1. ssh를 이용한 `staging` stage의 Django 서버 접속

```bash
ssh <원격서버 접속용으로 설정한 계정의 사용자명>@<Django 서버 Host 주소>
```

```bash
<원격서버 접속용으로 설정한 계정의 비밀번호> 입력 후 Enter
```

```bash
# 아래 명령어를 통해 컨테이너명 확인
docker ps
```

```bash
docker exec -it <컨테이너명> bash
```
### 2. 아래 명령어를 순서대로 실행하여 데이터 생성

> 데이터 수를 입력하라는 메시지가 뜨면 본인이 직접 입력

```bash
python manage.py 01_user
```

```bash
python manage.py 02_profile
```

```bash
python manage.py 03_follow
```

```bash
python manage.py 04_post
```

```bash
python manage.py 05_comment
```

```bash
python manage.py 06_image
```

```bash
python manage.py 07_like
```

### 3. 서버에 접속하여 데이터 조회 및 확인


<br>

## 🚧 추후 작업 혹은 개선할 만한 사항들

- [ ] 데이터 유효성 검증 추가 및 테스트 코드 개선
- [ ] 쿼리 속도 개선
- [ ] API Endpoint 개선
- [ ] 코드 리팩토링
- [ ] Infra Architecture Diagram 작성



<br>
<br>
