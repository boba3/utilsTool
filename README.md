# 🚀 极简加解密工作台 (Advanced Crypto Tool)



这是一个基于 Python 和 `CustomTkinter` 开发的高性能安全加解密桌面应用。它不仅支持常用的哈希与对称加密算法，还集成了**多核并行暴力破解**引擎和**智能自学习字典**系统，旨在提供一个兼具美观与效率的安全实验环境。

---

## ✨ 核心特性

* **⚡ 高性能破解**：内置多进程（Multiprocessing）并行计算引擎，支持自动识别 CPU 核心数并预留系统资源，破解速度提升 400%-1200%。
* **🧠 智能字典管理**：
    * **自动学习**：每次加密或破解成功后，自动记录明密文对。
    * **秒级查表**：解密时优先检索本地字典，实现已知哈希的“秒破”。
    * **字典清洗**：一键去重、排序及优化字典结构。
* **🎨 现代 UI 交互**：
    * **Element UI 配色**：严格遵循专业 UI 色系（成功绿、危险红、主导蓝）。
    * **双色主题**：支持深色（Dark）与浅色（Light）模式一键切换。
* **🔒 算法全支持**：
    * 哈希算法：MD5 (带暴力破解)
    * 编码算法：Base64
    * 对称加密：AES (16/24/32位密钥)、DES (8位密钥)

---

## 🛠️ 技术栈

* **GUI 框架**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (现代 Material Design 风格)
* **核心算法**: `hashlib`, `pycryptodome`
* **并行处理**: `multiprocessing`, `threading`
* **数据存储**: 基于本地文本文件的哈希映射

---

## 🚀 快速开始

### 环境依赖
确保你的电脑已安装 Python 3.8+ 及以下库：
```bash
pip install customtkinter pycryptodome

---

### 运行主脚本
```bash
python Advanced_Crypto_Tool.py

---

### 打包
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter --name "极简安全工作台" Advanced_Crypto_Tool.py

---

## 📋 功能说明
* **暴力破解限时逻辑
	* 为了防止无休止的计算占用系统资源，暴力破解被硬性限制为1 分钟。
	* 如果在 1 分钟内未果，程序将自动停止并提示破解失败。
	* 建议开启 “高性能模式” 以在 1 分钟内尝试更多的组合。
* **字典管理
	* 路径: md5dictionary.txt 始终生成在程序同级目录下，方便携带。
	* 导出: 支持将你日积月累生成的 “个人彩虹表” 导出为外部文件。
	* 清洗: 建议在字典条目超过 10,000 条后执行一次清洗，以优化加载速度。
	
---

## ⚠️ 免责声明

本工具仅用于个人学习和安全研究。请勿将此工具用于任何非法活动或未经授权的渗透测试。开发者不对因使用此工具导致的任何损失负责。
