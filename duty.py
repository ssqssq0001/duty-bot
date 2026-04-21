import requests
import csv
from datetime import datetime, timedelta

# ====================== 只改这里 ======================
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=792b09d9-335a-4fc6-bb63-6f963ea72ded"
# ======================================================

# 读取值班表
def load_duty_table():
    duty_map = {}
    try:
        with open("duty.csv", "r", encoding="utf-8") as f:            
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if len(row) >= 2:
                    date = row[0].strip()
                    name = row[1].strip()
                    duty_map[date] = name
    except Exception as e:
        print(f"读取CSV失败: {e}")
    return duty_map

duty_map = load_duty_table()

# 北京时间
beijing_time = datetime.utcnow() + timedelta(hours=8)
today_str = beijing_time.strftime("%Y/%-m/%-d")  # 2026/4/21（Linux/GitHub可用）

print(f"📅 今天日期(匹配用)：{today_str}")
name = duty_map.get(today_str, "暂无排班")

# 构造消息
if name in ["假期", "暂无排班"]:
    content = "🎉 今日休息，无需值班～"
    mentioned_list = []
else:
    content = f"📢 今日值班：@{name}"
    mentioned_list = [name]

payload = {
    "msgtype": "text",
    "text": {
        "content": content,
        "mentioned_list": mentioned_list
    }
}

# 发送
try:
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    result = resp.json()
    print("✅ 推送成功")
    print(f"👤 值班人：{name}")
    print(f"📩 微信返回：{result}")
except Exception as e:
    print(f"❌ 发送失败：{str(e)}")
