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
window.title("GoodSearch")
window.geometry("1000x800+100+100")
window.resizable(False, False)
# window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file=''))
label=tk.Label(window, text="GoodSearch!", width=40, height=3, fg="black", relief="solid",font= 'D2Coding')
label.pack()


def find_sim_product(df, sorted_ind, similarity, product_description, top_n = 10):
    product_description = df[df['Description'] == product_description]
    product_index = product_description.index.values
    similar_indexes = sorted_ind[product_index,:(top_n)]          
    similar_indexes = similar_indexes.reshape(-1)
    a = similarity[product_index,:(top_n)]
    new_df = df.iloc[similar_indexes].copy()
    # new_df['similarity'] = similarity[product_index,:(top_n)]
    return new_df
product_copy_df = pd.read_csv('../')
# 사용자 입력값 받기
def submit():
    for widget in window.winfo_children():
            if widget.winfo_class() == 'Label':
                widget.destroy()


    value = value_entry.get()

    # 입력값을 데이터프레임으로 만들기
    data = {'입력값': [value]}
    df = pd.DataFrame(data)
    
    product_copy_df = pd.read_csv('Recommand and image making\\product_copy.csv')


    count_vect = CountVectorizer(min_df=0, ngram_range=(1,2))
    # description_mat = count_vect.fit_transform(product_copy_df['Description'])
    # print(description_mat)
    count_vect.fit(product_copy_df['Description'])
    description_mat = count_vect.transform(product_copy_df['Description'])

    print(description_mat.shape)
    product_sim = cosine_similarity(description_mat,description_mat)

    product_sim_sorted_ind = product_sim.argsort()[:,::-1]
    product_sim_sorted_ind
    similarity = np.round(np.sort(product_sim)[:,::-1],3)



    if len(product_copy_df[product_copy_df['Description'].str.contains('box',case = False)]) > 0:
        x = rd.randint(0,len(product_copy_df[product_copy_df['Description'].str.contains(value, case = False)]))
        similar_target = product_copy_df[product_copy_df['Description'].str.contains(value, case = False)].iloc[x]['Description']
    else:
        # 검색어가 포함된 행이 없으면 '없음'을 출력
        print('검색어가 포함된 행이 없습니다.')

    similar_product = find_sim_product(product_copy_df, product_sim_sorted_ind, similarity, similar_target,5)
    similar_product.drop(['Unnamed: 0', 'Country','CustomerID','Description_literal'], axis=1,inplace=True)
    
    similar_product.columns = ['상품코드', '상품명', '                    가격', '         누적구매량']
    present_image_name = similar_product['상품명'].iloc[0].strip()
        
        
    # 데이터프레임 출력하기

    df_label = tk.Label(window, text=similar_product.to_string(), font=('Arial', 12))
    df_label.pack()

    
        
    # 발급받은 API 키 설정
    KAKAO_API_KEY = '0a4de529e0392f4e061a94adf9cce499'

    # Karlo API 인스턴스 생성
    karlo = Karlo(service_key = KAKAO_API_KEY)

    text = present_image_name

    # 이미지 생성하기 REST API 호출
    img_dict = karlo.text_to_image(text, 1)

    # 생성된 이미지 정보
    img_str = img_dict.get("images")[0].get('image')

    # base64 string을 이미지로 변환
    present_image = karlo.string_to_image(base64_string = img_str, mode = 'RGBA')
    label=tk.Label(window, text="GoodSearch!", width=40, height=3, fg="black", relief="solid",font= 'D2Coding')
    label.pack()
    value_entry.pack()
    submit_button.pack()
    # 이미지 출력하기
    
    image = present_image  # 이미지 파일 경로 설정
    image = image.resize((480,480))
    photo = ImageTk.PhotoImage(image)
    
    image_label = tk.Label(window, image=photo)
    image_label.image = photo
    image_label.pack()

# 사용자 입력값 받을 텍스트박스 생성
value_label = tk.Label(window, text='검색어를 입력해주세요')
value_label.pack()
value_entry = tk.Entry(window)
value_entry.pack()

# '제출' 버튼 생성
submit_button = tk.Button(window, text='제출', command=submit)
submit_button.pack()
submit_button.place(x=600, y=75, relwidth=0.1)
# tkinter 창 실행
window.mainloop()