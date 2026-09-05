"""通用工具函数"""

import re

# Windows/Linux 文件系统不允许出现在文件名中的字符
_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


def sanitize_filename(name):
    """将文件名中的非法字符替换为下划线"""
    return _INVALID_FILENAME_CHARS.sub("_", name)
