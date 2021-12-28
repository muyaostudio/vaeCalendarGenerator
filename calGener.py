#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    : calGener2022.py
@Date    : 2021/12/28 05:14:00
@Author  : MuyaoStudio
@Version : 1.0
@Desc    : 生成Vae+风格台历
'''

from PIL import Image, ImageDraw, ImageFont
from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals import *
from datetime import datetime
import datetime as dt
from tqdm import tqdm
import os


zi = False   # 是否输出为妹妹紫样式（默认蓝色）

OUTPUT_PATH = './output'
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

def CalendarGen(year, month, day, month_en, week_zh, week_en, holiday, farmerday, info):
    # 打开背景图
    bg = Image.open("./statics/bg-lan.png") if not zi else Image.open("./statics/bg-zi.png")
    width, height = bg.size
    draw = ImageDraw.Draw(bg)  # 新建绘图对象
    fillColor = "#6ca5ff" if not zi else "#cb67f5"

    # section 1
    ################# 最上方202x年x月x日 ##################
    setFont = ImageFont.truetype('./fonts/msyhbd.ttc', 22)  # 选择文字字体和大小
    text = "%d年%d月%d日" % (year, month, day)
    pos = (100, 220)  # 位置
    draw.text(pos, text, font=setFont, fill=fillColor, direction=None)

    # section 2
    ################# 农历 & 中文星期 ##################
    setFont = ImageFont.truetype('./fonts/Deng.ttf', 40)  # 选择文字字体和大小
    text1 = farmerday  # 正月初一
    text2 = "星期%s" % week_zh
    text3 = holiday
    t_width, t_height = setFont.getsize(text2)
    pos1 = (100, 330)  # 位置
    pos2 = int((width - t_width) / 2), 330  # 位置
    pos3 = (745 - 40, 330) if text3 and len(text3) == 3 else (745, 330)  # 位置
    draw.text(pos1, text1, font=setFont, fill=fillColor, direction=None)
    draw.text(pos2, text2, font=setFont, fill=fillColor, direction=None)
    draw.text(pos3, text3, font=setFont, fill=fillColor, direction=None)

    # section 3
    ################# 英文星期 ##################
    setFont = ImageFont.truetype('./fonts/SOURCEHANSANSSC-BOLD.OTF', 27)  # 选择文字字体和大小
    text = week_en
    t_width, t_height = setFont.getsize(text)
    pos = int((width - t_width) / 2), 380
    draw.text(pos, text, font=setFont, fill=fillColor, direction=None)

    # section 4
    ################# 中间最大的阿拉伯数字 “日” ##################
    setFont = ImageFont.truetype('./fonts/EngschriftDINDOT.otf', 490)  # 选择文字字体和大小
    text = str(day)
    t_width, t_height = setFont.getsize(text)
    pos = int((width - t_width) / 2), 460
    draw.text(pos, text, font=setFont, fill=fillColor, direction=None)

    # section 5
    ################# 英文月份（January...） ##################
    setFont = ImageFont.truetype('./fonts/din1451alt G.ttf', 60)  # 选择文字字体和大小
    text = month_en  # January
    t_width, t_height = setFont.getsize(text)
    pos = int((width - t_width) / 2), 850 - 6
    draw.text(pos, text, font=setFont, fill=fillColor, direction=None)

    # section 6
    ################# 数字月份（12月...） ##################
    setFont = ImageFont.truetype('./fonts/SOURCEHANSANSSC-BOLD.OTF', 50)  # 选择文字字体和大小
    text = "%d月" % (month)
    t_width, t_height = setFont.getsize(text)
    pos = int((width - t_width) / 2), 940 - 10
    draw.text(pos, text + '', font=setFont, fill=fillColor, direction=None)

    # section 6 【最下面部分】
    ################# 若info中text非空，绘制文字 ##################
    if info["text"]:
        setFont = ImageFont.truetype('./fonts/SourceHanSerifSC-SemiBold.otf', 35)  # 选择文字字体和大小
        text = info["text"].split('\n')
        for i, line in enumerate(text):
            t_width, t_height = setFont.getsize(line)
            pos = int(934/2-t_width/2), int((height - t_height) / 2) + 480 + i * 50 - len(text) * 10 - 6 + 20
            draw.text(pos, line, font=setFont, fill=fillColor, direction=None)
    
    ################# 若info中line非空，绘制线条 ##################
    if info["line"]:
        setFont = ImageFont.truetype('./fonts/SourceHanSerifSC-SemiBold.otf', 30)  # 选择文字字体和大小
        text = "今日记录："
        t_width, t_height = setFont.getsize(text)
        pos = 120, 1085
        draw.text(pos, text, font=setFont, fill=fillColor, direction=None)
        draw.line([(280,1120), (120+680,1120)], fill=fillColor, width=2)  #线的起点和终点，线宽
        draw.line([(120,1200), (120+680,1200)], fill=fillColor, width=2)  #线的起点和终点，线宽
        draw.line([(120,1280), (120+680,1280)], fill=fillColor, width=2)  #线的起点和终点，线宽

    # section 7
    ################# 最上方贴图logo #################
    suo = 4
    logo = Image.open('./statics/logo-lan.png').resize((312 // suo, 120 // suo), Image.ANTIALIAS)
    if zi:
        logo = Image.open('./statics/logo-zi.png').resize((312 // suo, 120 // suo), Image.ANTIALIAS)

    r, g, b, a = logo.split()  # 分离alpha通道
    # bg.paste(logo, (10,10))
    bg.paste(logo, (745, 220), mask=a)

    bg.convert('RGB')
    # bg.show()

    output = "./output/%s%s%s.png" % (str(year),
                                      str(month) if len(str(month)) == 2 else '0' + str(month),
                                      str(day) if len(str(day)) == 2 else '0' + str(day))
    bg.save(output)


def get_week_day(w):
    week_day_dict = {
        0: ['一', 'Monday'],
        1: ['二', 'Tuesday'],
        2: ['三', 'Wednesday'],
        3: ['四', 'Thursday'],
        4: ['五', 'Friday'],
        5: ['六', 'Saturday'],
        6: ['日', 'Sunday']
    }
    return week_day_dict[w]


def get_en_mon(m):
    m_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    return m_dict[m]


def run(year, month, day):
    # 周几
    week_zh, week_en = get_week_day(datetime(year=year, month=month, day=day).weekday())
    # https://www.dazhuanlan.com/2020/02/01/5e350023c1c45/
    # https://www.bookstack.cn/read/borax/docs-guides-festival.md

    # 农历
    ld = LunarDate.from_solar_date(year, month, day)
    farmerday = ld.strftime('%M月%D')  # 农历日期
    jieqi = ld.term  # 节气

    if jieqi:
        holiday = jieqi
    else:
        if month == 1 and day == 1: holiday = '元旦'
        elif farmerday == '腊月廿九': holiday = '除夕'
        elif farmerday == '正月初一': holiday = '春节'
        elif farmerday == '正月十五': holiday = '元宵节'
        elif month == 5 and day == 1: holiday = '劳动节'
        elif farmerday == '五月初五': holiday = '端午节'
        elif farmerday == '八月十五': holiday = '中秋节'
        elif month == 10 and day == 1: holiday = '国庆节'
        elif month == 6 and day == 1: holiday = '儿童节'
        elif month == 12 and day == 25: holiday = '圣诞节'
        else: holiday = ''

    # print(f"{year}-{month}-{day}:{farmerday}({holiday})")
    info = {"text": None,"pic": None,"line": True}

    if holiday == '元旦': info = {"text": "新的一年，新的收获！","pic": None,"line": None}
    elif holiday == '春节': info = {"text": "春风得意，开门见喜！","pic": None,"line": None}
    elif holiday == '端午节': info = {"text": "端午安康！","pic": None,"line": None}
    elif holiday == '儿童节': info = {"text": "做一个懂事的孩子。","pic": None,"line": None}
    elif holiday == '国庆节': info = {"text": "国庆节快乐！","pic": None,"line": None}
    elif holiday == '中秋节': info = {"text": "中秋快乐！","pic": None,"line": None}
    elif holiday == '清明': info = {"text": "又是清明雨上。","pic": None,"line": None}
    elif holiday == '雨水': info = {"text": "在非晴非雨平庸时刻，你掏出伞垂直撑着。","pic": None,"line": None}
    elif farmerday == '七月初七': info = {"text": "皎月归，我轻随，烟火对影赏。","pic": None,"line": None}
    elif farmerday == '九月初九': info = {"text": "那远去的少年，恍然间长大。","pic": None,"line": None}
    elif month == 5 and day == 14: info = {"text": "想到你，就不会勉强合群。","pic": None,"line": None}
    elif month == 5 and day == 4: info = {"text": "青年节快乐！","pic": None,"line": None}
    elif month == 11 and day == 11: info = {"text": "重温和你逛超市的傍晚。","pic": None,"line": None}

    CalendarGen(
        year=year,
        month=month,
        day=day,
        month_en=get_en_mon(month),
        week_zh=week_zh,
        week_en=week_en,
        holiday=holiday,
        farmerday=farmerday,
        info=info
    )

if __name__ == "__main__":
    year = 2022
    start = dt.datetime(year, 1, 1)
    end = dt.datetime(year+1, 1, 1)
    for n in tqdm(range(int((end - start).days))):
        date = start + dt.timedelta(n)
        run(date.year, date.month, date.day)

