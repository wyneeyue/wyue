---
name: "shudu-game"
description: "生成可交互的数独(九宫格)游戏HTML页面。支持4种难度(简单/中等/困难/地狱)和4种视觉主题(暗黑/明亮/赛博朋克/极简)。内置笔记模式、计时器、撤销、提示、错误检测等完整功能。输出独立HTML单文件，浏览器打开即玩。触发词：数独、九宫格、sudoku、shudu。"
---

# 数独游戏生成器

通过 `scripts/generate.py` 生成独立可交互的数独 HTML 游戏文件。

## 用法

```bash
# 默认：中等难度 + 暗黑主题
venv/bin/python3 .claude/skills/shudu-game/scripts/generate.py

# 自定义
venv/bin/python3 .claude/skills/shudu-game/scripts/generate.py \
  --difficulty hard --theme cyberpunk --title "赛博数独" --output output/my_sudoku.html
```

### 参数

| 参数 | 可选值 | 默认 |
|------|--------|------|
| `--difficulty` | easy, medium, hard, expert | medium |
| `--theme` | dark, light, cyberpunk, minimal | dark |
| `--title` | 任意字符串 | 九宫格数独 |
| `--output` | 文件路径 | output/sudoku_{diff}_{时间戳}.html |

### 难度

| 难度 | 空格数 | 说明 |
|------|--------|------|
| easy | 36/81 | 入门 |
| medium | 46/81 | 普通 |
| hard | 54/81 | 进阶 |
| expert | 60/81 | 高手 |

### 主题

- **dark**: 暗黑紫色渐变
- **light**: 明亮白底
- **cyberpunk**: 霓虹赛博风
- **minimal**: 极简黑白灰

## 游戏功能

- 数独谜题自动生成，4种难度
- 点击或键盘(1-9)输入，方向键移动
- 笔记模式(N键)标记候选数
- 撤销(Ctrl+Z)、擦除(Delete)、提示
- 错误检测标红，5次错误结束
- 计时器 + 通关统计弹窗
- 同行/列/宫高亮 + 相同数字高亮
- 移动端自适应

## 输出

生成的 HTML 是完全独立的单文件（无外部依赖），统一输出到 `output/` 目录。
