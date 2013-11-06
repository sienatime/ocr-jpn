  # -*- coding: utf-8 -*-
from PIL import Image
import os

def open_threshold_save(im, save_name):
    new_image = threshold_image(im)
    save_image(new_image, save_name, "BMP")

def threshold_image(im):
    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(im.getpixel((j,i)))
        pixel_vals.append( l )

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    return im

def save_image(im, filename, filetype):
    im.save(filename, filetype)

def crop_to_whitespace(im):
    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(im.getpixel((j,i)))
        pixel_vals.append( l )

    #umm okay yeah so if the ENTIRE ROW is white, we need that info

    nonwhiterows = []

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                nonwhiterows.append((j,i))
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    #so now that I have a list of nonwhite rows, I need to find the extreme x AND y values. so I probably need a list of coordinates anyway. and then i can compare the coordinates to each other. so i should probably have a list of tuples or something.

    upper = nonwhiterows[0][1]
    lower = nonwhiterows[-1][1]

    min_x = im_x
    max_x = 0

    for x, y in nonwhiterows:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

    box = (min_x, upper, max_x+1, lower+1)

    region = im.crop(box)

    return region

def make_templates(im, kanji):
    width = 125
    height = 145
    origin = 0
    box = (0, 0, width, height)
    row = 1

    for i in range(1, len(kanji)+1):
        print i
        print box
        work = im.crop(box)
        new_work = crop_to_whitespace(work)
        open_threshold_save(new_work, kanji[i-1]+".bmp")

        if i % 8 == 0 and i != 0:
            #go to the next line
            box = (origin, origin + (row*height), width, height*(row+1))
            row += 1
        else:
            box = (box[0]+width, box[1], box[2]+width, box[3])

