---
name: pipeline-guide
description: MAA_SnowBreak Pipeline JSON 编写指南。基于 MaaFramework Pipeline 协议，提供节点命名、识别算法、动作类型、流程控制等编码规范；自定义识别/动作以 Python（agent/）为准。在编写、修改或审查 Pipeline JSON、设计节点流程、使用 TemplateMatch/OCR/Custom 识别或 Click/Swipe 动作时使用。
---

# MAA_SnowBreak Pipeline 编写指南

## 核心原则

1. **状态驱动**：遵循「识别 → 操作 → 识别」循环。每次操作必须基于识别结果，禁止假设操作后画面状态。
2. **高命中率**：扩充 `next` 列表，覆盖当前操作后所有可能画面，力争一次截图命中。
3. **避免硬延迟**：尽量不用 `pre_delay` / `post_delay` / `timeout`，优先通过增加中间识别节点解决；只在必须等画面稳定时才用 `pre_wait_freezes` / `post_wait_freezes`。协议默认存在隐式等待（如 `rate_limit`、`pre_delay`/`post_delay`）；若某节点确实不需要这些等待，应在 JSON 中显式设为 `0`，避免省略字段带来的默认延时。
4. **720p 基准**：所有坐标、ROI、图片必须基于 **1280×720**。
5. **格式化**：JSON/JSONC 保持可读缩进（可与仓库内现有 pipeline 文件风格一致）。

## 节点命名

- 使用 **PascalCase**，同一任务内节点以任务名或模块名为前缀。
- 内部实现节点以 `__` 开头（如 `__ScenePrivateXXX`），不对外暴露。
- 示例：`ResellMain`、`DailyProtocolPassInMenu`。

## Pipeline v2 格式（推荐）

使用 v2 格式时，`recognition` 和 `action` 放入二级字典：

```jsonc
{
    "MyNode": {
        "recognition": {
            "type": "TemplateMatch",
            "param": {
                "template": "MyTask/button.png",
                "roi": [100, 200, 300, 100],
                "threshold": 0.7,
            },
        },
        "action": {
            "type": "Click",
        },
        "next": ["NextNode"],
    },
}
```

## 常用识别算法

### TemplateMatch（找图）

```jsonc
"recognition": {
    "type": "TemplateMatch",
    "param": {
        "template": "path/to/image.png",  // 相对 resource 下 image 目录
        "roi": [x, y, w, h],              // 720p 坐标，缩小搜索范围
        "threshold": 0.7                   // 默认 0.7，按需调整
    }
}
```

- 图片应从无损原图裁剪并缩放到 720p。
- `green_mask: true` 可遮蔽不参与匹配的区域（用 RGB(0,255,0) 涂色）。

### OCR（文字识别）

```jsonc
"recognition": {
    "type": "OCR",
    "param": {
        "roi": [x, y, w, h],
        "expected": ["完整文本"]
    }
}
```

- `expected` 尽量写完整、稳定出现的文本；需正则或片段匹配时按协议与资源实际情况书写。

### ColorMatch（找色）

```jsonc
"recognition": {
    "type": "ColorMatch",
    "param": {
        "roi": [x, y, w, h],
        "method": 40,                     // HSV 空间（推荐）
        "lower": [h_low, s_low, v_low],
        "upper": [h_high, s_high, v_high],
        "count": 100
    }
}
```

- 优先使用 HSV（method: 40）或灰度（method: 6），避免 RGB 直接匹配（不同显卡渲染差异）。

### And / Or（组合识别）

```jsonc
// And：全部子识别都成功才算命中
"recognition": {
    "type": "And",
    "param": {
        "all_of": ["NodeA", "NodeB"],
        "box_index": 0
    }
}

// Or：任一子识别成功即命中
"recognition": {
    "type": "Or",
    "param": {
        "any_of": ["NodeA", "NodeB"]
    }
}
```

### Custom（自定义识别 · Python）

本仓库自定义识别走 **Python**，不使用其他语言实现的识别服务。

1. **`custom.json`（配置文件方案）**：`maapicli` 等入口会按 `agent/custom.json` 动态加载模块；条目包含 `type: "recognition"`、`class`、`file_path`。
2. **`Agent_file.py`（Agent 启动）**：通过 `agent/main.py` 启动 Agent 时，需在 **`Agent_file.py`** 中用 `@AgentServer.custom_recognition("名称")` 包装实现类，名称应与 Pipeline、`custom.json` **一致**。

实现类需继承 `maa.custom_recognition.CustomRecognition`（见 `agent/Recognition/` 下示例）。

无额外参数时可直接写注册名：

```jsonc
"recognition": {
    "type": "Custom",
    "param": {
        "custom_recognition": "CheckResolution"
    }
}
```

带参数时由具体类约定（例如 `LOp` 在实现中对 `custom_recognition_param` 做 `json.loads`，需传入合法 JSON 字符串）。新增识别器：实现类 → 更新 `custom.json` → 如需 Agent 路径则同步 `Agent_file.py` → 在 Pipeline 中引用注册名。

## 常用动作类型

