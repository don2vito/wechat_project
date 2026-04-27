[toc]



# Picgo 让配置图床就像喝水一样简单

## 一、起因

众所周知，前几周常用的排版软件 mdnice 突然实行了收费政策，并且收取的费用还不低。当然，我们都能理解服务器运行需要很大一笔费用，但也实实在在影响到了我们这些内容生产者对外部平台进行排版、发布的工作流程。

虽然我第一时间找到了在线部署的替代项目，但这毕竟也是人家部署的，总没有`本地和异地备份相结合`的方式那么靠谱。因此 ，寻找让自己放心的免费、平替工作流就成为了当务之急。所幸经过一番查找和实践，`typora + picgo + github`的办法最终让我感到满意，支持 markdown 进行排版，同时可以在线同步图片，支持以 HTML 格式直接发布到公众号。

这篇文章就把简单地配置图床的步骤教给大家，今后一段时间，我应该都会以这个新的工作流程来进行书写记录。

## 二、Github 的配置

### 1. 新建仓库

![新建仓库](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161313901.png)

![配置仓库](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161315638.png)

### 2. 生成令牌

![进入设置](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161316284.png)

![进入开发者设置](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161316991.png)

![进入令牌设置](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161317943.png)

![对令牌进行设置](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161318810.png)

![保存令牌](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161319058.png)

## 三、Picgo 的配置

### 1. 对 Github 图床进行配置

![配置 GitHub 图床](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161312044.png)

### 2. 设定自定义域名

- ** https://cdn.jsdelivr.net/gh/ + 设定仓库名**

## 四、Typora 的配置

### 1. 进入“偏好设置”，对“图像”进行配置

![配置 Picgo](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161305597.png)

### 2. 验证图片上传状态

![验证图片上传选项](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202407161305523.png)