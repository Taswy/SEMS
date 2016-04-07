#校园电动车管理系统
Smart Electric-Bike Management System (SEMS)

----------
##1.系统架构
* 环境：Centos5.6+Apache+Python2.7+Django1.8.2
* 数据库：Django自带的轻量级数据库SQLite
* web前端：html5

##2.充电站服务端 /service/
###2.1用户检索识别
**API**

URL ：http://wechat123.ngrok.cc/service/checkStudent

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:{"student_number":1030614418}

说明：字段：student_number ; 类型：int ; 必须：是 ; 备注：学生学号

返回数据格式 ：JSON

返回数据示例 ：

1) {"result":1} 学生存在

2）{"result":0} 学生不存在

说明: 字段：result ; 类型：int
###2.2 充电过程交互
**API**

URL ：http://wechat123.ngrok.cc/service/charge

HTTP请求方式 ：POST

请求数据格式 ：JSON

POST数据示例:{"student_number":1030614418,"Ammeter_id":1,"message"：1}

说明：

字段：student_number ; 类型：int ; 必须：是 ; 备注：学生学号


字段：Ammeter_id ; 类型：int ; 必须：是 ; 备注：充电处编号

字段：message ; 类型：int ; 必须：是；备注 : **1：开始充电 2：结束充电 3：取车**

返回数据格式 ：JSON

返回数据示例 ：

1）开始充电的情况：

{"result":1}  数据库更新成功

{"result":0}  数据库更新失败

说明: 字段：result ; 类型：int

2）结束充电情况：

{"result":1}  数据库更新成功

{"result":0}  数据库更新失败

说明: 

字段：result ; 类型：int  备注：数据库更新结果

3）取车：
{"result":1，"money":10.4}  数据库更新成功,充电金额：10.4元

{"result":0}  数据库更新失败

字段：result ; 类型：int  备注：数据库更新结果

字段：money ; 类型：double  备注：消费金额
###2.3 反向控制
**API**

URL ：http://wechat123.ngrok.cc/service/AmmeterControl

HTTP请求方式 ：GET

返回数据格式 ：JSON

返回数据示例 ：

1) {"Ammeter_id":1,"control":1} 1号充电站打开

2) {"Ammeter_id":1,"control":0} 1号充电站关闭 

说明: 

字段：Ammeter_id ; 类型：int ; 备注：充电站编号

字段：control ; 类型：int ; 备注：指令
##3.WEB端管理 /Web/
###3.1管理员入口 /admin/
* 管理员登陆界面
* 管理首页
* 用户信息的管理
* 充电站信息的管理(包括对充电站的实时控制)
* 消费情况的管理

###3.2学生入口 /stu/
* 学生注册登录界面
* 管理首页
* 信息的修改
* 过往消费记录的查询

##4.微信公众号开发 /WeChat/
* 用户资料的绑定
* 消费记录的查询
* 充好电的信息推送


