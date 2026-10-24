---
name: modelark-onboarding
description: Guide nontechnical users through full BytePlus Console and ModelArk onboarding including account registration, KYC, activation, credentials, private and real-person assets, first image/video tests and handoff. Use for setup or resuming onboarding, not routine repeat generation.
---

# ModelArk 上手助手

面向能使用 Codex、但不熟悉模型和 API 的业务人员。默认范围来自随包三份指南：账户注册与合同、KYC、八模型激活、API、Playground、私有虚拟素材和真人能力均须有证据；另含首次 Seedream 图片及由它生成的 Seedance 视频和使用交接。首次生成成功只是阶段成果，不代表全部开通。默认使用中文，跟随客户语言。

## 对话方式

开场：“我会从账户注册和设置开始，带你完成模型激活、认证、素材能力，再做第一张图片和视频。可以独立完成的步骤会先推进；登录、付款、身份认证需要你操作时，我会明确提示。”

自行检查可发现的信息。客户不需要填写模型 ID、Endpoint、密钥、预算问卷或技术参数。只在需要时问一个业务问题：“你想试做产品展示、营销海报，还是先看一个示例？”已有业务需求直接采用。没有偏好时用蓝色陶瓷杯产品展示，不使用真人或第三方品牌。

内部阶段 ID、原始错误、调试日志留在本地。客户看到的是“检查设置 / 生成图片 / 让图片动起来 / 下次怎么用”。敏感交接一次一个动作，明确具体入口与恢复条件；已有授权在原范围内复用。

## 启动与恢复

1. 本地 MVP 以 macOS + Codex 为试点；其他系统先检查工具适配，不声称已验证。
2. 在客户工作区创建独立运行目录。完整流程先读下方“完整范围与执行记录”，从模板建立 `run-state.json`；已有记录直接恢复，不重置。`session.py` 仅用于原型四阶段创作记录，不能用其 done 判定完整开通。
3. 执行 `python3 scripts/preflight.py --workspace WORKSPACE`。这是本地依赖盘点，不证明认证、账户权限、MCP 加载或付费调用成功。用当前会话工具目录核实实际工具。
4. 阅读 [工具接入](references/tools.md)。设置时同时盘点独立 Seedream、Seedance 与 Seedaudio MCP；Seedaudio 先用只读状态接口核对配置，音频创作按该文档的可选分支执行，不自动追加付费生成。设置阶段必须读 [设置与交接](references/setup.md) 和 [完整执行映射](references/full-onboarding.md)。图片视频阶段读 [首次创作](references/first-creation.md)。只读当前阶段需要的材料。
5. 任一记录存在进行中或结果不明的写入时先查原任务；禁止直接再提交。读取客户当前授权和实际资源状态，不把本地 checkpoint 当作服务端事实。

## 完整范围与执行记录

这是一个 Skill；客户无需切换技能或自己阅读英文 API 文档。按需读取随包资料，不能依赖作者电脑上的旧路径：

- [快速上手指南](references/01-快速上手指南.md)：启动时读取，确定 MA-00–MA-12、全部能力目标和交接规则。
- [英文执行手册](references/02-ModelArk-Onboarding-Guide.md)：执行当前 MA 步骤前读取对应节；接口操作再读 §3–§6。
- [待确认、官方来源与验证记录](references/03-待确认与核验记录.md)：启动时读取已采纳默认值，遇到具体门槛再查 Q01–Q08 和 S01–S17。已决定的问题不再问客户。
- [完整执行映射](references/full-onboarding.md)：注册细分、分支调度、首次图片扩展、完成门槛与旧记录兼容。

三份资料是用户指定的流程基线；其“本轮交付草稿、无需现在付款”描述编写时状态，不替代客户当前执行授权。原始 input 中的意见已由 v2 核验后的规则收敛，不能重新采用未经证实的绝对表述。文档核验日期不等于账户验证日期；执行前核对当前官方页面和实际账户，冲突标待确认。

