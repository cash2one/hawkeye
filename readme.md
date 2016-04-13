# hawkeye

* 多线程
* 防被拦
* 抓取模块独立

## 使用
0. proxy.txt, 代理列表
1. url_constructor, 构造搜索 url
2. search_handler, 解析并提取搜索结果
3. result_handler, 依次处理 search_handler 返回的结果
4. reduce_handler, 对最后返回的所有结果合并处理

*具体可参考 git_parser.py*

### proxy.txt
* 格式为：ip:port，一行一个代理

### url_constructor
* 参数 keyword，返回值 (keyword, urls) 元组

### search_handler
* 参数
* 返回值：列表，元素为字典类型
* 默认值：[{'result': text}], text 为请求 url 返回的结果
* 如果元素中存在需要解析的 url，则用 request 指明 url 字段名
* 设置 redirect 为 True，替换 url 为重定向后的 url，在处理 baidu,google 等搜索结果的时候很好用

### result_handler
* 参数：第一个为 keyword，第二个为 search_handler 返回列表中单个元素
* 返回值：作为最终处理结果列表元素返回，返回为 None 表示丢弃处理结果
* 默认值：将参数打包为元组返回

### reduce_handler
自定义