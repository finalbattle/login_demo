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
skip-grant-table
```
重新登录数据库


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
