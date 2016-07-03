# 校园电动车管理系统
Smart Electric-Bike Management System (SEMS)

----------
## 1.系统架构
* 环境：Ubantu14.2+Apache+Python2.7+Django1.8.3
* 环境：Ubantu14.4+Apache+Python2.7+Django1.8.3
* 数据库：Django自带的轻量级数据库SQLite
* web前端：html5

## 2.充电站服务端 /service/
URLBase = http://wechat.tunnel.qydev.com/service
### 2.1用户检索识别
**API**

URL ：/checkStudent

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:{"card_number":"5sdf87e4"}

id_number ; 类型：str ; 必须：是 ; 备注:序列号

返回数据格式 ：JSON

返回数据示例 ：

1) {"student_number":1030412535, "username":"胡勇", "result": 1} 学生存在且已经注册，返回学号

2）{"student_number":1030412535, "username":None, "result": 0 , "message":"你的账号未注册"} 学生存在但并未注册

3）{"student_number":1030412535, "username":"胡勇", "result": 0 ,"message":"你的账号被封啦"}

4）{"student_number":None, "result":0,"message":"序列号没有对应的学号"} 序列号没有对应的学号

5) {"result":-1,message:"Exception"} 异常错误返回-1

说明:
字段：student_number ； 类型：int ；学号
字段：student_name ； 类型：str ； 姓名
字段：result ; 类型：int ； 0表示收到请求但逻辑错误 -1表示出现异常
字段：message ; 类型：str ； 当result为0或-1时返回错误详细信息

### 2.2 充电开始
**API**

URL ：/start

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "card_number":"5sdf87e4",
      "ammeterGroup_number": '0001',
      "ammeter_number":'0001'
    }

card_number ; 类型：str ; 必须：是 ; 备注:序列号

ammeterGroup_number ; 类型：str； 必须：是； 备注：客户端id

ammeter_number ; 类型：str； 必须：是； 备注：电表

返回数据格式 ：JSON

返回数据示例 ：

    {
        "result":1
    }
字段：result ; 类型：int ； 1表示成功 -1表示出现异常

### 2.3 充电结束
**API**
URL ：/end

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "card_number":"5sdf87e4",
      "ammeterGroup_number": '0001',
      "ammeter_number":'0001'
    }

card_number ; 类型：str ; 必须：是 ; 备注:序列号

ammeterGroup_number ; 类型：str； 必须：是； 备注：客户端id

ammeter_number ; 类型：str； 必须：是； 备注：电表

返回数据格式 ：JSON

返回数据示例 ：

    {
        "result":1
    }
    
字段：result ; 类型：int ； 1表示成功 -1表示出现异常

### 2.4 充电过程交互
**API**

URL ：/charge

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "current_value":1.05,
      "voltage_value":2.01,
      "ammeterGroup_number": '0001',
      "ammeter_number":'0001'
    }

ammeterGroup_number ; 类型：str； 必须：是； 备注：客户端id

ammeter_number ; 类型：str； 必须：是； 备注：电表

current_value ; 类型：float； 必须：是； 备注：当前电流值

voltage_value ; 类型：float； 必须：是； 备注：当前电压值

返回数据格式 ：JSON

返回数据示例 ：

    {
        "result":1
    }
    
说明:

字段：result ; 类型：int ； 1表示成功 -1表示出现异常


### 2.5 反向控制
**API**

URL ：/AmmeterControl

HTTP请求方式 ：POST

POST数据示例:

    {"ammeterGroup_number": "0001"}

返回数据格式 ：JSON

返回数据示例 ：

    {
           "21652" : "1",
           "54855" : "0",
            ..
           "14524" : "2"
    }

说明:
返回一个数组status 
键：电表号，值类型：str  值：1代表电表合闸，0代表电表开闸,2代表释放电表，3代表锁定电表

### 2.6 询问当前金额

**API**

URL ：/money

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "ammeterGroup_number": "0001",
      "ammeter_number":"0001"
    }

说明：

字段：ammeterGroup_number ; 类型：str； 必须：是； 备注：客户端id

字段：ammeter_number ; 类型：str ; 必须：是 ; 备注：充电处编号

返回数据格式 ：JSON

返回数据示例 ：

    {
      "money":1.12
    }

说明:

money ； 类型：float；当前金额

## 3.WEB端管理 /Web/
### 3.1管理员入口 /admin/
* 管理员登陆界面
* 管理首页
* 用户信息的管理
* 充电站信息的管理(包括对充电站的实时控制)
* 消费情况的管理

### 3.2学生入口 /stu/
* 学生注册登录界面
* 管理首页
* 信息的修改
* 过往消费记录的查询

## 4.微信公众号开发 /WeChat/
###4.1用户资料绑定
* 通过登陆或者注册绑定

###4.2当前充电状态信息查询
* 充电制图，当前状态（类似手机充电的图）,充电全过程绘制曲线图

###4.3对自己电表的实时控制
* 反向控制，开-->关  关-->开

###4.4消费记录查询
* 前端数据可视化

###4.5查询每个点的可用状态
* 接入地图API
* 根据位置排序输出

###4.5微信推送

1.充电完成推送

WeChatPush_alreadyFinish(user,charge)

2.充电完毕本次充电信息推送

WeChatPush_payFinish(user,account)

3.超时取车
WeChatPush_delay(user)

4.充电异常推送

WeChatPush_Exception(user,charge)

## 5.数据建模及分析
###5.1数据采集
每次电动车的充电时，客户端会每隔10秒采集一充电时的电流值电压值
###5.2数据分析
1.根据电压电流值绘制充电过程的 电流-时间 与 电压-时间 曲线进而识别出充电的各个阶段 满电流充电、涓流充电、零电流等（待测试）

2.对充电异常状态的识别

3.根据电流电压测算充电的能耗
###5.3数据建模
1.经过大量的数据可以给各个品牌的电动车充电情况进行数据建模

2.可以通过数据模型测算电池的“健康状态”。如果某个电池的充电与正常充电的数据模型有某些特定的出入，可以判定电池可能发生老化。

