# streamlit_bendibao
从微信本地宝解析中高风险地区情况

linked-web-site : https://opink-streamlit-bendibao-streamlit-bendibao-rb3om6.streamlitapp.com/

> 通过streamlit上线，时时刷新时时下载

> 我实在是整不明白时区，就直接不自己写时间函数了

### Bugfixed
#### 1、网页数据写入本地文件bug。已解决
1. 网络数据流如无BOM或Xml的encoding声明，默认是使用utf-8encoding的。
2. 网络数据流是byte。~~解码至内存中统一使用Unicode对应的可读明文。~~
3. 因此从本地内存中写入硬盘文件的encoding要至少能覆盖网络数据流byte的encoding的编码格式，不然会encode时存在超出编码范围的byte码不能正确encode而报错。
