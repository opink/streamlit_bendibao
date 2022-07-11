# streamlit_bendibao
从微信本地宝解析中高风险地区情况

linked-web-site : https://opink-streamlit-bendibao-streamlit-bendibao-rb3om6.streamlitapp.com/

> 通过streamlit上线，时时刷新时时下载

> 我实在是整不明白时区，就直接不自己写时间函数了

### Bugfixed
#### 1、网页数据写入本地文件bug。已解决
1. raw python 跟随系统的encoding，简中默认gbk。
2. 而网络数据流如无BOM或Xml的encoding声明，默认是使用utf-8encoding的。
3.网络数据流是byte。因此写入的文件的encoding要与网络数据流的encoding一致，不然会解析byte出错。
