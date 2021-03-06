# !/usr/bin/python3
import pymysql
import time
import numpy as np
import scipy.io as sio # 重新安装该库
import random
import os
from lshash import LSHash
DB_INFO = {'host':'127.0.0.1','port':3306,'DB':'YJ_TEST','TB':'test'}
folder = 'F:/Study/510/DocYJ/DataBase/'
mat_file = 'tensor.mat'
binary_file = 'functionname/binaryname.txt'
result_file = 'result.txt'
select_result_folder = 'result/'

# 数据库操作类
class DB_Actor():
    # 初始化数据库连接，配置信息见全局变量
    def __init__(self):
        global DB_INFO
        self.conn = pymysql.Connect(host=DB_INFO['host'], port=DB_INFO['port'],\
                               user='root', passwd='jiang', db=DB_INFO['DB'], charset='utf8')
        self.cursor = self.conn.cursor()
        self.CreateTB(DB_INFO['TB'])

    # 创建表格
    def CreateTB(self,DBname):
        sql = "create table " + DBname + " (binary_name VARCHAR(100) NOT NULL,\
                                            function_name VARCHAR(100) NOT NULL,\
                                            feature VARCHAR(500) NOT NULL)"
        try:
            self.cursor.execute(sql)
            print('create db %s success.' %(DBname))
        except Exception as e:
            print(e)

    # 执行SQL语句
    def DoSql(self,SQL):
        try:
            self.cursor.execute(SQL)
            self.conn.commit()
            # print(SQL,'success')
        except Exception as e:
            print(e,SQL)
            self.conn.rollback()

    # 删除表格
    def DropTB(self,DBname):
        sql = "drop table " + DBname
        try:
            self.cursor.execute(sql)
            print('table:',DBname,'drop success')
        except Exception as e:
            print(e,sql)

    # 展示数据库数据
    def ShowDB(self,DBname):
        sql = "select * from " + DBname
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(e,sql)

    # 断开数据库连接
    def CutLink(self):
        self.cursor.close()
        self.conn.close()

