# readme_for_ai

## 项目定位

这是一个 Python 命令行工具骨架，目标是通过读取本地日志来判断《洛克王国：世界》遭遇精灵是否为异色。

当前仓库还处在“可运行的研究脚手架”阶段，不是已经完成真实日志适配的成品。现有 `config/`、`data/`、`samples/` 中的内容主要用于跑通流程和承载后续真实规则。

这个文档只保留稳定总览，不承载会持续膨胀的实现细节。实现细节放到子目录 `readme_for_ai.md`。

基于官方 FAQ 已经可以确认一件事：客户端存在可手动开启的“深度日志”，因此后续真实适配的前置条件不是“游戏是否有日志”，而是“用户是否已经开启深度日志，以及开启后实际产出了什么文件”。

## 技术栈

- Python 3.11+
- 纯标准库实现，当前没有运行时第三方依赖
- 打包方式是 `setuptools`，入口命令在 `pyproject.toml`
- 测试框架当前是 `unittest`

## 顶层目录概览

- `src/rocoworld_yise_detector/`
  运行时核心代码。入口、配置解析、日志读取、日志解析、规则判定都在这里。
- `config/`
  运行配置模板。定义日志路径、数据库路径、编码、行过滤条件和字段别名。
- `data/`
  本地规则数据库样例。当前是演示用 JSON，不是已确认的真实游戏数据。
- `samples/`
  示例日志与后续可能扩展的日志样本目录。适合放人工确认过的 fixture。
- `tests/`
  单元测试。当前只覆盖解析与判定层。
- `README.md`
  面向用户的项目说明，不是 AI 导航入口。应优先保留通知、前置条件、安装、配置、运行、输出和排障，不要把内部架构、研究计划、AI 导航信息堆进去。
- `test.md`
  当前是本地临时文件，不属于项目结构的一部分。除非用户明确要求，否则不要把它当成实现依据。

## 核心模块划分

- CLI 编排层
  负责命令分发、组装配置、构造解析器与判定器、打印输出。核心文件是 `src/rocoworld_yise_detector/cli.py`。
- 配置层
  负责读取 JSON 配置、解析相对路径、准备字段别名。核心文件是 `src/rocoworld_yise_detector/config.py`。
- 日志读取层
  负责整文件扫描与轮询式 tail。核心文件是 `src/rocoworld_yise_detector/watcher.py`。
- 日志解析层
  负责从原始行提取 key=value，对齐到标准字段。核心文件是 `src/rocoworld_yise_detector/parser.py`。
- 规则数据库层
  负责把 JSON 规则装载成内存对象。核心文件是 `src/rocoworld_yise_detector/database.py`。
- 判定层
  负责基于遭遇字段与规则库做 `SHINY / NORMAL / UNKNOWN` 判定。核心文件是 `src/rocoworld_yise_detector/detector.py`。
- 模型层
  负责共享数据结构。核心文件是 `src/rocoworld_yise_detector/models.py`。

## 主流程 / 主调用链路

### 命令入口

`python -m rocoworld_yise_detector ...`
-> `src/rocoworld_yise_detector/__main__.py`
-> `src/rocoworld_yise_detector/cli.py:main()`

### `scan` 调用链

`cli._scan()`
-> `load_config()`
-> `load_variants()`
-> `EncounterParser(...)`
-> `ShinyDetector(...)`
-> `scan_log_file()`
-> `parser.parse_line()`
-> `detector.detect()`
-> `cli._format_result()`

### `watch` 调用链

`cli._watch()`
-> 与 `scan` 相同的初始化
-> `tail_log_file()` 持续产生日志行
-> `parser.parse_line()`
-> `detector.detect()`
-> `cli._format_result()`

### `parse-line` 调用链

`cli._parse_line()`
-> `load_config()`
-> `EncounterParser(...)`
-> `parser.parse_line()`
-> 直接输出结构化 JSON，不经过判定器

### 总体数据流

配置 JSON
-> `AppConfig`
-> 决定日志路径、数据库路径、编码和字段别名

规则 JSON
-> `MonsterVariant` 列表
-> 作为判定器输入

日志文本行
-> `EncounterRecord`
-> `DetectionResult`
-> CLI 文本输出

## 全局约定

