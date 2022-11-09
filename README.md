# shopping-demo
silk assessment component

## Version 1.0.0（20221109 17:40)
After 4 days' work, I have finished the demo by myself. It's my first developing demo as I enjoyed machine learning and deep learning in my college life. I have learnt a lot from database designing to coding and testing. It is like a summry of my learning time and a presantation of my first job. I know it has many disadvantages, but I love it.  

## my coding diary
### 20221103下午
#### 1.pip install Django==2.1.12
#### 2.
django-admin startproject django_study
#### 3.
拖出来
#### 4.
pip install psycopg2-binary==2.8.6
#### 5.
Python manage.py runserver
#### 6.
Settings.py数据库改为以下内容
DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123654',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
#### 8.
python manage.py migrate
#### 9.
Python manage.py createsuperuser
#### 10.
python manage.py startapp apps
#### 11.
创建users、carts、goods、orders四个app并注册
    'apps.users',
    'apps.goods',
    'apps.orders',
    'apps.carts',

### 20221104上午
#### 1.昨天的文件上传到github
#### 2.新建utils
写auth即token校验方法和basemodel
#### 3.每个app的model中创建数据表
一个存users；一个存goods；建立一个中间表，由于一个用户对应一个购物车，因此不需要建立购物车表，同时用户与商品构成m:n的关系，因此建立中间表存储添加购物车这个过程，为CartsGoods；用户与订单构成1：n关系，因此在订单中添加用户的外键，订单表为Orders；订单与商品构成m：n关系，因此创建中间表储存下单的过程，为OrdersGoods。共5个表。
#### 4.makemigrations、migrate，
期间出现问题，因为中途改了数据库，django不允许在已有数据库中新增一个非空列，除非有默认值，因此设置default=xxx。
#### 5.写admin页面
在网站上各新增一条数据。注意建立数据库时候要指定表名，不然很可能django找不到表。
#### 6.设置日志
settings里面写日志
#### 7.解决跨域cors和跨站
1.安装
 pip install django-cors-headers==3.3.0
2.settings里面，3处设置，apps里面
"corsheaders",#跨域设置
3.middleware里面，注意放置位置
MIDDLEWARE=[
"corsheaders.middleware.CorsMiddleware",#跨域设置
'django.middleware.common.CommonMiddleware',]
4.加一行
CORS_ORINGINS_ALLOW_ALL=True#允许跨域
5.注释一行（解决跨站）
    # 'django.middleware.csrf.CsrfViewMiddleware',
#### 8.django rest framework
1.安装
pip install djangorestframework==3.10.3
2.Settings installed apps加入
'rest_framework'
#### 9.userinfo接口
在app目录下，view.py里面写getuserinfo接口，render方法写入html
在app同级目录创建templates目录
templates目录下写html文档
项目目录下，settings.py，templates选项中，'DIRS':[os.path.join(BASE_DIR,'templates')],
在项目目录下找到urls.py，进入注册新的url
postman进行测试
#### 10.jwt校验基础配置
1.安装包
pip install PyJWT==1.7.1
2.utls中新建（之前完成了）
utils中创建auth.py，定义JWT检验的方法
3.settings加入下面的内容
REST_FRAMEWORK = {    #把JWTtoken校验注册
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'apps.utils.auth.JWTAuthentication',
    ),
}
#### 11.rap2建好仓库
RAP2 (bundleb2b.net)

### 20221104下午
#### 1.配置redis
1.安装包
pip install django-redis==4.10.0
2.设置setting
CACHES = {
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://:@localhost:6379/0",#最后的反斜杠0代表第几个数据库，redis默认有16个数据库
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@localhost:6379/1",  # 最后的反斜杠0代表第几个数据库，redis默认有16个数据库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
#### 2.写注册接口
成功
又改了一下数据库，user表加了密码，别忘了设置default
#### 3.写登录接口
403forbidden
#### 4.写改密码接口
还没写完


### 20221107上午
#### 1.登录接口
一共三种方法避免，我试了两种，依然报403错误。
放弃rest framwork，用原生django再写一次。因为这个接口不需要token校验，因此并不一定要用restframwork。问题得以避免，接口正常运行
#### 2.改密码接口
两种方法，一种是save，一种是update，我用的update，注意不要查一个人两次，不然要花双倍时间
#### 3.查看商品接口
注意模糊查询位置，还没有写好所有参数
#### 4.添加购物车接口
没写完!
### 20221107下午
#### 1.添加购物车接口
注意添加外键的过程中，需要指定外键值为主表一个对象，而不为主表的主键。
#### 2.编辑购物车接口
如果判断过程需要多次在其他表搜索，最好提前搜索完并将数据记录下来，每次判断储存下来的搜索结果即可。
#### 3.下单接口
一次只能下一种物品，这样在ordersgoods表里是一行，方便操作。
下单时要输入orderid，如果不输入视为新建订单，需要输入地址和电话，否则视为修改订单。
修改储存order的数据库结构，添加总价格、地址、电话三个参数。
下单整体流程：
0.如果没有此order，新建一个order
1.更新ordergoods表
2.更新goods表商品库存
3.更新order表的总价格
#### 4.查看订单接口
输出order表全部信息
缓存的设置有一些问题

### 20221108上午
#### 1.更改下单接口
如果添加已在ordergoods数据库中出现的数据，那应该仅更改物品数量，而不是新增一条。
修改数据库后删除缓存
#### 2.更改查看订单接口
增加缓存的设置，直接把序列化过后的list放入缓存，这样再次查询很方便。
#### 3.更改查看商品接口
修改缓存的设置。
#### 4.rap2仓库写好
根据代码定义
#### 5.画er图
我的navicat16过期了，从之前的网盘找到了navicat15。
Navicat15无法打开postgressql15，能打开postgres13。
因此我只能把项目端口迁移到5433，之后用navicat画er图。
之后再迁移回5432，数据
库里数据还在。

### 20221108下午
#### 1.更改添加购物车接口
如果之前购物车存在了该商品，此次添加应该在原有记录上增加数量， 而不是新增一条记录
#### 2.新写一个可以接收多个物品，一步到位的下单接口
没写完


### 20221109上午
#### 1.新写一个可以接收多个物品，一步到位的下单接口
1.获取列表
2.orders新增一条订单
3.遍历列表，ordersgoods新增
4.遍历过程中累计订单totalprice
5.遍历过程中不断更改goods库存
6.遍历结束后，一次性写入订单totalprice
#### 2.Rap2定义好
根据新写的接口定义即可。
修改之前rap2中的一些问题，有的接口response没有code和message
#### 3.附加题1，实现用户注册后bc也有用户
实现了，但是没把两个接口写在一起，创建bc用户一个接口，在本地数据库创建用户一个接口。但是这两个接口的输入格式是一样的，写在一起很简单。
创建bc用户的接口很简单，就是把用户的输入经过自己的serilizer校验后，用requests包转发到bc的api上，之后将bc返回的respons转化为json格式返还给用户。
#### 4.附加题2，实现创建订单后bc也有订单
没写完


### 20221109下午
#### 1.实现创建订单后bc也有订单
成功，但这个接口写的很水，保持了bc原有的输入格式，没有任何调整。也没有用序列化器校验输入是否合法。
可以说他就是BC的接口，只是传进来的数据被我们拿到了。
#### 2.rap2完善附加题的两个接口
附加题1的接口很好写，因为没多少输入
附加题2的接口内容太复杂了，因为没有任何调整，因此要根据文档的要求都打进去。
后来发现rap2可以导入，直接把json实例粘贴进去，他会自己创建。
