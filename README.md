# QQVoice Capturer
一个简单的、可能会对被使用者产生语音PTSD的Bot

目的:将受害者每次发的语音进行解压 转码

你可以创建一个项目或网站将受害者的语音以非常离谱的形式在网络上公开（

这可能是违法的 但是我们不负任何责任（

[一个实例](https://github.com/VmLuRui262/HarryYu_Voice)

如果你喜欢这种社死项目，你可以做我老婆

# 依赖
- [websocket-client](https://pypi.org/project/websocket-client/)
- [pyyaml](https://pypi.org/project/PyYAML/)
- [datetime](https://pypi.org/project/datetime/)
<!-- - [platform](https://pypi.org/project/platform/)-->
<!-- - [os](https://pypi.org/project/os/) -->
<!-- - [json](https://pypi.org/project/json/) -->
# 如何使用
- 将本仓库git clone下来 `git clone https://github.com/VmLuRui262/QQVoice_Capturer.git`
- 第一次运行以生成配置文件 `python3 main.py`
- 在配置文件中设置你go-cqhttp的配置,如IP,端口,access_token等等
- 在 `sufferer` 输入受害人的QQ
- `gocq_path`输入你的go-cqhttp的路径
- `voice_path`输入你的语音存放路径
- `voice_Name`输入你的语音名称及格式
- 运行main.py `python3 main.py`
# `voice_Name` 格式及支持的变量
! : 格式化函数在 `main.py` 的57行 `def voice_nformat(voice_name,id):`

支持的变量:
- `^date^` - 发送语音的日期 如(2022-06-01)
- `^time^` - 发送语音的时间 如(12:00:00)
- `^id^` - 发送语音的序号 如(001)

# 感谢

本项目基于以下项目

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [silk-v3-decoder](https://github.com/kn007/silk-v3-decoder)