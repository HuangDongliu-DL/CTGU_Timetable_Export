#coding=utf-8
import sys
import getopt

from time_calculation import Calculation

def usage():
    print(
    """请输入完整参数
    -h:显示帮助
    -u:学号
    -p:密码
    -y:学年
    -t:学期""".replace(" ",''))
# 获取参数
argv = sys.argv
# 如果没有获取到任何参数，显示提示
if len(argv) == 1:
    usage()
    sys.exit()
# 检测是否成功获取到参数
try:
    opts,args = getopt.getopt(argv[1:],"u:p:y:t:h")
except getopt.GetoptError:
    usage()
    sys.exit()

username,password,year,term = None,None,None,None
for opt,arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt == '-u':
        username = arg
    elif opt == '-p':
        password = arg
    elif opt == '-y':
        year = arg
    elif opt == '-t':
        term = arg
# 检测参数是否完整
if None in [username,password,year,term]:
    usage()
    sys.exit()
Calculation(username=username,password=password,shool_year=year,term=term)

