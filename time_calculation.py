#coding=utf-8
import time
from jwc_schedule import jwc
from ics import Ics

def Calculation(username:str,password:str,shool_year:int,term:int)->bool:
    j = jwc(username=username,password=password)
    # 实例化ics对象
    Icalendar = Ics()
    # 获取课表数据
    curriculum_data= j.Get_curriculum(shool_year=shool_year,term=term,to_html=True)
    # 学期开始时间
    Semester_start_time = "2021-3-01 08:00:00"
    # 学期开始时间戳
    Semester_start_timestamp = time.mktime(time.strptime(Semester_start_time,'%Y-%m-%d %H:%M:%S'))
    # 每一节课持续时间（算下课时间）：100min=100*60s
    Class_time = 100*60
    # 一个小时的时间戳
    One_hour_timestamp = 60*60
    # 一天的时间戳
    One_day_timestamp = 24*One_hour_timestamp
    for i in curriculum_data:
        # 构建事件数据
        event_data = {}
        event_data['summary'] = i['course_name']
        event_data['location'] = i['location']
        event_data['description'] = i['teacher']
        event_data['count'] = eval(i['period_of_week'][1]) - eval(i['period_of_week'][0]) + 1
        #开始周
        Start_week = eval(i['period_of_week'][0])
        # 这里是在匹配单双周
        if i['sing_or_double'] == None:
            event_data['interval'] = 7
        elif i['sing_or_double'] == "单周":
            event_data['interval'] = 14
            event_data['count'] = int(event_data['count']*0.5)
        elif i['sing_or_double'] == "双周":
            event_data['interval'] = 14
            event_data['count'] = int(event_data['count']*0.5)
            Start_week += 1
        # 这里是在匹配第几周开课
        Start_time_stamp = Semester_start_timestamp + (Start_week - 1) * 7 * One_day_timestamp
        # 这里是在匹配星期几
        Start_time_stamp += (i['day_of_week'] - 1) * One_day_timestamp
        # 这是在匹配第几节课
        if i['period_of_day'] == 2:
            Start_time_stamp += 2 * One_hour_timestamp
        elif i['period_of_day'] == 3:
            Start_time_stamp += 6 * One_hour_timestamp
        elif i['period_of_day'] == 4:
            Start_time_stamp += 8 * One_hour_timestamp
        elif i['period_of_day'] == 5:
            Start_time_stamp += 11 * One_hour_timestamp
        # 一般第十一~十二节课会在九点四十五下课
        elif i['period_of_day'] == 6:
            Start_time_stamp += 12 * One_hour_timestamp + 40 * 60
        if i['period_of_day'] == 6:
            End_time_stamp = Start_time_stamp + 45 * 60
        else:
            End_time_stamp = Start_time_stamp + Class_time
        event_data['start_day'] = time.strftime("%Y%m%d",time.localtime(Start_time_stamp))
        event_data['start_time'] = time.strftime("%H%M",time.localtime(Start_time_stamp))
        event_data['end_day'] = time.strftime("%Y%m%d",time.localtime(End_time_stamp))
        event_data['end_time'] = time.strftime("%H%M",time.localtime(End_time_stamp))
        Icalendar.add_event(event_data)
    Icalendar.to_file('t')
    return True



