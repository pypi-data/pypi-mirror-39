# 동식물 모니터링 시스템의 Python용 Datalib.

## 목적

  UTC로 기록된 데이터를 국가별 시간대에 맞게 가져오려면 범위에 대한 적절한 변환이 필요하다.  변환 과정은 생각하므로 데이터 분석의 장애물이 될 수 있다. 이러한 장애물을 해소하고 데이터 분석 과정을 돕기 위해 본 라이브러리를 개발하였다.



## 개요

  현재 MongoDB에 저장된 데이터는 UTC를 기준으로 저장된다. UTC로 저장하는 이유는 시간대나 위치 등에 구애받지 않고, 데이터를 공통적으로 저장하고 이용하기 위해서이다. 

  그러나 국가별 시차가 존재한다. 시차로 인해 데이터를 가져올 때 범위의 변환이 필요하다. 예를 들어 한국 시간 기준  15일의 데이터를 가져오려면 UTC 기준 14일 오후 3시부터 15일 오후 3시까지의 데이터를 가져와야 한다. 

본 라이브러리는 이러한 변환 기능과 더불어 손쉽게 데이터를 가져올 수 있는 다양한 API를 제공한다.

## API 명세

본 라이브러리의 패치키명은 apmondatalib이다.



### create_raw_data_fetcher 메소드

  create_raw_data_fetcher는 apmondatalib의 인스턴스를 생성하는 함수이다. 본 라이브러리를 사용하기 위한 첫 번째 진입 함수이다.

| 역할     |                        |                                     |
| -------- | ---------------------- | ----------------------------------- |
| 파라메터 | host                   | MongoDB의 접속 주소                 |
|          | port                   | MongoDB의 포트 (기본값: 27017)      |
|          | database               | 데이터베이스 이름 (기본값: apmonv1) |
|          | sensor_id              | 센서의 식별자                       |
|          | default_page_size      | 기본 페이지 크기                    |
|          | time_offset            | 시간대 (한국의 기본값: 9)           |
| 반환값   | DataFetcher의 인스턴스 |                                     |



### SensorRawDataFetcher 클래스

#### 생성자

| 분류     | 이름                   | 설명                                |
| -------- | ---------------------- | ----------------------------------- |
| 파라메터 | host                   | MongoDB의 접속 주소                 |
|          | port                   | MongoDB의 포트 (기본값: 27017)      |
|          | database               | 데이터베이스 이름 (기본값: apmonv1) |
|          | sensor_id              | 센서의 식별자                       |
|          | default_page_size      | 기본 페이지 크기                    |
|          | time_offset            | 시간대 (한국의 기본값: 9)           |
| 반환값   | DataFetcher의 인스턴스 |                                     |



#### read

데이터베이스에 저장된 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | sensor_type             | SensorType Enum 중 하나     |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |



#### read_humidity

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_temperature

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_light

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### read_motion

| 분류     | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 | 센서값의 목록               |



#### count

데이터베이스에 저장된 센서 데이터의 갯수를 반환하는 함수이다.

| 파라메터 | 이름          | 설명                    |
| -------- | ------------- | ----------------------- |
| 파라메터 | sensor_type   | SensorType Enum 중 하나 |
| 반환값   | 데이터의 갯수 |                         |



#### count_humidity

습도 데이터의 갯수를 반환하는 함수이다.

| 파라메터 | 이름          | 설명 |
| -------- | ------------- | ---- |
| 반환값   | 데이터의 갯수 |      |



#### count_temperature

온도 데이터의 갯수를 반환하는 함수이다.

| 파라메터 | 이름          | 설명 |
| -------- | ------------- | ---- |
| 반환값   | 데이터의 갯수 |      |



#### count_light

조도 데이터의 갯수를 반환하는 함수이다.

| 파라메터 | 이름          | 설명 |
| -------- | ------------- | ---- |
| 반환값   | 데이터의 갯수 |      |



#### count_motion

움직임 데이터의 갯수를 반환하는 함수이다.

| 파라메터 | 이름          | 설명 |
| -------- | ------------- | ---- |
| 반환값   | 데이터의 갯수 |      |



#### count_total_pages

데이터베이스에 저장된 센서 데이타의 총 페이지 갯수를 반환하는 함수이다.

| 파라메터 | 이름        | 설명                        |
| -------- | ----------- | --------------------------- |
| 파라메터 | sensor_type | SensorType Enum 중 하나     |
|          | page_size   | 한번에 가져올 데이터의 갯수 |
| 반환값   | 페이지 수   |                             |



#### count_total_humidity_pages

습도 데이터의 총 페이지 갯수를 반환하는 함수이다.

