# srt_ticketing
## Pseudo code
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
