#　GFP画像と位相差画像を各１つ読み込んで、各35画像に分割。それぞれ対応する画像を連結する
#　画像のディレクトリはプログラム実行時に引数として指定する
#
#　ディレクトリ構造
#　　日付名ホルダー　・・・（プログラム実行の引数として入力名に使用予定）
#　　　　ウェル番号名フォルダー
#　　　　　　ファイル名Image_CH1.tif
#            ファイル名Image_CH2.tif
#　images_outフォルダに連結画像が保存される
#　使用方法
#　画像のフォルダはtoolsフォルダと同じ階層にあるとする
#　$python tools/cropmix.py xxxx2019
#　　　xxxx2019は画像のフォルダ


from PIL import Image 
import numpy as np
import re
import sys
import os
import glob

date_dir_name = sys.argv # イメージファイルを格納したディレクトリ名を指定

if (len(date_dir_name) != 2): # 入力の規則を間違えたことを知らる
    print ("Usage: $ python " + date_dir_name[0] + " DataDirectoryName")
    quit()

print(date_dir_name[1])

# ウェル番号名フォルダのパスのリストを取得する
l = glob.glob(date_dir_name[1] + '/**/')
print(l[0])
print(l[1])
counter = 0 # 出力ファイルに通し番号を付けるために設定

# ウェルパスのディレクトリ毎に2つのファイル名を開いて実行
for ii in l:
    img1 = Image.open(ii + '/Image_CH1.tif') # 指定名のイメージファイルを開く
    img2 = Image.open(ii + '/Image_CH2.tif') # 指定名のイメージファイル2を開く
    print(img1.size)
    print(img2.size)
    im = np.array(img1) # カラー画像をアレイに分解して読み込む
    im_gray = im[:,:,1] # BZ-X800のモノクロCCDで取得した画像の場合はグリーンをそのままグレーとして取得
    img1_gray = Image.fromarray(im_gray) #　アレイから画像を生成
    print(img1_gray.size)

# 読み込んだ画像を256*256のサイズで35枚に分割する
    height = 256
    width = 256
#    counter = 0
    subregion_img1_gray = list() # 分割したimg1_grayを代入する配列を用意
    subregion_img2 = list() # 分割したimg2を代入する配列を用意

# 切り出す位置の初期定義
    defX = 80 # 縦方向のピクセル位置初期値
    defY = 64 # 横方向のピクセル位置初期値


# img1_grayとimg2をそれぞれ分割する
# 縦の分割枚数
    for h1 in range(5):
    # 横の分割枚数
        for w1 in range(7):
            w2 = defY + (w1 * width)
            h2 = defX + (h1 * height)
            counter = counter + 1
            print(counter, w2, h2, width + w2, height + h2)
            c1 = img1_gray.crop((w2, h2, width + w2, height + h2)) # 左上と右下の座標で指定したimg1_gray画像を切り出す
            c2 = img2.crop((w2, h2, width + w2, height + h2)) # 左上と右下の座標で指定したimg2画像を切り出す
            dst = Image.new('L', (c1.width + c2.width, c1.height)) # 白黒画像を収める大きさを確保
            dst.paste(c1, (0,0))
            dst.paste(c2, (c1.width, 0))
            dst.save("./images_out/" + str(counter) +'.jpg',"JPEG") # 配列から画像を読みだして、番号をふってファイルを出力
