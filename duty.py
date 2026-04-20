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
        reader = csv.reader(f, delimiter="\t")  # 支持制表符分隔的CSV
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
today_slash = beijing_time.strftime("%Y/%-m/%-d")  # 2026/4/10 格式
today_normal = beijing_time.strftime("%Y-%m-%d")

# 优先匹配 csv 格式
name = duty_map.get(today_slash, duty_map.get(today_normal, "暂无排班"))

# 生成消息
if name in ["假期", "暂无排班"]:
    content = "🎉 今日休息，无需值班～"
    mentioned_list = []
else:
    content = f"📢 今日值班：@{name}"
    mentioned_list = [name]

# 发送消息
payload = {
    "msgtype": "text",
    "text": {
        "content": content,
        "mentioned_list": mentioned_list
    }
}

try:
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()

    # =============== 自动输出 UserID 核心代码 ===============
    print("✅ 运行成功")
    print(f"📅 今日日期：{today_slash}")
    print(f"👤 值班姓名：{name}")
    print(f"🔍 微信返回完整结果：{result}")

    # 这里会直接打印出 【值班人真实 UserID】
    if "mentioned_list" in result:
        print(f"\n🎉 【重要】当前值班人 UserID：{result['mentioned_list']}")
    if "invaliduser" in result:
        print(f"\n⚠️ 无效用户名：{result['invaliduser']}")
    # ======================================================

except Exception as e:
    print(f"❌ 发送失败：{str(e)}")
