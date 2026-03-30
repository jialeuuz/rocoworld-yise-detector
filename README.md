# Rocoworld Yise Detector

《洛克王国：世界异色检测器》是一个面向本地日志解析的轻量工具骨架，目标是在遭遇精灵时，基于游戏日志中的稳定字段快速判断是否为异色。  
Rocoworld Yise Detector is a lightweight local log parsing scaffold that aims to determine whether an encountered creature is shiny by reading stable fields from game logs.

这个仓库当前提供的是第一版项目初始化结果：项目结构、可运行的最小样例、示例数据库、示例日志、基础测试，以及后续继续研究真实日志格式时需要的扩展点。  
This repository currently contains the first initialization pass: project structure, a runnable minimal example, sample database data, sample logs, basic tests, and extension points for future work with real logs.

## 项目背景 / Background

《洛克王国：世界》里的异色精灵具有明显的收藏价值，但玩家在实际遭遇中通常还是依赖肉眼判断，这种方式效率低，也容易漏判。  
Shiny creatures in Rocoworld have obvious collection value, but in actual encounters players still mostly rely on visual inspection, which is slow and easy to miss.

公开内容里常见的是图鉴整理、异色盘点和攻略视频，但缺少一个真正面向“遭遇当下快速判断异色”的本地辅助工具。  
Public content often focuses on encyclopedias, shiny showcases, and guide videos, but there is still a gap for a local tool that helps players decide quickly during the actual encounter.

## 项目目标 / Goal

本项目的目标很明确：在遭遇精灵时更快判断是否为异色，减少纯手动观察带来的漏判，并做成一个轻量、本地、实用的辅助工具。  
The goal is straightforward: identify shiny encounters faster, reduce misses caused by manual visual checks, and keep the tool lightweight, local, and practical.

之所以优先选择“日志解析”而不是“计算机视觉”，是因为如果日志中存在稳定字段，方案会更直接、更稳、更容易维护。  
The project prioritizes log parsing over computer vision because if stable fields exist in the logs, the solution will be more direct, more reliable, and easier to maintain.

## 项目边界 / Scope

- 只读取本地日志。  
- Read only local log files.
- 不读取内存。  
- Do not read process memory.
- 不注入、不 Hook、不抓包。  
- Do not inject, hook, or sniff network traffic.
- 不修改游戏数据。  
- Do not modify game data.
- 不做自动点击、自动战斗、自动刷图。  
- Do not automate clicking, combat, or grinding.

## 唯一方案 / Single Approach

本项目采用的唯一方案是：读取游戏本地日志文件，提取遭遇精灵信息，并与本地数据库比对，从而判断是否为异色。  
The only planned approach is to read the game's local log files, extract encounter data, and compare it against a local database to determine whether the encounter is shiny.

整体流程分为四步。  
The end-to-end flow is split into four steps.

1. 找到本地日志，确认日志路径、更新时机和文件格式。  
   Find the local logs and confirm the path, update behavior, and file format.
2. 提取遭遇字段，重点确认精灵名称、精灵 ID、形态、皮肤、颜色标记和其他能映射异色状态的字段。  
   Extract encounter fields, especially creature name, creature ID, form, skin, color markers, and any other fields that can map to shiny state.
3. 建立本地数据库，用于维护普通形态、异色形态、特殊变体以及日志字段到精灵信息的映射规则。  
   Build a local database that stores normal variants, shiny variants, special forms, and the mapping rules from log fields to creature records.
4. 监听日志变化并自动判定，在出现新的遭遇记录后输出“普通 / 异色 / 未知”。  
   Watch log changes and detect automatically, then output "normal / shiny / unknown" when a new encounter record appears.

## 当前仓库内容 / What This Repository Includes

这个初始化版本先提供一套 Python 骨架，围绕“日志监听、行解析、规则匹配、命令行输出”拆分模块，方便后续替换成真实日志规则。  
This initialization provides a Python scaffold organized around log watching, line parsing, rule matching, and CLI output so it can later be adapted to real log rules.

仓库里附带的是演示数据，不代表真实游戏日志字段，也不代表已经完成逆向确认；它们只是为了让项目从第一天起就是可运行、可测试、可扩展的。  
The repository ships with demo data only; it does not represent confirmed real game log fields or finished reverse engineering. It exists so the project is runnable, testable, and extensible from day one.

## 目录结构 / Project Layout

