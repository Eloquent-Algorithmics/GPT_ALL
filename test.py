
# Filename: gemini_pro_expert.py
# Path: plugins\_google_vertex\gemini_pro_expert.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/22

from plugins.plugin_base import PluginBase
from plugins._google_vertex.gemini_pro_tools import GeminiProToolsPlugin
from plugins._google_vertex.gemini_pro_vision_tools import GeminiProVisionToolsPlugin


class GeminiProExpertPlugin(PluginBase):
    """
    This class defines the Google Pro Expert plugin.
    """

    def __init__(self):

        self.gemini_pro_tools_plugin = GeminiProToolsPlugin()
        self.gemini_pro_vision_tools_plugin = GeminiProVisionToolsPlugin()

        super().__init__()

    async def initialize(self):
        # Initialization code if needed
        pass

    def ask_gemini_pro_expert(self, question):
        """
        Ask the controller of the Gemini Pro and Pro Vision model for a response.

        Args:
            question: The question to ask.

        Returns:
            The response from the Gemini Pro controller.
        """
        response = self.ask_gemini_pro_expert(question)
        return response
    
    async def ask_gemini_pro(self, question, generation_config=None, safety_settings=None):
        if generation_config is None:
            generation_config = self.default_generation_config()
        if safety_settings is None:
            safety_settings = self.default_safety_settings()
        self.model.configure(generation_config=generation_config, safety_settings=safety_settings)
        self.convo.send_message(question)
        response_text = self.convo.last.text
        return response_text

    def get_tools(self):
        gemini_expert_tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_gemini_pro_expert",
                    "description": "Ask the controller of the Gemini Pro and Pro Vision model for a response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "q": {
                                "type": "string",
                                "description": "Query to ask Gemini Pro.",
                            },
                        },
                        "required": ["q"],
                    },
                },
            },
        ]

        self.tools.extend(gemini_expert_tools)

        available_functions = {
            "ask_gemini_pro_expert": self.ask_gemini_pro_expert,
        }

        return available_functions, self.tools
