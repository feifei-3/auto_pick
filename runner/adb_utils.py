import subprocess, time, random

ADB = 'adb'  # 或者指定到adb可执行路径

def adb_shell(cmd):
    full = [ADB, 'shell'] + cmd.split()
    return subprocess.check_output(full)

def screencap_to_file(local_path='/tmp/screen.png'):
    tmp = '/sdcard/screen.png'
    subprocess.check_call([ADB, 'shell', 'screencap', '-p', tmp])
    subprocess.check_call([ADB, 'pull', tmp, local_path])
    return local_path

def tap(x, y):
    # 随机偏
    rx = x + random.randint(-5, 5)
    ry = y + random.randint(-5, 5)
    subprocess.check_call([ADB, 'shell', 'input', 'tap', str(rx), str(ry)])

def long_press(x, y, ms=500):
    rx = x + random.randint(-5,5)
    ry = y + random.randint(-5,5)
    subprocess.check_call([ADB, 'shell', 'input', 'swipe', str(rx), str(ry), str(rx), str(ry), str(ms)])

def drag(x1,y1,x2,y2,duration=300):
    # 模拟拖拽：swipe from -> to
    x1 += random.randint(-5,5); y1 += random.randint(-5,5)
    x2 += random.randint(-5,5); y2 += random.randint(-5,5)
    subprocess.check_call([ADB, 'shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)])

def is_game_foreground(package):
    out = subprocess.check_output([ADB, 'shell', 'dumpsys', 'window', 'windows'])
    return package.encode() in out

def start_game(package):
    subprocess.check_call([ADB, 'shell', 'monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1'])
    time.sleep(6)