# 数据分析与保存类
class Date_Analysis():
    # 初始化数据精度，生成数据库实例
    def __init__(self):
        global DB_INFO
        self.accuracy = 6 # 设置精度小数位数
        self.table = DB_INFO['TB']
        self.DOSQL = DB_Actor()
        # self.DOSQL.CreateTB(self.table)

    # 数据分析主过程
    def MainAnalysis(self,binary_addr,mat_addr,folder):
        i = 0
        j = 0
        s_data = self.GetSourceMat(mat_addr)
        # write_file = open('log1.txt','a')
        matrix_shape = s_data.shape
        x_max = matrix_shape[0]
        y_max = matrix_shape[1]
        z_max = matrix_shape[2]

        # print(s_data[:,93,1332])
        # exit()

        try:
            binary_handle = open(binary_addr,'r')
            binary_contents = binary_handle.readlines()
            # 首先遍历所有的binary_name
            for each_binary in binary_contents:
                if i < y_max:
                    j = 0
                    binary_name = each_binary.split("'")[1]
                    func_addr = folder + 'functionname/' + binary_name + '.txt'
                    func_handle = open(func_addr,'r')
                    func_contents = func_handle.readlines()
                    # 然后遍历每个binary_name的所有function_name
                    for each_func in func_contents:
                        if j < z_max:
                            func_name = each_func.split(' ')[0]
                            ch_index = self.JudgeCharIndex(func_name)
                            func_name = func_name[ch_index:]
                            if self.JudgeNorZero(s_data[:,i,j]): # 全零
                                pass
                            else:
                                temp = self.DataAccuray(s_data[:,i,j])
                                str_data = temp.astype(str)
                                feature = "-".join(str_data)
                                print(binary_name,func_name,feature)
                                self.SaveData(binary_name,func_name,feature)
                                # write_file.write(binary_name+func_name+feature+'\n')
                            j=j+1
                        else:
                            break
                    i=i+1
                    func_handle.close()
                else:
                    break
            binary_handle.close()
        except Exception as e:
            print(e)
        print(i, j)
        # write_file.close()
        self.DOSQL.CutLink()

    def ResultAnalysis(self,res_addr,select_addr):
        '''
        result_handle = open(res_addr,'r')
        select_handle = open(select_addr,'a')
        result_contents = result_handle.readlines()
        for res in result_contents:
            feature_list = res.split(',')
            feature_array = self.ListStr2ArrayFloat(feature_list)
            temp = self.DataAccuray(feature_array)
            str_data = temp.astype(str)
            feature = "-".join(str_data)
            print(feature)
            exit()

            rows = self.DatafromFeature(feature)
            select_data = rows[0]
            select_handle.write(select_data+'\n')
            print(rows)
        result_handle.close()
        select_handle.close()
        '''
        feature = '0.008346-0.008392-0.005623-0.021094-0.004259-0.00653-4e-06-0.001683-0.00178-0.002022-0.001373-0.000187-0.005874-0.000901-0.003495'
        rows = self.DatafromFeature(feature,0,20)
        select_data = ''
        for row in rows:
            row_data = row[0] + ':' + row[1]
            select_data = select_data + row_data + '#'
        print(select_data)



    # 根据feature查询数据库 从0开始,num表示查询数量 注意limit是返回查询结果中的指定行数
    def DatafromFeature(self,feature,sta,num):
        res = []
        sql = "select * from " + self.table + " LIMIT " + str(sta) + ',' + str(num)
        self.DOSQL.cursor.execute(sql)
        rows = self.DOSQL.cursor.fetchall()
        for row in rows:
            if row[2] == feature:
                res.append(row)
                break
            else:
                pass
        return res

    # 字符串list转浮点数array
    def ListStr2ArrayFloat(self,data):
        for i in range(0,len(data)):
            data[i] = float(data[i])
        return np.array(data)

    # 修改数据精度np.array float类型
    def DataAccuray(self,data):
        i = 0
        for num in data:
            data[i] = round(num, self.accuracy)
            i = i + 1
        return data

    # 判断是否全零
    def JudgeNorZero(self,data):
        for num in data:
            if num > 0.0:
                return 0
        return 1

    # 找到字符串第一个字母的位置，用于裁剪字符串开头的破折号
    def JudgeCharIndex(self,s):
        i = 0
        for ch in s:
            if ch >= 'a' and ch <= 'z':
                return i
            elif ch >= 'A' and ch <= 'Z':
                return i
            else:
                i=i+1

    # 读取.mat文件
    def GetSourceMat(self,Mat_addr):
        m = sio.loadmat(Mat_addr)
        return m['FFE']

    # 保存数据库
    def SaveData(self,binary_name,fun_name,feature):
        sql = "insert into " + self.table + " (binary_name,function_name,feature) values('" + binary_name + "','" + fun_name + "','" + feature  + "')"
        self.DOSQL.DoSql(sql)

    # 确定保留小数
    def as_num(self,x):
        y = '{:.6f}'.format(x)
        return y