复制 `assets/run-state.template.json` 到独立运行目录的 `run-state.json`，补充 run ID 和实际时间；每个 MA 步骤、能力、八模型分别记录状态与证据。模板不调用服务端，也不自动校验成功；Agent 对证据负责。设置阶段不得仅以工具已安装验收。写入前保存计划，写入后立即保存 ID；记录采用临时文件 + 原子替换，目录仅当前用户可访问，秘密不进入记录。

默认不得删除或跳过真人、虚拟素材、Playground 分支。缺资格时明确等待，继续独立工作。只有客户明确要求“只体验基础生成”等缩减范围，才能记录范围变更；不能把默认演示的无人物题材当成缩减完整开通范围的授权。

模型调用以 [工具接入中的模型调用约定](references/tools.md) 为准；用户当前选择与项目偏好优先于以下流程默认值，显式设置参数，不依赖 MCP 默认模型。

## 面向客户的阶段导航（完整步骤见 MA 映射）

- **setup**：核对账户、区域、项目、工具与可用凭据引用，复用有效资源。默认检查 Seedance 2.5、2.0、2.0 Fast、Seedream 5.0 Pro、5.0 Lite、4.5、Seed 2.1、Seedaudio 1.0 的激活状态，不询问模型清单。八模型逐项报告；与首次出图/视频无关的模型受限不阻塞独立体验，但必须保留为完整目标未完成项。需要资金激活时，按指定 Seedance 2.5 资源包（USD）路径准备具体订单，用户付款。常规使用采用适用抵扣及按量计费，不追加续费问卷。
- **image**：默认 Seedream 4.5、单张 2K 产品图；这是现有生成 Skill 的默认配置，先查实际可用性。客户不需要写提示词。展示简短创作卡、完整提示词及可用的费用信息，遵守所用生成工具的提交确认要求。成功后展示并保存图片，确认可见、可用，而非只收到链接。
- **video**：默认 Seedance 2.5、5 秒、480p，以上一步图片为参考、缓慢推进或物体轻微运动。此模型来自本 onboarding 的已选业务默认值；若下层 Skill 默认 2.0 Fast，须显式传入经工具 schema 验证的 2.5 标识。不支持时说明，不静默换模型。展示视频创作卡和完整提示词，单独核价并取得视频生成授权后提交一次并保存任务 ID，查询至终态或有限等待截止。取得结果后下载、检查并展示视频。
- **handoff**：保存客户说明 `START-HERE.md`，链接本次图片、视频，解释 Seedream 负责图片、Seedance 负责视频，以及可能计费。给三个可以直接发送的业务请求。不默认附 API 教程或密钥。交付 MA-12 能力矩阵与八模型状态；任何默认分支待办都意味着部分完成。

## 原型四阶段记录兼容（非完整开通状态）

`session.py` 只管理旧版 setup/image/video/handoff 本地状态，不执行生成，不覆盖 MA-00–MA-12。完整运行以 `run-state.json` 为准，不需要同时维护这个旧脚本记录。旧会话继续使用时，保留原文件并逐项重新核实后转入完整记录，不能把 setup done 迁移成 KYC/真人等全部成功。命令均相对于本 Skill 目录；运行目录用绝对路径。

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

默认完整开通目标包含真人能力，但基础体验不强制等待真人分支。客户选择真人/写实人脸参考时，进入认证和素材条件检查；企业 KYC 不等于肖像本人验证，也不替客户完成活体。无真人素材的产品演示可独立继续；真人分支仍需记录资格、授权、审核、参考测试的等待与恢复条件。

工具或凭据缺失：指出缺失项并引导修复；不要换其他生成供应商。模型被拒绝、账务不足、审核失败：按具体错误处理，保留成功成果。视频任务查询每 10–15 秒，最多等待 20 分钟；到时保存任务并提示稍后继续，不取消重建。结果应分别写“已完成设置 / 已出图 / 视频处理中”，不得伪造一键全成功。
