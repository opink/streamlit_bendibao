# -*- coding: utf-8 -*-
"""
想要实现streamlit share的引用微信本地宝的中高风险地区信息并保存至本地，学习用
Created on 2022年7月9日 15:39:14
@author: 学习者KarlQu
"""

import requests 
from lxml import etree
import pandas as pd
import streamlit as st

class BendibaoFXDQ:
    """
    主要用于储存和解析本地宝的网页
    """
    def __init__(self, base_url:str = 'http://m.bendibao.com/news/gelizhengce/fengxianmingdan.php') -> None:
        self.base_url = base_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'}
        self.zhixiashi = ['北京市','上海市','天津市','重庆市']

    def get_list(self, path:str ='today') -> pd.DataFrame:
        response = requests.get(self.base_url,headers=self.headers)
        # print(response) # 本地调试响应用
        jiexi = etree.HTML(response.text)
        got_time = jiexi.xpath('//div[@class="border-title"]//p[@class="time"]/text()')
        # print(got_time) # 本地调试用
        # xiangmus = jiexi.xpath('//div[@class="info"]/div/p/text()') # 本地调试用
        # print(xiangmus) 
        xiangmus = ['height-title','middle-title','tiaogao-title','tiaozhong-title','tiaodi-title']
        linshi_list = []
        for xiangmu in xiangmus:
            provinces = jiexi.xpath(f'//p[@class="{xiangmu}"]/..//div[@class="shi flex-between"]')
            # print(len(provinces)) # 调试用
            if len(provinces):
                details = jiexi.xpath(f'//p[@class="{xiangmu}"]/..//ul[@class="info-detail"]')
                assert len(details) == len(provinces) # 网页xpath两者是一一对应的
                for province, sites in zip(provinces, details):
                    if province[0][0][0].text not in self.zhixiashi: # span[0]元素的文本是省份或者直辖市
                        prov, city = province[0][0][0].text, province[0][0][1].text
                    else: 
                        prov, city = province[0][0][0].text, province[0][0][0].text
                    for site in sites:
                        linshi_list.append([xiangmu, prov, city, site[1].text]) # 组装好一个数据
        df = pd.DataFrame(linshi_list,columns=['项目','省or自治区or直辖市','市or直辖市','点位'])
        df['项目'] = df['项目'].replace({'height-title':'高风险地区','middle-title':'中风险地区','tiaogao-title':'今日调高',
                                        'tiaozhong-title':'今日调中','tiaodi-title':'今日调低'}
                                        )
        return df, got_time

# @st.cache加在哪里啊?没整明白啊
def convert_df(df):
    return df.to_csv().encode('utf-8') 
    # raw python 跟随系统的encoding，简中默认gbk。
    # 而网络数据流如无BOM或Xml的encoding声明，默认是使用utf-8encoding的。
    # 网络数据流是byte。因此写入的文件的encoding要与网络数据流的encoding一致，不然会解析byte出错。

st.title('通过本地宝获取全国疫情中高风险地区名单的CSV表格')
st.write('实时更新数据来源 ->  http://m.bendibao.com/news/gelizhengce/fengxianmingdan.php')

if st.button('点击开始获取数据'):
    df, now = BendibaoFXDQ().get_list()
    st.dataframe(df,800,480)
    st.write(f'截止{now}获取数据')
    csv = convert_df(df)
    st.download_button('选择本地文件夹进行保存,保存后网页数据清除', 
                        data=csv,file_name=f'截止{now}全国中高风险地区名单.csv')
    
