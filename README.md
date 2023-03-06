2023.3.6 `增加了gpt-3.5-turbo模型调用，效果与官方chatgpt接近`

2023.2.24 `增加了ChatYuan调用和UI，体验下国产货`

2023.2.21 `本人只是增加了一个微信风格的UI，重新build一个镜像即可`
>原作者项目地址：[slippersheepig/chatgpt-web](https://github.com/slippersheepig/chatgpt-web)

2023.2.20 `重构关键代码，内置本人使用的UI，支持查看历史对话记录`
> 感谢某爱心人士捐助，https://gpt.sheepig.top/chat 已恢复使用

# chatgpt-web
### 使用GPT-3.5中的text-davinci-003模型，利用OpenAI API实现简单HTML网页版在线聊天（基于[此项目](https://github.com/AlliotTech/chatgpt-web)调整而来）
> 该版本基于OPENAI API KEY开发，想使用`ChatGPT`的请访问[chatgpt-html](https://github.com/slippersheepig/chatgpt-html)
#### ![G L%7VF I~{@83}SVRI_WPN](https://user-images.githubusercontent.com/58287293/207792987-a0a781df-8273-4148-a369-aa4a2379686a.png)（重要）ChatGPT与GPT-3.5（OpenAI API）的区别
- 在[OpenAI官方网页](https://openai.com/blog/chatgpt/)中，我们可以看到官方对ChatGPT的描述为“ChatGPT is fine-tuned from a model in the GPT-3.5 series, which finished training in early 2022. You can learn more about the 3.5 series [here](https://beta.openai.com/docs/model-index-for-researchers). ChatGPT and GPT 3.5 were trained on an Azure AI supercomputing infrastructure”，从而得知ChatGPT与GPT-3.5是两个不同产品
- 官方对GPT-3.5系列的[介绍](https://beta.openai.com/docs/model-index-for-researchers)里，`text-davinci-003`是其中的模型之一
- 我们再查阅官方对OpenAI API KEY的[介绍](https://beta.openai.com/docs/introduction/key-concepts)，其中有一句“The API is powered by a set of models with different capabilities and price points. Our base GPT-3 models are called Davinci, Curie, Babbage and Ada”，davinci赫然在列
#### ![I4{CU~ G( OH$WR_ T_1JWF](https://user-images.githubusercontent.com/58287293/207798807-a4dce6d3-14a0-40af-8008-30de8a55d513.png) 至此，我们可以得出结论：现在所有使用OpenAI API KEY的项目，`都不是基于ChatGPT开发的项目`，官方并未发布ChatGPT的API接口
- 事实上，ChatGPT最近发生过登录认证风波，想了解详细过程的可以查看这个[issue](https://github.com/acheong08/ChatGPT/issues/261)
- 如果你自己有分别使用过ChatGPT的官方chat和OpenAI的API接口chat，你会发现API接口chat比ChatGPT的官方chat“笨”得多
## 部署
### 获取OpenAI API KEY
- 建议参考[此教程](https://blog.csdn.net/hekaiyou/article/details/128303729)获取
### 配置
#### 从源码配置
- 请参考原作者[github](https://github.com/AlliotTech/chatgpt-web)
#### 使用Docker Compose
- 新建`docker-compose.yml`配置文件，粘贴以下内容并保存
```bash
services:
  chatgpt:
    image: sheepgreen/chatgpt-web #如果是arm架构，需要改成chatgpt-web:arm
    container_name: webchat
    environment:
      - OPENAI_API_KEY=前面你获取到的OpenAI API KEY
#    volumes:
#      - ./chat.html:/chatgpt-web/templates/chat.html #默认内置我的UI，如需替换自用网页请取消注释
    ports:
      - "8888:8088" #8088为容器内部端口，不可更改；8888为外部映射端口，可自行更改
    restart: always
```
- 输入`docker-compose up -d`即启动成功
## 注意事项
- gpt3.5访问地址：http://ip:port
- 原作者访问地址：http://ip:port/chat
- YuanChat访问地址：http://ip:port/yuan
