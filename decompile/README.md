# decompile
二进制反编译自动化工具链 / Automated Binary Decompilation Toolchain

---

## 📌 项目简介 / Introduction
本项目实现了一套基于 **IDA Pro** 和 **Ghidra** 的自动化反编译工具链，支持对 SPECCPU 2006 与 GitHub 开源项目的二进制文件进行批量反编译、失败日志记录与失败类型统计。可用于反编译效果评估、逆向工程研究、编译器优化对比等场景。

This project implements an automated decompilation toolchain based on **IDA Pro** and **Ghidra**. It supports batch decompilation of binaries from SPECCPU 2006 and GitHub open-source projects, decompilation failure logging, and failure type statistics. It can be used for decompilation effect evaluation, reverse engineering research, and compiler optimization comparison.

---

## 📚 目录 Table of Contents
- [项目结构 Project Structure](#项目结构-Project-Structure)
- [环境依赖 Requirements](#环境依赖-Requirements)
- [使用方法 Getting Started](#使用方法-Getting-Started)
  - [Ghidra 反编译流程 Ghidra Decompilation](#ghidra-反编译流程-ghidra-decompilation)
  - [IDA 反编译流程 IDA Decompilation](#ida-反编译流程-ida-decompilation)
  - [失败统计 Failure Analysis](#失败统计-Failure-Analysis)
- [项目声明 Project Statement](#项目声明-Project-Statement)
- [许可证 License](#许可证-License)

---

## 📁 项目结构 Project Structure
```text
decompile/
├── Ghidra/
│   ├── decompilation_failure.py      # 反编译失败统计脚本
│   ├── decompile.py                  # 反编译核心类（Ghidra + IDA）
│   ├── ghidra_single_fun_decompilation.py  # Ghidra 单函数反编译脚本
│   └── ida_decompiler_test.py        # IDA 反编译测试脚本
├── IDA/
│   ├── batch_decompile_ida.py        # SPECCPU 批量 IDA 反编译脚本
│   ├── batch_decompile_ida_no_order.py  # GitHub 项目批量 IDA 反编译脚本（无顺序）
│   ├── ida_decompiler.py             # IDA 反编译核心脚本（带顺序）
│   ├── ida_decompiler_no_order.py    # IDA 反编译核心脚本（无顺序）
│   ├── run_github.sh                 # GitHub 项目 IDA 反编译执行脚本
│   └── run_speccpu.sh                # SPECCPU 项目 IDA 反编译执行脚本
├── README.md                         # 项目说明文档
└── LICENSE                           # 项目许可证
⚙️ 环境依赖 Requirements
操作系统：Linux（推荐 Ubuntu 18.04+）
Python：3.8+（兼容 Ghidra 与 IDA 脚本环境）
IDA Pro：7.5+（需安装 Hex-Rays 反编译器插件）
Ghidra：10.0+（需配置脚本运行环境）
tmux：用于并行任务调度（可选）
