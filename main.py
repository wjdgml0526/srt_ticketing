import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from vars import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
import time
import random


def select_stn(dpt: str, arv: str):
    '''
    출발, 도착 기차역 입력
    '''
    # 전역변수 설정
    global driver
    
    # 출발 기차역 입력
    elm_dpt_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
    dft_stn_name = elm_dpt_stn.get_attribute('value')
    if dft_stn_name != dpt:
        elm_dpt_stn.clear()
        elm_dpt_stn.send_keys(dpt)

    # 도착 기차역 입력
    elm_arv_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
    dft_stn_name = elm_arv_stn.get_attribute('value')
    if dft_stn_name != arv:
        elm_arv_stn.clear()
        elm_arv_stn.send_keys(arv)


def select_dt_tm(date: str = dpt_date, time: str = dpt_time, ret: bool = False):
    '''
    열차 검색 날짜, 시간 선택
    '''
    # 전역변수 설정
    global driver
    
    # 돌아오는 열차일 경우 id 변경
    if ret:
        date_id = 'dptDt2'
        time_id = 'dptTm2'
    else:
        date_id = 'dptDt'
        time_id = 'dptTm'
    
    # 가는 열차 검색 날짜 선택
    elm_date = driver.find_element(By.ID, date_id)
    try:
        Select(elm_date).select_by_value(date)
    except:
        pass
    
    # 출발 시간 선택
    elm_time = driver.find_element(By.ID, time_id)
    Select(elm_time).select_by_value(time + '0000')


def select_headcount(adult_num: str):
    '''
    탑승 인원수 선택
    '''
    # 전역변수 설정
    global driver
    
    elm_adl_num = driver.find_element(
        By.XPATH,
        '//*[@id="search-form"]/fieldset/div[1]/div/ul/li[2]/div[2]/div[1]/select'
        )
    dft_adl_num = elm_adl_num.get_attribute('value')
    if dft_adl_num != adult_num:
        Select(elm_adl_num).select_by_value(adult_num)


def train_time(col: int, bs_xpath: str):
    '''
    열차 출발 or 도착 시간 저장
    '''
    # 전역변수 설정
    global driver
    
    tm_xpath = bs_xpath + 'tr[{}]/td[4]/em'.format(col)
    train_hour, train_min = driver.find_element(By.XPATH, tm_xpath).text.split(':')
    
    return train_hour, train_min


def but_text(col: int, bs_xpath: str, resve: bool = False):
    '''
    예약하기, 좌석+입석, 신청하기 버튼 텍스트 추출
    '''
    # 전역변수 설정
    global driver
    
    txt_xpath = bs_xpath + 'tr[{}]/td[{}]/a/span'.format(col, 8 if resve else 7)
    try:
        txt = driver.find_element(By.XPATH, txt_xpath).text
    except:
        txt = ''
    return txt


def but_click(col: int, bs_xpath: str, resve: bool = False):
    '''
    예약하기, 좌석+입석, 신청하기 버튼 클릭
    '''
    # 전역변수 설정
    global driver
    
    but_xpath = bs_xpath + 'tr[{}]/td[{}]/a'.format(col, 8 if resve else 7)
    # driver.find_element(By.XPATH, but_xpath).click()
    driver.find_element(By.XPATH, but_xpath).send_keys('\n')


