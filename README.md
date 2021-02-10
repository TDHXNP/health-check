# health-check

> LNPU形式主义自动化打卡python脚本
> 写的蛮乱的,但我懒得改了

## 自动打卡
1. Fork本项目

2. 前往Fork后的项目的`Settings`页面

3. 侧边栏点击`Secrets`

4. 通过`add a new secret`添加自己的如下信息（冒号前面的是需要添加的secret的`Name`，后面是对应的`Value`的含义）

    - Uid : 学号
    - Pwd : 手机号
    - qmsgkey : 消息推送key,详见[Qmsg酱](https://qmsg.zendee.cn/)


## 停止使用

1. 进入Fork后的项目的`Settings`页面
2. 点击左侧侧边栏的 `Actions`进入设置页面
3. 选择`Disable Actions for this repository `即可禁用掉自动打卡

当然，也可以直接删除Fork后的仓库

## 手动打卡

建议挂自己服务器上,Cookies保存到cookies.txt,一星期更新一次
系统要求: 已安装`python`

1. 下载本项目
2. 进入项目目录`cd health-check`
3. 安装依赖`pip install -r requirements.txt`
4. 执行`python ./local.py 学号 密码 qmsgkey`
> qmsgkey : 消息推送key,详见[Qmsg酱](https://qmsg.zendee.cn/)

之后日常打卡只需要执行`python ./local.py 学号 密码 qmsgkey`
