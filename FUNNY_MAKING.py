import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import warnings; warnings.filterwarnings('ignore')
import random as rd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import PIL.ImageTk
import matplotlib.pyplot as plt
from PyKakao import Karlo



# tkinter 창 생성
window=tk.Tk()
window.title("FUNNY MAKING!")
window.geometry("1000x800+100+100")
window.resizable(False, False)
# window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file=''))
label=tk.Label(window, text="FUNNY MAKING!", width=40, height=3, fg="black", relief="solid",font= 'D2Coding')
label.pack()


# 사용자 입력값 받기
def submit():
    for widget in window.winfo_children():
            if widget.winfo_class() == 'Label':
                widget.destroy()

    value = value_entry.get()

    # 입력값을 데이터프레임으로 만들기
    data = {'입력값': [value]}
    df = pd.DataFrame(data)
    
        
    # 발급받은 API 키 설정
    KAKAO_API_KEY = '0a4de529e0392f4e061a94adf9cce499'

    # Karlo API 인스턴스 생성
    karlo = Karlo(service_key = KAKAO_API_KEY)

    text = value

    # 이미지 생성하기 REST API 호출
    img_dict = karlo.text_to_image(text, 1)

    # 생성된 이미지 정보
    img_str = img_dict.get("images")[0].get('image')

    # base64 string을 이미지로 변환
    present_image = karlo.string_to_image(base64_string = img_str, mode = 'RGBA')
    label=tk.Label(window, text="GoodSearch!", width=40, height=3, fg="black", relief="solid",font= 'D2Coding')
    value_entry.pack()
    submit_button.pack()
    # 이미지 출력하기
    label_item=tk.Label(window, text="생성 이미지", width=40, height=3, fg="black", relief="solid",font= 'D2Coding')
    label_item.pack()
    image = present_image  # 이미지 파일 경로 설정
    image = image.resize((480,480))
    photo = ImageTk.PhotoImage(image)
    
    image_label = tk.Label(window, image=photo)
    image_label.image = photo
    image_label.pack()

# 사용자 입력값 받을 텍스트박스 생성
value_label = tk.Label(window, text='키워드를 입력해주세요!')
value_label.pack()
value_entry = tk.Entry(window)
value_entry.pack()

# '제출' 버튼 생성
submit_button = tk.Button(window, text='제출', command=submit)
submit_button.pack()
submit_button.place(x=600, y=75, relwidth=0.1)
# tkinter 창 실행
window.mainloop()