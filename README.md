# EAE - 个人记账工具（学习版）

这是一个给 Codex 新手的可运行项目：命令行记账工具（CLI）。

## 当前功能（V0）
- 新增收入/支出记录
- 查看所有记录
- 查看总收入/总支出/结余

## 运行环境
- Python 3.10+

## 使用方式
```bash
python3 app.py add income 12000 工资 --note "5月工资"
python3 app.py add expense 35.8 餐饮 --note "午饭"
python3 app.py list
python3 app.py summary
```

## 数据存储
- 默认写入 `data/ledger.json`

## 下一步可扩展
- 按月份筛选
- 按分类统计
- 导出 CSV
- 增加单元测试
