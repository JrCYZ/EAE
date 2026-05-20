# Mini 3D Sandbox Demo（Ursina 版）

这是一个可运行的 3D 沙盒最小原型（第一人称 + 可放置/删除方块）。

## Windows 安装与运行（请分两行执行）
```bash
py -m pip install ursina
py sandbox_game_3d.py
```

> 注意：不要把两条命令写在同一行，也不要加 `+`。

## 常见报错排查
### 1) `Invalid requirement: '+'`
你把 `+` 当成了命令的一部分。请改为**逐行**执行上面的两条命令。

### 2) `No module named ursina`
说明安装还没成功，请重新执行：
```bash
py -m pip install ursina
```

### 3) pip 升级提示
`[notice] A new release of pip is available` 只是提示，不是错误，不影响运行。

## 操作方式
- `W/A/S/D`：移动
- 鼠标：自由视角
- 左键：放置方块
- 右键：删除方块
- `1~5`：切换方块类型
- `ESC`：释放鼠标

## 资产与模型接入（你后续的计划）
- 你可以在仓库中放模型资产文件夹（例如 `assets/models/`、`assets/textures/`）。
- 后续可以把模型导入到 3D 场景中（常见格式如 `.obj` / `.glb`）。
- 也可以先做“资产检查脚本”（检查文件是否存在、命名是否规范、贴图是否齐全），再自动加载到场景。

## 下一步可升级
- 区块（Chunk）加载
- 存档/读档
- 背包系统
- 光照和昼夜循环
- 模型资产自动检查与批量挂载
