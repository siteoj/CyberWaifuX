# CyberWaifuX
(Copy from CyberWaifu)
一个基于CyberWaifu开发的个人QQ机器人，可以进行人格设定，上下文语境结合，长期记忆链以及QQ说说的发送

本项目基于[Syan-Lin/CyberWaifu](https://github.com/Syan-Lin/CyberWaifu)开发更改，修复部分原项目bug添加了部分功能

该项目使用 [LangChain](https://github.com/hwchase17/langchain) 作为 LLM 主体框架，使用 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 进行 QQ 机器人部署，TTS 支持 vits、[edge-tts](https://github.com/rany2/edge-tts)。

语言模型支持：
- ChatGPT
- Claude

### 功能

✅ 预定义的思考链：使 AI 可以进行一定的逻辑思考，进行决策。例如在文本中添加 Emoji、发送表情包等等。

✅ 记忆数据库：自动总结对话内容并导入记忆数据库，根据用户的提问引入上下文，从而实现长时记忆。同时支持批量导入记忆，使人设更丰富、真实和可控。

✅ 现实感知：AI 可以感知现实的时间并模拟自己的状态和行为，例如晚上会在睡觉、用户隔很久回复会有相应反馈（这部分表现暂时不稳定）。

✅ 联网搜索：根据用户的信息，自主构造搜索决策，并引入上下文。

✅ QQ 机器人部署

✅ QQ 表情支持

✅ 人设模板、自定义人设

✅ edge-tts, azure 语音服务支持

✅ QQ空间图文发送（可选自写文案或原文发送）

✅ vits, emotion-vits 支持

✅ 百度翻译api支持

⬜ bark 支持

✅ AI 绘图支持，将绘图引入思考链，使 AI 可以生成图片，例如 AI 自拍

### 安装💻

Python 版本：3.10.10
为了保存记忆方便，我修改了原有的langchain库
需要将项目中的langchain.rar解压覆盖至pyhton根目录下的\Lib\site-packages中

#### QQ 机器人部署
根据 [go-cqhttp 下载文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E4%B8%8B%E8%BD%BD)，下载相应平台的可执行程序，并放入 `qqbot` 目录中

#### 记忆数据库向量计算模型（使用 Claude 需要）
为了支持本地的文本向量计算，需要引入 text embedding 模型，这里使用 [Sentence Transformer](https://github.com/UKPLab/sentence-transformers)

首先 [下载模型](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/paraphrase-multilingual-MiniLM-L12-v2.zip)，然后解压到根目录的 `st_model` 文件夹，如果不存在请手动创建

### 配置✏️

按照 `template.ini` 进行配置，配置完成后改名为 `config.ini`

#### 大语言模型配置

- OpenAI：需要配置 `openai_key`，这部分网上有很多教程，就不赘述了
- Claude：需要配置 `user_oauth_token` 和 `bot_id`，具体参考 [Claude API 接入教程](https://juejin.cn/post/7230366377705472060)

#### QQ 机器人配置：
运行 `main.py` 提示：

```
PyCqBot: go-cqhttp 警告 账号密码未配置, 将使用二维码登录.
PyCqBot: go-cqhttp 警告 虚拟设备信息不存在, 将自动生成随机设备.
PyCqBot: go-cqhttp 警告 当前协议不支持二维码登录, 请配置账号密码登录.
```

在 `qqbot/device.json` 文件中，找到字段 `protocol`，将值修改为 2 即可扫码登录

权限设置：`qqbot/bot.json` 文件

```json5
// 本项目针对私聊场景设计，目前不支持群组
{
    // 需要处理的 QQ 私聊信息，为空处理所有
    "user_id_list": [
        1234567,
        7654321
    ]
}
```
#### 百度翻译api设置
在config.ini 中找到appkey和apiid
```
# 百度翻译 API
[Translate_Baidu]
baidu_appid =
baidu_secretKey =
```
填入自己的key
#### 人设 Prompt 配置
根据 `presets/charactor/模板.txt` 进行编写，将编写好的人设 Prompt 丢到 `presets/charactor` 目录下即可，随后在 `config.ini` 配置文件中的 `charactor` 字段填写文件名（不包含后缀名）

记忆设定同样是丢到 `presets/charactor` 目录下，多段记忆用空行分开，并在配置文件中填写 `memory` 字段

#### 联网搜索配置
在 [Google Serper](https://serper.dev/) 中注册并创建一个 API key，在 `config.ini` 中配置并开启即可。Google Serper 可以免费使用 1000 次调用，实测可以使用很久。

由于上下文长度的限制，目前搜索引入的内容并不多，只能获取简单的事实信息。

### 使用🎉
运行 `main.py` 即可

```powershell
conda activate CyberWaifu
python main.py
```