class LSHAnalysis():
    def __init__(self):
        global DB_INFO
        self.table = DB_INFO['TB']
        self.DODB = DB_Actor()
        self.SelectDB = Date_Analysis()
        pass

    # key表示获得相似feature的个数
    def Mainfunc(self,mat_addr,base,result_folder,binary_file):
        # base数据的所有binary_func_name
        Total_binary_func = [] # binnary:funcution#
        #  np.set_printoptions(suppress=True, precision=6, threshold=8)
        s = sio.loadmat(mat_addr)
        svec = s['FFE']
        datalen = len(svec)
        n1, n2, n3 = np.shape(svec)
        test_dict = {'core':[0,12],'curl':[48,60],'libgmp':[60,72],'busybox':[72,84],'openssl':[84,96],'sqlite':[96,108]}
        compareDict = {'core_arm_o0':4,'core_arm_o1':5,'core_arm_o2':6,'core_arm_o3':7,
                       'curl_arm_o0':52,'curl_arm_o1':53,'curl_arm_o2':54,'curl_arm_o3':55,
                       'libgmp.so.10.3.2_arm_O0':64,'libgmp.so.10.3.2_arm_O1':65,
                       'libgmp.so.10.3.2_arm_O2':66,'libgmp.so.10.3.2_arm_O3':67,
                       'busybox_arm_o0':72,'busybox_arm_o1':73,'busybox_arm_o2':74,'busybox_arm_o3':75,
                       'openssl_arm_o0':84, 'openssl_arm_o1':85,'openssl_arm_o2':86,'openssl_arm_o3':87,
                       'sqlite_arm_o0':96,'sqlite_arm_o1':97, 'sqlite_arm_o2':98,'sqlite_arm_o3':99,
                       }
        FUNCTIONNUMBER={'coreutils_dir_X86_O0':290,
                        'coreutils_dir_X86_O1':239,
                        'coreutils_dir_X86_O2':291,
                        'coreutils_dir_X86_O3':255,
                        'coreutils_dir_arm_O0':451,
                        'coreutils_dir_arm_O1':368,
                        'coreutils_dir_arm_O2':377,
                        'coreutils_dir_arm_O3':334,
                        'coreutils_dir_mips_O0':306,
                        'coreutils_dir_mips_O1':247,
                        'coreutils_dir_mips_O2':242,
                        'coreutils_dir_mips_O3':244,
                        'coreutils_du_X86_O0':237,
                        'coreutils_du_X86_O1':182,
                        'coreutils_du_X86_O2':211,
                        'coreutils_du_X86_O3':176,
                        'coreutils_du_arm_O0':529,
                        'coreutils_du_arm_O1':393,
                        'coreutils_du_arm_O2':387,
                        'coreutils_du_arm_O3':329,
                        'coreutils_du_mips_O0':401,
                        'coreutils_du_mips_O1':288,
                        'coreutils_du_mips_O2':273,
                        'coreutils_du_mips_O3':248,
                        'coreutils_ls_X86_O0':290,
                        'coreutils_ls_X86_O1':239,
                        'coreutils_ls_X86_O2':291,
                        'coreutils_ls_X86_O3':255,
                        'coreutils_ls_arm_O0':451,
                        'coreutils_ls_arm_O1':368,
                        'coreutils_ls_arm_O2':377,
                        'coreutils_ls_arm_O3':334,
                        'coreutils_ls_mips_O0':306,
                        'coreutils_ls_mips_O1':247,
                        'coreutils_ls_mips_O2':242,
                        'coreutils_ls_mips_O3':244,
                        'coreutils_vdir_X86_O0':290,
                        'coreutils_vdir_X86_O1':239,
                        'coreutils_vdir_X86_O2':291,
                        'coreutils_vdir_X86_O3':255,
                        'coreutils_vdir_arm_O0':451,
                        'coreutils_vdir_arm_O1':368,
                        'coreutils_vdir_arm_O2':377,
                        'coreutils_vdir_arm_O3':334,
                        'coreutils_vdir_mips_O0':306,
                        'coreutils_vdir_mips_O1':247,
                        'coreutils_vdir_mips_O2':242,
                        'coreutils_vdir_mips_O3':244,
                        'curl_X86_O0':128,
                        'curl_X86_O1':102,
                        'curl_X86_O2':152,
                        'curl_X86_O3':134,
                        'curl_arm_O0':263,
                        'curl_arm_O1':223,
                        'curl_arm_O2':213,
                        'curl_arm_O3':209,
                        'curl_mips_O0':130,
                        'curl_mips_O1':107,
                        'curl_mips_O2':169,
                        'curl_mips_O3':186,
                        'libgmp.so.10.3.2_X86_O0': 621,
                        'libgmp.so.10.3.2_X86_O1': 568,
                        'libgmp.so.10.3.2_X86_O2': 591,
                        'libgmp.so.10.3.2_X86_O3': 571,
                        'libgmp.so.10.3.2_arm_O0':971,
                        'libgmp.so.10.3.2_arm_O1':876,
                        'libgmp.so.10.3.2_arm_O2':854,
                        'libgmp.so.10.3.2_arm_O3':844,
                        'libgmp.so.10.3.2_mips_O0':606,
                        'libgmp.so.10.3.2_mips_O1':551,
                        'libgmp.so.10.3.2_mips_O2':545,
                        'libgmp.so.10.3.2_mips_O3':544,
                        'busybox_arm_o0':3216,
                        'busybox_arm_o1':2128,
                        'busybox_arm_o2':2099,
                        'busybox_arm_o3':1730,
                        'busybox_mips_o0':2900,
                        'busybox_mips_o1':2243,
                        'busybox_mips_o2':1726,
                        'busybox_mips_o3':1381,
                        'busybox_x86_o0':3196,
                        'busybox_x86_o1':2390,
                        'busybox_x86_o2':2542,
                        'busybox_x86_o3':2045,
                        'openssl_arm_o0':1778,
                        'openssl_arm_o1':1692,
                        'openssl_arm_o2':1675,
                        'openssl_arm_o3':1658,
                        'openssl_mips_o0':414,
                        'openssl_mips_o1':333,
                        'openssl_mips_o2':333,
                        'openssl_mips_o3':324,
                        'openssl_x86_o0':414,
                        'openssl_x86_o1':322,
                        'openssl_x86_o2':350,
                        'openssl_x86_o3':333,
                        'sqlite_arm_o0':2876,
                        'sqlite_arm_o1':2058,
                        'sqlite_arm_o2':1972,
                        'sqlite_arm_o3':1805,
                        'sqlite_mips_o0':2701,
                        'sqlite_mips_o1':1936,
                        'sqlite_mips_o2':1830,
                        'sqlite_mips_o3':1705,
                        'sqlite_x86_o0':2693,
                        'sqlite_x86_o1':1931,
                        'sqlite_x86_o2':1967,
                        'sqlite_x86_o3':1772,
                                                }


        FUNCTIONNAME = []
        func_name = open(binary_file,'r')
        func_contents = func_name.readlines()
        for func_content in func_contents:
            FUNCTIONNAME.append(func_content.split("'")[1])

        # # 确认数据库偏移量
        # binary_db_num = []
        # for binary in FUNCTIONNAME:
        #     sql = "select * from " + self.table + " where binary_name=" + "'" + binary + "'"
        #     self.DODB.cursor.execute(sql)
        #     rows = self.DODB.cursor.fetchall()
        #     binary_db_num.append({binary:len(rows)})
        # print(binary_db_num)
        # exit()


        #core 只针对DIR
        imodel_name = 'openssl_arm_o3'
        imodel_BIN_name = 'openssl_arm_o3'
        imodel=compareDict[imodel_name]
        # 输入binanry全称
        imdel_s = self.GetSqlStart(FUNCTIONNUMBER,FUNCTIONNAME,imodel_BIN_name)
        # 确定数据库范围
        imodel_s_n = [imdel_s,FUNCTIONNUMBER[imodel_BIN_name]]

        itest_name = 'openssl_arm_o0'
        itest_BIN_name = 'openssl_arm_o0'
        itest=compareDict[itest_name]
        itest_s = self.GetSqlStart(FUNCTIONNUMBER,FUNCTIONNAME,itest_BIN_name)
        itest_s_n = [itest_s,FUNCTIONNUMBER[itest_BIN_name]]


        ######## 两两对比
        data = np.zeros((n1,3500))
        test = np.zeros((n1,3500))
        model_num = 0
        test_num = 0
        for j in range(n3):
            if svec[:, imodel, j].all() != 0:
                data[:, model_num] = svec[:, imodel, j]
                model_num = model_num + 1
            if svec[:, itest, j].all() != 0:
                test[:, test_num] = svec[:, itest, j]
                test_num = test_num + 1
        dataves = np.transpose(data)
        testves=np.transpose(test)
    #    output_total = open(result_folder + 'result_total.txt', 'w')

        model = np.zeros((model_num, n1))
        lsh_model = LSHash(7, n1)
        for jj in range(model_num):
            lsh_model.index(dataves[jj, :])
            model[jj, :] = dataves[jj, :]

        test = np.zeros((test_num, n1))
        for ii in range(test_num):
            test[ii, :] = testves[ii, :]


        ##############################################################################
        itest_func_list = self.GetFuncListFromFeature(test,itest_s_n[0],itest_s_n[1])
        #imodel_func_list = self.GetFuncListFromFeature(model,imodel_s_n[0],imodel_s_n[1])
        print('target_list get success\n')

       # Inmodel_Total = self.GetInmodelTotal(imodel_func_list,itest_func_list)
        Inmodel_NUM = 0.0
        output = open(result_folder + 'BetweenTestRecored' + '.txt', 'a')
        # SelectDB = Date_Analysis()
        for queryi in range(test_num):
            key = 20
            test_funcname = itest_func_list[queryi]
            if test[queryi, :].all() != 0:
                Atemp = lsh_model.query(test[queryi, :], key, 'euclidean')
                for i in range(0,key):
                    if i < len(Atemp):
                        try:
                            feature_str = str(Atemp[i]).split(')')[0].split('(')[2]
                            feature_list = feature_str.split(',')
                            feature_array = self.SelectDB.ListStr2ArrayFloat(feature_list)
                            temp = self.SelectDB.DataAccuray(feature_array)
                            str_data = temp.astype(str)
                            feature = "-".join(str_data)
                            rows = self.SelectDB.DatafromFeature(feature,imodel_s_n[0],imodel_s_n[1])
                            select_funcname = rows[0][1]
                            if test_funcname.find(select_funcname):
                                Inmodel_NUM = Inmodel_NUM + 1
                                print('Get One')
                                break
                            else:
                                pass
                        except Exception as e:
                            print(e)
                            print(str(Atemp[i]))
                    else:
                        print('AtempLen:',len(Atemp),' ','key:',key)
                        break
        res = str(float('%.4f' % (Inmodel_NUM/len(itest_func_list))))
        msg = itest_name + '----->' + imodel_name + \
              ' Res:' + res + ' Inmodel_NUM:' + str(Inmodel_NUM) +\
            ' Test_NUM:' + str(len(itest_func_list)) #+ ' Model_NUM:' + str(len(imodel_func_list))# ' Inmodel_Total:' + str(Inmodel_Total)# +\
        output.write(msg + '\n')
        print(msg)
        output.close()

    def GetInmodelTotal(self,model_func,test_func):
        total = 0
        for t_func in test_func:
            if t_func in model_func:
                total=total+1
        return total

    def GetFuncListFromFeature(self,featurelist,sta,num):
        target_list = []
        # 获取test的所有funcname
        for queryi in range(len(featurelist)):
            target = featurelist[queryi, :]
            if target.all() != 0:
                temp_target = self.SelectDB.DataAccuray(target)
                str_target = temp_target.astype(str)
                feature_target = "-".join(str_target)
                rows = self.SelectDB.DatafromFeature(feature_target,sta,num)
                if len(rows):
                    target_funcname = rows[0][1]
                    target_list.append(target_funcname)
                   # print('find record',feature_target, sta, num)
                # else:
                    #print('Not find record',feature_target,sta,num)
        return target_list


    def Row2Str(self,rows):
        data = ''
        for row in rows:
            # row_data = row[0] + ':' + row[1] + ':' + row[2]
            row_data = row[0] + ':' + row[1]
            data = data + row_data + '#'
        return data

    def Row2Dict(self,row):
        res = {'binary_name':row[0],'function_name':row[1]}
        return res


    # 清除空格
    def ClearStr(self,data):
        res = ''
        for ch in data:
            if ch != '_':
                res = res + ch
            else:
                pass
        return res

    # 比较两字符串是否相似
    def CompareStr(self,target,test):
        target = self.ClearStr(target)
        test = self.ClearStr(test)
        n = len(target)-3
        for i in range(0,n):
            temp = target[i:i+5]
            if test.find(temp) != -1:
                return 1
        return 0

    # 获取当前M的值sour是所有base里的数据，字符串，target是要判断的数据
    def GetGlobalM(self,func):
      #  m = 0
        sql = "select * from " + self.table + " where function_name = " + "'" + func + "'"
        # 查询记录数
        # sql = "select * from test where binary_name='busybox_X86_O3'"
        self.DODB.cursor.execute(sql)
        rows = self.DODB.cursor.fetchall()
        return len(rows)

    # funcnum DICT   funcname LIST   target STR
    def GetSqlStart(self,funcnum,funcname,target):
        n = funcname.index(target)
        sta = 0
        for i in range(0,n):
            temp = funcnum[funcname[i]]
            sta = sta + temp
        return sta