| 파라메터 | 이름      | 설명                        |
| -------- | --------- | --------------------------- |
| 파라메터 | page_size | 한번에 가져올 데이터의 갯수 |
| 반환값   | 페이지 수 |                             |



#### count_total_temperature_pages

온도 데이터의 총 페이지 갯수를 반환하는 함수이다.

| 파라메터 | 이름      | 설명                        |
| -------- | --------- | --------------------------- |
| 파라메터 | page_size | 한번에 가져올 데이터의 갯수 |
| 반환값   | 페이지 수 |                             |



#### count_total_light_pages

조도 데이터의 총 페이지 갯수를 반환하는 함수이다.

| 파라메터 | 이름      | 설명                        |
| -------- | --------- | --------------------------- |
| 파라메터 | page_size | 한번에 가져올 데이터의 갯수 |
| 반환값   | 페이지 수 |                             |



#### count_total_motion_pages

움직임 데이터의 총 페이지 갯수를 반환하는 함수이다.

| 파라메터 | 이름      | 설명                        |
| -------- | --------- | --------------------------- |
| 파라메터 | page_size | 한번에 가져올 데이터의 갯수 |
| 반환값   | 페이지 수 |                             |



#### read_in_rage

데이터베이스에서 지정된 시간 범위 내의 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | sensor_type             | SensorType Enum 중 하나     |
|          | from_date               | 시작일                      |
|          | to_date                 | 종료일                      |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |

#### read_humidity_in_range

데이터베이스에서 지정된 시간 범위 내의 습도 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | from_date               | 시작일                      |
|          | to_date                 | 종료일                      |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |

#### read_temperature_in_range

데이터베이스에서 지정된 시간 범위 내의 온도 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | from_date               | 시작일                      |
|          | to_date                 | 종료일                      |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |

#### read_light_in_range

데이터베이스에서 지정된 시간 범위 내의 조도 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | from_date               | 시작일                      |
|          | to_date                 | 종료일                      |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |

#### read_motion_in_range

데이터베이스에서 지정된 시간 범위 내의 움직임 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | from_date               | 시작일                      |
|          | to_date                 | 종료일                      |
|          | page_number             | 페이지 번호                 |
|          | page_size               | 한번에 가져올 데이터의 갯수 |
| 반환값   | RawData 클래스의 리스트 |                             |


### DailyDataFetcher 클래스

#### 생성자

| 분류     | 이름                   | 설명                                |
| -------- | ---------------------- | ----------------------------------- |
| 파라메터 | host                   | MongoDB의 접속 주소                 |
|          | port                   | MongoDB의 포트 (기본값: 27017)      |
|          | database               | 데이터베이스 이름 (기본값: apmonv1) |
|          | sensor_id              | 센서의 식별자                       |
|          | default_page_size      | 기본 페이지 크기                    |
|          | time_offset            | 시간대 (한국의 기본값: 9)           |
| 반환값   | DataFetcher의 인스턴스 |                                     |


#### read


def read(self, sensor_type, year, month, day):
데이터베이스에서 지정된 시간 범위 내의 움직임 센서값을 가져오는 함수이다.

| 파라메터 | 이름                    | 설명                        |
| -------- | ----------------------- | --------------------------- |
| 파라메터 | sensor_type               | SensorType Enum 중 하나                      |
|          | year                | 년도                      |
|          | month             | 월                 |
|          | day               | 날짜 |
| 반환값   | DailySummary 클래스 |                             |

#### SensorType (Enum)

시스템이 지원하는 센서의 타입이며, 다음과 같은 항목을 사용할 수 있다.

| 이름        | 설명             |
| ----------- | ---------------- |
| Humidity    | 습도 센서        |
| Temperature | 온도 센서        |
| Light       | 조도 센서        |
| Motion      | 움직임 감지 센서 |



#### RawData 클래스

센서값을 표현하는 클래스이며, 현재 네 가지 항목을 가지고 있다.

| 이름      | 설명                         |
| --------- | ---------------------------- |
| id        | MongoDB에 저장된 데이터의 ID |
| sensor_id | 센서 보드의 식별자           |
| type      | SensorType Enum 중 하나      |
| value     | 측정값                       |
| timestamp | 기록시간                       |



#### HourlySummary 클래스

시간당 센서값의 통계값을 표현하는 클래스이며, 현재 네 가지 항목을 가지고 있다

| 이름      | 설명                         |
| --------- | ---------------------------- |
| hour        | 시간 (0~23시) |
| average | 평균값           |
| min      | 최소값      |
| max     | 최대값                       |


#### DailySummary 클래스