- 所有运行时源码都放在 `src/rocoworld_yise_detector/`，不要把核心逻辑散落到顶层目录。
- 配置负责“运行参数”，数据文件负责“判定规则”，不要把二者混在一个 JSON 里。
- `parser.py` 只做行过滤、字段提取和字段标准化，不负责异色判定。
- `detector.py` 只做规则匹配，不负责读文件、打印、组命令行参数。
- `watcher.py` 只负责日志读取，不负责解析和业务判断。
- `samples/` 里的日志样本默认只是 fixture，不自动视为真实游戏格式。
- 真实游戏日志格式、真实字段语义、真实数据库结构一旦确认，要优先更新对应 AI 文档，让文档反映代码和事实。

## 子目录 AI 文档索引

- `src/rocoworld_yise_detector/readme_for_ai.md`
  看运行时代码时先读这个。适用于新增命令、改解析、改判定、改日志监听、查主链路。
- `config/readme_for_ai.md`
  改配置结构、字段别名、路径解析、编码策略时看这里。
- `data/readme_for_ai.md`
  改规则库结构、补真实精灵规则、排查规则误判时看这里。
- `samples/readme_for_ai.md`
  管理日志样本、补 fixture、做手工回放或复现样本时看这里。
- `tests/readme_for_ai.md`
  补测试、找当前覆盖缺口、定位应该新增哪类测试时看这里。

## 修改需求时的导航指引

- 新增 CLI 子命令
  先看 `src/rocoworld_yise_detector/readme_for_ai.md`，重点是 `cli.py`，其次看是否需要同步测试。
- 新增一个新的标准字段，比如 `rarity_code`
  先看 `src/rocoworld_yise_detector/readme_for_ai.md`，通常会同时改 `models.py`、`config.py`、`parser.py`，如果字段参与判定，还要改 `detector.py` 和 `data/` 里的规则 JSON。
- 修改日志路径、编码、别名或配置加载方式
  先看 `config/readme_for_ai.md`，然后回到源码文档中的 `config.py` 和 `cli.py`。
- 修改用户可见的使用方式、前置条件、已知限制或最新进展
  先同步 `README.md` 顶部的通知区，再决定是否需要更新本文件或子目录 AI 文档。
- 排查“日志读到了但没有输出”
  先确认是否已开启深度日志，再看 `src/rocoworld_yise_detector/readme_for_ai.md` 中的 `watcher.py`、`parser.py`、`cli.py`，最后结合 `samples/readme_for_ai.md` 和 `tests/readme_for_ai.md`。
- 排查“输出是 UNKNOWN 或误判”
  先看 `data/readme_for_ai.md`，确认规则是否缺失；如果规则存在，再看源码文档里的 `parser.py` 和 `detector.py`。
- 想替换日志监听实现，比如从轮询改成更高效的文件事件
  先看 `src/rocoworld_yise_detector/readme_for_ai.md`，重点是 `watcher.py` 和 `cli.py`，再补测试。
- 想把项目从脚手架推进到真实可用版本
  先看 `data/readme_for_ai.md` 和 `samples/readme_for_ai.md`，因为当前最大的阻塞不是代码结构，而是真实日志与规则尚未确认。

## 维护规则

1. 新增模块或目录职责明显变化时，同步更新对应目录下的 `readme_for_ai.md`。
2. 当某个部分内容膨胀到不适合继续放在根文档时，拆分新的子目录文档，并在根文档登记索引。
3. 根文档只保留稳定总览，不承载持续膨胀的实现细节。
4. 如果实现与文档不一致，优先修正文档，使文档反映真实代码结构。
5. 文档更新目标是让下一个 AI 少搜、少猜、少漏看文件。

## 当前待确认

- 官方 FAQ 已确认客户端存在深度日志；当前待确认的是深度日志开启后的真实落盘路径、编码、轮转方式和文件命名。
- 真实遭遇事件在日志中的稳定标记尚未确认，当前 `line_filters` 只是演示值。
- 是否存在能直接表示异色状态的字段尚未确认，当前规则库只是样例。
- 当前 `watcher.py` 采用整文件轮询读取，真实大日志下的性能与重复读取问题尚未验证。
- 当前没有 GUI、通知、持久化状态、样本回放工具，这些都还不是既定架构。

以上待确认信息一旦落地：
- 日志样本相关更新到 `samples/readme_for_ai.md`
- 规则结构相关更新到 `data/readme_for_ai.md`
- 运行时实现变化更新到 `src/rocoworld_yise_detector/readme_for_ai.md`
- 若变化影响全局导航，再同步更新本文件
