#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import pygame.mixer
import numpy as np
import picamera
from PIL import Image
from time import sleep
import efficientnet.keras
import time

photo_filename = 'data.jpg'

def shutter():
    photofile = open(photo_filename, 'wb')
    print(photofile)

    # pi camera 用のライブラリーを使用して、画像を取得
    with picamera.PiCamera() as camera:
        #camera.resolution = (640,480)
        camera.resolution = (300,400)
        camera.start_preview()
        sleep(1.000)
        camera.capture(photofile)
        

def cosine_similarity(x1, x2):
    """
    test_dataと学習済み商品のコサイン類似度を算出
    n_dimはベクトルの次元　1000~1500程度
    x1: 対象の商品のベクトル   shape(1, n_dim)
    x2: 学習済みの商品のベクトル(hold_vector) shape(5, n_dim)
    return: 5つの商品に対するコサイン類似度 shape(1,5)
    """
    
    if x1.ndim == 1:
        x1 = x1[np.newaxis]
    if x2.ndim == 1:
        x2 = x2[np.newaxis]
    x1_norm = np.linalg.norm(x1, axis=1)
    x2_norm = np.linalg.norm(x2, axis=1)
    cosine_sim = np.dot(x1, x2.T)/(x1_norm*x2_norm+1e-10)
    return cosine_sim     
        
        
def judgment(predict_vector, hold_vector, thresh):
    """
    predict_vector : shape(1,1028)
    hold_vector : shape(5, 1028)
    """
    cos_similarity = cosine_similarity(predict_vector, hold_vector) # shape(1, 5)
    print(cos_similarity[0])
    # 最も値が高いindexを取得
    high_index = np.argmax(cos_similarity[0]) # int
    # cos類似度が閾値を超えるか
    if cos_similarity[0][high_index] > thresh:
        return high_index
    
    else:
        return 5        
        
        


if __name__ == '__main__':
    # モデル+重みを読込み
    #self_model = load_model('MobileNet_auto_fine3_150_3.h5')
    self_model = load_model('models/eff3_model.h5')
    
    # 音声ファイル初期化
    pygame.mixer.init()

    # pygame.mixer.music.load("incorrect1.mp3")
    
    hold = np.load("models/hold_vector.npy") ###

    # 正解ラベル
    label = ['o-iocha', 'life-guard', 'pocari-sweat', 'coffee-Georgia', 'water', 'error']
    # 商品価格
    money = {'o-iocha':110, 'life-guard':120, 'pocari-sweat':130, 'coffee-Georgia':140, 'water':150, 'error':0}

# 「いらっしゃいませ」の音声


    lang = input('which langage?\n English:press "e"\n Flench:press "f"\n Japanese:press "j"')

    
    if lang == "e":
        pygame.mixer.music.load("sound/start_eng.mp3")
        pygame.mixer.music.play(1)
    elif lang == "f":
        pygame.mixer.music.load("sound/start_fr.mp3")
        pygame.mixer.music.play(1)
        #pygame.mixer.music.stop()
    else:
        pygame.mixer.music.load("sound/start_jpn.mp3")
        pygame.mixer.music.play(1)
        #pygame.mixer.music.stop()
        



    while True:
        basket = []
        money_sum = 0
        if lang == "e":
            key = input('Press "Enter" to scan products')
        elif lang == "f":
            key=input('Appuyez sur "Enter" pour numeriser les produits')
        else:
            key = input('商品をスキャンする場合は「Enter」を押して下さい')
        while True:
            # 画像の取得
            shutter()

            # 音声再生
            pygame.mixer.music.load("sound/Cash_Register-Beep01-1.mp3")
            pygame.mixer.music.play(1)
            sleep(1)
            # 再生の終了
            pygame.mixer.music.stop()
            t1 = time.time() 

            # 画像をモデルの入力用に加工
            img = Image.open(photo_filename)
            #img = Image.open("./0.jpg")
            img = img.resize((224, 224))
            img_array = img_to_array(img)
            img_array = img_array.astype('float32')/255.0
            img_array = img_array.reshape((1,224,224,3))
            
            
            
            # predict
            img_pred = self_model.predict(img_array)
            jd = judgment(predict_vector=img_pred, hold_vector=hold, thresh=0.992) ###
            ######
            name=label[jd]
            print(name ,money[name])
            if jd != 5:
                basket.append(name)
            else:
                if lang == "e":
                    print("Error. Please scan the product again.")
                elif lang == "f":
                    print("Erreur. Veuillez numeriser a nouveau le produit.")
                else:
                    print("エラーです。再度商品をスキャンしてください。")
                
                break
            #print("judgment",jd) ###
            
            #print("debug:",img_pred)
            #name = label[np.argmax(img_pred)]
            #print(name)
            for i, j in enumerate(basket):
                print(i,j,sep=":")
            
            money_sum += money[name]
            if lang == "e":
                print("subtotal",money_sum)
            elif lang == "f":
                print("Sous-total",money_sum)
            else:
                print("小計",money_sum)
            
            t2 = time.time() 
            elapsed_time = t2-t1
            print("処理時間：{}".format(elapsed_time))


            
            if lang == "e":
                key = input(' Press "y" to continue scanning products. When you want to pay, please press "Enter". \n Press "x" if you have any items to cancel.')
            elif lang == "f":
                key = input(' ppuyez sur "y" pour continuer a numeriser les produits ou sur "Enter" pour verifier. \n Appuyez sur "x" si vous avez des elements a annuler.')
            else:
                key = input(' 続けて商品をスキャンする場合は「Enter」,会計する場合は「y」を押して下さい \n キャンセルする商品がある場合は「ｘ」を押してください')
            
            #try:
            if key == "x":
                if lang == "e":
                    num = input("Enter the number of the product you want to cancel")
                    c_product = basket[int(num)]
                    c_money = money[c_product]
                    money_sum -= c_money
                    basket.pop(int(num))
                    print("subtotal",money_sum)
                    key = input(' Press "y" to continue scanning products. When you want to pay, please press "Enter".')
                elif lang == "f":
                    num = input("Entrez le numero du produit que vous souhaitez annuler.")
                    c_product = basket[int(num)]
                    c_money = money[c_product]
                    money_sum -= c_money
                    basket.pop(int(num))
                    print("Sous-total",money_sum)
                    key = input(' ppuyez sur "y" pour continuer a numeriser les produits ou sur "Enter" pour verifier.')
                else:
                    num = input("キャンセルする商品の番号を入力してください")
                    c_product = basket[int(num)]
                    c_money = money[c_product]
                    money_sum -= c_money
                    basket.pop(int(num))
                    print("小計",money_sum)
                    key = input(' 続けて商品をスキャンする場合は「Enter」,会計する場合は「y」を押して下さい')
                   

            if key == 'y':
                if lang == "e":
                    print("{} yen payment".format(money_sum))
                    pygame.mixer.music.load("sound/end_eng.mp3")
                    pygame.mixer.music.play(1)
                elif lang == "f":
                    print("Paiement de {} yens".format(money_sum))
                    pygame.mixer.music.load("sound/end_fr.mp3")
                    pygame.mixer.music.play(1)
                else:
                    print("{}円のお支払いです。".format(money_sum))
                    # 「ありがとうございました」の音声
                    pygame.mixer.music.load("sound/end_jpn.mp3")
                    pygame.mixer.music.play(1)
                break
            

            

