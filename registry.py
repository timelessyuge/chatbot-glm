import pandas as pd
import requests
from zhipuai import ZhipuAI

import os
from dotenv import load_dotenv

load_dotenv()

client = ZhipuAI(api_key=os.getenv('api_key'))
appid=os.getenv('appid')
appsecret=os.getenv('appsecret')

def aqi(city):
    url = (
        f"http://v1.yiketianqi.com/api?version=v10&appid={appid}&appsecret={appsecret}&city={city}"
    )

    response = requests.get(url)
    data = response.json()

    air = data["air"]
    pm25 = data["pm25"]

    return f"{city}当前的空气指数为{air}，pm2.5为{pm25} 🎈"


def weather(city, n_days=1):
    n_days = max(1, n_days)
    n_days = min(7, n_days)

    url = (
        "http://v1.yiketianqi.com/free/week?unescape=1&appid=15642225&appsecret=uK5WmT3Y"
        + f"&city={city}"
    )
    response = requests.get(url)
    weathers = response.json()["data"][:n_days]

    # output = "日期 | 天气 | 白天气温 | 夜间气温 | 风力 |\n"
    # for weather in weathers:
    #     date = weather["date"]
    #     wea = weather["wea"]
    #     tem_day = weather["tem_day"]
    #     tem_night = weather["tem_night"]
    #     win_speed = weather["win_speed"]

    #     output += f"{date} | {wea} | {tem_day} | {tem_night} | {win_speed} |\n"

    # return output+"\n🎈🎈"

    df = pd.DataFrame(weathers)[["date", "wea", "tem_day", "tem_night", "win_speed"]]
    df.columns = ["日期", "天气", "白天气温", "夜间气温", "风力"]

    df.set_index("日期", inplace=True)

    # df = df.set_index('日期', inplace=False)

    return df


def gen_image(prompt):

    model = "cogview-3"
    response = client.images.generations(
        model=model,
        prompt=prompt,
    )

    url = response.data[0].url

    return url, prompt


def gen_image_by_request(city, request):
    df = weather(city)
    wea = df[["天气"]].iloc[0, 0]
    tem_day = df[["白天气温"]].iloc[0, 0]
    win_speed = df[["风力"]].iloc[0, 0]

    prompt = f"{city}今天{wea}，风力{win_speed}，白天气温{tem_day}摄氏度。" + request

    return gen_image(prompt)


tools = [
    {
        "type": "function",
        "function": {
            "name": "aqi",
            "description": "根据用户提供的信息，查询“空气质量”，或者“pm2.5”",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市"},
                    # "prov":{"type":"string"...}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "根据用户提供的信息，查询天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市"},
                    "n_days": {"type": "integer", "description": "天数"},
                    # "prov":{"type":"string"...}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gen_image",
            "description": "根据用户描述，生成图片",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "用户描述"},
                    # "n_days": {"type": "integer", "description": "天数"},
                    # "prov":{"type":"string"...}
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gen_image_by_request",
            "description": "根据城市和用户要求，生成图片",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市"},
                    "request": {"type": "string", "description": "用户要求"},
                    # "n_days": {"type": "integer", "description": "天数"},
                    # "prov":{"type":"string"...}
                },
                "required": ["city"],
            },
        },
    },
]

if __name__ == "__main__":
    print(weather("北京", 5))
