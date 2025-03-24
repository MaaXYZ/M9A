def ms_timestamp_diff_to_dhm(timestamp1_ms, timestamp2_ms):
    """
    将两个毫秒级时间戳的差值转换为天-时-分格式

    参数:
        timestamp1_ms (int): 第一个毫秒时间戳
        timestamp2_ms (int): 第二个毫秒时间戳

    返回:
        str: 格式化为"X天-X时-X分"的字符串
    """
    # 计算时间戳之间的绝对差值（毫秒）
    diff_ms = abs(timestamp2_ms - timestamp1_ms)

    # 转换为秒
    diff_seconds = diff_ms / 1000

    # 计算天、小时、分钟
    days = int(diff_seconds // (24 * 3600))
    remaining_seconds = diff_seconds % (24 * 3600)
    hours = int(remaining_seconds // 3600)
    remaining_seconds %= 3600
    minutes = int(remaining_seconds // 60)

    # 返回中文格式的结果
    return f"{days}天-{hours}时-{minutes}分"