def payment(
    card_num: list,
    exp_date_mon: str,
    exp_date_yr: str,
    card_pwd: str,
    user_brth: str,
    round_trip: bool,
    rsv_txt: str,
    adult_num: str,
    user_name: list
    ):
    '''
    결제 단계 진행
    '''
    # 전역변수 설정
    global driver
    
    # 결제하기 버튼 클릭
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            '#list-form > fieldset > div.tal_c > a.btn_large.btn_blue_dark.val_m.mgr10'
            ).click()
    except:
        driver.find_element(
            By.CSS_SELECTOR,
            '#list-form > fieldset > div.tal_c > button.btn_large.btn_blue_dark.val_m.mgr10'
            ).click()
        driver.find_element(By.XPATH, '//*[@id="list-form"]/fieldset/div[6]/button').click()
        driver.find_element(By.XPATH, '//*[@id="_LAYER_"]/div/div/div[1]/ul/li[2]/a').click()
        driver.find_element(By.XPATH, '//*[@id="_LAYER_"]/div/div/div[4]/input').click()
    
    # 카드번호 입력
    driver.find_element(By.ID, 'Tk_stlCrCrdNo14_checkbox').click()
    driver.find_element(By.ID, 'stlCrCrdNo11').send_keys(card_num[0])
    driver.find_element(By.ID, 'stlCrCrdNo12').send_keys(card_num[1])
    driver.find_element(By.ID, 'stlCrCrdNo13').send_keys(card_num[2])
    driver.find_element(By.ID, 'stlCrCrdNo14').send_keys(card_num[3])
    # 유효기간 입력
    elm_exp_mon = driver.find_element(By.ID, 'crdVlidTrm1M')
    Select(elm_exp_mon).select_by_value(exp_date_mon)
    elm_exp_yr = driver.find_element(By.ID, 'crdVlidTrm1Y')
    Select(elm_exp_yr).select_by_value(exp_date_yr)
    # 비밀번호 앞자리 입력
    driver.find_element(By.ID, 'Tk_vanPwd1_checkbox').click()
    driver.find_element(By.ID, 'vanPwd1').send_keys(card_pwd)
    # 인증번호 입력
    driver.find_element(By.ID, 'athnVal1').send_keys(user_brth)
    
    # 좌석+입석이 아닌 경우 스마트폰 발권 선택
    if (not round_trip) and (rsv_txt == '예약하기'):
        # 스마트폰 발권 선택
        driver.find_element(
            By.XPATH,
            '//*[@id="select-form"]/fieldset/div[11]/div[2]/ul/li[2]/a'
            ).click()
        Alert(driver).accept()
    
    # 2명 이상일 경우 승차자명 입력
    if int(adult_num) >= 2:
        for i, name in enumerate(user_name, start = 1):
            name_xpath = '//*[@id="select-form"]/fieldset/div[11]/div[5]/div[3]/table/tbody/tr[{}]/td[8]/input[2]'.format(i*2 + 1)
            driver.find_element(By.XPATH, name_xpath).send_keys(name)
    
    # 개인정보 제공 동의 선택
    driver.find_element(By.ID, 'agreeTmp').click()
    # 결제 및 발권 버튼 선택
    driver.find_element(By.ID, 'requestIssue1').click()
    # 경고창 확인 클릭
    Alert(driver).accept()


