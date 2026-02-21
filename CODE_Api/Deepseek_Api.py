# DeepSeek_Api.py
from openai import OpenAI

def DeepSeek_Api_APIKEY():
    USER_DeepSeekKey_Input = input("输入你的DeepSeek apikey: ")
    client = OpenAI(
        api_key=USER_DeepSeekKey_Input,
        base_url="https://api.deepseek.com/v1"
    )
    return client

def DeepSeek_Api(client, msg, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": msg}
        ],
        stream=False
    )
    return response.choices[0].message.content

def DeepSeek_Api_AIlist(client):
    models = client.models.list()
    return [model.id for model in models.data]