# 校园电动车管理系统
Smart Electric-Bike Management System (SEMS)

----------
## 1.系统架构
* 环境：Centos5.6+Apache+Python2.7+Django1.8.2
* 数据库：Django自带的轻量级数据库SQLite
* web前端：html5

## 2.充电站服务端 /service/
### 2.1用户检索识别
**API**

URL ：http://jnsems.applinzi.com/service/checkStudent

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:{"card_number":"5sdf87e4"}

id_number ; 类型：str ; 必须：是 ; 备注:序列号

返回数据格式 ：JSON

返回数据示例 ：

1) {"student_number":1030412535, "result": 1} 学生存在且已经注册，返回学号

2）{"student_number":1030412535, "result":0} 学生存在但并未注册

3）{"student_number":None, "result":0} 序列号没有对应的学号

说明:
字段：student_number ； 类型：int
字段：result ; 类型：int

### 2.2 充电开始与结束
**API**

URL ：http://jnsems.applinzi.com/service/checkStudent

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "id_number":"5sdf87e4",
      "id_client": 1,
      "Ammeter_id":2541,
      "message":1
    }

id_number ; 类型：str ; 必须：是 ; 备注:序列号

id_client ; 类型：int； 必须：是； 备注：客户端id

Ammeter_id ; 类型：int； 必须：是； 备注：电表id

message ; 类型：int； 必须：是； 备注：**开始充电：1，结束充电：0**


返回数据格式 ：JSON

返回数据示例 ：

    {
      "usage": 1,
      "money": -2.34
    }

usage ; 类型：int； 备注：使用情况。为防止用户的不良操作导致不良后果的产生，添加usage字段加以限制。**用户可用：1，用户不可用：2**

money ； 类型：float；备注：1.开始充电显示上次亏欠金额,取值为负或0。2.结束充电显示本次结账金额，取值为正**（不论usage字段返回值，本次操作都要将金额扣取）**

### 2.3 充电过程交互
**API**

URL ：http://jnsems.applinzi.com/service/charge

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "id_client": 1,
      "Ammeter_id":1,
      "message"：1
    }

说明：

字段：id_client ; 类型：int； 必须：是； 备注：客户端id

字段：Ammeter_id ; 类型：int ; 必须：是 ; 备注：充电处编号

字段：message ; 类型：int ; 必须：是；备注 : **1：电表断电 2：电流异常 3：涓流充电 4：零电流充电**

返回数据格式 ：JSON

返回数据示例 ：

    {"result":1}

说明:

字段：result ; 类型：int  备注：数据库更新结果，简单应答

### 2.4 反向控制
**API**

URL ：http://jnsems.applinzi.com/service/AmmeterControl

HTTP请求方式 ：POST

POST数据示例:
{"id_client":1}

返回数据格式 ：JSON

返回数据示例 ：

{
  21652 : 1,
  54855 : 0,
  ...
  14524 : 1
}

说明:

键：Ammeter_id ; 值：当前电表状态

### 2.5 询问当前金额

**API**

URL ：http://jnsems.applinzi.com/service/charge

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:

    {
      "id_client": 1,
      "Ammeter_id":1
    }

说明：

字段：id_client ; 类型：int； 必须：是； 备注：客户端id

字段：Ammeter_id ; 类型：int ; 必须：是 ; 备注：充电处编号

返回数据格式 ：JSON

返回数据示例 ：

    {
      "money":1.12
    }

说明:

money ； 类型：float；

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
* 用户资料的绑定
* 消费记录的查询
* 充好电的信息推送
