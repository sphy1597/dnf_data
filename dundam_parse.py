# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By 
from urllib import parse
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

import pandas as pd 




# 크롬드라이버 실행
driver = webdriver.Chrome() 

data = {
    'name': [],
    'fame': [],
    'damage': []
}

# create df
df_job = pd.DataFrame(data)
df_all = pd.DataFrame(data)



job_list = {
    '귀검사(남)': ['眞 웨펀마스터', '眞 버서커', '眞 소울브링어', '眞 아수라', '眞 검귀'],
    '격투가(남)': ['眞 넨마스터', '眞 스트리트파이터', '眞 그래플러', '眞 스트라이커'],
    '거너(남)': ['眞 레인저', '眞 메카닉', '眞 런처', '眞 스핏파이어', '眞 어썰트'],
    '마법사(남)': ['眞 블러드 메이지', '眞 엘레멘탈 바머', '眞 빙결사', '眞 디멘션워커', '眞 스위프트 마스터'],
    '프리스트(남)': ['眞 퇴마사', '眞 인파이터', '眞 어벤져'],
    '귀검사(여)': ['眞 소드마스터', '眞 데몬슬레이어', '眞 다크템플러', '眞 베가본드', '眞 블레이드'],
    '격투가(여)': ['眞 넨마스터', '眞 스트리트파이터', '眞 그래플러', '眞 스트라이커'],
    '마법사(여)': ['眞 엘레멘탈마스터', '眞 마도학자', '眞 소환사', '眞 배틀메이지'],
    '프리스트(여)': ['眞 이단심판관', '眞 미스트리스', '眞 무녀'],
    '도적': ['眞 로그', '眞 쿠노이치', '眞 섀도우댄서', '眞 사령술사'],
    '나이트': ['眞 엘븐나이트', '眞 카오스', '眞 드래곤나이트', '眞 팔라딘'],
    '마창사': ['眞 뱅가드', '眞 듀얼리스트', '眞 다크 랜서', '眞 드래고니안 랜서'],
    '총검사': ['眞 요원', '眞 트러블 슈터', '眞 히트맨', '眞 스페셜리스트'],
    '외전': ['眞 크리에이터', '眞 다크나이트'],
    '아처': ['眞 트래블러', '眞 헌터', '眞 비질란테'],

}

data_count = 0



# 총검사 >> 히트맨, 스페셜리스트
for base_job, jobs in job_list.items():
    
    
    
    for job in jobs:
        
        flag = True
        pageNum = 1
        
        url = "https://dundam.xyz/damage_ranking?page=1&type=8&job="+parse.quote(job)+"&baseJob="+parse.quote(base_job)+"&weaponType=%EC%A0%84%EC%B2%B4&weaponDetail=%EC%A0%84%EC%B2%B4"
        #크롬 드라이버에 url 주소 넣고 실행
        driver.get(url)
        
        print("baseJob : ", base_job)
        print("job start : ", job)
        time.sleep(1)
        
        bottomNum = 2
        
        while flag:
            nextBtn = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[5]/div/ul/li['+str(bottomNum)+']/span').click()
            time.sleep(1)
            
             # 한페이지에서 1~10번 가져오기
            for i in range(1, 11):
                name = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[4]/div[2]/div[2]/div['+str(i)+']/div[2]/span[2]').text
                fame = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[4]/div[2]/div[2]/div['+str(i)+']/div[2]/div/div[1]/span[2]').text
                damage = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[4]/div[2]/div[2]/div['+str(i)+']/div[3]/span[2]').text
                server = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[4]/div[2]/div[2]/div['+str(i)+']/div[2]/div/div[2]/div/span').text
        
                
                damage_replace = damage.replace(',', '')
                damage_int = int(damage_replace)
                
                fame_int = int(fame)
                
                # 안개신 컷인 4500억 이하면 중지
                if fame_int < 58087:
                    flag = False
                    break
                
                data_count += 1
                print("count : ", data_count)
                print("name : ", name)
                print("fame : ", fame)
                print("damage : ", damage_int)
                
                newData = {
                    'name' : name+"("+server+")",
                    'fame' : fame,
                    'damage' : damage_int
                }
                
                # df에 추가
                df_job.loc[len(df_job)] = newData
                df_all.loc[len(df_all)] = newData
            
            
            bottomNum += 1
        
            # 1~10 page까지 끝나면 다음 page로 넘어가서 11번 부터 다시 반복할 수 있도록
            if bottomNum >= 12:
                nextPage = driver.find_element(By.XPATH, '//*[@id="content-container"]/div[5]/div/ul/li[12]/span').click()
                bottomNum = 2

        df_job.to_csv('./dundam_'+job+'.csv', index=True)
        df_job.dropna(inplace=True)

df_all.to_csv('./dundam_all.csv', index=True)
    
# driver 종료
driver.quit() 

