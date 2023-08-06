### 说明

这是一个 python logging 的配置，主要做了以下配置；

- json 格式输出
- 添加 `request_id` 字段，在日志中打印 http 请求中的 `X-Request-Id` 的内容，基于 flask 框架。
- 配置输出的默认字段。

### 使用指南

1. 添加依赖 `atman-logging-config >= 0.1`
2. 在程序的入口文件中添加 `import logging_config` 即可以使用默认配置，默认 logger 的名称是 root，可以通过 logging.getLogger('name')，来修改名称。