| 动作                   | 用途            | 关键字段                               |
| ---------------------- | --------------- | -------------------------------------- |
| `Click`                | 点击            | `target`, `target_offset`              |
| `LongPress`            | 长按            | `target`, `duration`                   |
| `Swipe`                | 滑动            | `begin`, `end`, `duration`             |
| `Scroll`               | 滚轮（仅 Win32 等） | `target`, `dx`, `dy`               |
| `ClickKey`             | 按键            | `key`（虚拟键码）                      |
| `InputText`            | 输入文本        | `input_text`                           |
| `StartApp` / `StopApp` | 启停应用        | `package`                              |
| `StopTask`             | 停止当前任务链  | 无                                     |
| `Custom`               | 自定义动作（Python） | `custom_action`, `custom_action_param` |
| `DoNothing`            | 不执行（默认）  | 无                                     |

`target` 支持：`true`（当前识别结果）、节点名字符串、`[x, y]`、`[x, y, w, h]`。

### Custom 动作（Python）

与识别类似：`custom.json` 注册 +（Agent 路径下）**`Agent_file.py`** 中 `@AgentServer.custom_action("名称")`。`custom_action` 填写注册键名。示例（节选自本仓库 `General.jsonc`）：

```jsonc
"action": {
    "type": "Custom",
    "param": {
        "custom_action": "ScreenShot",
        "custom_action_param": {
            "type": "CUSTOM"
        }
    }
}
```

## 流程控制

### next 列表

按序识别，首个命中的节点执行其 `action` 后成为当前节点。`next` 为空或全部超时则任务结束。

### on_error

识别超时或动作失败时执行的节点列表。

### Node Attributes（节点属性）

**`[JumpBack]`**：命中后执行完该节点链，自动返回父节点继续识别 `next`。适用于处理弹窗、加载等中断场景。

```jsonc
"next": [
    "BusinessNode",
    "[JumpBack]HandlePopup",
    "[JumpBack]WaitLoading"
]
```

**`[Anchor]`**：动态引用锚点，运行时解析为最后设置该锚点的节点。

### 等待画面稳定

只在必须时使用 `pre_wait_freezes` / `post_wait_freezes` 等待画面静止，不要为了「执行稳定」而滥用固定延迟：

```jsonc
"post_wait_freezes": {
    "time": 200,
    "target": [0, 0, 0, 0]  // 全屏
}
```

避免对同一按钮重复点击——第二次点击可能作用于下一界面的其他元素。

### max_hit

限制节点最大命中次数，超过后自动跳过：

```jsonc
"max_hit": 3
```

## 可复用逻辑与本仓库资源

- 编写前先浏览 **`resource/base/pipeline/`** 下已有任务 JSONC，复用通用片段（如启动、关闭应用、通用 OCR 按钮名等），避免重复造轮子。
- 已注册的自定义能力以 **`agent/custom.json`** 与 **`agent/Agent_file.py`** 为准（二者名称需对齐），Pipeline 中仅使用这些注册名。

## 典型模式

### 带弹窗处理的任务入口

```jsonc
{
    "MyTaskEntry": {
        "next": [
            "MyTaskMainStep",
            "[JumpBack]SomeDialogConfirm",
            "[JumpBack]SomeWaitLoading",
        ],
    },
}
```

（具体节点名以本仓库对应 pipeline 文件为准。）

### 确认后验证画面变化

```jsonc
{
    "ClickConfirm": {
        "recognition": { "type": "TemplateMatch", "param": { "template": "confirm.png", "roi": [...] } },
        "action": { "type": "Click" },
        "post_wait_freezes": { "time": 200, "target": [0, 0, 0, 0] },
        "next": ["VerifyNextScreen", "[JumpBack]ClickConfirm"]
    }
}
```

### And 组合识别（背景 + 图标）

```jsonc
{
    "MyButton": {
        "recognition": {
            "type": "And",
            "param": {
                "all_of": ["ButtonBackground", "ButtonIcon"],
                "box_index": 0,
            },
        },
        "action": {"type": "Click"},
    },
}
```

## 审查清单

- [ ] 字段名拼写正确、类型合法（可对照 `tools/schema/pipeline.schema.json`）
- [ ] 无不必要的 `pre_delay` / `post_delay` / `timeout`
- [ ] `next` 列表覆盖所有可能画面，含弹窗/加载/异常
- [ ] 每次点击后有识别验证，不假设操作后状态
- [ ] ROI / target 坐标基于 1280×720
- [ ] JSONC 格式与仓库内同类文件一致
- [ ] OCR `expected` 与游戏内实际文案一致、足够稳定
- [ ] 优先通过中间节点避免重复点击，只在必须时用 `post_wait_freezes`
- [ ] `Custom` 识别/动作的名称已在 `custom.json`（及 Agent 路径下的 `Agent_file.py`）注册

## 参考

- Pipeline 协议：[PipelineProtocol](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/en_us/3.1-PipelineProtocol.md)
- 本仓库 schema：`tools/schema/pipeline.schema.json`、`tools/schema/custom.recognition.schema.json`、`tools/schema/custom.action.schema.json`
- 自定义扩展目录：`agent/`
- 项目说明：`README.md`
