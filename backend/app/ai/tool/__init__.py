# app/tool包的初始化文件
# 注意：此文件不再自动导入所有工具，避免全部注册
# 请使用 ToolRegistry 进行按需注册

from .registry import ToolRegistry

__all__ = ['ToolRegistry'] 