#coding=utf-8
from bs4 import BeautifulSoup

from jwc_login import Login
class jwc:
    def __init__(self,username,password):
        # 用户名，即学号
        self.username = username
        # 培养计划URL
        self.training_url = "http://210.42.38.26:84/jwc_glxt/Plan_Train/PlanTrain_Query.aspx"
        # 课表查看URL
        self.curriculum_url = "http://210.42.38.26:84/jwc_glxt/Course_Choice/Course_Schedule.aspx"
        # 选课首页
        self.Choose_course_main_page = "http://210.42.38.26:84/jwc_glxt/Course_Choice/Course_Choice.aspx"
        # 实例化loggin对象
        to_login = Login(username=username, password=password)
        # 开始登入并返回session对象
        self.session = to_login()
    def __HTML_data(self,url:str,shool_year:int,term:int,type=None)->str:
        '''HTML_data:获取输入的网页数据（内部函数，非单独使用）
            输入：
                url：链接，用于选择网页，例如课表或培养计划
                shool_year:学年，例如2020
                term：学期，1代表春季学期，3代表秋季学期
            返回：
                content：网页数据
        '''
        viewstate = None
        eventvalidation = None
        for item in BeautifulSoup(self.session.get(url).text, 'html.parser').find_all('input'):
            if item['name'] == '__VIEWSTATE':
                viewstate = item['value']
            elif item['name'] == '__EVENTVALIDATION':
                eventvalidation = item['value']
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventvalidation,
            'ctl00$MainContentPlaceHolder$School_Year': str(shool_year),
            'ctl00$MainContentPlaceHolder$School_Term': str(term),
            'ctl00$MainContentPlaceHolder$BtnSearch.x': '10',
            'ctl00$MainContentPlaceHolder$BtnSearch.y': '11'
        }
        # 这个是因为解析选课的HTML的时候需要一个type参数
        if type != None:
            data['ctl00$MainContentPlaceHolder$Course_Type'] = str(type)
        return self.session.post(url=url,data=data).text
    def PlanTrain_Query(self,shool_year:int,term:int)->list:
        '''
        获取培养计划
        :param
            shool_year int 学年
            term       int 学期
        :return
            以列表的形式返回当前的的培养计划
        '''
        Html_data = self.__HTML_data(self.training_url,shool_year,term)
        soup = BeautifulSoup(Html_data,'html.parser')
        d = soup.findAll('table',id="ctl00_MainContentPlaceHolder_GridScore")[0]
        Course = []
        # 表格头部信息['学年', '学期', '课程编号', '课程名称', '课程学时', '课程学分', '课程性质', '学位课']
        Header = [h.string for h in d.find_all('th')]
        Course_all = [s.string for s in d.find_all('td')]
        for i in range(0,len(Course_all),len(Header)):
            Course.append([Course_all[j] for j in range(i,i+8)])
        print(Header)
        for i in Course:
            print(i)
        return [Header,Course]
    def Get_curriculum(self,shool_year:int,term:int,to_html=False)->list:
        '''获取课表
        :return:
        {
            'course_name':course_name,
            'location':location,
            'period_of_week':period_of_week,
            'teacher':teacher,
            'day_of_week':day_of_week,
            'period_of_day':period_of_day
        }
        '''
        Html_data = self.__HTML_data(self.curriculum_url,shool_year,term)
        soup = BeautifulSoup(Html_data,'html.parser')
        d = soup.findAll('table',id="ctl00_MainContentPlaceHolder_GridScore")[0]
        if to_html:
            with open(self.username+'.html','w',encoding='utf-8') as f:
                print("您的课表已经写入HTML中，请用浏览器打开程序目录下的 Course_HML 文件夹查看")
                f.write(str(d))
        Course = []
        # 第几节课
        period_of_day = 1
        # 第一行是不需要的所以舍弃
        for h in d.find_all('tr')[1:]:
            day_of_week = 1
            for i in h.find_all('td')[1:]:
                i = i.encode('GBK').decode('GBK').replace('&#160;',';').replace('<br/>',';').replace('<td>','').replace('</td>','')
                if i != '' and i!=';':
                    split_data = [j for j in i.split(';') if j != ' ']
                    # 因为体育课没有上课地点，所以排除
                    if len(split_data) == 3:
                        course_name, period_of_week, teacher = split_data
                        location = ''
                        # 对周数做一点小修改，方便以后的计算
                        period_of_week = tuple(period_of_week.replace("周",'').split('-'))
                        Course.append({
                                'sing_or_double':None,
                                'course_name':course_name,
                                'location':location,
                                'period_of_week':period_of_week,
                                'teacher':teacher,
                                'day_of_week':day_of_week,
                                'period_of_day':period_of_day
                            })
                    # 开始匹配单双周
                    elif len(split_data) > 4:
                        course_name,location_one,period_of_week,sing_or_double_one,teacher,*_ = split_data
                        # 对周数做一点小修改，方便以后的计算
                        period_of_week = tuple(period_of_week.replace("周",'').split('-'))
                        location_two = split_data[-4]
                        sing_or_double_two = split_data[-2]
                        Course.append({
                                "sing_or_double":sing_or_double_one,
                                'course_name':course_name,
                                'location':location_one,
                                'period_of_week':period_of_week,
                                'teacher':teacher,
                                'day_of_week':day_of_week,
                                'period_of_day':period_of_day
                            })
                        Course.append({
                                "sing_or_double":sing_or_double_two,
                                'course_name':course_name,
                                'location':location_two,
                                'period_of_week':period_of_week,
                                'teacher':teacher,
                                'day_of_week':day_of_week,
                                'period_of_day':period_of_day
                            })
                    else:
                        course_name, location, period_of_week, teacher = split_data
                        # 对周数做一点小修改，方便以后的计算
                        period_of_week = tuple(period_of_week.replace("周",'').split('-'))
                        Course.append({
                                "sing_or_double":None,
                                'course_name':course_name,
                                'location':location,
                                'period_of_week':period_of_week,
                                'teacher':teacher,
                                'day_of_week':day_of_week,
                                'period_of_day':period_of_day})
                day_of_week += 1
            period_of_day += 1
        return Course
