import requests
import re
from pyquery import PyQuery as pq

from lxml import etree

#css路径正则表达式
re_html_css = 'href="(//s3plus.meituan.net.*?svgtextcss.*?.css)'
#css匹配svg链接和class属性【class后续会用到】
re_css_svg = 'class\^="(\w+)".*?(//s3plus.*?\.svg)'

def get_session():
    s = requests.Session()
    s.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "Cookie": "s_ViewType=10; _lxsdk_cuid=175118e665fc8-016b7da57b05e8-4313f6b-1fa400-175118e665fc8; _lxsdk=175118e665fc8-016b7da57b05e8-4313f6b-1fa400-175118e665fc8; _hc.v=3456dc36-e1ce-968f-d12a-ec6416e133c1.1602317347; fspop=test; cy=10; cye=tianjin; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1602317347,1602318334,1602318340; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1602571583; _lxsdk_s=17520b5b7f6-2ac-329-e7a%7C%7C99"
    }
    return s
def get_html(url):
    s = get_session()
    r = s.get(url, timeout=20, verify=False)
    #print(url, r.status_code)
    if r.status_code != 200:
        if r.status_code == 404 or r.status_code == 410:
            content = ""
            return content
        else:
            ex = Exception('not 200')
            raise ex
    return r.text

#对提取到的svg链接进行处理
def svg_handle(svg_url):
    svg_req = get_html(svg_url)
    #该正则匹配的数字的svg
    font = re.findall('" y="(\d+)">(\w+)</text>',svg_req,re.M)
    #匹配文字类
    if not font:
        font = []
        #"textLength.*?(\w+)</textPath>"
        z = re.findall('">(\w+)</textPath>', svg_req, re.M)
        y = re.findall('id="\d+" d="\w+\s(\d+)\s\w+"', svg_req, re.M)
        for a, b in zip(y, z):
            font.append((int(a), b))
    width = re.findall("font-size:(\d+)px", svg_req)[0]
    return font,int(width)


def font_handle(ft):
    #ft = [afaxp,224,1003]
    # FT = [('pjbj8', 462, 1199), ('pj6ie', 210, 1162), ('pj98q', 266, 2178)]
    for i in s_parser:
        if i["code"] in ft[0]:
            font = sorted(i["font"])
            #print(font)
            if ft[2] < int(font[0][0]):
                # print(ft,int(font[0][0]))
                x = int(ft[1] / i["wd"])
                #之前按照判断条件，可以找出汉字，现在按照判断条件有些汉字找不出来，只好做个异常处理，不影响
                try:
                    return font[0][1][x]
                except:
                    print("获取失败")
            for j in range(len(font)):
                if (j + 1) in range(len(font)):
                    if (ft[2] >= int(font[j][0]) and ft[2] < int(font[j + 1][0])):
                        x = int(ft[1] / i["wd"])
                        return font[j + 1][1][x]

def get_info(req):
    # contents = pq(req)
    contents = etree.HTML(req)
    li_list = contents.xpath('//div[@class="reviews-items"]/ul/li')
    #print(li_list)
    for doc in li_list:
        txt = doc.xpath('.//div[@class="review-truncated-words"]//text()|.//div[@class="review-words"]//text()')[0]
        print(txt.strip().replace("\n",""))


if __name__ == '__main__':

    url = "http://www.dianping.com/shop/k5xCPmTViazD3iRf/review_all"
    #请求url，获取页面源码
    req = get_html(url)
    # 使用正则匹配，svg的css链接
    css_url = "http:" + re.findall(pattern=re_html_css,string=req)[0]
    #print(css_url)
    #请求css链接，获取页面进行匹配
    css_content = get_html(css_url)
    #正则匹配svg链接
    svg_url = re.findall(pattern=re_css_svg,string=css_content)
    #print("svg_url",svg_url)
    s_parser = []
    for a , b in svg_url:
        #svg_handle("http:" + b)
        f, w = svg_handle("http:" + b)
        s_parser.append({"code": a, "font": f, "wd": w})
    print("s_pa",s_parser)
    #.mtxoze{background:-210.0px -2847.0px;}
    # 正则匹配css内容，匹配的两个像素对应svg文字位置的背景图
    css_list = re.findall('(\w+){background:.*?(\d+).*?px.*?(\d+).*?px;', '\n'.join(css_content.split('}')))
    css_list = [(i[0],int(i[1]),int(i[2])) for i in css_list]
    #print(css_list)
    replace_dic = []
    for i in css_list:
        replace_dic.append({"code": i[0], "word": font_handle(i)})
    print(replace_dic)
    reqs = ""
    for i in range(len(replace_dic)):
        # print(replace_dic[i]["code"])
        try:
            if replace_dic[i]["code"] in req:
                a = re.findall(f'<\w+\sclass="{replace_dic[i]["code"]}"><\/\w+>', req)[0]
                #print(a,replace_dic[i]["word"])
                req = req.replace(a, replace_dic[i]["word"])
                #print(req)
        except Exception as e:
            print(e)
    #print(req)
    get_info(req)










