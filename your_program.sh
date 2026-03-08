#!/bin/sh
#
# Use this script to run your program LOCALLY.
#
# Note: Changing this script WILL NOT affect how CodeCrafters runs your program.
#
# Learn more: https://codecrafters.io/program-interface

set -e # Exit early if any commands fail

# Copied from .codecrafters/run.sh
#
# - Edit this to change how your program runs locally
# - Edit .codecrafters/run.sh to change how your program runs remotely
SCRIPT_DIR="$(dirname "$0")"
PYTHONSAFEPATH=1 PYTHONPATH="$SCRIPT_DIR" exec uv run \
  --project "$SCRIPT_DIR" \
  --quiet \
  -m app.main \
  "$@"

# 参数解释：
# SCRIPT_DIR: 存储脚本所在目录路径
# PYTHONSAFEPATH=1: 启用 Python 安全路径检查
# PYTHONPATH="$SCRIPT_DIR": 设置 Python 模块搜索路径
# exec uv run: 使用 uv 包管理器执行程序
# --project "$SCRIPT_DIR": 指定项目根目录
# --quiet: 静默模式运行
# -m app.main: 运行 app.main 模块（即 main.py 文件）
# "$@": 将脚本接收到的所有参数传递给 Python 程序