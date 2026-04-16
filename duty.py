import requests
from datetime import datetime, timedelta


# 把这里换成你的企业微信机器人 WebHook 地址
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=792b09d9-335a-4fc6-bb63-6f963ea72ded"
# ================================================================

# 排班表（直接在这里增删改日期和人名）
duty_map = {
    "2025-04-01": "顾余晨",
    "2025-04-02": "林卓怡",
    "2025-04-03": "刘月溪",
    "2025-04-06": "假期",
    "2025-04-07": "白镁慧",
    "2025-04-08": "郦莜扬",
    "2025-04-09": "王芷慧",
    "2025-04-10": "孙嗣琦",
    "2025-04-13": "归燕婷",
    "2025-04-14": "邵方",
    "2025-04-15": "顾余晨",
    "2025-04-16": "林卓怡",
    "2025-04-17": "刘月溪",
    "2025-04-20": "白镁慧",
    "2025-04-21": "郦莜扬",
    "2025-04-22": "王芷慧",
    "2025-04-23": "孙嗣琦",
    "2025-04-24": "归燕婷",
    "2025-04-27": "邵方",
    "2025-04-28": "顾余晨",
    "2025-04-29": "林卓怡",
    "2025-04-30": "刘月溪",
}

# 自动获取【北京时间】，不会时区错乱
beijing_time = datetime.now() + timedelta(hours=8)
today = beijing_time.strftime("%Y-%m-%d")
name = duty_map.get(today, "暂无排班")

# 消息内容
if name == "假期":
    content = "🎉 今日休息，无需值班～"
    mentioned_users = []
else:
    content = f"📢 今日值班：@{name}"
    mentioned_users = [name]

# 发送企业微信
payload = {
    "msgtype": "text",
    "text": {
        "content": content,
        "mentioned_list": mentioned_users
    }
}

try:
    resp = requests.post(WEBHOOK_URL, json=payload)
    print(f"✅ 运行成功")
    print(f"📅 今日日期：{today}")
    print(f"👤 值班人员：{name}")
    print(f"📩 发送结果：{resp.json()}")
except Exception as e:
    print(f"❌ 发送失败：{e}")
