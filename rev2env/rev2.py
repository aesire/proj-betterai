from openai import OpenAI
client = OpenAI()

#텍스트 파일 생성
pvcv = open("pvcv.txt", 'w')
pvcv.close()

clst = open("clst.txt", 'w')
clst.close()

fsmy = open("smry.txt", 'w')
clst.close()

pvcv = 0    #사용자가 이전에 응답한 내용
clst = []   #누적 채팅 내역
tick = 0    #마지막 정리 이후 누적 채팅량
slst = []   #전체 로그 내역
fact = 0    #임시
smry = 0    #요약한 횟수
fsmy = []   #전체 요약 내용 

smcu = 5    #가지고 있을 요약본의 수
tsel = 10   #내용 요약의 빈도
cset = ("ai assint, Previous Conversations:")   #ai의 시작 캐릭터
smru = ("Summarize the following by the rules below. 1. reveal the speaker's personality 2. summarize the content of the conversation succinctly 3. in the shortest possible length")   #ai의 요약 규칙

#from
while True: #채팅 내용
    usnp = input("내용 입력: ") 
    cnxt = (cset, clst), 

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": cnxt},
        {"role": "user", "content": usnp}
    ]
    )
    print(completion.choices[0].message)
    pvcv = open("pvcv.txt", 's')
    pvcv.write(completion.choices[0].message)
#to

#to change 1
    tick + 1

    if tick < tsel: #채팅 요약
        completion = client.chat.completions.create(
            model="gpt-4",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": clst}
        ]
        ),
        slst = clst
        clst = []
        clst = (completion.choices[0].message)
        tick = 0
        tsel + 1
        print("내용 요약됨")
#XXXXXXXXXXXXXXXXX

#to change 2
    elif tsel < smcu: #요약 내용의 재처리
         completion = client.chat.completions.create(
            model="gpt-4",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": clst}
        ]
        )
        slst = clst
        clst = []
        clst = completion.choices[0].message
        tsel = 0
        print("재처리 완료")
#XXXXXXXXXXXXXXXXX
            
        elif usnp == "/save":
            fact = 0

        elif usnp == "/exit":
            fact = 0
