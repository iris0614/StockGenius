from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recommendations(risk_level, investment_duration, investment_strategy):
    prompt = f"""
    根据以下用户偏好，推荐适合的美股：
    - 风险偏好：{risk_level}
    - 投资时长：{investment_duration}
    - 投资策略：{investment_strategy}

    请提供 5 只股票，并为每只股票提供简要推荐理由。
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 如果 GPT-4 不可用，使用 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "你是一名金融顾问。"},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"无法生成推荐：{e}"

def run_simulation(investment_amount, investment_period, risk_level):
    prompt = f"""
    根据以下定投计划，生成模拟结果：
    - 每月定投金额：${investment_amount}
    - 定投时长：{investment_period} 个月
    - 风险偏好：{risk_level}

    请提供预期年化收益率、最大回撤，并简要解释模拟结果。
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 如果 GPT-4 不可用，使用 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "你是一名金融分析师。"},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"无法运行模拟：{e}"

def generate_report(risk_level, investment_duration, investment_strategy):
    prompt = f"""
    根据以下信息，生成投资分析报告：
    - 风险偏好：{risk_level}
    - 投资时长：{investment_duration}
    - 投资策略：{investment_strategy}

    报告应包括以下部分：
    1. 推荐股票
    2. 定投模拟结果
    3. 风险分析
    4. 结论
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 如果 GPT-4 不可用，使用 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "你是一名金融顾问。"},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"无法生成报告：{e}"