# 🚀 极简加解密工作台 (Advanced Crypto Tool)



# 🚀 极简安全加解密工作台 (Advanced Crypto Tool) v4.0



这是一个基于 Python 和 `CustomTkinter` 开发的高性能全能加解密桌面应用。本版本在原有基础上深度集成了**国密系列算法 (SM3/SM4)**、**数据混淆算法 (Hashids)**，并优化了多核暴力破解引擎。

---

## ✨ 核心特性

* **⚡ 极致性能**：
    * **多核破解**：内置并行计算引擎，自动调用多核心资源。
    * **秒级查表**：解密时优先检索本地字典，实现已知哈希的“秒破”。
* **🇨🇳 国密支持 (SM Series)**：
    * **SM3**：国产商用密码杂凑算法（哈希），安全性高于 MD5。
    * **SM4**：国产分组对称加密算法，用于替代 DES/AES，密钥长度固定为 128 位 (16 字符)。
* **🧠 智能字典管理**：
    * **自动学习**：加密或破解成功后，自动记录明密文对。支持 MD5 与 SM3。
    * **一键清洗**：提供清洗功能，自动执行去重、排序及空行过滤。
* **🎨 现代 UI & 交互**：
    * **Element UI 配色**：主导蓝 (`#409EFF`)、成功绿 (`#67C23A`)、危险红 (`#F56C6C`)。
    * **动态交互**：高性能开关圆点随状态变色，UI 细节更加精致。
    * **双色主题**：支持浅色 (Light)、深色 (Dark) 及系统同步模式。

---

## 🛠️ 技术栈

* **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* **核心算法**: `hashlib`, `pycryptodome`, `gmssl`, `hashids`
* **并行处理**: `multiprocessing`, `threading`

---

## 🚀 快速开始

### 环境依赖
确保你的电脑已安装 Python 3.8+ 及以下库：
```bash
python -m pip install --upgrade pip
pip install customtkinter pycryptodome gmssl hashids
```

---

### 运行主脚本
```bash
python Advanced_Crypto_Tool.py
```

---

### 打包
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter --name "极简安全工作台" Advanced_Crypto_Tool.py
```

---

## 📋 功能说明
* **暴力破解限时逻辑
	* 为了防止无休止的计算占用系统资源，暴力破解被硬性限制为1 分钟。
	* 如果在 1 分钟内未果，程序将自动停止并提示破解失败。
	* 建议开启 “高性能模式” 以在 1 分钟内尝试更多的组合。
* **算法输入规范
  	* Hashids：加密时请输入整数，支持逗号分隔（如 102, 204, 306）。
  	* SM4：密钥 (Key) 必须严格为 16 位 字符。
* **字典管理
	* 路径: md5dictionary.txt 始终生成在程序同级目录下，方便携带。
	* 导出: 支持将你日积月累生成的 “个人彩虹表” 导出为外部文件。
	* 清洗: 建议在字典条目超过 10,000 条后执行一次清洗，以优化加载速度。
	
---

## ⚠️ 免责声明

本工具仅用于个人学习和安全研究。请勿将此工具用于任何非法活动或未经授权的渗透测试。开发者不对因使用此工具导致的任何损失负责。


