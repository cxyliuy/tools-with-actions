import whois
import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")

def send_telegram_message(message):
    """通过 Telegram Bot 发送消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Telegram 消息发送成功！")
    else:
        print(f"Telegram 消息发送失败: {response.text}")

def check_domain_availability(domain):
    try:
        # 查询域名信息
        domain_info = whois.whois(domain)
        
        # 如果域名状态包含 'No match for domain'，则表示域名未注册
        if 'No match for domain' in str(domain_info):
            message = f"域名 {domain} 可以购买！"
            print(message)
            send_telegram_message(message)
        else:
            message = f"域名 {domain} 已被注册。"
            print(message)
            send_telegram_message(message)
    except Exception as e:
        error_message = f"查询域名 {domain} 时出错: {e}"
        print(error_message)
        send_telegram_message(error_message)

if __name__ == "__main__":
    domain_names = os.getenv("DOMAIN_NAMES", "").split(",")
    if not domain_names:
        print("未设置域名环境变量 DOMAIN_NAMES")
    else:
        for domain in domain_names:
            domain = domain.strip()
            if domain:
                check_domain_availability(domain)
