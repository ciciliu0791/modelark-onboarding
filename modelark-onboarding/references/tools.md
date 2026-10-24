# 工具接入与依赖修复

本 Skill 是编排层，不内置 API 密钥、生成服务或自动安装器。运行时选择实际存在且已验证的 BytePlus 路径，不猜测工具名称或参数。依赖的产品能力应以当前工具 schema 和官方资料为准。

## 模型调用约定（2026-10-24 工具 schema 核对）

执行顺序：用户当前明确选择及项目约定 → 本流程默认值 → 工具默认值。工具默认值不能覆盖前两者。每次提交显式指定模型和关键规格，并检查返回的实际模型；改变模型、数量或规格须说明并重新核对授权与预算。以下是当前 MCP 参数映射，执行时再次核对 schema，不把工具别名直接作为原始 HTTP model ID。

| 用途 | 首选工具与显式参数 | 结果处理 |
|---|---|---|
| 首张图片 | `seedream_generate`：`model="4.5"`、`size="2K"`、`sequential=false`、`num_images=1` | 同步返回 `images`；保存并看图，无需轮询 |
| 默认首次视频 | `seedance_generate`：`model="2.5"`、`fast_mode=false`、`duration=5`、`resolution="480p"`、`output_format="mp4"` | 立即保存 `task_id`，用 `seedance_check_task` 查询 |
| 可选音频 | `seedaudio_generate`；当前服务固定 Seed Audio 1.0，无 `model` 参数 | 先查 `seedaudio_status`；生成返回本地文件，按实际结果验收 |
| Seed 2.1 及其他非默认创作模型 | 只读核对模型目录、权益及可用证据 | 三个媒体 MCP 不代表 Seed 2.1 调用接口；本流程不自动新增付费测试 |

2.5 首帧生成使用 `first_frame_url` 与 `ratio="adaptive"`，不能用普通 `image_url` 假装锁定首帧。`generate_audio` 必须按视频创作卡明确设置；它控制视频配音轨，不等于调用独立 Seedaudio。2.5 提示词引用用 `@Image1` / `@Video1` / `@Audio1`；2.0 使用 `[image1]` / `[video1]` / `[audio1]`，顺序对应实际输入。不得使用长时间阻塞的 `seedance_auto_generate`。

`seedance_generate` 接收 HTTPS 图片时可能自动创建素材组并上传素材，须将这些写入纳入授权、项目与记录检查。已有正确素材组/asset URI 优先复用；真人素材必须使用经过本人验证的正确组，不交给自动建普通组流程。工具缺少目标项目、组或审核控制能力时，改用有该能力的 BytePlus 接口。已有 `asset://` 素材须核对项目及 Active 状态。

图片在已明确的模型、素材、数量与预算范围内，复用用户生图授权，不重复索要常规费用批准；提交前仍核价并告知估算，未知价格不得记为零。视频提交前单独核价并获得具体授权；音频按音频创作授权处理。报价不明或超预算时先说明并解决，不自动扩量。看图审核与费用授权分开：后续依赖选图时等待用户选图，不用未选定或被拒绝的图片推进。

状态区分：工具已发现、服务已配置、认证/权益已验证、生成已验收。任一前项不推导后项。API key、SSO 管理认证、素材管理签名与语音凭据分别核实；不把一个服务的凭据或 endpoint 通用于其他服务。

## 已有生成 MCP

会话发现 Seedream / Seedance 工具后，如有适用的生成 Skill，读取它及其实际存在的引用文件；以当前 MCP schema 为调用依据，不将缺少同名 Skill 视为 MCP 不可用。使用其签名、上传、计费确认与结果处理流程。常见工具名 seedream_generate、seedance_generate、seedance_check_task 只是发现线索，不是保证可调用的接口。

读取的 Skill 如指向缺失文件，先在配置的技能根和项目内查找正确位置；不能声称已读取不存在的规范，不能自动用另一模型供应商替代。必要时报告缺失路径并指导恢复相应包。无需读取或显示 MCP 配置中的秘密。

## Seedaudio MCP（音频）

将独立 `seedaudio` MCP 纳入设置与能力盘点；先从当前会话目录发现 `seedaudio_status`、`seedaudio_generate` 和 `seedaudio_generate_variations`，以实际 schema 为准，不要求存在同名本地 Skill。

