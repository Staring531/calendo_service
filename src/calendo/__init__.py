"""跨国公共假日 MCP 服务，面向 AI agent/LLM 客户端，支持多语言。"""

__version__ = "0.1.0"

from calendo.china_holidays import ChinaHoliday, list_china_holidays

__all__ = ["ChinaHoliday", "list_china_holidays"]
