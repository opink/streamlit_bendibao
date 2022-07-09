# -*- coding: utf-8 -*-
"""
想要实现streamlit share的引用微信本地宝的中高风险地区信息并保存至本地，学习用
Created on 2022年7月9日 15:39:14
@author: 学习者KarlQu
"""

import requests 
from lxml import etree
import pandas as pd
import datetime
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
        print(response)
        jiexi = etree.HTML(response.text)
        xiangmus = jiexi.xpath('//div[@class="info"]/div/p/text()')
        print(xiangmus)
        xiangmus = ['height-title','middle-title','tiaogao-title','tiaozhong-title','tiaodi-title']
        linshi_list = []
        for xiangmu in xiangmus:
            provinces = jiexi.xpath(f'//p[@class="{xiangmu}"]/..//div[@class="shi flex-between"]')
            print(len(provinces))
            if len(provinces):
                details = jiexi.xpath(f'//p[@class="{xiangmu}"]/..//ul[@class="info-detail"]')
                assert len(details) == len(provinces)
                for province, sites in zip(provinces, details):
                    if province[0][0][0].text not in self.zhixiashi:
                        prov, city = province[0][0][0].text, province[0][0][1].text
                    else: 
                        prov, city = province[0][0][0].text, province[0][0][0].text
                    for site in sites:
                        linshi_list.append([xiangmu, prov, city, site[1].text])
        df = pd.DataFrame(linshi_list,columns=['项目','省','市','点位'])
        df['项目'] = df['项目'].replace({'height-title':'高风险地区',
                                        'middle-title':'中风险地区',
                                        'tiaogao-title':'今日调高',
                                        'tiaozhong-title':'今日调中',
                                        'tiaodi-title':'今日调低'})
        return df

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('gbk') # raw python 不支持ANSI

st.title('通过本地宝获取全国疫情中高风险地区名单的CSV表格')
st.write('实时更新数据来源 ->  http://m.bendibao.com/news/gelizhengce/fengxianmingdan.php')

if st.button('点击开始获取数据'):
    df = BendibaoFXDQ().get_list()
    now = datetime.datetime.now()
    now = now.strftime("%Y年%m月%d日%H时%M分%S秒")
    st.dataframe(df,200,100)
    st.write(f'截止{now}获取数据')
    csv = convert_df(df)
    st.download_button('选择本地文件夹进行保存,保存后网页数据清除', 
                        data=csv,file_name=f'截止{now}全国中高风险地区名单.csv')

    
