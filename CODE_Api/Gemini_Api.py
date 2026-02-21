# GeminiAPI.py
from google import genai


def Gemini_Api_APIKEY():
    USER_GeminiKey_Input  = input("输入你的gemini apikey")
    client = genai.Client(api_key=USER_GeminiKey_Input)
    return client  #client 是以后AIapikey的限定变量名
def Gemini_Api(client,msg,model):
    
    response = client.models.generate_content(
    model=model,contents=msg
)
    return (response.text)#response是AI回答的限定变量名
def Gemini_Api_AIlist(client):
    models = client.models.list()
    return [model.name for model in models]#models是apiAI名称的限定变量名
    
