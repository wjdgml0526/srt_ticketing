# srt_ticketing
## Pseudo code
```python
def srt_ticketing():
    while srt_time + 2hours >= now:
        로그인 코드
        
        가는 열차 옵션 입력
        if round_trip:
            오는 열차 옵션 입력
        조회 버튼 클릭
        
        if not round_trip:
            while 기차 출발 시간 <= 입력 시간 + 1:
                if 표 있음:
                elif 입석 있음:
                else:
                    if 예약 가능:
                    else:
                        다음 행 확인
			if 다음 행 없는 경우:
                            경고창 확인
                            코드 종료
        else:
            # 가는 열차 확인
            while 기차 출발 시간 <= 입력 시간 + 1:
                if 표 있음:
                elif 입석 있음:
                    열차 선택
                    결제
                    예약대기 실행 플래그
                else:
                    다음 행 확인
            # 오는 열차 확인
            while 기차 출발 시간 <= 입력 시간 + 1:
                if 표 있음:
                elif 입석 있음:
                    열차 선택
                    결제
                    예약대기 실행 플래그
                else:
                    다음 행 확인
            if 가는 열차 입석:
                srt_ticketing()
            if 오는 열차 입석:
                srt_ticketing()
        
        time.sleep(30 ~ 60)
        now
```

## 필요한 변수
vars.py
```python
# 로그인 정보
user_id = 'srt id'                            # 숫자 10자리 string 타입으로 입력
user_pwd = 'srt passward'                     # 비밀번호 string 타입으로 입력

# 예매할 기차 정보
dpt = '수서'
arv = '부산'
dpt_date = '20230922'                          # 출발일 8자리 string 타입으로 입력
dpt_time = '08'                                # 출발시간 2시간 간격, 2자리 string 타입으로 입력
adult_num = '2'                                # 탑승객수 string 타입으로 입력
# 예약자 제외한 이름 입력
user_name = ['ㅇㅇㅇ']                           # 탑승객 이름 string 객체가 포함된 list 타입으로 입력

round_trip = True                              # 왕복 여부 boolean

ret_date = '20230924'                          # 도착일 8자리 string 타입으로 입력
ret_time = '22'                                # 출발시간 2시간 간격, 2자리 string 타입으로 입력

# 결제 정보
card_num = ['0000', '0000', '0000', '0000']    # 카드 번호 4자리(string)씩 list로 입력
exp_date_mon = '00'                            # 카드 만료 월, 2자리 string 타입으로 입력
exp_date_yr = '00'                             # 카드 만료 월, 2자리 string 타입으로 입력
card_pwd = '00'                                # 카드 비밀번호 앞 2자리 string 타입으로 입력
user_brth = '940526'                           # 생일 6자리 string 타입으로 입력

phn_num = ['010', '0000', '0000']              # 전화번호 string 객체가 포함된 list 타입으로 입력
```