- `src/rocoworld_yise_detector/`：核心源码，包含配置加载、日志监听、解析与判定。  
- `src/rocoworld_yise_detector/`: core source code for config loading, log watching, parsing, and detection.
- `config/config.example.json`：示例配置文件。  
- `config/config.example.json`: sample configuration file.
- `data/monsters.sample.json`：示例精灵数据库。  
- `data/monsters.sample.json`: sample local creature database.
- `samples/sample_encounter.log`：示例日志。  
- `samples/sample_encounter.log`: sample encounter log.
- `tests/`：基础单元测试。  
- `tests/`: basic unit tests.

## 快速开始 / Quick Start

1. 创建虚拟环境并安装项目。  
   Create a virtual environment and install the project.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -e .
   ```

2. 复制示例配置并按实际环境修改日志路径、编码和数据库路径。  
   Copy the sample configuration and update the log path, encodings, and database path for your local environment.

   ```powershell
   Copy-Item config\config.example.json config\config.local.json
   ```

3. 先用示例日志跑一次扫描，确认骨架工作正常。  
   Run a one-off scan against the sample log to confirm the scaffold works.

   ```powershell
   python -m rocoworld_yise_detector scan --config config/config.example.json
   ```

4. 如果已经拿到真实日志路径，再启动监听模式。  
   Once the real log path is known, start watch mode.

   ```powershell
   python -m rocoworld_yise_detector watch --config config/config.local.json
   ```

## 当前输出约定 / Current Output Contract

当前命令行输出只有三种状态：`SHINY`、`NORMAL`、`UNKNOWN`。  
The current CLI only emits three statuses: `SHINY`, `NORMAL`, and `UNKNOWN`.

`SHINY` 表示日志字段命中了本地数据库中的异色规则，`NORMAL` 表示命中了普通规则，`UNKNOWN` 表示当前日志字段不足以完成判定或数据库中还没有对应规则。  
`SHINY` means the log fields matched a shiny rule in the local database, `NORMAL` means a normal rule matched, and `UNKNOWN` means the available fields are not sufficient yet or the database does not have a matching rule.

## 下一步研究重点 / Immediate Research Priorities

最关键的工作不是继续堆功能，而是尽快拿到真实日志样本，确认到底有没有稳定字段可以唯一映射异色状态。  
The most important next step is not adding more features, but collecting real log samples and proving whether stable fields exist that can uniquely map to shiny state.

如果真实日志里没有可靠字段，这个项目就应该尽早调整策略，而不是在错误前提上继续投入。  
If the real logs do not contain reliable fields, the project should pivot early instead of continuing on a flawed assumption.

## TODO

- [ ] 采集真实游戏日志样本，确认日志目录、文件轮转方式和编码。  
- [ ] Collect real game log samples and confirm the log directory, rotation behavior, and encoding.
- [ ] 找出稳定的遭遇事件标记，确认哪些行真正代表“遇敌”。  
- [ ] Identify the stable encounter event marker and confirm which lines actually represent encounters.
- [ ] 验证精灵名称、精灵 ID、形态、皮肤、颜色等字段是否稳定存在。  
- [ ] Verify whether creature name, creature ID, form, skin, color, and similar fields are consistently present.
- [ ] 确认是否存在能直接表示异色状态的字段，或者只能通过组合字段间接判断。  
- [ ] Confirm whether there is a direct shiny flag or whether shiny state must be inferred from combined fields.
- [ ] 建立真实精灵数据库和映射规则，而不是继续使用演示数据。  
- [ ] Build the real creature database and rule set instead of relying on demo data.
- [ ] 增加日志样本回放工具，方便批量验证规则。  
- [ ] Add a log replay tool to validate rules against batches of samples.
- [ ] 增加更严格的测试样例，覆盖日志轮转、编码切换和未知字段。  
- [ ] Add stricter test cases covering log rotation, encoding changes, and unknown fields.
- [ ] 评估是否需要桌面通知、声音提醒或极简 GUI。  
- [ ] Evaluate whether desktop notifications, sound alerts, or a minimal GUI are needed.

## 声明 / Disclaimer

本仓库与游戏官方无关，仅用于本地日志研究与个人辅助用途。  
This repository is not affiliated with the game publisher and is intended only for local log research and personal helper use.

请在遵守当地法律、平台条款以及游戏规则的前提下使用。  
Use it only in compliance with local law, platform terms, and game rules.

