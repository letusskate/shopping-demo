# shopping-demo
silk assessment component
## my coding diary
### 20221103下午
1.pip install Django==2.1.12
2.
django-admin startproject django_study
3.
拖出来
4.
pip install psycopg2-binary==2.8.6
5.
Python manage.py runserver
6.
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
8.
python manage.py migrate
9.
Python manage.py createsuperuser
10.
python manage.py startapp apps
11.
创建users、carts、goods、orders四个app并注册
    'apps.users',
    'apps.goods',
    'apps.orders',
    'apps.carts',

### 20221104上午
1.昨天的文件上传到github
2.新建utils
写auth即token校验方法和basemodel
3.每个app的model中创建数据表
一个存users；一个存goods；建立一个中间表，由于一个用户对应一个购物车，因此不需要建立购物车表，同时用户与商品构成m:n的关系，因此建立中间表存储添加购物车这个过程，为CartsGoods；用户与订单构成1：n关系，因此在订单中添加用户的外键，订单表为Orders；订单与商品构成m：n关系，因此创建中间表储存下单的过程，为OrdersGoods。共5个表。
4.makemigrations、migrate，
期间出现问题，因为中途改了数据库，django不允许在已有数据库中新增一个非空列，除非有默认值，因此设置default=xxx。
5.写admin页面
在网站上各新增一条数据。注意建立数据库时候要指定表名，不然很可能django找不到表。
6.设置日志
settings里面写日志
7.解决跨域cors和跨站
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
8.django rest framework
1.安装
pip install djangorestframework==3.10.3
2.Settings installed apps加入
'rest_framework'
9.userinfo接口
在app目录下，view.py里面写getuserinfo接口，render方法写入html
在app同级目录创建templates目录
templates目录下写html文档
项目目录下，settings.py，templates选项中，'DIRS':[os.path.join(BASE_DIR,'templates')],
在项目目录下找到urls.py，进入注册新的url
postman进行测试
10.jwt校验基础配置
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
11.rap2建好仓库
RAP2 (bundleb2b.net)

### 20221104下午
