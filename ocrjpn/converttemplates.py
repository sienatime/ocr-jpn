  # -*- coding: utf-8 -*-
from PIL import Image
import os
from recognize import save_image, crop_image

def threshold_image(im):
    im_x, im_y = im.size

    black_pixels = []

    # threshold the image
    for i in range(im_y):
        for j in range (im_x):
            #this is not the exact same function as in imagetests since we don't need to bother getting the average of the image since we already know what it is.
            if im.getpixel((j,i)) < 172:
                black_pixels.append((j,i))
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    return im, black_pixels

def make_templates(im, kanji):
    # you are going to want to change the WIDTH and HEIGHT of each character. use the grid in photoshop to help you.
    # you are also going to want to change the number of kanji per row (you mod by it around line 41)
    width = 150 #125 for mincho kanji, 200 for kana
    height = 150 #145 for kanji, 150 for kana
    origin = 0
    box = (0, 0, width, height)
    row = 1

    for i in range(1, len(kanji)+1):
        print i
        print box
        work = im.crop(box)

        new_image, black_pixels = threshold_image(work)
        new_work = crop_image(new_image, black_pixels)
        save_image(new_work, kanji[i-1]+".bmp", "BMP")

        if i % 6 == 0 and i != 0: #8 for mincho kanji, 5 for kana
            #go to the next line
            box = (origin, origin + (row*height), width, height*(row+1))
            row += 1
        else:
            box = (box[0]+width, box[1], box[2]+width, box[3])

