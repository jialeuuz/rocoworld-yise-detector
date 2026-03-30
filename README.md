# Rocoworld Yise Detector

A local log-based helper that tries to tell whether a Rocoworld encounter is shiny.

《洛克王国：世界异色检测器》是一个本地日志辅助工具，目标是在遭遇时尽快判断精灵是否为异色。

## Notice

- `2026-03-30`: Real game usage requires enabling deep logging (`深度日志`) first.
- `2026-03-30`: The current repository is still a runnable scaffold. Bundled configs, rules, and logs are demo data, not confirmed real-game data.

- `2026-03-30`：如果要接真实游戏日志，必须先开启`深度日志`。
- `2026-03-30`：当前仓库仍然是可运行的研究脚手架；仓库自带的配置、规则和日志样本都是演示数据，不是已经确认的真实游戏数据。

## What It Does

- Reads local log files.
- Parses encounter-related lines.
- Matches parsed fields against a local rule database.
- Prints `SHINY`, `NORMAL`, or `UNKNOWN`.

- 读取本地日志文件。
- 解析遭遇相关日志行。
- 将解析结果与本地规则库匹配。
- 输出 `SHINY`、`NORMAL` 或 `UNKNOWN`。

## What It Does Not Do

- It does not read memory.
- It does not inject, hook, or sniff packets.
- It does not click for you, fight for you, or automate grinding.

- 不读取内存。
- 不注入、不 Hook、不抓包。
- 不自动点击、不自动战斗、不自动刷图。

## Prerequisites

- Python `3.11+`
- For real game logs, enable deep logging in the game client first.

- Python `3.11+`
- 如果要使用真实游戏日志，先在客户端里开启`深度日志`。

Known entry points from the official FAQ:

- In game: `Compass -> Settings -> User -> Enable deep logging`
- Login screen: `Repair Tool -> Enable deep logging`

官方 FAQ 里已确认的入口：

- 游戏内：`罗盘 -> 设置 -> 用户 -> 开启深度日志`
- 登录界面：`修复工具 -> 开启深度日志`

The client also exposes a "submit/upload logs" action, but this project only depends on local log files.

客户端里还有“上报日志”入口，但本项目只依赖本地落盘日志，不依赖上传流程。

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Configure

1. Copy the sample config:

   ```powershell
   Copy-Item config\config.example.json config\config.local.json
   ```

2. Edit `config/config.local.json`.
3. Set `log_path` to your real deep-log file path.
4. Adjust `encodings` if your local logs are not `utf-8` or `gbk`.
5. Keep `database_path` pointed at the rule file you want to use.

1. 复制示例配置：

   ```powershell
   Copy-Item config\config.example.json config\config.local.json
   ```

2. 修改 `config/config.local.json`。
3. 把 `log_path` 指向你的真实深度日志文件。
4. 如果本地日志不是 `utf-8` 或 `gbk`，同步调整 `encodings`。
5. 让 `database_path` 指向你要使用的规则文件。

## Usage

Run a one-time scan against the sample file:

对示例日志执行一次扫描：

```powershell
python -m rocoworld_yise_detector scan --config config/config.example.json
```

Watch a real log file continuously:

持续监听真实日志文件：

```powershell
python -m rocoworld_yise_detector watch --config config/config.local.json
```

Parse one raw log line for debugging:

调试单行日志的解析结果：

```powershell
python -m rocoworld_yise_detector parse-line --config config/config.local.json --line "ENCOUNTER monster_id=1001 monster_name=火花 form=default palette=crimson"
```

## Output

- `SHINY`: matched a shiny rule.
- `NORMAL`: matched a normal rule.
- `UNKNOWN`: not enough fields were parsed yet, or no rule matched.

- `SHINY`：命中了异色规则。
- `NORMAL`：命中了普通规则。
- `UNKNOWN`：当前字段还不足以判断，或者规则库里没有命中的规则。

## Troubleshooting

- `Log file not found`
  Check whether deep logging is enabled and whether `log_path` points to the generated file.
- No output in `watch`
  Check whether the game is really writing to that file, and whether your `line_filters` are too strict.
- Too many `UNKNOWN`
  The parser may be missing fields, or the rule database may not cover that encounter yet.

- `Log file not found`
  先检查是否已经开启`深度日志`，再检查 `log_path` 是否指向真实生成的日志文件。
- `watch` 没输出
  先确认游戏是否真的在写这个文件，再检查 `line_filters` 是否设得太严。
- `UNKNOWN` 太多
  可能是解析层没抓到关键字段，也可能是规则库还没覆盖到该遭遇。

## Current Limitations

- This repository still ships with synthetic sample data.
- Real encounter fields, log paths, and rule coverage are still being verified.
- There is currently no GUI, notification system, or replay tool.

- 当前仓库仍然只附带人工构造的演示数据。
- 真实遭遇字段、真实日志路径和规则覆盖还在确认中。
- 目前还没有 GUI、通知系统或样本回放工具。

## For Developers

Developer-facing architecture and maintenance notes live in `readme_for_ai.md`.

面向开发和维护的架构说明放在 `readme_for_ai.md`。

