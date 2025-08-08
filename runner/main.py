from curses import napms
import json, time
from tkinter import N
from adb_utils import screencap_to_file, tap, drag, is_game_foreground, start_game
from ocr import extract_items_from_image
from price_manager import PriceManager

config = json.load(open('config.json', 'r', encoding='utf-8'))
npm = PriceManager(config)

MAX_CRASH = config.get('max_crash_count', 3)

def calculate_vpu(item):
    price = npm.get_price(item['name'])
    if price is None:
        return config.get('min_vpu_threshold', 0) / item['size']
    return price / item['size']

while True:
    # 确保游戏在前台
    if not is_game_foreground(config['game_package']):
        start_game(config['game_package'])
        time.sleep(3)

    # 进局检测 -> 使用模板匹配（此处省略）

    # 截图并识别物品
    path = screencap_to_file('/tmp/screen.png')
    items = extract_items_from_image(path)
    items = [it for it in items if it['name'] not in config['blacklist']]
    items.sort(key=lambda it: calculate_vpu(it), reverse=True)

    # 逐个拖入安全箱（坐标需要你填）
    for it in items:
        if it['name'] in config['whitelist']:
            # 强制拾取
            pass
        vpu = calculate_vpu(it)
        if vpu < config.get('min_vpu_threshold', 0):
            continue
        # 拖拽: it['x'], it['y'] -> box_x, box_y
        drag(it['x'], it['y'], 1000, 1800)
        time.sleep(0.3)

    time.sleep(1)