- 先调用只读 `seedaudio_status`，核对 configured、provider、model、base_url 和 supports。`configured: true` 只证明服务报告已有配置，不证明远端认证、模型权益或付费生成成功。
- 当前已核对接口为 BytePlus Seed Audio 1.0；状态报告的服务地址是 `https://voice.ap-southeast-1.bytepluses.com`。运行时重新检查，不将 Seedance/Seedream 的 Ark endpoint 或凭据假定可用于语音服务。
- 用户需要配音或音频场景时，用 `seedaudio_generate` 生成一个结果。支持文本描述的语音、环境音、音乐和音效；具体参数遵守当前 schema。音频参考总计最多三个，通过 `audio_paths`、`audio_urls` 或 `speaker_ids` 提供，并在提示词中使用 `@Audio1`–`@Audio3`。单张图片参考不能与音频参考混用；使用声音参考前确认使用授权。
- `seedaudio_generate_variations` 会生成 2–5 个独立结果，仅在用户明确要求多个备选并确认数量与费用后使用，不作为默认重试。
- 音频是可选创作分支；现有八模型检查中的 Seedaudio 1.0 保留，不因加入 MCP 自动追加收费验收。生成前准备具体文本、输出格式和费用估计，取得音频生成授权；图片免逐次批准的偏好不自动适用于音频。
- 结果由工具保存到本地；选择本次运行目录下的独立输出路径，默认不覆盖。记录实际结果路径与费用，检查文件非空、可解码并试听后交付。结果未知时先检查原结果，不盲目重复提交；当前工具目录没有独立音频任务查询接口，不编造查询命令。
- MCP 缺失或配置不完整时记录待修复项。不得自动安装 BytePlus Creative Kit，也不猜测 MCP 安装包、启动命令或密钥环境变量；从实际服务分发说明核实后再配置，秘密通过安全配置提供。CLI 备选必须先确认独立 BytePlus 版本实际支持 Seed Audio，不能从图片/视频支持推断音频支持。

## 官方 CLI 路径

优先使用已验证的独立 Seedream / Seedance / Seedaudio MCP；MCP 不可用或缺少所需能力时，使用独立 BytePlus Ark CLI。先检查 `arkcli` 的实际可执行文件来源及所属包，读取 BytePlus 版本的 arkcli-shared 和当前能力 Skill，再运行帮助、版本与只读诊断。仅发现同名命令不证明它属于 BytePlus，不从这里猜测 gen 子命令。

独立 BytePlus Ark CLI 的安装包为 `@byteplus/ark-cli`，命令入口为 `arkcli`：

```bash
npm install -g @byteplus/ark-cli
```

执行安装前重新核对当前包来源、系统要求和官方 setup/auth 文档，使用受支持安装方式；不得覆盖现有 profile 或 MCP 配置。客户请求实际 setup 时，必要的常规安装在任务范围内；涉及登录、权限、条款和费用时走具体交接。

- [官方 Ark CLI 安装入口](https://docs.byteplus.com/en/docs/modelark/coding-plan-personal-ai-opencode)：只复用安装信息，不采用其 Coding Plan 配置作为媒体生成配置。
- 使用与 `@byteplus/ark-cli` 匹配的 BytePlus `arkcli-*` 技能；核对其 product boundary 为 standalone BytePlus，核实技能与安装包来自同一产品。Agent 调用须遵守该版本 arkcli-shared 的调用者元数据和更新抑制约定。
- [BytePlus 数据面地址与认证](https://docs.byteplus.com/en/docs/modelark/base-url-and-authentication)

调用前分别验证目标模型、服务地域和 API endpoint 的实际支持；控制面认证与推理 API key 不混用。支持不足时说明并使用已验证的 BytePlus API/控制台路径。

在 CLI 路径验证可以生成 Seedream 图片和 Seedance 视频之前，环境只标“工具已发现”，不标“可生成”。不能访问当前规范时停在依赖修复，不临时拼接未经验证的接口。

## 本机试点已知限制（2026-10-22）

历史构建环境的工具发现结果不代表当前环境。每次执行重新发现独立 MCP，并分别验证配置、认证与目标模型能力。
