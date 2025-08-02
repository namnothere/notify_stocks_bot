import logging, coloredlogs
from PIL import Image

coloredlogs.install()

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)), resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def concat_images_horizontally(im_list: list[Image.Image], resample=Image.BICUBIC, limit = 3):
    try:
        logging.info("Concat images horizontally")
        lines = [im_list[i:i + limit] for i in range(0, len(im_list), limit)]

        concatenated_lines: list[list[Image.Image]] = []
        for line in lines:
            min_height = min(im.height for im in line)
            line_resize = [im.resize((int(im.width * min_height / im.height), min_height), resample=resample)
                        for im in line]
            concatenated_lines.append(line_resize)

        max_height = sum(line[0].height for line in concatenated_lines)
        # max_height = sum(sum(im.height for im in line) line[0].height for line in concatenated_lines)
        total_width = sum(im.width for im in concatenated_lines[0])

        # dst = Image.new('RGB', (total_width, max_height))
        dst = Image.new('RGB', (total_width, max_height))

        pos_y = 0
        for line in concatenated_lines:
            pos_x = 0
            for im in line:
                dst.paste(im, (pos_x, pos_y))
                pos_x += im.width
            pos_y += im.height

        return dst
    except Exception as e:
        logging.info(im_list)
        logging.error("[concat_images_horizontally] {}".format(e))
        return None
