import codecs
import hashlib
import http
import json
import os
import random
import urllib

import streamlit as st
from PIL import Image


def main():

    #侧边栏
    #st.sidebar.title("")
    st.sidebar.text("这是一个鸟儿描述文字生成图片的生成器。")
    #expimg=
    st.sidebar.text("你可以尝试增加更多的描述来获得一只更贴合你心意的鸟。（ 但我们都不确定它会生成怎么样的效果^ ^ ）")
    #st.sidebar.image(expimg,"")

    #正文栏
    st.title("Attention-GAN app")
    st.text(" you can write a sentence and the attngan can transfer it to a picuture.")
    text = st.text_input('请描述你心中的鸟', '一只有蓝色眼睛的红鸟')
    #sentence = translate(text)

    if st.button('生成鸟') and text:
        sentence=translate(text)

        #将sentence写入txt中  清空写
        textpath='../data/birds/example_captions.txt'
        with codecs.open(textpath,'a','utf-8') as w:
            w.seek(0)
            w.truncate()
            w.write(sentence)
            w.write('\n')
            w.write(sentence)
            w.write('\n')
            w.write(sentence)

        os.system("python main.py --cfg cfg/eval_bird.yml --gpu 0")

        imagepath0 = '../models/bird_AttnGAN2/example_captions/0_s_0_g2.png'
        imagepath1 = '../models/bird_AttnGAN2/example_captions/0_s_1_g2.png'
        imagepath2 = '../models/bird_AttnGAN2/example_captions/0_s_2_g2.png'

        #img=Image.open();
        img=Image.open(imagepath0)
        st.image(img, caption=text)
        img = Image.open(imagepath1)
        st.image(img, caption=text)
        img = Image.open(imagepath2)
        st.image(img, caption=text)


    #st.write('The current movie title is', sentence)


#https://blog.csdn.net/weixin_44259720/article/details/104648444
def translate(text):
    appid='20220212001081221'
    secretKry='3GylVRuw7LMQ9VtBxFWk'

    httpClient=None
    myurl='/api/trans/vip/translate'
    #myurl='https://fanyi-api.baidu.com/api/trans/vip/fieldtranslate'

    formLang='zh'
    toLang='en'
    salt=random.randint(32768,65536)
    sign=appid+text+str(salt)+secretKry
    sign=hashlib.md5(sign.encode()).hexdigest()
    myurl=myurl+'?appid='+appid+'&q='+urllib.parse.quote(text)+'&from='+formLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        httpClient=http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET',myurl)
        response=httpClient.getresponse()
        result_all=response.read().decode("utf-8")
        result=json.loads(result_all)
        result=result['trans_result'][0]['dst']


        return result
    except Exception as e:
        return e
    finally:
        if httpClient:
            httpClient.close()




if __name__ == "__main__":
    #print("fefef")
    #print(translate("一只可爱的鸟"))
    main()
    #os.system("cd code")

    #os.system("python main.py --cfg cfg/eval_bird.yml --gpu 0")
