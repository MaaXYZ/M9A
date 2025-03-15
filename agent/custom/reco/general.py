import time
import json
from typing import Union, Optional
import numpy as np

from skimage.metrics import structural_similarity
from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import RectType

from utils import logger


@AgentServer.custom_recognition("IsSimilar")
class IsSimilar(CustomRecognition):
    """
    比较两次截图的相似度，判断屏幕内容是否发生变化。

    参数格式:
    {
        "threshold": 图片匹配阈值，默认0.9，大于等于此值判定为相似
        "roi": 识别区域坐标[x, y, width, height]，默认[0, 0, 0, 0]表示整个屏幕
        "interval_ms": 两次截图间隔时间，单位毫秒，默认100毫秒
        "times": 重复比较次数，取平均值，默认5次
    }

    返回结果:
    如相似度大于等于阈值，返回AnalyzeResult，detail包含:
        - ssim: 相似度值
        - similar: 是否相似
        - values: 所有次数的相似度列表
    如相似度小于阈值，返回None
    """

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> Union[CustomRecognition.AnalyzeResult, Optional[RectType]]:

        try:
            params = json.loads(argv.custom_recognition_param)
            threshold = params.get("threshold", 0.9)
            roi = params.get("roi", [0, 0, 0, 0])
            interval_ms = float(params.get("interval", 100.0))
            times = int(params.get("times", 5))

            logger.info(
                f"开始比较，次数：{times}，间隔：{interval_ms}毫秒，阈值：{threshold}"
            )

            ssim_values = []

            for i in range(times):
                if i > 0:
                    logger.info(f"第 {i+1}/{times} 次比较...")

                img1 = context.tasker.controller.post_screencap().wait().get()

                if roi[2] > 0 and roi[3] > 0:
                    x, y, w, h = roi
                    img1 = img1[y : y + h, x : x + w]

                sleep_seconds = interval_ms / 1000.0
                logger.info(f"等待 {interval_ms} 毫秒...")
                time.sleep(sleep_seconds)

                img2 = context.tasker.controller.post_screencap().wait().get()

                if roi[2] > 0 and roi[3] > 0:
                    x, y, w, h = roi
                    img2 = img2[y : y + h, x : x + w]

                ssim_value = self.compare_ssim(img1, img2)
                ssim_values.append(float(ssim_value))
                logger.info(f"当前ssim: {float(ssim_value):.4f}")

                if i < times - 1:
                    time.sleep(sleep_seconds)

            # 计算平均相似度
            avg_ssim = float(np.mean(ssim_values)) if ssim_values else 0.0
            is_similar = bool(avg_ssim >= threshold)  # 确保是Python原生bool

            logger.info(f"平均ssim: {avg_ssim:.4f}")
            logger.info(f"threshold: {threshold}, similar: {is_similar}")

            # 将所有numpy值转换为Python原生类型
            python_values = [float(v) for v in ssim_values]

            if is_similar:
                return CustomRecognition.AnalyzeResult(
                    box=roi,
                    detail=json.dumps(
                        {
                            "ssim": avg_ssim,
                            "similar": is_similar,
                            "values": python_values,
                        }
                    ),
                )
            else:
                return None

        except Exception as e:
            logger.error(f"IsSimilar 识别过程中出错：{e}")
            return None

    def compare_ssim(self, img1, img2):
        """计算两个图像的相似度，处理所有可能的错误情况"""
        try:
            # 获取图像尺寸
            h1, w1 = img1.shape[0], img1.shape[1]
            h2, w2 = img2.shape[0], img2.shape[1]

            # 检查图像是否足够大
            min_dim = min(h1, w1, h2, w2)

            if min_dim < 2:
                logger.warning("图像尺寸太小(< 2px)，使用像素差异计算")
                diff = np.mean(np.abs(img1.astype(float) - img2.astype(float))) / 255.0
                return float(1.0 - diff)

            # 计算合适的窗口大小
            # SSIM窗口大小必须是奇数
            if min_dim < 7:
                win_size = min_dim if min_dim % 2 == 1 else min_dim - 1
                win_size = max(1, win_size)  # 确保至少为1
                logger.info(f"图像较小，调整窗口大小为 {win_size}")
            else:
                win_size = 7  # 默认窗口大小

            try:
                # 尝试使用新版API (skimage 0.16+)
                ssim = structural_similarity(
                    img1, img2, channel_axis=2, win_size=win_size
                )
            except TypeError:
                # 回退到旧版API
                ssim = structural_similarity(
                    img1, img2, multichannel=True, win_size=win_size
                )

            return float(ssim)  # 确保返回Python原生float类型

        except Exception as e:
            # 捕获所有可能的错误，提供备选计算方法
            logger.warning(f"SSIM计算错误: {e}，使用像素差异替代")
            # 使用简单的像素差异作为备选
            try:
                diff = np.mean(np.abs(img1.astype(float) - img2.astype(float))) / 255.0
                return float(1.0 - diff)
            except Exception as e2:
                logger.error(f"备选方法也失败: {e2}，返回默认值0")
                return 0.0