def main():
    # HOW TO USE THIS FILE
    # in word, MAKE SURE your rows are EVENLY SPACED across ALL PAGES. put a hard return in there, it helps! don't let word do them differently!
    # put all of your images in a folder that you specify in raw_dir
    # paste the kanji from your word file into raw_kanji
    # num_chars is the number of characters per page (file)
    # the template_boxes are where you want to crop the whitespace to (x1,y1,x2,y2)
    # see more instructions in make_templates()

    raw_dir = "../idk/original gothic files/jinmeiyou"

    num_chars = 48 #for mincho kanji templates, 64, for kana, 35

    list_of_files = os.listdir(raw_dir) 
    raw_kanji = u"娃 阿 挨 逢 葵 茜 渥 旭 葦 芦 梓 斡 宛 絢 綾 鮎 或 粟 庵 按 闇 鞍 杏 伊 夷 惟 椅 畏 謂 亥 郁 磯 溢 茨 鰯 允 胤 蔭 烏 迂 卯 鵜 窺 丑 碓 臼 唄 姥 厩 瓜 閏 噂 云 叡 曳 瑛 榎 堰 奄 燕 艶 苑 薗 於 甥 旺 襖 岡 荻 臆 桶 牡 俺 伽 嘉 珂 禾 茄 蝦 嘩 迦 霞 俄 峨 牙 臥 駕 廻 恢 魁 晦 芥 蟹 凱 崖 蓋 鎧 浬 馨 柿 笠 樫 梶 恰 葛 叶 椛 樺 鞄 兜 蒲 釜 鎌 鴨 茅 萱 粥 瓦 侃 柑 竿 莞 韓 巌 玩 雁 伎 嬉 毅 畿 稀 徽 亀 祇 誼 掬 鞠 桔 橘 砧 杵 汲 灸 笈 鋸 亨 匡 卿 喬 蕎 饗 尭 桐 僅 巾 錦 欣 欽 禽 芹 衿 玖 矩 駈 駒 喰 寓 串 櫛 釧 屑 窟 沓 窪 熊 隈 栗 鍬 袈 祁 圭 慧 桂 稽 詣 戟 隙 桁 訣 倦 喧 拳 捲 牽 硯 鍵 絃 舷 諺 乎 糊 袴 胡 虎 跨 伍 吾 梧 檎 瑚 醐 鯉 倖 勾 宏 巷 庚 弘 昂 晃 杭 梗 浩 紘 腔 膏 閤 鴻 劫 壕 轟 忽 惚 此 頃 昏 些 叉 嵯 沙 瑳 裟 坐 哉 塞 采 犀 砦 冴 阪 堺 榊 肴 埼 鷺 朔 柵 窄 笹 拶 薩 皐 錆 晒 撒 燦 珊 纂 讃 仔 孜 斯 獅 爾 而 蒔 汐 鹿 竺 雫 悉 篠 偲 柴 縞 紗 灼 錫 惹 洲 蒐 蹴 輯 峻 竣 舜 駿 楯 淳 醇 曙 渚 恕 哨 嘗 庄 捷 昌 梢 樟 湘 菖 蕉 裳 鞘 丞 杖 穣 埴 拭 燭 晋 榛 秦 芯 壬 腎 訊 諏 須 厨 逗 翠 錐 瑞 嵩 雛 菅 頗 雀 裾 摺 凄 棲 栖 醒 戚 蹟 碩 尖 撰 煎 穿 羨 詮 閃 膳 噌 曾 曽 楚 疏 蘇 遡 叢 爽 宋 惣 槍 漕 綜 聡 蒼 捉 袖 其 揃 遜 汰 舵 楕 陀 堆 戴 苔 黛 鯛 醍 鷹 瀧 啄 托 琢 茸 凧 只 辰 巽 竪 辿 樽 誰 坦 旦 歎 湛 耽 檀 弛 智 馳 筑 註 酎 猪 喋 寵 帖 暢 牒 蝶 椎 槌 槻 佃 柘 辻 蔦 綴 椿 紬 爪 鶴 悌 挺 梯 汀 禎 諦 蹄 鄭 釘 鼎 擢 填 纏 貼 顛 兎 堵 杜 砥 套 宕 嶋 燈 董 藤 憧 撞 瞳 萄 栃 鳶 寅 酉 惇 敦 沌 遁 頓 奈 那 凪 薙 謎 灘 捺 鍋 楢 馴 楠 汝 匂 賑 虹 廿 濡 禰 祢 捻 乃 之 埜 巴 播 杷 琶 芭 盃 煤 這 秤 萩 柏 箔 曝 莫 函 箸 肇 筈 幡 畠 鳩 塙 隼 斑 汎 挽 磐 蕃 庇 斐 緋 樋 枇 毘 琵 眉 柊 疋 彦 菱 肘 畢 桧 媛 紐 彪 瓢 豹 廟 彬 瀕 冨 斧 芙 阜 撫 葡 蕪 楓 葺 蕗 淵 吻 焚 蔽 頁 碧 瞥 篇 娩 鞭 圃 甫 輔 戊 菩 峯 捧 朋 萌 蓬 蜂 鋒 鳳 鵬 貌 卜 睦 勃 殆 幌 昧 哩 槙 枕 柾 鱒 亦 俣 沫 迄 麿 蔓 巳 箕 蜜 湊 蓑 稔 牟 椋 冥 姪 孟 蒙 儲 勿 餅 尤 籾 貰 也 冶 耶 弥 靖 佑 宥 柚 湧 祐 邑 輿 傭 妖 楊 耀 蓉 遥 淀 螺 洛 嵐 藍 蘭 李 梨 璃 裡 掠 劉 溜 琉 龍 侶 亮 凌 梁 瞭 稜 諒 遼 淋 琳 鱗 麟 瑠 伶 嶺 怜 玲 憐 漣 煉 簾 蓮 呂 魯 櫓 狼 麓 禄 肋 倭 脇 鷲 亙 亘 詫 藁 蕨 椀 碗 乘 亞 佛 侑 來 俐 傳 僞 價 儉 兒 凉 凛 凰 刹 剩 劍 勁 勳 卷 單 嚴 圈 國 圓 團 壞 壘 壯 壽 奎 奧 奬 孃 實 寢 將 專 峽 崚 巖 已 帶 廣 廳 彈 彌 彗 從 徠 恆 惡 惠 惺 愼 應 懷 戰 戲 拔 拜 拂 搜 搖 攝 收 敍 昊 昴 晏 晄 晝 晨 晟 暉 曉 曖 檜 栞 條 梛 椰 榮 樂 樣 橙 檢 櫂 櫻 盜 毬 氣 洸 洵 淨 滉 漱 滯 澁 澪 濕 煌 燒 燎 燿 爭 爲 狹 默 獸 珈 珀 琥 瑶 疊 皓 盡 眞 眸 碎 祕 祿 禪 禮 稟 稻 穗 穰 笙 粹 絆 綺 綸 縣 縱 纖 羚 翔 飜 聽 脩 臟 與 苺 茉 莊 莉 菫 萠 萬 蕾 藏 藝 藥 衞 裝 覽 詢 諄 謠 讓 賣 赳 轉 迪 逞 醉 釀 釉 鎭 鑄 陷 險 雜 靜 頌 顯 颯 騷 驍 驗 髮 鷄 麒 黎 齊 堯 槇 遙 凜 熙 俠 摑 擊 焰 瘦 禱 繡 繫 萊 蔣 蠟 醬 頰 鷗"
    kanji = raw_kanji.split()
    start = 0
    end = num_chars

    kanji_template_box_m = (125,145,1145,1305) # 1020 x 1160
    kanji_template_box_g = (117, 141, 1017, 1341)
    kana_template_box = (95,148,1095,1198)

    print len(kanji)

    for f in list_of_files:

        im = Image.open(raw_dir+"/"+f).convert("L")

        cropped = im.crop(kanji_template_box_g)
        make_templates(cropped, kanji[start:end])
        start += num_chars
        end += num_chars

if __name__ == "__main__":
    main()