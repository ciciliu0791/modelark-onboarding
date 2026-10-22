# 工具接入与依赖修复

本 Skill 是编排层，不内置 API 密钥、生成服务或自动安装器。运行时选择实际存在且已验证的 BytePlus 路径，不猜测工具名称或参数。依赖的产品能力应以当前工具 schema 和官方资料为准。

## 已有生成 MCP

若会话可发现 Seedream / Seedance 工具，读取对应生成 Skill 及其实际存在的引用文件，使用其签名、上传、计费确认与结果处理流程。常见工具名 seedream_generate、seedance_generate、seedance_check_task 只是发现线索，不是保证可调用的接口。

读取的 Skill 如指向缺失文件，先在配置的技能根和项目内查找正确位置；不能声称已读取不存在的规范，不能自动用另一模型供应商替代。必要时报告缺失路径并指导恢复相应包。无需读取或显示 MCP 配置中的秘密。

## 官方 CLI 路径

CLI 可作为独立接入路径，不要求安装本机的私有 MCP 包。先发现当前安装的 arkcli/ve 和相关产品 Skill，读取其安装、认证、调用约定，再运行真实帮助/版本/只读诊断。不从这里猜测 gen 子命令。

若使用 ve，读取 volcengine-cli Skill，遵守其版本门槛和调用者元数据，并按它要求加载官方 Ark Skill。不要将 Volcengine 默认区域、账户或凭据用于 BytePlus。明确选择正确 BytePlus profile 后再查询实际模型列表。

若组织选择 standalone BytePlus Ark CLI，官方资料给出的包为 `@byteplus/ark-cli`。执行安装前重新核对当前包来源、系统要求和官方 setup/auth 文档，使用受支持安装方式；不得覆盖现有 profile 或 MCP 配置。客户请求实际 setup 时，必要的常规安装在任务范围内；涉及登录、权限、条款和费用时走具体交接。

- [官方 Ark CLI 安装入口](https://docs.byteplus.com/en/docs/modelark/coding-plan-personal-ai-opencode)：只复用安装信息，不采用其 Coding Plan 配置作为媒体生成配置。
- [Ark CLI 上游技能](https://github.com/volcengine/ark-cli/tree/main/skills)：按当前操作选择 shared/auth/models/generation 等真实存在的 Skill，不假定本机已加载。
- [BytePlus 数据面地址与认证](https://docs.byteplus.com/en/docs/modelark/base-url-and-authentication)

在 CLI 路径验证可以生成 Seedream 图片和 Seedance 视频之前，环境只标“工具已发现”，不标“可生成”。不能访问当前规范时停在依赖修复，不临时拼接未经验证的接口。

## 本机试点已知限制（2026-10-22）

制作此版本时，当前会话未暴露 Seedream/Seedance 生成工具；workspace 下 seedream/seedance Skill 的 canonical 引用文件缺失。检测到 ve 可执行文件，未执行认证或生成，也未证明其 BytePlus profile 可用。该事实只属于构建时环境，每次试用重新检查。可继续本地助手试用与文案演练，但真实出图出视频需要修复生成路径。
