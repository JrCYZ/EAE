# Mini 3D Sandbox Demo（Ursina 版）

这是一个可运行的 3D 沙盒最小原型（第一人称 + 可放置/删除方块）。

## Windows 安装与运行
```bash
py -m pip install ursina
py sandbox_game_3d.py
```

## 操作方式
- `W/A/S/D`：移动
- 鼠标：自由视角
- 左键：放置方块
- 右键：删除方块
- `1~5`：切换方块类型
- `ESC`：释放鼠标

## 说明
- 这是可玩 MVP（最小可行原型），用于验证 3D 交互闭环。
- 下一步可加：存档、背包、区块加载、光照、地形噪声。
