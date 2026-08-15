"""浏览器生命周期与页面操作适配。

支持通过环境变量 GROK_BROWSER_BACKEND=nexbrowser 切换后端。

当设为 nexbrowser 时，from backend.automation import session 自动解析为
nexbrowser_session 模块，所有现有代码无需修改导入路径。
"""
import os as _os
import sys as _sys

_backend = _os.environ.get("GROK_BROWSER_BACKEND", "")

if _backend == "nexbrowser":
    from . import nexbrowser_session as _session
    _sys.modules[__name__ + ".session"] = _session
else:
    from . import session