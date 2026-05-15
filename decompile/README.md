# 反编译工具集（Ghidra + IDA Pro）

本仓库提供了一套用于批量反编译二进制文件中指定函数的脚本，同时支持 Ghidra和IDA Pro两种反编译器，适用于大规模二进制分析任务（如 SPEC CPU 2006、GitHub 开源项目等）。


## 文件结构

| 文件 | 反编译器 | 功能描述 |
|------|----------|----------|
| `ghidra_single_fun_decompilation.py` | Ghidra | 单二进制反编译脚本，读取函数列表并输出 |
| `decompile.py` | Ghidra + IDA | 封装类，包含两种反编译器的实现 |
| `ida_decompiler.py` | IDA Pro | 带处理顺序的反编译脚本 |
| `ida_decompiler_no_order.py` | IDA Pro | 无处理顺序的反编译脚本 |
| `batch_decompile_ida.py` | IDA Pro | 批量处理入口（带顺序） |
| `batch_decompile_ida_no_order.py` | IDA Pro | 批量处理入口（无顺序） |
| `run_speccpu.sh` | IDA Pro | SPEC CPU 2006 批量运行脚本 |
| `run_github.sh` | IDA Pro | GitHub 项目批量运行脚本 |
| `decompilation_failure.py` | 通用 | 反编译失败日志分析工具 |

---

## 环境依赖

### Ghidra
- Ghidra 9.x 或更高版本
- 需要分析的目标二进制文件已在 Ghidra 中打开

### IDA Pro
- IDA Pro 7.7 或更高版本（脚本中路径为 `/opt/idapro-7.7/idat64`）
- Hex-Rays 反编译器（根据架构安装对应插件）
- IDA Python 环境

### 系统环境
- Linux 操作系统（脚本使用 `cp`、`rm`、`mkdir` 等命令）
- Python 2.7 或 3.x

---


