# readme_for_ai

## 目录职责

这个目录是项目的运行时核心包。所有真正参与执行链路的代码都在这里。

它负责的事情是：
- 接收 CLI 命令
- 读取配置和规则库
- 读取日志文件
- 把原始日志行解析为结构化遭遇记录
- 根据规则库做异色判定
- 输出命令行结果

它不负责的事情是：
- 保存用户文案或产品介绍
- 保存真实规则数据
- 保存长期日志样本
- 定义测试策略

## 在整体项目中的位置

顶层关系是：

`config/`
-> 提供运行参数

`data/`
-> 提供规则库输入

`samples/`
-> 提供人工验证或示例输入

`src/rocoworld_yise_detector/`
-> 消费以上输入并产出判定结果

`tests/`
-> 验证这里的行为

## 关键路径

### `src/rocoworld_yise_detector/__main__.py`

- `python -m rocoworld_yise_detector` 的入口。
- 基本不承载业务逻辑，只把控制权交给 `cli.main()`。
- 只有当入口方式变化时才需要改它。

### `src/rocoworld_yise_detector/cli.py`

- 当前最重要的编排文件。
- 定义 `scan`、`watch`、`parse-line` 三个子命令。
- 负责把 `config.py`、`database.py`、`watcher.py`、`parser.py`、`detector.py` 串起来。
- 当日志文件不存在时，会在 stderr 输出“先确认已开启深度日志并检查日志路径”的提示。
- 新增子命令、修改输出格式、调整命令参数时，优先看这里。
- 它和 `config.py`、`watcher.py`、`parser.py`、`detector.py` 强相关。

### `src/rocoworld_yise_detector/config.py`

- 定义 `AppConfig`。
- 负责读取 JSON 配置、解析相对路径、补齐默认字段别名。
- 改配置 schema、改路径解析、改字段别名策略时优先看这里。
- 它和 `config/config.example.json` 强相关。

### `src/rocoworld_yise_detector/watcher.py`

- 负责日志文件读取。
- `scan_log_file()` 做一次性整文件读取。
- `tail_log_file()` 做轮询式追加读取，当前实现会每轮重读整个文件，再按行数差分。
- 改 watch 行为、处理日志截断、处理编码问题、优化大文件读取时优先看这里。
- 它和 `cli.py`、`samples/`、后续相关测试强相关。

### `src/rocoworld_yise_detector/parser.py`

- 负责从单行日志里抽取 `key=value` 字段。
- 基于 `field_aliases` 把原始字段映射为标准字段。
- 目前要求至少有 `monster_id` 或 `monster_name` 才认为是一条有效遭遇记录。
- 新增标准字段、修改日志匹配规则、放宽或收紧遇敌识别条件时优先看这里。
- 它和 `models.py`、`config.py`、`data/` 强相关。

### `src/rocoworld_yise_detector/database.py`

- 负责把 JSON 规则装载成 `MonsterVariant` 列表。
- 当前只做直接映射，不做验证、不做推导、不做多文件合并。
- 当规则库结构变化时，要同时看这里和 `detector.py`。

### `src/rocoworld_yise_detector/detector.py`

- 负责核心判定逻辑。
- 当前规则是：
  - 先用 `monster_id` / `monster_name` / `form` / `skin` 这些身份字段过滤候选
  - 再用 `match_fields` 逐项匹配
  - 若有多个候选，用“越具体分数越高”的规则选最佳匹配
- 修改误判逻辑、替换匹配策略、引入更复杂优先级时优先看这里。
- 它和 `models.py`、`database.py`、`data/` 强相关。

### `src/rocoworld_yise_detector/models.py`

- 共享数据结构定义。
- `EncounterRecord` 是解析后的日志行。
- `MonsterVariant` 是规则库中的一个可匹配变体。
- `DetectionResult` 是判定输出。
- 任何跨模块新增字段，通常都要先改这里，再回头改 `parser.py`、`detector.py`、`database.py`。

