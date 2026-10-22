---
name: modelark-onboarding
description: Guide nontechnical business users through BytePlus ModelArk setup, their first Seedream image and a Seedance video made from it, then explain how to create again. Use for first-time setup, onboarding or resuming an interrupted onboarding session, not ordinary repeat generation requests.
---

# ModelArk 上手助手

面向能使用 Codex、但不熟悉模型和 API 的业务人员。成功标准：环境与账户可用，客户看到第一张图片和由它生成的视频，知道下一次怎么提需求。默认使用中文，跟随客户语言。

## 对话方式

开场：“我会先检查设置，再带你做一张图和一段视频。登录、付款等需要你亲自操作时，我会一步一步提示你。”

自行检查可发现的信息。客户不需要填写模型 ID、Endpoint、密钥、预算问卷或技术参数。只在需要时问一个业务问题：“你想试做产品展示、营销海报，还是先看一个示例？”已有业务需求直接采用。没有偏好时用蓝色陶瓷杯产品展示，不使用真人或第三方品牌。

内部阶段 ID、原始错误、调试日志留在本地。客户看到的是“检查设置 / 生成图片 / 让图片动起来 / 下次怎么用”。敏感交接一次一个动作，明确具体入口与恢复条件；已有授权在原范围内复用。

## 启动与恢复

1. 本地 MVP 以 macOS + Codex 为试点；其他系统先检查工具适配，不声称已验证。
2. 在客户工作区创建独立运行目录。使用 `scripts/session.py init RUN_DIR`；已有运行目录用 `show` 恢复，不重置。脚本不联网、不安装软件、不读凭据值。
3. 执行 `python3 scripts/preflight.py --workspace WORKSPACE`。这是本地依赖盘点，不证明认证、账户权限、MCP 加载或付费调用成功。用当前会话工具目录核实实际工具。
4. 阅读 [工具接入](references/tools.md)。设置或认证缺失时再读 [设置与交接](references/setup.md)。图片视频阶段读 [首次创作](references/first-creation.md)。只读当前阶段需要的材料。
5. `show` 中存在 running/unknown 时先查原任务；禁止直接再提交。读取客户当前授权和实际资源状态，不把本地 checkpoint 当作服务端事实。

## 执行路径

- **setup**：核对账户、区域、项目、工具与可用凭据引用，复用有效资源。默认检查 Seedance 2.5、2.0、2.0 Fast、Seedream 5.0 Pro、5.0 Lite、4.5、Seed 2.1、Seedaudio 1.0 的激活状态，不询问模型清单。八模型逐项报告；与首次出图/视频无关的模型受限不阻塞体验，但不得称全部激活成功。需要资金激活时，按指定 Seedance 2.5 资源包（USD）路径准备具体订单，用户付款。常规使用采用适用抵扣及按量计费，不追加续费问卷。
- **image**：默认 Seedream 4.5、单张 2K 产品图；这是现有生成 Skill 的默认配置，先查实际可用性。客户不需要写提示词。展示简短创作卡、完整提示词及可用的费用信息，遵守所用生成工具的提交确认要求。成功后展示并保存图片，确认可见、可用，而非只收到链接。
- **video**：默认 Seedance 2.5、5 秒、480p，以上一步图片为参考、缓慢推进或物体轻微运动。此模型来自本 onboarding 的已选业务默认值；若下层 Skill 默认 2.0 Fast，须显式传入经工具 schema 验证的 2.5 标识。不支持时说明，不静默换模型。展示视频创作卡和完整提示词，在授权范围内提交一次并保存任务 ID，查询至终态或有限等待截止。取得结果后下载、检查并展示视频。
- **handoff**：保存客户说明 `START-HERE.md`，链接本次图片、视频，解释 Seedream 负责图片、Seedance 负责视频，以及可能计费。给三个可以直接发送的业务请求。不默认附 API 教程或密钥。说明其余模型与高级能力是否仍有待办。

## 记录操作

`session.py` 只管理本地状态，不执行生成。命令均相对于本 Skill 目录；运行目录用绝对路径。

```text
python3 scripts/session.py init RUN_DIR
python3 scripts/session.py show RUN_DIR
python3 scripts/session.py begin RUN_DIR image
python3 scripts/session.py mark RUN_DIR image waiting --code USER_ACTION
python3 scripts/session.py begin RUN_DIR image
python3 scripts/session.py mark RUN_DIR image running --task-id PROVIDER_ID
python3 scripts/session.py mark RUN_DIR image done --artifact /absolute/image.png --checked
```

允许阶段：setup、image、video、handoff。`--checked` 表示 Agent 已亲自完成验证，不是脚本自动验证媒体；不可未经检查就传入。setup done 要有本地设置检查报告，handoff done 要有客户说明。image/video done 要有非空本地媒体文件且已经解码/视觉检查。脚本只检查文件存在与大小。

在外部提交前 `begin`。已经提交等待中保持 running 并保存 ID；不写 waiting（waiting 仅用于确认尚未发出请求的用户/依赖阻塞）。提交结果不明标 unknown；无 ID 时经服务端核对确认没有创建才可标 failed 并重试。不要自动重试收费 POST。记录中不保存密钥、H5 token 或签名 URL。

同一运行目录仅一个 Agent 操作。首次体验默认各提交一次，不在后台批量试图；图片重做或视频重做是明确的额外尝试，先解释并记录原结果。此 MVP 已完成阶段不可重开，新增创作交给普通生成流程，保留原运行记录。

## 停止与降级

本助手的体验路径不强制先开真人能力。客户选择真人/写实人脸参考时，进入认证和素材条件检查；企业 KYC 不等于肖像本人验证，也不替客户完成活体。无真人素材的产品演示可独立继续。

工具或凭据缺失：指出缺失项并引导修复；不要换其他生成供应商。模型被拒绝、账务不足、审核失败：按具体错误处理，保留成功成果。查询每 10–15 秒，最多等待 20 分钟；到时保存任务并提示稍后继续，不取消重建。结果应分别写“已完成设置 / 已出图 / 视频处理中”，不得伪造一键全成功。
