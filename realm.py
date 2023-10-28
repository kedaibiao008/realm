import requests
import re
import time
import logging
import os

# 配置日志
logging.basicConfig(filename="crawler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 定义初始 number 和 URL
number = 5127
base_url = "https://ep.atomicals.xyz/proxy/blockchain.atomicals.get?params=[{}]&pretty"

# 保存文件的目标目录
target_directory = os.path.expanduser("~/atom/ok")

# 创建目标目录（如果不存在）
os.makedirs(target_directory, exist_ok=True)

# 无限循循环
while True:
    url = base_url.format(number)

    # 发送 GET 请求
    try:
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            data = response.text
            match = re.search(r'"request_realm": "(.*?)"', data)
            if match:
                request_realm = match.group(1)
                print("提取到的数据为:", request_realm)

                # 将数据写入文件
                with open(os.path.join(target_directory, "realmbase.txt"), "a") as file:
                    file.write(request_realm + "\n")

                # 重置重试计数
                number += 1
            else:
                print("未找到匹配的数据")
                # 没有匹配到数据，增加 number 并继续下一次循环
                number += 1
        else:
            print("请求失败，状态码:", response.status_code)
            if response.status_code == 500:
                # 如果状态码为 500，等待一段时间后重试
                time.sleep(10)  # 等待10秒后重试
            else:
                # 如果状态码不是 500，记录错误信息
                logging.error("请求失败，状态码: %d", response.status_code)

    except requests.exceptions.RequestException as e:
        print("请求异常:", str(e))
        # 记录异常信息
        logging.error("请求异常: %s", str(e))

    # 添加一些延时以避免太快地发送请求
    time.sleep(1)

# 关闭日志
logging.shutdown()
