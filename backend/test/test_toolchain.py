import os
import sys

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from app.services.qwen_service import QwenService

# 工具链：文本分析 -> 翻译成英文 -> 英文求解 -> 翻译回中文
class ToolChain:
    def __init__(self, model_name: str = "qwen-turbo", test_mode: bool = True):
        self.qwen = QwenService(model_name=model_name, test_mode=test_mode)

    def text_analysis(self, text: str) -> str:
        prompt = f"请对以下文本进行简要分析，指出其主题和核心问题：\n{text}"
        result = self.qwen.chat_with_qwen(prompt)
        return result.get('message', '')

    def translate_to_english(self, text: str) -> str:
        prompt = f"请将以下内容翻译成英文：\n{text}"
        result = self.qwen.chat_with_qwen(prompt)
        return result.get('message', '')

    def solve_in_english(self, english_text: str) -> str:
        prompt = f"Please answer or solve the following question in English:\n{english_text}"
        result = self.qwen.chat_with_qwen(prompt)
        return result.get('message', '')

    def translate_to_chinese(self, english_text: str) -> str:
        prompt = f"请将以下英文内容翻译成中文：\n{english_text}"
        result = self.qwen.chat_with_qwen(prompt)
        return result.get('message', '')

    def run_chain(self, text: str) -> dict:
        analysis = self.text_analysis(text)
        english = self.translate_to_english(analysis)
        answer_en = self.solve_in_english(english)
        answer_zh = self.translate_to_chinese(answer_en)
        return {
            'analysis': analysis,
            'english': english,
            'answer_en': answer_en,
            'answer_zh': answer_zh
        }

# 简单测试用例
def test_toolchain():
    toolchain = ToolChain()
    input_text = "小明想知道如何高效学习英语，有什么建议？"
    result = toolchain.run_chain(input_text)
    print("文本分析：", result['analysis'])
    print("翻译成英文：", result['english'])
    print("英文回答：", result['answer_en'])
    print("翻译回中文：", result['answer_zh'])

if __name__ == "__main__":
    test_toolchain() 