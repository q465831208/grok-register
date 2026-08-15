#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""管理控制台命令行入口。

运行示例：``python -m backend.web.cli --host 0.0.0.0 --port 8787``。

在导入应用之前，先从 config.json 读取 browser_backend 并设置环境变量，
确保 __init__.py 能根据配置选择正确的浏览器后端。
"""
from __future__ import annotations

import os
import json
import sys


def _apply_browser_backend() -> None:
    """从 config.json 读取 browser_backend，设置 GROK_BROWSER_BACKEND 环境变量。

    优先级：环境变量 > config.json > 默认（camoufox）。
    环境变量已设置时不覆盖，让用户显式指定的优先级更高。
    """
    if os.environ.get("GROK_BROWSER_BACKEND"):
        return  # 用户显式设置了环境变量，不覆盖

    # 优先查找 data/config.json（Docker 模式），再找根目录 config.json
    for path in ("data/config.json", "config.json"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                backend = cfg.get("browser_backend", "").strip()
                if backend:
                    os.environ["GROK_BROWSER_BACKEND"] = backend
                    sys.stderr.write(
                        f"[config] 浏览器后端: {backend} "
                        f"（来自 {path} 的 browser_backend 字段）\n"
                    )
                return
            except (json.JSONDecodeError, OSError):
                pass


_apply_browser_backend()

from backend.web.application import main

if __name__ == "__main__":
    main()