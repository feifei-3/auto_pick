from paddleocr import PaddleOCR
from collections import defaultdict

ocr = PaddleOCR(use_angle_cls=False, lang='ch')

# 物品名归一化表
normalize_map = {
  '芳 纶': '芳纶',
  '卡 尺': '卡尺'
}

def normalize_name(name):
    name = name.replace(' ', '')
    return normalize_map.get(name, name)

def extract_items_from_image(img_path):
    res = ocr.ocr(img_path, cls=False)
    items = []
    for line in res:
        txt = line[1][0]
        txt = normalize_name(txt)
        # 这里需要自定义解析逻辑：把 OCR 文本解析成物品名、坐标、占格数
        # 示例假设 txt = "芳纶 x1" 或 "卡尺"
        items.append({'name': txt, 'x': 100, 'y': 200, 'size': 1})
    return items