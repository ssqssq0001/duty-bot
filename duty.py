import requests
import csv
from datetime import datetime, timedelta

# ====================== 只改这里 ======================
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=792b09d9-335a-4fc6-bb63-6f963ea72ded"
# ======================================================

# 从 duty.csv 读取（A列日期，B列姓名）
def load_duty_table():
    duty_map = {}
    with open("duty.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                date = row[0].strip()
                name = row[1].strip()
                duty_map[date] = name
    return duty_map

# 加载值班表
duty_map = load_duty_table()

# 获取北京时间
beijing_time = datetime.now() + timedelta(hours=8)
today = beijing_time.strftime("%Y-%m-%d")
name = duty_map.get(today, "暂无排班")

# 生成消息
if name == "假期":
    content = "🎉 今日休息，无需值班～"
else:
    content = f"📢 今日值班：@{name}"

# 发送（保留 @姓名）
payload = {
    "msgtype": "text",
    "text": {
        "content": content,
        "mentioned_list": [name] if name != "假期" else []
    }
}

try:
    resp = requests.post(WEBHOOK_URL, json=payload)
    print("✅ 运行成功")
    print(f"📅 今日日期：{today}")
    print(f"👤 值班人员：{name}")
    print(f"📩 发送结果：{resp.json()}")
except Exception as e:
    print(f"❌ 发送失败：{e}")