if __name__ == "__main__":

    DOAnalysis = Date_Analysis()
    # keylist = [i for i in range(1,200)]

    # base = 10
    # DOlsh = LSHAnalysis()
    # DOlsh.Mainfunc(folder+mat_file,base,folder+select_result_folder,folder+binary_file)


    # DODB = DB_Actor()
    # 创建数据库
    # create database YJ_TEST;
    # 查询某条记录
    # sql = "select * from test where function_name = 'fts3EvalStartReaders'"
    # 查询记录数
    # sql = "select * from test where binary_name='coreutils_dir_X86_O0'"
    # sql = "select * from test LIMIT 2271,1"

    #sql = "select * from " + 'test' + " where binary_name='" + \
    #      'coreutils_dir_arm_O3' + \
     #     "'" + \
     #     " limit " + str(2271) + ',' + str(1)
    # print(sql)
    #
    #
    # DODB.cursor.execute(sql)
    # rows = DODB.cursor.fetchall()
    # print(len(rows))

    # 清空数据库表格
    # DODB.DropTB(DB_INFO['TB'])

    # 数据分析并保存数据库
    DOAnalysis.MainAnalysis(folder+binary_file,folder+mat_file,folder)

    # 根据feature查询数据库
    # DOAnalysis.ResultAnalysis(folder+result_file,folder+result_file)

    # str与float转换
    # x = float('0.1234')
    # y = str(x)
    # print(type(x),type(y))

    # array与list转换
    # a = list()
    # b = np.array(a)
    # c = b.tolist()


    # 展示数据库数据
    # DODB.ShowDB(DB_INFO['TB'])

    # 断开数据库连接
    # DODB.CutLink()
