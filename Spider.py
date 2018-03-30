# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib import urlencode

#获取验证码
s = requests.session()
login_url = 'http://202.203.194.2/'
yzm_url = 'http://202.203.194.2/CheckCode.aspx'
login = s.get(login_url)
soup = BeautifulSoup(login.text,'html.parser')
__VIEWSTATE_1 = soup.select('#form1 > input[type="hidden"]')[0].get('value')
userid = raw_input("学号：")  
pwd = raw_input("密码：")  
r = s.get(yzm_url)
i = Image.open(BytesIO(r.content))
i.show() 
yzm = raw_input("验证码：")
#需要post的数据
header = {
    'Origin': 'http://202.203.194.2',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
postdata = {
    "__VIEWSTATE":__VIEWSTATE_1,
    "txtUserName":userid,  
    "TextBox2":pwd, 
    "txtSecretCode":yzm,  
    "RadioButtonList1": u'学生'.encode('gbk'),
    "Button1": "", 
    "lbLanguage": "",
}
#将数据post给服务器，登录！
post = s.post(
    url = 'http://202.203.194.2/default2.aspx', 
    data = postdata, 
    headers = header
    )

# 测试有没有进入登录成功的界面
# with open("login.html", "w") as f:
#     f.write(post.content)

#print(type(post.content))   获得的网页是‘str’型，要解码
if post.content.decode("gbk").find(u"同学") > 0:
    print("login in successful!")
else:
    print("login in failed!")
    exit()
# 获取姓名
soup = BeautifulSoup(post.text,'html.parser')
names = soup.select('#xhxm')
name = names[0].get_text()[:-2]  #name类型为unicode
print name,', welcome to 教务系统！' 

# 进入有成绩的页面
# get和post同一个url，但发送的headers的Referer是不同的
data = urlencode({
    'xh': userid,
    'xm': name.encode("gbk")
})
get_url = 'http://202.203.194.2/xs_main.aspx?xh=%s' % userid
lncj_url = 'http://202.203.194.2/xscjcx.aspx?%s&gnmkdm=N121613' % data
# print lncj_url
s.headers['Referer'] = get_url
graderesponse = s.get(lncj_url)
soup = BeautifulSoup(graderesponse.text,'html.parser')
a = soup.select('#Form1 > input[type="hidden"]')
__VIEWSTATE_2 = a[2].get('value')
s.headers['Referer'] = lncj_url
data_cj = {
        "__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":__VIEWSTATE_2,  
        "hidLanguage":"",
        "ddlXN":"",
        "ddlXQ": "",
        "ddl_kcxz":"",
        "btn_zcj":u'历年成绩'.encode('gbk')
}
web_lncj = s.post(
    url = lncj_url,
    data = data_cj
    )
# with open("grade.html", "w") as f:
#     f.write(web_lncj.content)

# 准备打印成绩
grade_code = ['xn', 'xq', 'kcdm', 'kcmc', 'kcxz', 'kcgs', 'xf', 'jd', 'cj', 'fxbj', 'bkcj', 'cxck', 'kcxy', 'bz', 'cxbj']
soup = BeautifulSoup(web_lncj.text,'html.parser')
tables = soup.find_all('table')
print tables[0].get_text().replace('\n\n', '')
grades = []
trs = tables[1].find_all('tr')
for tr in trs[1:]:
    grades.append(dict(zip(grade_code,
                           map(lambda x:x.get_text(), tr.find_all('td')))))
# print(grades)
for grade in grades:
    print grade['kcmc'], grade['cj']

# 201505001298
# 789512357.
