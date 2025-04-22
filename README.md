# DeepSeek Translator - 文件翻译工具

## 项目概述

DeepSeek Translator 是一个基于 DeepSeek API 的桌面应用程序，用于将文本文件内容翻译成多种语言。它提供了一个用户友好的图形界面，支持批量翻译大型文本文件。

## 功能特性

• 多语言支持：支持中文、英语、法语、德语、西班牙语、日语和韩语翻译

• 文件处理：可以处理任意大小的文本文件，自动分块翻译

• API 密钥管理：自动保存 API 密钥，无需每次输入

• 进度显示：实时显示翻译进度和状态

• 自动命名：自动生成翻译后的文件名

• 高分辨率支持：适配高 DPI 显示器

## 系统要求

• Python 3.6 或更高版本

• 操作系统：Windows / macOS / Linux

## 安装指南

### 使用预构建的二进制文件

我们为Windows用户提供了预编译的二进制版本，无需安装Python环境即可直接运行。

#### Windows 用户

1. 从 Releases 页面 下载最新版本的 `DeepSeekTranslator-Windows.zip`
2. 解压到任意目录
3. 双击运行 `Translator.exe`
4. 首次运行会自动创建配置文件目录



### 使用源代码

1. 克隆或下载本项目

2. 安装依赖库：

   ```
   pip install tkinter openai
   ```

3. 获取 DeepSeek API 密钥（请访问 [DeepSeek 开放平台](https://platform.deepseek.com/)）

## 使用说明

1. 运行程序：

   ```
   python translator.py
   ```

2. 在 "API Configuration" 部分输入您的 DeepSeek API 密钥

3. 选择要翻译的输入文件

4. 选择或指定输出文件路径（可选，程序会自动生成默认输出路径）

5. 选择目标语言（默认为中文）

6. 点击 "Translate" 按钮开始翻译

7. 翻译完成后，结果将保存到指定的输出文件中

## 配置说明

API 密钥会自动保存在用户主目录下的 `.translator/config.txt` 文件中，无需每次运行都重新输入。

## 注意事项

• 请确保您的 API 密钥有效且有足够的配额

• 大文件翻译可能需要较长时间

• 程序会自动将大文件分块处理以避免 API 限制

• 翻译过程中请保持网络连接稳定

## 已知限制

• 目前仅支持文本文件（.txt）

• 翻译质量取决于 DeepSeek API 的能力

• 免费 API 可能有调用频率限制

## 贡献指南

欢迎提交问题和拉取请求来改进本项目。主要改进方向包括：
• 支持更多文件格式

• 添加更多语言选项

• 优化翻译算法

• 改进用户界面

## 许可证

MIT License

## 联系方式

如有问题，请通过 GitHub Issues 提交。

---

*注意：本项目与 DeepSeek 官方无直接关联，API 使用需遵守 DeepSeek 的相关条款。*
