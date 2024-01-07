import os
os.environ["OPENAI_API_KEY"] = "api key here"
from openai import OpenAI
from builtins import input
client = OpenAI()

# Open files for writing
pvcv = open("pvcv.txt", 'a')
clst = open("clst.txt", 'a')
fsmy = open("smry.txt", 'a')
log = open("log.txt", 'a')  # New file for logging all chat dialogues

# Initialize variables
tick = 0
smry = 0
smcu = 5
tsel = 10
cset = ("ai assint, Previous Conversations:")
smru = ("Summarize the following by the rules below. 1. reveal the speaker's personality 2. summarize the content of the conversation succinctly 3. in the shortest possible length")

while True: #채팅 내용
    usnp = input("내용 입력: ") 
    clst_content = open("clst.txt", 'r').read()
    cnxt = (cset, clst_content)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": str(cnxt)},  # Ensure the content is converted to a string
            {"role": "user", "content": str(usnp)}  # Ensure the content is converted to a string
        ]
    )
    print(completion.choices[0].message.content)
    pvcv.write(completion.choices[0].message.content + '\n')
    clst.write(usnp + '\n')
    log.write(f"User: {usnp}\nAI: {completion.choices[0].message.content}\n")  # Log the dialogue

    tick += 1

    if tick >= tsel: #채팅 요약
        clst_content = open("clst.txt", 'r').read()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": clst_content}
        ]
        )
        fsmy.write(completion.choices[0].message.content + '\n')
        clst.truncate(0)  # Clear the contents of clst.txt
        tick = 0
        tsel += 1

    elif tsel >= smcu: #요약 내용의 재처리
        fsmy_content = open("smry.txt", 'r').read()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": smru},
            {"role": "user", "content": fsmy_content}
        ]
        )
        fsmy.truncate(0)  # Clear the contents of smry.txt
        fsmy.write(completion.choices[0].message.content + '\n')
        tsel = 0

    elif usnp == ("/save"):
        pvcv.flush()
        clst.flush()
        fsmy.flush()
        log.flush()

    elif usnp == ("/exit"):
        pvcv.close()
        clst.close()
        fsmy.close()
        log.close()
        break
