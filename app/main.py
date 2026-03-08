import argparse
import os
import sys
import json
from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [
        {"role": "user", "content": args.p}
    ]
    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            # model="arcee-ai/trinity-large-preview:free",
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "Read",
                        "description": "Read and return the contents of a file",
                        "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                            "type": "string",
                            "description": "The path to the file to read"
                            }
                        },
                        "required": ["file_path"]
                        }
                    }
                }
            ],
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)

    # TODO: Uncomment the following line to pass the first stage
    # print(chat.choices[0].message.content)
    # print(chat.choices[0])

    # tool_calls = chat.choices[0].message.tool_calls
    # if tool_calls:
    #     for tc in tool_calls:
    #         args = json.loads(tc.function.arguments)
    #         if tc.function.name == "Read":
    #             with open(args["file_path"]) as f:
    #                 print(f.read())
    # else:
    #     print(chat.choices[0].message.content)
    
        tool_calls = chat.choices[0].message.tool_calls
        
        if tool_calls:
            assistant_message = {
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls
                ]
            }
            messages.append(assistant_message)
            for tc in tool_calls:
                args = json.loads(tc.function.arguments)
                if tc.function.name == "Read":
                    with open(args["file_path"]) as f:
                        tool_result = f.read()
                    tool_call_id = tc.id
                    content = chat.choices[0].message.content
                    
                    messages.append({"role": "tool", "tool_call_id": tool_call_id, "content": tool_result})
        else:
            print(chat.choices[0].message.content)
            break


if __name__ == "__main__":
    main()
