# AI Image Detector Skill

这是一个 Codex skill，用来检测图片是否存在 AI 生成或 AI 合成证据，并生成中文报告。

## 能检测什么

- `TC260:AIGC` 国内 AIGC 标识
- `C2PA / Content Credentials / JUMBF` 来源凭证
- PNG / JPEG / XMP 里的生成器元数据
- Stable Diffusion、ComfyUI、Midjourney、DALL-E/OpenAI、Adobe Firefly、NovelAI 等常见字段
- OCR 可见水印文字
- 视觉/内容层面的“疑似 AI”判断和理由

报告会把两类结论分开：

- **硬证据检测**：来自文件元数据、水印、内容凭证等可验证信息。
- **视觉/内容判断**：来自画面风格、截图/压缩导致元数据丢失等人工判断理由。

## 安装到 Codex

把仓库根目录作为 skill 目录放到 Codex skills 目录下，例如：

```bash
mkdir -p ~/.codex/skills/ai-image-detector
cp -R . ~/.codex/skills/ai-image-detector/
```

也可以直接从 GitHub 安装到 `~/.codex/skills/ai-image-detector`。

## 命令行使用

```bash
PYTHONPATH=./scripts python3 -m ai_image_detector.cli /path/to/image.png \
  --ocr \
  --content-assessment likely_ai \
  --content-note "画面符合生成式视觉特征" \
  --output-dir /tmp/ai-image-report \
  --artifacts-dir /tmp/ai-image-report
```

输出文件：

- `*-ai-image-detection-report.html`
- `*-ai-image-detection-report.json`
- `*-fft-spectrum.png`

## 判断标签

硬证据标签：

- `strong_ai_evidence`：发现强证据，例如 AIGC 元数据、C2PA、生成器字段。
- `possible_ai_evidence`：只有弱证据。
- `no_ai_evidence`：没有发现可支持的 AI 元数据或水印证据。

视觉/内容标签：

- `likely_ai`：高度疑似 AI
- `possible_ai`：疑似 AI
- `unclear`：无法判断
- `likely_not_ai`：不像 AI
- `not_provided`：未提供视觉判断

## 注意

没有检测到元数据不等于图片不是 AI。截图、微信/社交平台压缩、格式转换、二次编辑都可能清除 C2PA、AIGC 标识或生成器字段。私有隐形水印，例如某些厂商的模型级水印，通常需要官方检测器，不能靠通用脚本稳定提取。
