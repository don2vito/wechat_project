## 一、需求

AI 发展到今天的水平，用来翻译外文书籍已经不在话下了。在学习的过程中，经常需要在保留原始排版的情况下，对外文文档进行翻译并保存在本地，网上也有相关网站能够实现这个需求。但用起来总是不舒服，要不就是免费且限制颇多（文件大小限制、翻译页数限制、调用 API 限制等），要不就是收费昂贵（也不是无限量的）。

比如著名插件`沉浸式翻译`开发的`BabelDOC`就能满足需要，可以去`https://app.immersivetranslate.com/babel-doc`体验。界面和效果如下，项目地址在https://github.com/funstory-ai/BabelDOC'，纯命令行部署和运行，具备一定的门槛。

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221422664.png)

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221423306.png)

使用网页端的限制比较多，费用也不低，随便看两家，你就会心里打鼓，这和抢钱有什么区别嘛！

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221427361.png)

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221428607.png)

我迫切需要一个能够在本地部署，可以自行调用 API 的，并且能保留原始排版的翻译神器。一开始，我准备通过 vibe coding 的方式自己造个轮子，但转念一想，上面的 BabelDOC 不就是个很好的轮子嘛，我直接在 GitHub 上找一下现成的轮子岂不是更方便，带着这个思路去搜索了一番。

## 二、解决方案

很快，就找到一个叫做`BabelDOC-WebUI`的开源项目，没错，就是上面这个项目套了一个前端的外壳，更加方便操作，项目地址在`https://github.com/ChenjieXu/BabelDOC-WebUI`，是基于 NiceGUI 构建的 BabelDOC Web 界面。

直接跟着文档的步骤进行操作，第一次运行会初始化下载一些必备的组件，根据网速情况的不同，需要耐心等待一些时间。

如果你实在不会，也可以把下载好的项目文件丢给 AI，让 AI 来帮你部署，其实我就是这么干的，嘿嘿~

如果你有魔法工具，建议连上魔法工具再运行，因为初始化需要下载的组件默认链接地址都在国外，会引起超时报错。

没有工具的同学，可以让 AI 把命令换成国内源，就可以解决这个问题了。

命令很简单，就三步：

```bash
# 克隆仓库
git clone https://github.com/ChenjieXu/BabelDOC-WebUI.git
cd BabelDOC-WebUI

# 安装依赖
uv sync

# 运行应用
uv run python main.py
```

运行应用后，浏览器会自动弹出界面，如果没有弹出，访问 `http://localhost:8080/` 即可使用。

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221456483.png)

接下来，要配置模型。点击右上角「设置」按钮，选择服务商，添加模型配置，填入 API Key，保存并选择模型。

这里我推荐使用 `deepseek` 的推理模型，效果和价格相对好一些，性价比比较高。可以去 `https://platform.deepseek.com/usage` 进行充值，然后创建自己的 key。

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221502370.png)

经过试用，使用 V3 模型翻译一页大概花费约 1 分钱，使用 R1 模型翻译一页大概花费约 3 分钱，R1 模型的翻译结果更好，所以我建议使用 R1 推理模型，这个价格可以接受。

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221504985.png)

还可以对输出效果进行设置，双语对照 PDF、纯译文 PDF、水印模式、QPS 限制、术语表、OCR 模式、自定义提示词等。

设置保存在 `~/.config/babeldoc-webui/settings.json`，可以手动更改配置。

## 三、避坑指南

通过简单使用，发现一些 bug，还不是太稳定。我把自己亲身经历遇到过的踩坑问题列在下面，希望大家能够避坑。

- 配置服务商和 API key，显示成功之后，运行翻译时，提示没有配置模型。
- 不支持图片型 PDF 文档，强行运行会报错。
- 使用免费 API 时，API 会限制调用频率，容易引起报错。
- 配置多个服务商，切换选择后，运行翻译时，提示错误；重启之后，配置丢失；

以上问题，是目前我遇到过的，也许你还会遇到新问题。但遇事不要慌，把命令行中的报错消息和前端界面提示的截图丢给 AI，基本上都能解决，再也不用去 StackOverflow 上碰运气了。

## 四、备选方案

### 1. PDFMathTranslate

项目地址：`https://github.com/PDFMathTranslate/PDFMathTranslate`

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221519540.png)

### 2. PDFMathTranslate-next

项目地址：`https://github.com/PDFMathTranslate-next/PDFMathTranslate-next`

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221523281.png)

### 3. GBabelDocUI

项目地址：`https://github.com/eaiu/GBabelDocUI`

![](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse@main/202604221517940.png)