import os
import re
import asyncio
from quart import Quart, request, jsonify, send_file, send_from_directory
from quart_cors import cors
from hypercorn.config import Config
from hypercorn.asyncio import serve
from config import MAIN_SYSTEM_PROMPT
from app import run_conversation, enable_plugins
from utils.openai_model_tools import (
    ask_chat_gpt_4_0314_synchronous,
    ask_chat_gpt_4_0314_asynchronous,
    ask_chat_gpt_4_32k_0314_synchronous,
    ask_chat_gpt_4_32k_0314_asynchronous,
    ask_chat_gpt_4_0613_synchronous,
    ask_chat_gpt_4_0613_asynchronous,
    ask_gpt_4_vision,
)
from utils.openai_dalle_tools import generate_an_image_with_dalle3
from utils.core_tools import get_current_date_time

app = Quart(__name__)
app = cors(app, allow_origin="*")


@app.route("/")
async def index():
    return await send_file("templates/index.html")


@app.route("/static/<path:path>")
async def send_static(path):
    return await send_from_directory("static", path)


def format_response_text(response_text):
    response_text = response_text.replace("[View Image]", "<strong>View Image</strong>")
    
    # Match any character that's not a whitespace until the next space or end of line
    url_pattern = r"(https://oaidalleapiprodscus/.blob/.core/.windows/.net/private/org-[^\s]+)"
    response_text = re.sub(url_pattern, r'<a href="\1" target="_blank">View Image</a>', response_text)

    lines = response_text.split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    response_text = "<br>".join(lines)

    return response_text


available_functions = {
    "get_current_date_time": get_current_date_time,
    "ask_chat_gpt_4_0314_synchronous": ask_chat_gpt_4_0314_synchronous,
    "ask_chat_gpt_4_0314_asynchronous": ask_chat_gpt_4_0314_asynchronous,
    "ask_chat_gpt_4_32k_0314_synchronous": ask_chat_gpt_4_32k_0314_synchronous,
    "ask_chat_gpt_4_32k_0314_asynchronous": ask_chat_gpt_4_32k_0314_asynchronous,
    "ask_chat_gpt_4_0613_synchronous": ask_chat_gpt_4_0613_synchronous,
    "ask_chat_gpt_4_0613_asynchronous": ask_chat_gpt_4_0613_asynchronous,
    "generate_an_image_with_dalle3": generate_an_image_with_dalle3,
    "ask_gpt_4_vision": ask_gpt_4_vision,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date_time",
            "description": "Get the current date and time from the local machine.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_0314_synchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_0314_asynchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_32k_0314_synchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_32k_0314_asynchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_0613_synchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                    "tools": {
                        "type": "string",
                        "description": "The tools to use for the request.",
                    },
                    "tool_choice": {
                        "type": "string",
                        "description": "The tool choice to use for the request.",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_chat_gpt_4_0613_asynchronous",
            "description": "Ask a more experienced colleague for assistance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "integer",
                        "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                    },
                    "question": {
                        "type": "string",
                        "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
                    },
                    "text": {
                        "type": "string",
                        "description": "The text to be analyzed",
                    },
                    "tools": {
                        "type": "string",
                        "description": "The tools to use for the request.",
                    },
                    "tool_choice": {
                        "type": "string",
                        "description": "The tool choice to use for the request.",
                    },
                },
                "required": ["question", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_gpt_4_vision",
            "description": "Ask GPT-4 Vision a question about a specific image file located in the 'uploads' folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_name": {
                        "type": "string",
                        "description": "The name of the image file in the 'uploads' folder.",
                    },
                },
                "required": ["image_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_an_image_with_dalle3",
            "description": "Generate an image with DALL-E 3.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to use for image generation.",
                    },
                    "n": {
                        "type": "integer",
                        "description": "The number of images to generate.",
                    },
                    "size": {
                        "type": "string",
                        "description": "The image size to generate.",
                    },
                    "quality": {
                        "type": "string",
                        "description": "The image quality to generate.",
                    },
                    "style": {
                        "type": "string",
                        "description": "The image style to generate. natural or vivid",
                    },
                    "response_format": {
                        "type": "string",
                        "description": "The response format to use for image generation b64_json or url.",
                    },
                },
                "required": ["prompt"],
            },
        },
    },
]


@app.route("/chat", methods=["POST"])
async def chat():
    data = await request.json
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    memory = data.get("memory", [])
    mem_size = data.get("mem_size", 200)

    base_functions, plugin_tools = await enable_plugins({}, [])
    all_functions = {**available_functions, **base_functions}

    final_response, memory = await run_conversation(
        messages=[
            {"role": "system", "content": f"{MAIN_SYSTEM_PROMPT}"},
            {"role": "assistant", "content": "Understood. As we continue, feel free to direct any requests or tasks you'd like assistance with. Whether it's querying information, managing schedules, processing data, or utilizing any of the tools and functionalities I have available."},
            {"role": "user", "content": f"{user_input}"},
        ],
        tools=tools + plugin_tools,
        available_functions=all_functions,
        original_user_input=user_input,
        mem_size=mem_size,
        memory=memory,
    )

    response_message = final_response.choices[0].message
    response_text = response_message.content if response_message.content is not None else "I'm not sure how to help with that."

    response_text = format_response_text(response_text)

    return jsonify({"response": response_text, "memory": memory})


if __name__ == "__main__":
    config = Config()
    port = int(os.environ.get("PORT", 8080))
    config.bind = [f"0.0.0.0:{port}"]
    asyncio.run(serve(app, config))