def srt_ticketing(
    user_id: str = user_id,
    user_pwd: str = user_pwd,

    dpt: str = dpt,
    arv: str = arv,
    dpt_date: str = dpt_date,
    dpt_time: str = dpt_time,
    adult_num: str = adult_num,

    round_trip: bool = round_trip,

    ret_date: str = ret_date,
    ret_time: str = ret_time,

    card_num: list = card_num,
    exp_date_mon: str = exp_date_mon,
    exp_date_yr: str = exp_date_yr,
    card_pwd: str = card_pwd,
    user_brth: str = user_brth,

    phn_num: list = phn_num
    ):
    # 전역변수 설정
    global driver
    
    
    '''
    2시간 지났는지 체크
    해당 코드는 최대 2시간 진행됨.
    '''
    srt_time = datetime.datetime.now()
    now_time = datetime.datetime.now()


    '''
    30 ~ 60초 중 랜덤하게 뽑아 기다리면서 반복해서 티켓 확인
    '''
    while srt_time + datetime.timedelta(hours = 2) >= now_time:
        
        # 코드 종료 플래그
        stop = False
        
        
        options = Options()
        # options.add_experimental_option('detach', True)
        options.add_argument('headless')                  # 서버에서 돌릴 경우 옵션

        driver = webdriver.Chrome(options = options)
        driver.implicitly_wait(10)
        
        
        '''
        srt 사이트 로그인 코드
        '''
        # 로그인
        signup_url = 'https://etk.srail.kr/cmc/01/selectLoginForm.do'
        driver.get(url = signup_url)

        driver.find_element(By.ID, 'srchDvNm01').send_keys(user_id)
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(user_pwd)
        driver.find_element(
            By.XPATH,
            '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
            ).click()

        # srt 메인 페이지에서 팝업창 삭제
        wait = WebDriverWait(driver, timeout = 5)
        wait.until(lambda d: 'main' in driver.current_url)
        main_brsr = driver.window_handles
        if len(main_brsr) > 1:
            for i in main_brsr:
                if i != main_brsr[0]:
                    driver.switch_to.window(i)
                    driver.close()
            driver.switch_to.window(main_brsr[0])
        
        
        '''
        일반승차권 일반승차권 조회 페이지로 이동
        '''
        schedule_url = 'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do'
        driver.get(url = schedule_url)
        wait.until(lambda d: 'selectScheduleList' in driver.current_url)
        
        
        '''
        가는 기차편 옵션 입력
        '''
        # 출발, 도착 기차역 입력
        select_stn(dpt = dpt, arv = arv)
        
        # 가는 열차 날짜 선택
        select_dt_tm(date = dpt_date, time = dpt_time)

        # 인원 선택
        select_headcount(adult_num = adult_num)
        
        
        '''
        왕복일 경우 오는 기차편 옵션 입력
        '''
        if round_trip:
            driver.find_element(By.ID, 'chtnDvCd3').click()
            Alert(driver).accept()
            
            # 오는 날 선택
            select_dt_tm(date = ret_date, time = ret_time, ret = True)
        
        
        '''
        조회하기 버튼 클릭
        '''
        elm_srch_but = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
        elm_srch_but.click()
        
        
        if not round_trip:
            '''
            편도일 경우 열차 선택
            표가 있는 경우:               결제 완료 후 코드 종료
            입석 + 좌석 표가 있는 경우:     결제 완료 후 다음 열차 체크
            예약대기인 경우:               예약 완료 후 다음 열차 체크
            예약대기 횟수 초과인 경우:       코드 종료
            '''
            col = 1
            bs_xpath = '//*[@id="result-form"]/fieldset/div[6]/table/tbody/'
            dpt_hour, dpt_min = train_time(col = col, bs_xpath = bs_xpath)

            while int(dpt_hour) <= (int(dpt_time) + 1):
                rsv_txt = but_text(col = col, bs_xpath = bs_xpath)
                if rsv_txt == '예약하기':
                    # 예약하기 버튼 클릭
                    but_click(col = col, bs_xpath = bs_xpath)
                    
                    # 경고창 확인 클릭
                    try:
                        Alert(driver).accept()
                    except:
                        pass
                    
                    # 결제 단계 진행
                    payment(
                        card_num = card_num,
                        exp_date_mon = exp_date_mon,
                        exp_date_yr = exp_date_yr,
                        card_pwd = card_pwd,
                        user_brth = user_brth,
                        round_trip = round_trip,
                        rsv_txt = rsv_txt,
                        adult_num = adult_num,
                        user_name = user_name
                        )
                    
                    # 코드 종료
                    stop = True
                    break
                elif rsv_txt == '입석+좌석':
                    but_click(col = col, bs_xpath = bs_xpath)
                    
                    # 경고창 확인 클릭
                    Alert(driver).accept()
                    
                    # 결제 단계 진행
                    payment(
                        card_num = card_num,
                        exp_date_mon = exp_date_mon,
                        exp_date_yr = exp_date_yr,
                        card_pwd = card_pwd,
                        user_brth = user_brth,
                        round_trip = round_trip,
                        rsv_txt = rsv_txt,
                        adult_num = adult_num,
                        user_name = user_name
                        )
                else:
                    '''
                    좌석, 입석 모두 없는 경우 예약대기 확인
                    '''
                    # 예약대기 버튼 확인
                    wait_txt = but_text(col = col, bs_xpath = bs_xpath, resve = True)
                    # 예약대기 버튼 클릭
                    if wait_txt == '신청하기':
                        '''
                        예약대기가 있는 경우
                        '''
                        # 신청하기 버튼 클릭
                        but_click(col = col, bs_xpath = bs_xpath, resve = True)
                        # 개인정보 수집 동의
                        driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div/div[2]/div[4]/div[2]').click()
                        # SMS알림서비스 선택
                        driver.find_element(By.XPATH, '//*[@id="smsY"]').click()
                        Alert(driver).accept()
                        # 휴대폰 번호 입력
                        dft_1st_phn_num = driver.find_element(
                            By.XPATH,
                            '//*[@id="list-form2"]/fieldset/div[6]/table/tbody/tr[2]/td/div/a/span[2]'
                            ).text
                        if dft_1st_phn_num != phn_num[0]:
                            driver.find_element(
                                By.XPATH,
                                '//*[@id="list-form2"]/fieldset/div[6]/table/tbody/tr[2]/td/div/a'
                                ).click()
                            if phn_num[0] == '010':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-1"]').click()
                            elif phn_num[0] == '011':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-2"]').click()
                            elif phn_num[0] == '016':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-3"]').click()
                            elif phn_num[0] == '017':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-4"]').click()
                            elif phn_num[0] == '018':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-5"]').click()
                            elif phn_num[0] == '019':
                                driver.find_element(By.XPATH, '//*[@id="ui-id-6"]').click()
                        driver.find_element(By.ID, 'phoneNum1').send_keys(phn_num[1])
                        driver.find_element(By.ID, 'phoneNum2').send_keys(phn_num[2])
                        # 다른 차실 예약
                        driver.find_element(By.ID, 'diffSeatY').click()
                        # 확인 버튼 클릭
                        driver.find_element(By.ID, 'moveTicketList').click()
                        # 경고창 확인 클릭
                        Alert(driver).accept()
                    else:
                        '''
                        예약대기가 없는 경우
                        '''
                        col += 1
                        dpt_hour, dpt_min = train_time(col = col, bs_xpath = bs_xpath)
                        continue
                
                # 다시 기차편 조회
                driver.get(url = schedule_url)
                wait.until(lambda d: 'selectScheduleList' in driver.current_url)
                
                '''
                가는 기차편 옵션 입력
                '''
                # 출발, 도착 기차역 입력
                select_stn(dpt = dpt, arv = arv)

                # 가는 날 선택
                select_dt_tm(date = dpt_date, time = dpt_time)
                
                # 인원 선택
                select_headcount(adult_num = adult_num)
                
                
                '''
                조회하기 버튼 클릭
                '''
                elm_srch_but = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
                elm_srch_but.click()
                
                # 다음 행 시간 확인
                col += 1
                dpt_hour, dpt_min = train_time(col = col, bs_xpath = bs_xpath)
        
        else:
            '''
            왕복일 경우 열차 선택
            표 있는 경우:         결제 완료 후 코드 종료
            입석+좌석 있는 경우:    결제 완료 후 편도 티켓 확인
            '''
            col = 1
            bs_xpath = '//*[@id="result-form"]/fieldset/div[6]/table/tbody/'
            dpt_hour, dpt_min = train_time(col = col, bs_xpath = bs_xpath)
            
            dpt_agn = False
            ret_agn = False
            while int(dpt_hour) <= (int(dpt_time) + 1):
                rsv_txt = but_text(col = col, bs_xpath = bs_xpath)
                if rsv_txt != '매진':
                    if rsv_txt == '입석+좌석':
                        dpt_agn = True
                    if dpt_date == ret_date:
                        # 가는 열차 도착 시간 저장
                        arv_time_xpath = bs_xpath + 'tr[{}]/td[5]/em'.format(col)
                        arv_time = datetime.datetime.strptime(
                            driver.find_element(
                                By.XPATH, arv_time_xpath
                                ).text,
                            '%H:%M'
                            )
                    
                    # 가는 열차 버튼 클릭
                    but_click(col = col, bs_xpath = bs_xpath)
            
                    # 경고창 확인 클릭
                    try:
                        Alert(driver).accept()
                    except:
                        pass
                    
                    break
                    
                else:
                    col += 1
                    dpt_hour, dpt_min = train_time(col = col, bs_xpath = bs_xpath)
                    continue
            else:
                time.sleep(random.randint(30, 60))
                now_time = datetime.datetime.now()
                continue
            
            col = 1
            bs_xpath = '//*[@id="result-form"]/fieldset/div[13]/table/tbody/'
            ret_hour, ret_min = train_time(col = col, bs_xpath = bs_xpath)
            
            while int(ret_hour) <= (int(ret_time) + 1):
                if dpt_date == ret_date:
                    # 가는 열차 도착 시간, 오는 열차 출발 시간 비교
                    if arv_time < datetime.datetime.strptime('{}:{}'.format(ret_hour, ret_min), '%H:%M'):
                        col += 1
                        ret_hour, ret_min = train_time(col = col, bs_xpath = bs_xpath)
                        continue
                    else:
                        pass
                
                rsv_txt = but_text(col = col, bs_xpath = bs_xpath)
                if rsv_txt != '매진':
                    if rsv_txt == '입석+좌석':
                        ret_agn = True
                    
                    # 오는 열차 버튼 클릭
                    but_click(col = col, bs_xpath = bs_xpath)
            
                    # 경고창 확인 클릭
                    try:
                        Alert(driver).accept()
                    except:
                        pass
                    
                    break
                    
                else:
                    col += 1
                    ret_hour, ret_min = train_time(col = col, bs_xpath = bs_xpath)
                    continue
            
            # 가는 열차, 오는 열차 모두 있는지 확인
            dpt_txt = driver.find_element(
                By.XPATH,
                '//*[@id="result-form"]/fieldset/div[17]/table/tbody/tr[1]/td[1]'
                ).text
            ret_txt = driver.find_element(
                By.XPATH,
                '//*[@id="result-form"]/fieldset/div[17]/table/tbody/tr[2]/td[1]'
                ).text
            if dpt_txt == '' or ret_txt == '':
                driver.quit()
                
                time.sleep(random.randint(30, 60))
                now_time = datetime.datetime.now()
                
                continue
            else:
                pass
            
            # 예약요청 버튼 클릭
            driver.find_element(By.XPATH, '//*[@id="result-form"]/fieldset/div[19]/input[2]').send_keys('\n')
            
            # 결제 단계 진행
            payment(
                card_num = card_num,
                exp_date_mon = exp_date_mon,
                exp_date_yr = exp_date_yr,
                card_pwd = card_pwd,
                user_brth = user_brth,
                round_trip = round_trip,
                rsv_txt = rsv_txt,
                adult_num = adult_num,
                user_name = user_name
            )
            
            driver.quit()
            
            if dpt_agn:
                '''
                가는 열차 좌석+입석인 경우
                '''
                # 편도 티켓팅 코드
                srt_ticketing(round_trip = False)
                
            if ret_agn:
                '''
                오는 열차 좌석+입석인 경우
                '''
                # 편도 티켓팅 코드
                srt_ticketing(dpt = arv, arv = dpt, dpt_date = ret_date, dpt_time = ret_time, round_trip = False)
            
            # 코드 종료
            stop = True
            break
        
        driver.quit()
        
        if stop:
            break
        else:
            time.sleep(random.randint(30, 60))
            now_time = datetime.datetime.now()


srt_ticketing()