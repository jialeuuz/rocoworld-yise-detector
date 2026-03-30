# readme_for_ai

## 目录职责

这个目录放日志样本和后续用于复现问题的 fixture。

它的用途是：
- 给 `config/config.example.json` 提供默认可运行输入
- 给手工调试 `scan` / `watch` / `parse-line` 提供样本
- 未来承载真实日志脱敏样本、误判复现样本、边界条件样本

## 在整体项目中的位置

这是“输入样本层”，不是规则层，也不是实现层。

这里的文件通常会被：
- 示例配置引用
- 手工命令调试使用
- 后续测试用例或回放工具使用

## 关键路径

### `samples/sample_encounter.log`

- 当前唯一样例日志。
- 用于演示 `ENCOUNTER` 行如何被解析和判定。
- 它是人工构造的演示输入，不是已确认的真实游戏日志格式。

## 修改落点指引

### 如果要新增复现样本

优先做法：
- 在本目录新增独立样本文件，而不是不断覆盖现有样例
- 在文件名里体现用途，比如 `real_log_redacted_xxx.log`、`watch_rotation_case.log`
- 若样本对应某个 bug 或需求，顺手在 `tests/` 或相关目录文档里登记

### 如果要排查解析问题

优先看：
- 本目录样本是否真的包含目标字段
- `src/rocoworld_yise_detector/parser.py`
- `config/config.example.json` 中的 `line_filters` 和 `field_aliases`

### 如果要排查 watch 模式问题

优先看：
- 是否需要构造新的追加写入样本
- `src/rocoworld_yise_detector/watcher.py`
- `tests/` 是否已有对应场景覆盖

## 边界与约定

- 样本默认只作为 fixture，不自动等同于真实协议。
- 如果引入真实日志样本，默认前提是采集时已经开启深度日志；否则样本对真实适配的参考价值很低。
- 如果引入真实日志样本，优先做脱敏和注释，避免把无关信息直接提交。
- 若未来样本数量上升，可以按用途拆子目录，比如 `synthetic/`、`real_redacted/`、`regressions/`。

## 当前待确认

- 官方 FAQ 已确认客户端存在深度日志；当前仍待确认深度日志是否稳定采用逐行追加格式。
- 真实日志编码、时间戳格式、字段分隔方式目前还未确认。
- 未来是否需要专门的“样本回放工具”，当前仓库里还没有实现。
