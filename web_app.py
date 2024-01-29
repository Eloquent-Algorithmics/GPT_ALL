import asyncio
from quart import Quart, request, jsonify, send_file, send_from_directory
from quart_cors import cors
from app import run_conversation, enable_plugins
from config import MAIN_SYSTEM_PROMPT
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Quart(__name__)
app = cors(app, allow_origin="*")


@app.route("/")
async def index():
    return await send_file("index.html")


@app.route("/static/<path:path>")
async def send_static(path):
    return await send_from_directory("static", path)


@app.route("/chat", methods=["POST"])
async def chat():
    data = await request.json
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    memory = data.get("memory", [])
    mem_size = data.get("mem_size", 200)

    available_functions, tools = await enable_plugins({}, [])

    final_response, memory = await run_conversation(
        messages=[
            {"role": "system", "content": f"{MAIN_SYSTEM_PROMPT}"},
            {"role": "assistant", "content": "Understood. As we continue, feel free to direct any requests or tasks you'd like assistance with. Whether it's querying information, managing schedules, processing data, or utilizing any of the tools and functionalities I have available, I'm here to help. Just let me know what you need, and I'll do my best to assist you effectively and efficiently."},
            {"role": "user", "content": f"{user_input}"},
        ],
        tools=tools,
        available_functions=available_functions,
        original_user_input=user_input,
        mem_size=mem_size,
        memory=memory,
    )

    response_message = final_response.choices[0].message
    response_text = response_message.content if response_message.content is not None else "I'm not sure how to help with that."

    return jsonify({"response": response_text, "memory": memory})


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    asyncio.run(serve(app, config))
