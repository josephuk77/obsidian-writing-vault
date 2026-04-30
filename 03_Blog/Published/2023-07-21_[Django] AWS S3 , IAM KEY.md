---
title: "[Django] AWS S3 , IAM KEY"
created: "2023-07-21"
type: blog
status: published
tags:
  - velog
publish_url: "https://velog.io/@josephuk77/Django-AWS-S3-IAM-KEY"
---

# [Django] AWS S3 , IAM KEY

### AWS S3란?
![](https://velog.velcdn.com/images/josephuk77/post/e21d08fb-4075-4ef9-a75b-67084013d4d2/image.png)
#### 공식문서
> Amazon Simple Storage Service(Amazon S3)는 업계 최고의 확장성, 데이터 가용성, 보안 및 성능을 제공하는 객체 스토리지 서비스입니다. 모든 규모와 업종의 고객은 Amazon S3를 사용하여 데이터 레이크, 웹 사이트, 모바일 애플리케이션, 백업 및 복원, 아카이브, 엔터프라이즈 애플리케이션, IoT 디바이스, 빅 데이터 분석 등 다양한 사용 사례에서 원하는 양의 데이터를 저장하고 보호할 수 있습니다. Amazon S3는 특정 비즈니스, 조직 및 규정 준수 요구 사항에 맞게 데이터에 대한 액세스를 최적화, 구조화 및 구성할 수 있는 관리 기능을 제공합니다

#### 내가 이해한 내용
> 하나의 객체당 최대 5TB까지 저장이 가능하고 따로 용량의 제한이 없어 사용자가 추후에 사용자가 스토리지를 관리하던가 확장/축소에 신경을 쓰지 않아도 된다(개으른 나한테는 매우 좋은 것 같다ㅎㅎ)한마디로 매우 좋은 서버용 저장공간이다 라고 생각하면 편할것 같다(아닌가..?)

#### AWS S3 기본 개념
- 객체(Object)
S3에 ㄷ에이터가 저장되는 기본 단위로써 파일과 메타데이터로 이루어져있다. 객체 하나의 크기는 1Byte부터 5TB까지 허용되며 메타데이터는 MIME 형식으로 파일 확장자를 통해 자동으로 설정되며 사용자 임의로도 지정 가능하다.

- 버킷(Bucket)
S3에서 생성할 수 있는 최상위 디렉토리의 개념으로 이름은 S3 리전 중에서 유일해야 한다. 계정별로 100개까지 생성 가능하며 버킷에 저장할 수 있는 객체수와 용량은 무제한이다.

- 표준스토리지
S3 서비스 수준 계약으로 객체에 대해 99.99999999999%의 내구성을 보장하며 99.99%의 가용성을 제공한다. 하지만 높은 내구성을 보장해야 하는 만큼 비용이 높으므로 유실되면 안되는 원본 데이터, 민감한정보, 개인정보 등의 중요한 데이터를 저장하는 것이 알맞다.

- RRS(Reduced Redundancy Storage)
표준 스토리지보다 저렴한 비용으로 데이터를 저장할 수 있다. RRS옵션은 여러 시설 전반에 다양한 디바이스에 객체를 저장하며 일반 디스크 드라이브의 400배에 달하는 내구성을 제공하나 표준 스토리지 만큼 많이 객체를 복제하지는 않으므로 원본을 복제한 데이터나 가공한 데이터(예를 들어 썸네일 같은)의 저장에 알맞다


### AWS IAM란?
![](https://velog.velcdn.com/images/josephuk77/post/474ec945-d230-410f-aab4-ee84e87f0b66/image.png)
#### 공식문서
> AWS Identity and Access Management(IAM)은 AWS 리소스에 대한 액세스를 안전하게 제어할 수 있는 웹 서비스입니다. IAM을 사용하면 사용자가 액세스할 수 있는 AWS 리소스를 제어하는 권한을 중앙에서 관리할 수 있습니다. IAM을 사용하여 리소스를 사용하도록 인증(로그인) 및 권한 부여(권한 있음)된 대상을 제어합니다.

#### 내가 이해한 내용
> AWS에 여러가지 기능들이 있늗데(S3 EC2 RDS 등등)이것들을 집과 차등으로 생각하고 하나의 전자키에 내가 원하는 키의 기능만넣어서 다른 사람에게 쓸수 있게 키를 건네주는데 사용되는 것이다 예를 들어 A는 내 물건중 차만 사용을 가능하게 하고 B는 차와 오토바이 집을 같이 쓸 수 있게 하려면 2개의 IAM key를 만들어 하나에는 차의 엑세스 권한을 주고 하나에는 차 오토바이 집에 엑세스 권한을 줘 관리를 하는 것이다
![](https://velog.velcdn.com/images/josephuk77/post/060c0c55-4d62-41c3-ad82-e7fb63304f48/image.png)
출처 : https://claudecloud.tistory.com/2

이제 IAM과 S3를 Django에 연결해보자
#### 1. IAM 생성
![](https://velog.velcdn.com/images/josephuk77/post/e3ee1539-7f85-4449-b201-1d657fa5890b/image.png)
aws에 로그인후 IAM으로 이동한 다음 사용자를 누른다
![](https://velog.velcdn.com/images/josephuk77/post/7ecea21d-033e-4579-877b-79869b1d8039/image.png)
사용자 추가 
![](https://velog.velcdn.com/images/josephuk77/post/8bdc9ad5-80f8-4918-b13f-8f6f36d999a7/image.png)
사용자 이름을 입력(중복 X 원하는 이름)
![](https://velog.velcdn.com/images/josephuk77/post/0049675b-0032-47c7-9f01-410e79804f97/image.png)
직접 정착 연결 -> AmazonS3fullAccess선택
우리는 S3를 사용할 것이므로 S3의 모든 권한이 들어가 있는 정책을 골라줍니다 위에서 말했던 전자키에 내 차키를 넣는 것과 동일한 작업입니다(S3외에도 여러 정책도 있고 S3도 작은 단위에 정책도 있음)
![](https://velog.velcdn.com/images/josephuk77/post/929c00bc-657c-4e6a-8cd6-8bd1cc04a606/image.png)
생성완료(IAM 생성은 생각보다 쉬웠습니다ㅎㅎ)
사용자 생성을 누를시 시크릿가 나오는데 그 키는 한번만 나오므로 자신만 볼 수 있는 곳에 잘 저장해두는게 좋습니다(까먹을 시 처음부터 다시생성 해야함..ㅎ)

#### 2. S3 버킷생성
![](https://velog.velcdn.com/images/josephuk77/post/bf3e9d53-2ad1-42f1-aced-8b344a6b2eaa/image.png)
AWS S3로 이동 후 버킷만들기 

![](https://velog.velcdn.com/images/josephuk77/post/49f28e4b-6216-4037-8ccb-56118f70ae28/image.png)

버킷이름(원하는 것 마음대로) -> AWS리전 서울로 변경
![](https://velog.velcdn.com/images/josephuk77/post/641b0b6d-07cf-4178-b773-1b828ff44717/image.png)
버킷의 퍼블릭 액세스 차단설정(아직 잘 이해가 안되어 추후에 추가작성하겠습니다)
![](https://velog.velcdn.com/images/josephuk77/post/881e3384-13d6-42fa-94d3-83ffd6f1041e/image.png)
나머지 그대로 나두고 버킷 만들기
![](https://velog.velcdn.com/images/josephuk77/post/7d671fb5-9781-4f75-88c7-34311f87e25b/image.png)

버킷에 들어가 권한으로 이동
![](https://velog.velcdn.com/images/josephuk77/post/d7a40511-9979-4051-8cd7-db673da94106/image.png)

권한에 버킷정책 -> 편집
 ```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::내 버킷이름/*",
                "arn:aws:s3:::내 버킷이름"
            ]
        }
    ]
}
```
이 권한은 모든 사용자가 이 버킷에 S3의 모든 권한을 부여한다는 코드이다
Princiapl는 허용된 사용자를 지정하는 것이고
Action은 s3의 어떤 것을 할 수 있는지 정하는 것이다

S3도 설정완료!!

#### 3. Django 설정
boto3, django-storages이 두가지으 패키지가 필요해 설치를 해준다 저는 도커를 사용하고 있기 때문에 requirments.txt에 추가해줬습니다.
가상환경을 사용시
```
pip install boto3 django-storages
```

```
config/setting.py

# AWS S3 관련 설정 추가
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")

# 기본값 설정 
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = AWS_S3_REGION_NAME
AWS_S3_ENDPOINT_URL = AWS_S3_ENDPOINT_URL

# DEFAULT_FILE_STORAGE 및 STATICFILES_STORAGE 설정
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

```
AWS_ACCESS_KEY_ID = IAM key ID
AWS_SECRET_ACCESS_KEY = IAM key secret key
AWS_STORAGE_BUCKET_NAME = 내 버킷 이름
AWS_S3_REGION_NAME = ap-northeast-2(버킷생성할 때 지역)
AWS_S3_ENDPOINT_URL = https://s3-accelerate.amazonaws.com
위처럼 채워주면 되고 무조건 .env파일을 사용해서 IAM key값을 숨기고 배포를 하든 깃허브에 올리든 해야한다 유출될경우 해커들이 열심히 비트코인을 캐 요금이 몇억씩 나온다는....
 
    
드디어 연결 끝 이제 사용하기마 하면 된다

#### 4. 사용코드 
이번 프로젝트에 dall-e를 사용하여서 위에는 dall-e 코드도 추가해서 작성하겠습니다
```
views.py

import datetime
import random
from PIL import Image
from io import BytesIO
import boto3
from django.conf import settings

def dalleIMG(query):
    OPENAI_API_KEY = os.getenv("OPENAI_SECRET_KEY")
  
    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY

    # 모델 - GPT 3.5 Turbo 선택
    model = "gpt-3.5-turbo"



    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who is good at translating."
        },
        {
            "role": "assistant",
            "content": query
        }
    ]

    # 사용자 메시지 추가
    messages.append(
        {
            "role": "user", 
            "content": "영어로 번역해주세요."
        }
    )

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer3 = response['choices'][0]['message']['content']
    print(answer3)

    # 새 메시지 구성
    messages = [
        {
            "role": "system",
            "content": "You are an assistant who is good at creating prompts for image creation."
        },
        {
            "role": "assistant",
            "content": answer3
        }
    ]

    # 사용자 메시지 추가
    messages.append(
        {
            "role": "user", 
            "content": "Condense up to 4 outward description to focus on nouns and adjectives separated by ,"
        }
    )

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer4 = response['choices'][0]['message']['content']
    print(answer4)

    # 이미지 생성을 위한 프롬프트
    params = ", concept art, realistic lighting, ultra-detailed, 8K, photorealism, digital art"
    prompt = f"{answer4}{params}"
    print(prompt)

    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="512x512"
    )
    image_url = response['data'][0]['url']
    print(image_url)


    # 이미지 다운로드
    res = requests.get(image_url)
    if res.status_code != 200:
        return JsonResponse({'error': 'Failed to download image'}, status=400)
    
    # 이미지 열기
    img = Image.open(BytesIO(res.content))

    # S3에 이미지 저장
    # 고유한 키 이름 생성
    now = datetime.datetime.now()
    random_suffix = random.randint(1000, 9999)
    s3_filename = f'images/{now.strftime("%Y-%m-%d-%H-%M-%S")}_{random_suffix}.png'
    
    s3_bucket = 'team-a-s3-bucket'
    
    save_image_to_s3(img, s3_bucket, s3_filename)

    # 저장된 이미지의 URL 생성
    image_s3_url = f'{settings.AWS_S3_ENDPOINT_URL}/{s3_bucket}/{s3_filename}'

    # JSON 형식으로 응답 반환
    return JsonResponse({'image_url': image_s3_url})
    

def save_image_to_s3(image, bucket_name, file_name):
    try:
        # S3에 이미지 업로드
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )
        with BytesIO() as output:
            image.save(output, format='PNG')
            output.seek(0)
            s3.upload_fileobj(output, bucket_name, file_name)
        print(f"Image saved successfully to S3 bucket: {bucket_name}, with file name: {file_name}")
        return True
    except Exception as e:
        print(f"Failed to save image to S3: {str(e)}")
        return False
```
dall-e 이미지를 저장을 하다 보니 같은 이름으로 저장이 안된다는 것을 깨닫고 이미지 앞에 시간을 넣어 이름을 구분하기로 하고 코드를 작성했습니다.
 
 
첫글이라서 저도 모라고 적었는지 하나도 모르겠네요 ㅎㅎ 혹시 틀린네요 있으면 바로 지적해주세요! 
    
    
    
    
참고: https://usefultoknow.tistory.com/entry/Amazon-S3%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C