## 模块内部调用关系

### `scan`

`cli._scan()`
-> `load_config()`
-> `load_variants()`
-> `EncounterParser(...)`
-> `ShinyDetector(...)`
-> `scan_log_file()`
-> `_process_line()`
-> `parser.parse_line()`
-> `detector.detect()`
-> `_format_result()`

### `watch`

`cli._watch()`
-> 与 `scan` 相同的初始化
-> `tail_log_file()` 持续提供新行
-> `_process_line()`
-> `parser.parse_line()`
-> `detector.detect()`

### `parse-line`

`cli._parse_line()`
-> `load_config()`
-> `EncounterParser(...)`
-> `parser.parse_line()`
-> 直接输出结构化字段

## 上游输入与下游输出

### 上游输入

- 配置文件里的日志路径、编码、字段别名、过滤规则
- 数据目录里的规则 JSON
- 日志文件里的原始文本行

### 下游输出

- `scan` / `watch`：命令行文本结果，状态是 `SHINY`、`NORMAL`、`UNKNOWN`
- 若日志文件不存在：CLI 会输出深度日志前置条件提示和当前 `log_path`
- `parse-line`：结构化 JSON，主要用于调试字段提取

## 修改落点指引

### 如果要新增一个 CLI 命令

优先看：
- `src/rocoworld_yise_detector/cli.py`
- `src/rocoworld_yise_detector/__main__.py`
- `tests/` 里是否要补集成测试

### 如果要新增一个新的标准字段

优先看：
- `src/rocoworld_yise_detector/models.py`
- `src/rocoworld_yise_detector/config.py`
- `src/rocoworld_yise_detector/parser.py`
- 若字段参与判定，再看 `src/rocoworld_yise_detector/detector.py`
- 同时同步 `config/` 与 `data/` 中的样例

### 如果要修改异色判定策略

优先看：
- `src/rocoworld_yise_detector/detector.py`
- `src/rocoworld_yise_detector/models.py`
- `src/rocoworld_yise_detector/database.py`
- `data/monsters.sample.json` 或后续真实规则文件

### 如果要优化 watch 模式

优先看：
- `src/rocoworld_yise_detector/watcher.py`
- `src/rocoworld_yise_detector/cli.py`
- `samples/` 中是否需要新的复现样本
- `tests/` 中是否需要新的日志读取测试

### 如果要排查“解析不到字段”

优先看：
- 是否已开启深度日志
- `src/rocoworld_yise_detector/parser.py`
- `src/rocoworld_yise_detector/config.py`
- `config/config.example.json`
- `samples/` 里的相关样本

### 如果要排查“规则存在但还是 UNKNOWN”

优先看：
- `src/rocoworld_yise_detector/detector.py`
- `src/rocoworld_yise_detector/database.py`
- `data/` 里的规则数据
- `parse-line` 命令打印出的结构化结果

## 边界与约定

- `cli.py` 负责编排，不要把匹配逻辑堆在这里。
- `parser.py` 负责把文本变成结构，不要在这里做“这是不是异色”的判断。
- `detector.py` 只使用结构化输入，不应该自己读文件或感知命令行参数。
- `database.py` 当前默认数据已经是合法 JSON，不承担复杂校验职责。
- `watcher.py` 当前是最低可用实现，如果未来加入文件事件监听或偏移量缓存，仍应保持“只负责读取”的边界。

## 当前待确认

- 官方 FAQ 已确认客户端存在深度日志，但开启后的真实日志是否稳定采用 `key=value` 结构，当前还没确认。
- 遇敌记录是否一定包含 `monster_id` 或 `monster_name`，当前判断条件只是基于样例假设。
- `tail_log_file()` 在真实环境下是否需要处理日志轮转、文件锁、超大文件和重复读取性能问题，当前未验证。
- 判定逻辑是否需要支持更复杂的优先级、排他规则、正则匹配或多字段组合推导，当前还没有真实需求依据。
