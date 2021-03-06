# login_demo
基于tornado + pycket + pymysql + sqlachemy打造一个简易的登录demo

# 安装环境:
```
sudo apt-get install marialdb-server marialdb-client
sudo apt-get install redis
```
安装tornado和mysql相关库
```
pip install tornado==6.0.4
pip install mysql-connector-python=8.0.20
pip install pymysql
pip install sqlalchemy==1.3.18
```
用于保存session的pycket和redis
```
pip install redis==3.5.3
pip install pycket==0.3.0
```
用于生成model.py的sqlacodegen
```
pip install sqlacodegen==2.2.0
```
# 准备数据库
查看数据库服务状态,并启动mysql
```
sudo service mysql status
ps aux | grep mysql
sudo service mysql restart
```

连接数据库
```
mysql -u root
```
如果报错:ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES),
打开/etc/mysql/my.conf或者/etc/mysql/marialdb.conf.d/50-server.cnf,增加如下配置
```
[mysqld]
...
skip-grant-tables
```
重启数据库
```
sudo service mysql restart
```
重新登录数据库
```
mysql -u root
```
修改密码
```
use mysql;
update user set authentication_string=password("root") where user="root";
```


创建数据库和数据表
```
create database demo1
use demo1
```
增加一个创建表的sql文件:demo1.sql
```
create table user(
  id INT(11) auto_increment,
  username varchar(20) not null,
  password varchar(100) not null,
  create_time datetime not null default current_time,
  primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```
mysql -u root demo1 < demo1.sql
```
此时登录到数据库,可以看到user表已经创建好了

使用sqlacodegen同步demo1中的表结构到models.py中,生成sqlalchemy的模型,使用python代码可以访问数据库
```
sqlacodegen mysql+pymysql://root:@localhost:3306/demo1 > models.py
```

# Application配置相关参数
```
class MyApplication(tornado.web.Application):
    def __init__(self):
        #handlers = [
        #    (r"/", IndexHandler),
        #    (r"/login", LoginHandler),
        #]
        handlers = handler_list
        # settings config
        settings = dict(
            template_path = 'templates', # 模板地址
            login_url = '/login', # 默认登录页面
            cookie_secret = '123456', # 安全cookie
            pycket = {  # pycket配置
                'engine': 'redis',  # session引擎采用redis作为服务端存储
                'storage': {  # redis的host和port
                    'host': 'localhost',
                    'port': 6379,
                },
                'cookie': { # 默认session过期时间
                    'expires_days': 1
                }
            },
            autoreload=True # 通过autoreload参数可以在修改代码以后自动重启服务
        )
        super(MyApplication, self).__init__(handlers, **settings)

app = MyApplication()
```

# 遇到的问题及解决办法:
## sqlalchemy Instance <User at xxx> is not bound to a Session;attribute refresh operation cannot proceed
出现这个问题的原因是在commit提交以后,导致当前操作的Model对象不在当前的session中
解决办法就是在提交之前来操作User对象或者使用merge方法,把对象重新放到session中
```
user = self.db.merge(user)
```
  
## connection refused:
出现连接被拒绝,并不是真的服务端拒绝了你,恰恰相反,是服务端挂了,或者这个端口压根没有任何程序在监听,所以处理方法是查找对应端口的服务进程是否异常