def main():

    raw_dir = "jouyousec"

    list_of_files = os.listdir(raw_dir) 
    raw_kanji = u"乙 了 又 与 及 丈 刃 凡 勺 互 弔 井 升 丹 乏 匁 屯 介 冗 凶 刈 匹 厄 双 孔 幻 斗 斤 且 丙 甲 凸 丘 斥 仙 凹 召 巨 占 囚 奴 尼 巧 払 汁 玄 甘 矛 込 弐 朱 吏 劣 充 妄 企 仰 伐 伏 刑 旬 旨 匠 叫 吐 吉 如 妃 尽 帆 忙 扱 朽 朴 汚 汗 江 壮 缶 肌 舟 芋 芝 巡 迅 亜 更 寿 励 含 佐 伺 伸 但 伯 伴 呉 克 却 吟 吹 呈 壱 坑 坊 妊 妨 妙 肖 尿 尾 岐 攻 忌 床 廷 忍 戒 戻 抗 抄 択 把 抜 扶 抑 杉 沖 沢 沈 没 妥 狂 秀 肝 即 芳 辛 迎 邦 岳 奉 享 盲 依 佳 侍 侮 併 免 刺 劾 卓 叔 坪 奇 奔 姓 宜 尚 屈 岬 弦 征 彼 怪 怖 肩 房 押 拐 拒 拠 拘 拙 拓 抽 抵 拍 披 抱 抹 昆 昇 枢 析 杯 枠 欧 肯 殴 況 沼 泥 泊 泌 沸 泡 炎 炊 炉 邪 祈 祉 突 肢 肪 到 茎 苗 茂 迭 迫 邸 阻 附 斉 甚 帥 衷 幽 為 盾 卑 哀 亭 帝 侯 俊 侵 促 俗 盆 冠 削 勅 貞 卸 厘 怠 叙 咲 垣 契 姻 孤 封 峡 峠 弧 悔 恒 恨 怒 威 括 挟 拷 挑 施 是 冒 架 枯 柄 柳 皆 洪 浄 津 洞 牲 狭 狩 珍 某 疫 柔 砕 窃 糾 耐 胎 胆 胞 臭 荒 荘 虐 訂 赴 軌 逃 郊 郎 香 剛 衰 畝 恋 倹 倒 倣 俸 倫 翁 兼 准 凍 剣 剖 脅 匿 栽 索 桑 唆 哲 埋 娯 娠 姫 娘 宴 宰 宵 峰 貢 唐 徐 悦 恐 恭 恵 悟 悩 扇 振 捜 挿 捕 敏 核 桟 栓 桃 殊 殉 浦 浸 泰 浜 浮 涙 浪 烈 畜 珠 畔 疾 症 疲 眠 砲 祥 称 租 秩 粋 紛 紡 紋 耗 恥 脂 朕 胴 致 般 既 華 蚊 被 託 軒 辱 唇 逝 逐 逓 途 透 酌 陥 陣 隻 飢 鬼 剤 竜 粛 尉 彫 偽 偶 偵 偏 剰 勘 乾 喝 啓 唯 執 培 堀 婚 婆 寂 崎 崇 崩 庶 庸 彩 患 惨 惜 悼 悠 掛 掘 掲 控 据 措 掃 排 描 斜 旋 曹 殻 貫 涯 渇 渓 渋 淑 渉 淡 添 涼 猫 猛 猟 瓶 累 盗 眺 窒 符 粗 粘 粒 紺 紹 紳 脚 脱 豚 舶 菓 菊 菌 虚 蛍 蛇 袋 訟 販 赦 軟 逸 逮 郭 酔 釈 釣 陰 陳 陶 陪 隆 陵 麻 斎 喪 奥 蛮 偉 傘 傍 普 喚 喫 圏 堪 堅 堕 塚 堤 塔 塀 媒 婿 掌 項 幅 帽 幾 廃 廊 弾 尋 御 循 慌 惰 愉 惑 雇 扉 握 援 換 搭 揚 揺 敢 暁 晶 替 棺 棋 棚 棟 款 欺 殖 渦 滋 湿 渡 湾 煮 猶 琴 畳 塁 疎 痘 痢 硬 硝 硫 筒 粧 絞 紫 絡 脹 腕 葬 募 裕 裂 詠 詐 詔 診 訴 越 超 距 軸 遇 遂 遅 遍 酢 鈍 閑 隅 随 焦 雄 雰 殿 棄 傾 傑 債 催 僧 慈 勧 載 嗣 嘆 塊 塑 塗 奨 嫁 嫌 寛 寝 廉 微 慨 愚 愁 慎 携 搾 摂 搬 暇 楼 歳 滑 溝 滞 滝 漠 滅 溶 煙 煩 雅 猿 献 痴 睡 督 碁 禍 禅 稚 継 腰 艇 蓄 虞 虜 褐 裸 触 該 詰 誇 詳 誉 賊 賄 跡 践 跳 較 違 遣 酬 酪 鉛 鉢 鈴 隔 雷 零 靴 頑 頒 飾 飽 鼓 豪 僕 僚 暦 塾 奪 嫡 寡 寧 腐 彰 徴 憎 慢 摘 概 雌 漆 漸 漬 滴 漂 漫 漏 獄 碑 稲 端 箇 維 綱 緒 網 罰 膜 慕 誓 誘 踊 遮 遭 酵 酷 銃 銑 銘 閥 隠 需 駆 駄 髪 魂 錬 緯 韻 影 鋭 謁 閲 縁 憶 穏 稼 餓 壊 懐 嚇 獲 穫 潟 轄 憾 歓 環 監 緩 艦 還 鑑 輝 騎 儀 戯 擬 犠 窮 矯 響 驚 凝 緊 襟 謹 繰 勲 薫 慶 憩 鶏 鯨 撃 懸 謙 賢 顕 顧 稿 衡 購 墾 懇 鎖 錯 撮 擦 暫 諮 賜 璽 爵 趣 儒 襲 醜 獣 瞬 潤 遵 償 礁 衝 鐘 壌 嬢 譲 醸 錠 嘱 審 薪 震 錘 髄 澄 瀬 請 籍 潜 繊 薦 遷 鮮 繕 礎 槽 燥 藻 霜 騒 贈 濯 濁 諾 鍛 壇 鋳 駐 懲 聴 鎮 墜 締 徹 撤 謄 踏 騰 闘 篤 曇 縄 濃 覇 輩 賠 薄 爆 縛 繁 藩 範 盤 罷 避 賓 頻 敷 膚 譜 賦 舞 覆 噴 墳 憤 幣 弊 壁 癖 舗 穂 簿 縫 褒 膨 謀 墨 撲 翻 摩 磨 魔 繭 魅 霧 黙 躍 癒 諭 憂 融 慰 窯 謡 翼 羅 頼 欄 濫 履 離 慮 寮 療 糧 隣 隷 霊 麗 齢 擁 露"
    kanji = raw_kanji.split()
    start = 0
    end = 64

    print len(kanji)

    for f in list_of_files:

        im = Image.open(raw_dir+"/"+f).convert("L")

        cropped = im.crop((125,145,1145,1305))

        make_templates(cropped, kanji[start:end])
        start += 64
        end += 64

if __name__ == "__main__":
    main()