센서값을 표현하는 클래스이며, 현재 네 가지 항목을 가지고 있다. 추후에 시간 정보가 추가될 예정이다.

| 이름      | 설명                         |
| --------- | ---------------------------- |
| id        | MongoDB에 저장된 데이터의 ID |
| sensor_id | 센서 보드의 식별자           |
| type      | SensorType Enum 중 하나      |
| year      | 년도                      |
| month     | 월                      |
| day       | 일                       |
| average   | 평균값           |
| min       | 최소값      |
| max       | 최대값                       |
| data_set  | HourlySummary의 배열 (24개)                       |



## 설치방법

```bash
pip install apmondatalib
```

위의 명령어를 입력하여 설치한다.



## 버전 정보

### 0.0.1

- read, read_* 계열의 함수 구현


### 0.0.3

- count, count_*, count_total_pages, count_*_total_pages 계열의 함수 구현

### 0.0.4

- read_in_range 계열의 함수 구현
- page_size 파라메터를 함수의 가장 뒤로 옮기고, 기본값을 생성자에 설정하도록 변경
- 쿼리문에 timestamp를 기준으로 내림차순 정렬하여 Raw Data를 가져오도록 변경
- Raw Data 출력 결과에 timestamp가 포함되도록 변경

### 0.0.5

- DailyDataFetcher 클래스 및 기타 클래스 추가

## 예제

  다음의 예제는 각 타입의 데이터를 가져오는 기본적인 예제이다.

```python

import sys
from datetime import datetime, timedelta, timezone
from apmondatalib import DataFetcher


def main():
    d = DataFetcher.create_raw_data_fetcher("49.247.210.243", 27017, "apmonv1", "SEN03", 9)

    sensor_types = [DataFetcher.SensorType.Humidity,
                    DataFetcher.SensorType.Temperature,
                    DataFetcher.SensorType.Light,
                    DataFetcher.SensorType.Motion]

    test_read_methods(d, sensor_types)
    test_count_methods(d, sensor_types)
    test_count_total_page_methods(d, sensor_types)
    test_read_in_range_methods(d, sensor_types)

    d = DataFetcher.create_daily_summary_fetcher("49.247.210.243", 27017, "apmonv1", "SEN03", 9)
    test_read_daily_summary(d, sensor_types)


def utc_to_local(utc_dt):
    if sys.version_info >= (3, 7):
        return utc_dt.astimezone()
    else:
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def test_read_in_range_methods(d, sensor_types):
    date_from = utc_to_local(datetime(2018, 11, 10, 0, 0, 0, 0))
    date_to = utc_to_local(datetime(2018, 11, 11, 0, 0, 0, 0))

    for t in sensor_types:
        print ('== read_in_range(%s) ==================================' % t)
        for t in d.read_in_range(
                DataFetcher.SensorType.Temperature,
                date_from,
                date_to, 1, 1000):
            print(t)

    for f in [d.read_humidity_in_range, d.read_temperature_in_range, d.read_light_in_range, d.read_motion_in_range]:
        print('== read_in_range(%s, %s, %s) ==================================' % (f.__name__, date_from, date_to))
        for x in f(date_from, date_to, 1, 1000):
            print(x)


def test_read_methods(d, sensor_types):
    for t in sensor_types:
        print ('== read(%s) ==================================' % t)
        for x in d.read(t, 50, 5):
            print(x)

    for f in [d.read_humidity, d.read_temperature, d.read_light, d.read_motion]:
        print('== %s ==================================' % f.__name__)
        for x in f(50, 5):
            print(x)


def test_count_methods(d, sensor_types):
    for t in sensor_types:
        print("== count(%s) ==================================" % t)
        print(d.count(t))

    for f in [d.count_humidity, d.count_temperature, d.count_light, d.count_motion]:
        print("== %s ==================================" % f.__name__)
        print(f())


def test_count_total_page_methods(d, sensor_types):
    for t in sensor_types:
        print("== count_total_pages(%s) ==================================" % t)
        print(d.count_total_pages(t, 100))

    for f in [d.count_total_humidity_pages,
              d.count_total_temperature_pages,
              d.count_total_light_pages,
              d.count_total_motion_pages]:
        print("== %s ==================================" % f.__name__)
        print(f(100))


def test_read_daily_summary(d, sensor_types):
    for t in sensor_types:
        print ('== read(%s) ==================================' % t)
        s = d.read(t, 2018, 12, 15)
        print ('== test_read_daily_summary(%s, 2018,12, 15) ==================================' % t)
        print(s)
        for x in s.data_set:
            print(x)


if __name__ == "__main__":
    main()


    
```

   

