# esp32-gemini-streaming-python
使用python脚本和esp32实现蓝牙连接AI模型<br>
支持 Gemini API 和 DeepSeek API 两种后端 可自行扩展<br>
你需要配置的pip包目前有 pyserial openai google-genai  <br>
显而易见的是 使用此方案前你需要拥有esp32(未来可能不止esp32渥)<br>
欢迎任何人加入此项目<br>

未来打算<br>
v0.8demo : 添加外设支持 上下文记忆 流式回传 完善项目文档<br>
v0.9demo : wifi直连 NVS配置持久化 鲁棒性测试 多开发板支持<br>


更新日志<br>
v0.5demo : 将我之前用的小工具提交到github上 并做了windows与linux双平台适配<br>
v0.6demo : 全面大改项目结构 将之前在一个python脚本内的代码模块化了 适合调试与改进 同时增加后续更新api的接口<br>
v0.7demo : 完成api模式 支持gemini与deepseek双后端 自动拉取可用模型列表 移除Selenium模式<br>

!!!!请注意 此分支不会再收到任何更新<br>
