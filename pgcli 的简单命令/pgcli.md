## 一、常用功能

>  pgcli -u 用户名 -w 密码 # 连接数据库

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148867856-01.png)

> \l  # 列出可用数据库

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148869543-02.png)

> \c 数据库名 # 进入数据库

> \d # 查看表名

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148872140-03.png)

> \d 表名 # 查看表中字段名及类型

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148873857-04.png)

> 执行 CRUD 命令

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148875692-05.png)

> \q # 退出

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148877488-06.png)

## 二、常用命令

```text
$ pgcli --help

Usage: pgcli [OPTIONS] [DBNAME] [USERNAME]

Options:
  -h, --host TEXT         PostgreSQL数据库所在主机地址.
  -p, --port INTEGER      PostgreSQL数据库实例的端口.
  -U, --username TEXT     PostgreSQL数据库用户名.
  -u, --user TEXT         PostgreSQL数据库用户名.
  -W, --password          强制提示输入密码.
  -w, --no-password       不提示输入密码.
  --single-connection     只是用单一的连接.
  -v, --version           查看pgcli版本.
  -d, --dbname TEXT       目标连接的数据库.
  --pgclirc PATH          pgclirc文件的路径.
  -D, --dsn TEXT          使用配置到[alias_dsn]部分的DSN pgclirc文件.
  --list-dsn              配置到[alias_dsn]部分的DSN列表pgclirc文件.
  --row-limit INTEGER     设置行限制提示的阈值。使用0禁用提示.
  --less-chatty           跳过启动时的介绍和退出时的再见.
  --prompt TEXT           提示格式(默认: "\u@\h:\d> ").
  --prompt-dsn TEXT       使用DSN别名的连接的提示格式(默认: "\u@\h:\d> ").
  -l, --list              列出可用的数据库，然后退出.
  --auto-vertical-output  如果输入内容比终端宽度宽，自动切换到垂直输出模式.
  --warn / --no-warn      在运行危险查询之前发出警告.
```

## 三、代码联想识别

![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630148865052-image01.png)

