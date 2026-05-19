# EAE - 个人记账工具（学习版）

这是一个给 Codex 新手的可运行项目：命令行记账工具（CLI）。

## 当前功能（V1）
- 新增收入/支出记录（自动生成 ID）
- 查看全部记录（支持按月份过滤）
- 查看总收入/总支出/结余（支持按月份过滤）
- 查看分类支出统计
- 按 ID 删除记录
- 运行阶段检查（库存/合规基础项）

## 运行环境
- Python 3.10+

## 使用方式
```bash
python app.py add income 12000 工资 --note "5月工资"
python app.py add expense 35.8 餐饮 --note "午饭"
python app.py list
python app.py list --month 2026-05
python app.py summary
python app.py summary --month 2026-05
python app.py category --month 2026-05
python app.py delete 2
python app.py health
```

## 数据存储
- 默认写入 `data/ledger.json`

## 每个阶段都要做的检查（建议）
1. 功能检查：`add/list/summary/category/delete` 至少跑一遍
2. 数据检查：打开 `data/ledger.json` 看字段是否完整（id/kind/amount/category/entry_date/note）
3. 文档检查：README 命令能复制即用
4. 版本检查：`git status` 干净再进入下个阶段

## 下一步可扩展
- 导出 CSV
- 预算阈值提醒
- 单元测试
- Web 版本（Flask/FastAPI）
- AI 自然语言记账

## 关于你提到的“双线程”
你可以并行两条线：
- 主线：继续做记账产品升级
- 支线：我帮你搭一个可试玩小游戏原型（例如 Godot 第一人称移动+交互）
