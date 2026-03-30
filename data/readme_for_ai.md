# readme_for_ai

## 目录职责

这个目录放判定所需的本地规则数据。

当前这里只有演示数据，但未来如果项目进入真实可用阶段，这里会成为高频更新目录，因为真实精灵、形态、异色规则都应主要落在这里，而不是散落到源码里。

## 在整体项目中的位置

`data/` 中的 JSON 会被 `src/rocoworld_yise_detector/database.py` 读取，转成 `MonsterVariant`，再被 `src/rocoworld_yise_detector/detector.py` 使用。

换句话说，这个目录提供“事实与规则”，源码层提供“装载与匹配逻辑”。

## 关键路径

### `data/monsters.sample.json`

- 当前唯一规则样例文件。
- 作用是演示规则库结构，不代表真实游戏已确认字段。
- 要改规则 schema 时，必须同时改：
  - `src/rocoworld_yise_detector/models.py`
  - `src/rocoworld_yise_detector/database.py`
  - `src/rocoworld_yise_detector/detector.py`

## 当前规则结构

当前 JSON 以 `variants` 数组为主，每个元素对应一个 `MonsterVariant`。

关键字段含义：
- `monster_id`
  精灵身份字段之一。
- `monster_name`
  精灵身份字段之一。
- `form`
  形态字段。
- `skin`
  外观字段。
- `label`
  方便输出和人工识别的规则名称。
- `is_shiny`
  命中该规则后返回 `SHINY` 还是 `NORMAL`。
- `match_fields`
  进一步判定这个变体所需满足的附加字段集合。

## 规则生效方式

当前判定器的工作方式是：
- 先使用 `monster_id` / `monster_name` / `form` / `skin` 过滤候选规则
- 再检查 `match_fields` 是否全部命中
- 如果命中多个规则，优先选择更具体的规则

因此，排查误判时不要只看 `is_shiny`，还要看：
- 身份字段是否过宽或过窄
- `match_fields` 是否覆盖了真正能区分普通和异色的字段
- 是否存在多个规则同时匹配但优先级不合理

## 修改落点指引

### 如果要补充新的精灵规则

优先看：
- `data/monsters.sample.json` 或未来真实规则文件
- `src/rocoworld_yise_detector/detector.py`
- `src/rocoworld_yise_detector/database.py`

### 如果要把演示数据替换成真实数据库

优先看：
- 本目录的数据文件
- `config/config.example.json` 中的 `database_path`
- `src/rocoworld_yise_detector/database.py`
- `tests/` 中是否需要补基于真实字段的测试

### 如果要排查“日志解析正常，但判定不对”

优先检查：
- 本目录规则是否缺失
- `match_fields` 是否与日志里的真实键名和真实取值一致
- `monster_id` / `monster_name` / `form` / `skin` 是否写错或过于模糊
- 若规则数据没问题，再回到 `detector.py` 看匹配逻辑

## 边界与约定

- 数据文件负责描述规则，不负责写流程逻辑。
- 不要把“路径、编码、轮询时间”之类的运行配置混进这里。
- 若未来规则量变大，优先考虑拆分多个数据文件，并在根目录文档登记，而不是继续把所有内容堆在单文件里。

## 当前待确认

- 真实游戏日志里能稳定拿到哪些字段，目前还未确认。
- 真实异色状态是直接由某个字段标记，还是需要多个字段联合推断，目前还未确认。
- 未来规则库是否只需要 JSON，还是需要引入更强的索引或校验层，目前还未确认。

