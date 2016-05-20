## Braavos

### Develop Dependence

- 1. postgresql
- 2. [pyenv](https://github.com/yyuu/pyenv) + [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
  - pyenv virtualenv braavos

### How To Start:

- 1. create database on postgresql #[PostgreSQL新手入门](http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)
  - createdb braavos
- 2. edit local_config.py, SQLALCHEMY_DATABASE_URI is required
  - cp local_config.py.sample local_config.py
  - edit local_config.py
- 3. pip install -r requirements.txt  # in your virtual env
- 4. make hook  # init git hooks
- 5. make web  # = make clear + make fill + make serve
- 6. use Account0: test0@inad.com Password: your_default_password to login


### Filled Data When make fill

- Account: test0 Password: your_default_password  Role: Admin
- Account: test1 Password: your_default_password  Role: Leader
- Account: test2 Password: your_default_password  Role: Saler


### 开发流程

- 1.Fork & Clone
- 2.git remote add upstream url
    git pull upstream
- 3.创建您的特性分支 (git checkout -b my-new-feature)
- 4.提交您的改动 (git commit -am 'Added some feature')
- 5.将您的修改记录提交到远程 git 仓库 (git push origin my-new-feature)
- 6.然后到 github 网站的该 git 远程仓库的 my-new-feature 分支下发起 Pull Request


### Test

    make test

### Deploy Dependence

- 1. nginx
- 2. supervisor
- 3. [pyenv](https://github.com/yyuu/pyenv) + [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
- 4. gunicorn

### Deploy

- 1. install fabric
- 2. add your id_rsa.pub to /home/inad/.ssh/authorized_keys on our server
- 3. fab deploy # read the tool/fabfile.py


### 目录介绍

- 1. models
  - 基础 
    - User 用户信息(名称，邮箱，密码)  Team 团队(角色，区域)
    - Client 客户 Agent 代理公司  AgentGroup 代理集团 Medium  媒体
    - Attachment 附件
    - Comment 留言评论
  - 合同流程
    - DoubanOrder 豆瓣订单，客户直接和豆瓣签署订单
    - FrameworkOrder 框架订单， 代理集团和致趣签署的全年框架
    - ClientOrder 客户订单，客户和致趣签署的订单(包含客户，代理，金额，时间等信息)
    - Order 媒体订单，致趣和媒体签订的订单(此订单和排期关联)
    - AssociatedDoubanOrder 关联豆瓣订单，媒体订单走第三方公司和豆瓣签署的订单
  - 外包流程
    - Outsource 外包
  - 排期投放
    - AdUnit 广告单元 AdPosition 广告位
    - AdItem 订单项(订单在某个广告位上的投放)  AdSchedule 排期(订单项的投放时间，投放量安排) Material 投放素材
    - Delivery 投放统计
- 2. controllers
  - user, client, medium 分别是基础信息的管理页面
  - order 包含整个合同流程，排期投放相关
  - storage 投放库存信息汇总
  - file 文件上传
- 3. templates
  - comment 评论组件
  - form 表单组件
- 4. forms
  - controllers中用到的表单


### 数据库升级

- 1. 如果新增了 model, 或者修改了model的字段
 - 在 ./migrations/env.py 里面引用新 model
 - python manage.py db revision --autogenerate --message "add your msg"  # 生成新的版本
 - python manage.py db upgrade
- 2. 如果其他人修改了数据库字段
 - 更新代码到最新版本
 - python manage.py db upgrade
