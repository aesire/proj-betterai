from openai import OpenAI
client = OpenAI()

# Open files for writing
pvcv = open("pvcv.txt", 'w')
clst = open("clst.txt", 'w')
fsmy = open("smry.txt", 'w')

# Initialize variables
tick = 0
smry = 0
smcu = 5
tsel = 10
cset = ("ai assint, Previous Conversations:")
smru = ("Summarize the following by the rules below. 1. reveal the speaker's personality 2. summarize the content of the conversation succinctly 3. in the shortest possible length")

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
    pvcv.write(completion.choices[0].message + '\n')
    clst.write(usnp + '\n')

    tick += 1

    if tick >= tsel: #채팅 요약
        clst.close()
        clst = open("clst.txt", 'r')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": clst.read()}
        ]
        )
        print("내용 요약됨: ", completion.choices[0].message)
        fsmy.write(completion.choices[0].message + '\n')
        clst.close()
        clst = open("clst.txt", 'w')
        tick = 0
        tsel += 1

    elif tsel >= smcu: #요약 내용의 재처리
        fsmy.close()
        fsmy = open("smry.txt", 'r')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": fsmy.read()}
        ]
        )
        print("재처리 완료: ", completion.choices[0].message)
        fsmy.close()
        fsmy = open("smry.txt", 'w')
        fsmy.write(completion.choices[0].message + '\n')
        tsel = 0

    elif usnp == ("/save"):
        pvcv.close()
        clst.close()
        fsmy.close()

    elif usnp == ("/exit"):
        pvcv.close()
        clst.close()
        fsmy.close()
        break