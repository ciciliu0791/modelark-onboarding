# 首次图片 → 视频 → 客户交付

## 默认示例

没有素材也可以开始：蓝色陶瓷杯、无人物、无品牌、无文字。默认单张图片、一次短视频，避免文字渲染和人物授权成为首次体验的额外门槛。客户指定产品时，用其已授权素材；不要上传未确认的个人文件。

图片卡（与下层 Skill 要求合并展示，不重复询问）：

> 我先做一张干净的产品展示图：蓝色陶瓷杯放在浅色桌面，柔和晨光，横向构图，方便接下来做视频。使用 Seedream 4.5，单张 2K。{工具可提供的费用估算；不能核实则明确说明}

提示词示例：

> A blue ceramic coffee cup on a light neutral studio table, soft morning light from the left, subtle shadow, premium product photography, simple warm background, centered composition with generous negative space, wide landscape framing, no people, no logos, no text.

由工具支持的规格确定横向尺寸，不把“2K”随意映射到未经验证的数值。若生成工具默认给多张，显式请求一张。Seedream MCP 同步返回时无需编造轮询；其他路径按真实响应处理。

展示并保存图片后，简短说明：“图片已经做好，接下来我会让镜头缓慢靠近它。”如客户不满意，先处理其修改，不用被拒绝图片继续视频；保留已有结果，额外生成走显式的新尝试。

视频卡：

> 用刚才这张图做一段 5 秒产品视频，镜头缓慢推进，保持杯子的外观和背景一致。默认 Seedance 2.5、480p。{费用信息}

提示词示例：

> Use the reference image as the first frame. A slow, smooth camera push toward the blue ceramic cup. Preserve the cup shape, blue glaze, lighting and background. Subtle natural light movement only. No new objects, no people, no text, no cuts.

图片作为首帧时，比例使用当前模型/工具支持的匹配模式；不要强制沿用一个不支持的 ratio。模型名称映射、首帧 role、duration 和 resolution 均以当前 schema 为准。不能用 seedance 默认 2.0 Fast 代替本流程已指定的 2.5 而不告知。

跨工具传图：优先读取上一步真实返回的可访问 URL；下载后仅有本地文件时，走已授权官方上传工具，不编造 URL、不公开桶。URL 过期优先恢复同一图片的可访问性，不自动重生成图片。

## 成功与恢复

图片检查：能解码，主体/构图符合意图；下载到客户运行目录。视频检查：服务端成功、下载非空、可解码、时长/尺寸可核实，抽看首尾或播放确认承接图片。工具不足以验证时如实标记等待验证。

一收到视频 task ID 就更新 running 记录。客户端中断先查该 ID，别重新生成。无 ID 且结果不明标 unknown。达到本地等待上限仍保留 running；下次从查询开始。HTTP 成功或返回 URL 不等于已完成验收。

## START-HERE.md 内容

用客户语言写一页，不含调试日志：

- 本次图片和视频的相对文件链接。
- “Seedream 用于生成和修改图片；Seedance 用于生成视频，也能让已有图片动起来。你描述业务目标，我来整理提示词和选择参数。”
- “生成可能产生费用；作品保存在本项目的运行文件夹。”
- 三个可直接使用的请求：“给这个产品做一张宣传图”“保持产品不变，把背景换成海边”“把这张图做成 5 秒视频，镜头缓慢推进”。
- 八个模型的检查结果简表；未完成项明确标出，不让它们掩盖客户已拿到的作品。
- 如果未来要做真人参考内容，说明需要另行检查认证与授权。

hand-off 的 done 记录必须指向实际保存的说明文件。最终直接展示图片与视频（工具原生输出或本地媒体），不要只交付任务 ID。
