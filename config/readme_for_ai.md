# readme_for_ai

## 目录职责

这个目录放运行配置模板，主要描述“程序去哪里读日志、去哪里读规则、按什么编码读、怎样识别字段”。

它负责运行时参数，不负责具体精灵规则。

## 在整体项目中的位置

`config/` 的内容会被 `src/rocoworld_yise_detector/config.py` 读取，产出 `AppConfig`，再被 CLI 和解析流程使用。

路径解析规则由代码层定义，不是在这里硬编码逻辑。

## 关键路径

### `config/config.example.json`

- 当前唯一配置模板。
- 用于演示项目如何跑通，也兼作配置 schema 的样例。
- 变更配置字段时，要同时改这个文件和 `src/rocoworld_yise_detector/config.py`。

## 当前配置字段

- `log_path`
  日志文件路径。相对路径会相对于当前配置文件所在目录解析。若接入真实游戏数据，这里应指向已开启深度日志后生成的日志文件。
- `database_path`
  规则数据库路径。相对路径同样相对于配置文件目录解析。
- `encodings`
  日志读取编码回退顺序。当前默认是 `utf-8`、`gbk`。
- `poll_interval_seconds`
  watch 模式轮询间隔。
- `line_filters`
  只有命中这些文本片段的行，解析器才会继续尝试提取字段。
- `field_aliases`
  原始日志字段名到标准字段名的映射别名集合。

## 对上游输入和下游输出

### 上游输入

- 人工编写或复制的 JSON 配置文件

### 下游输出

- `AppConfig`
- 给 `watcher.py` 提供日志路径、编码、轮询间隔
- 给 `parser.py` 提供 `line_filters` 和 `field_aliases`
- 给 `database.py` 提供规则文件路径

## 修改落点指引

### 如果要增加新的配置项

优先看：
- `config/config.example.json`
- `src/rocoworld_yise_detector/config.py`
- 若 CLI 也要暴露该项，再看 `src/rocoworld_yise_detector/cli.py`

### 如果要增加新的字段别名

优先看：
- `config/config.example.json`
- `src/rocoworld_yise_detector/config.py`
- `src/rocoworld_yise_detector/parser.py`

### 如果要支持本地私有配置

当前约定是使用 `config/config.local.json`，该文件已被 `.gitignore` 忽略。需要新增字段时，先更新示例配置和本目录文档，再让本地私有配置跟进。

### 如果要排查“配置改了但没生效”

优先检查：
- 相对路径是否是相对于配置文件目录而不是仓库根目录解析
- `field_aliases` 是否与 `parser.py` 当前支持的标准字段对齐
- `line_filters` 是否过严导致整行被过滤掉

## 边界与约定

- 配置层只描述运行参数，不保存具体精灵规则。
- 新增标准字段时，配置里只负责“别名映射”，不负责定义匹配算法。
- 不要把环境相关的私有路径直接写死到示例配置里。

## 当前待确认

- 官方 FAQ 已确认客户端支持手动开启深度日志；当前待确认的是深度日志文件的真实路径和命名是否稳定。
- 真实游戏日志的编码是否稳定只有 `utf-8` / `gbk`，还是还要支持其他编码。
- 真实遭遇日志的稳定标记是否适合继续用 `line_filters` 这种简单包含判断。
- 后续是否需要拆分出更细的配置文件，比如日志源配置、输出配置、通知配置，目前都还未定。
