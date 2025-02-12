from .maimaidx_image import *
from .maimaidx_tool import *


plate_diy: Dict[str, str] = {}

def show_all_plate():
    # 获取所有 PNG 文件
    png_files = [file for file in other_plate_dir.iterdir() if file.is_file() and file.suffix.lower() == '.png']
    if not png_files:
        print("文件夹中没有 PNG 文件。")
        return

    # 定义布局参数
    num_columns = 3  # 三列布局
    img_width = 720  # 每张图片的宽度
    img_height = 116  # 每张图片的高度
    spacing_x = 20  # 列间距
    spacing_y = 80  # 行间距
    margin = 20  # 边距

    # 计算大图的宽度和高度
    num_images = len(png_files)
    num_rows = (num_images + num_columns - 1) // num_columns  # 计算行数
    total_width = num_columns * (img_width + spacing_x) + margin * 2  # 总宽度
    total_height = num_rows * (img_height + spacing_y) + margin * 2  # 总高度

    # 创建空白大图
    _im = Image.new('RGBA', (total_width, total_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(_im)
    yh_font = DrawText(draw, YAHEI)

    # 拼接图片
    x = margin
    y = margin
    for i, file in enumerate(png_files):
        try:
            with Image.open(file) as img:
                # 调整图片大小
                img = img.resize((img_width, img_height))
                # 计算当前图片的位置
                col = i % num_columns  # 当前列
                row = i // num_columns  # 当前行
                x_pos = x + col * (img_width + spacing_x)
                y_pos = y + row * (img_height + spacing_y)
                # 拼接图片
                _im.alpha_composite(img, (x_pos, y_pos))
                yh_font.draw(x_pos + 20, y_pos + 156, 40, file.name, (0, 0, 0, 255), anchor='lm')
        except Exception as e:
            print(f"无法打开图片 {file.name}: {e}")

    # 显示或保存大图
    return image_to_base64(_im.resize((total_width // 5, total_height // 5)))


async def set_plate_diy(qqid: Optional[Union[str, int]] = None, plate_id: str = None):
    global plate_diy
    flag = -1
    if plate_id == 'default':
        if qqid in plate_diy.keys():
            del plate_diy[qqid]
        flag = 2
    else:
        plate_path = Path(other_plate_dir / f'UI_Plate_{plate_id}.png')
        if plate_path.exists():
            plate_diy[qqid] = plate_path.name
            flag = 0
        else:
            flag = 1

    # 异步写入文件
    await writefile(user_file, plate_diy)
    return flag

async def load_plate_diy():
    global plate_diy
    plate_diy = await openfile(user_file)

