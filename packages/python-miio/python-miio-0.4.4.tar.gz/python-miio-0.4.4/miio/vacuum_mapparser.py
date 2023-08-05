#!/usr/bin/env python3
# See https://github.com/marcelrv/XiaomiRobotVacuumProtocol/blob/master/RRMapFile/RRFileFormat.md
# original from https://github.com/dgiese/dustcloud/blob/master/devices/xiaomi.vacuum.gen1/mapextractor/extractor.py

# /mnt/data/rockrobo/robot.db


import sqlite3, gzip, io, struct, sys, argparse
from datetime import datetime
import io
from PIL import Image, ImageDraw, ImageChops

def read_int(data):
    return struct.unpack('<i', data.read(4))[0]


def read_short(data):
    return struct.unpack('<h', data.read(2))[0]


class MapParser:

    def __init__(self):
        pass

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d



    def build_live_map(self, slam_log_data, map_image_data):
        """
        Parses the slam log to get the vacuum path and draws the path into
        the map. Returns the new map as a BytesIO.
        Thanks to CodeKing for the algorithm!
        https://github.com/dgiese/dustcloud/issues/22#issuecomment-367618008
        """
        map_image = Image.open(io.BytesIO(map_image_data))
        map_image = map_image.convert('RGBA')

        # calculate center of the image
        center_x = map_image.size[0] / 2
        center_y = map_image.size[0] / 2

        # rotate image by -90°
        map_image = map_image.rotate(-90)

        red = (255, 0, 0, 255)
        grey = (125, 125, 125, 255)  # background color
        transparent = (0, 0, 0, 0)

        # prepare for drawing
        draw = ImageDraw.Draw(map_image)

        # loop each line of slam log
        prev_pos = None
        for line in slam_log_data.split("\n"):
            # find positions
            if 'estimate' in line:
                d = line.split('estimate')[1].strip()

                # extract x & y
                y, x, z = map(float, d.split(' '))

                # set x & y by center of the image
                # 20 is the factor to fit coordinates in in map
                x = center_x + (x * 20)
                y = center_y + (y * 20)

                pos = (x, y)
                if prev_pos:
                    draw.line([prev_pos, pos], red)
                prev_pos = pos

        # draw current position
        def ellipsebb(x, y):
            return x - 3, y - 3, x + 3, y + 3

        draw.ellipse(ellipsebb(x, y), red)

        # rotate image back by 90°
        map_image = map_image.rotate(90)

        # crop image
        bgcolor_image = Image.new('RGBA', map_image.size, grey)
        cropbox = ImageChops.subtract(map_image, bgcolor_image).getbbox()
        map_image = map_image.crop(cropbox)

        # and replace background with transparent pixels
        pixdata = map_image.load()
        for y in range(map_image.size[1]):
            for x in range(map_image.size[0]):
                if pixdata[x, y] == grey:
                    pixdata[x, y] = transparent

        temp = io.BytesIO()
        map_image.save(temp, format="png")
        return temp


    def parse_database(self, db):
        do_coloring = True
        output_folder = '/tmp/testmiio/'
        with sqlite3.connect(db) as conn:
            conn.row_factory = self.dict_factory
            for row in conn.cursor().execute('SELECT * FROM cleanmaps'):

                self.parse(row['begin'], io.BytesIO(row['map']), do_coloring, output_folder)

    def make_file_name(self, output_folder, timestamp, map_index):
        return '%s/%s_%d' % (output_folder, datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H.%M.%S'), map_index)

    def charger(self, data):
        pos_x = read_int(data)
        pos_y = read_int(data)
        return (pos_x, pos_y)

    def grayscale_color(pixel):
        if pixel == 1:  # wall pixel
            return 128  # gray color
        else:  # outside, inside or unknown pixel
            return pixel

    def rgb_color(self, pixel):
        if pixel == 1:  # wall pixel
            return [105, 207, 254]
        elif pixel == 255:  # inside pixel
            return [33, 115, 187]
        else:  # outside or unknown pixel
            return [pixel, pixel, pixel]

    # http://netpbm.sourceforge.net/doc/pgm.html
    def export_image_grayscale(self, data, image_len, output_file):
        if image_len == 0:
            print('Warning: %s - empty image. Will not extract.')
            return

        top = read_int(data)
        left = read_int(data)
        height = read_int(data)
        width = read_int(data)
        print("  top: %s left: %s" % (top, left))
        print("  h: %s w: %s" % (height, width))

        pixels = [self.grayscale_color(p) for p in data.read(image_len)]

        output_file.write(('P5\n%d %d\n255\n' % (width, height)).encode())
        for h in range(height)[::-1]:
            output_file.write(bytes(pixels[h * width: h * width + width]))


    # http://netpbm.sourceforge.net/doc/ppm.html
    def export_image_colored(self, data, image_len, output_file):
        if image_len == 0:
            print('Warning: %s - empty image. Will not extract.')
            return

        top = read_int(data)
        left = read_int(data)
        height = read_int(data)
        width = read_int(data)
        print("  top: %s left: %s" % (top, left))
        print("  h: %s w: %s" % (height, width))
        rgb_width = width * 3

        if image_len != (height * width):
            raise Exception("invalid image block length")

        pixels = [rgb for pixel in data.read(image_len) for rgb in self.rgb_color(pixel)]

        output_file.write(('P6\n%d %d\n255\n' % (width, height)).encode())
        for h in range(height)[::-1]:
            output_file.write(bytes(pixels[h * rgb_width: h * rgb_width + rgb_width]))


    def path(self, data, block_size, charger_pos, output_file):
        set_point_length = read_int(data)
        print("  set_point_length: %s" % set_point_length)
        set_point_size = read_int(data)
        print("  set_point_size: %s" % set_point_size)
        set_angle = read_int(data)
        print("  set_angle: %s" % set_angle)
        image_width = (read_short(data), read_short(data))
        print("  image_width: %s" % (image_width,))

        if (set_point_length * set_point_size) != block_size:
            raise Exception("path block size invalid")


        # extracting path
        path = [(read_short(data), read_short(data)) for _ in range(set_point_length)]

        # rescaling coordinates
        path = [((p[0]) // 50, (p[1]) // 50) for p in path]
        charger_pos = ((charger_pos[0]) // 50, (charger_pos[1]) // 50)

        # Creating image
        width, height = image_width[0] // 25, image_width[1] // 25

        pixels = [0] * width * height

        for x, y in path:
            pixels[y * width + x] = 155

        for off_x in range(-2, 2):
            for off_y in range(-2, 2):
                idx = (charger_pos[1] + off_y) * width + charger_pos[0] + off_x
                pixels[idx] = 255


        output_file.write(('P5\n%d %d\n255\n' % (width, height)).encode())
        for h in range(height)[::-1]:
            output_file.write(bytes(pixels[h * width: h * width + width]))


    def parse(self, timestamp, bytes, do_coloring, output_folder):
        data = gzip.GzipFile(fileobj=bytes)

        magic = data.read(2)
        #print(magic)
        #if magic != b'rr':
        #    raise Exception("invalid packet magic")

        header_len = read_short(data)
        if header_len != 20:
            raise Exception("uknown header len %s" % header_len)

        checksum_pointer = data.read(4)
        major_ver = read_short(data)
        minor_ver = read_short(data)

        if (major_ver, minor_ver) != (1, 0):
            raise Exception("Unsupported version %s %s" % (major_ver, minor_ver))

        map_index = read_int(data)
        map_sequence = read_int(data)



        #print("magic: %s" % magic)
        print("checksum_ptr: %s" % checksum_pointer)
        #print("header len: %s" % header_len)
        #print("version: %s %s" % (major_ver, minor_ver))


        print("map_idx: %s map_seq: %s" % (map_index, map_sequence))

        charger_pos = (-1, -1)
        while True:
            block_type = read_short(data)
            unknown = data.read(2)
            block_size = read_int(data)
            print("block type: %s (size: %s)" % (block_type, block_size))
            print("  unknown (flags?): %s" % unknown)
            if block_type == 1:
                charger_pos = self.charger(data)
                print("  charger pos: %s" % (charger_pos, ))
            elif block_type == 2:
                #if charger_pos == (-1, -1):
                #    print("  NO CHARGER POSITION KNOWN, cannot save")
                #    return
                if do_coloring:
                    color_file_name = self.make_file_name(output_folder, timestamp, map_index) + '.ppm'
                    with open(color_file_name, 'wb') as output_file:
                        self.export_image_colored(data, block_size, output_file)
                else:
                    grayscale_file_name = self.make_file_name(output_folder, timestamp, map_index) + '.pgm'
                    with open(grayscale_file_name, 'wb') as output_file:
                        self.export_image_grayscale(data, block_size, output_file)
            elif block_type == 3:
                if charger_pos == (-1, -1):
                    print("  NO CHARGER POSITION KNOWN, cannot save")
                    return
                path_file_name = self.make_file_name(output_folder, timestamp, map_index) + '_path.pgm'
                with open(path_file_name, 'wb') as output_file:
                    self.path(data, block_size, charger_pos, output_file)
            elif block_type == 20:
                break
            else:
                print("  unknown block type %s with size %s" % (block_type, block_size))
                print("    hex: %s" % data.read(block_size).hex())
                continue #break


def main():
    parser = argparse.ArgumentParser(description='Map Extractor for Xiaomi Vacuum.\n'.format(sys.argv[0]))
    parser.add_argument('-c', '--color', dest='color', action='store_true', help='Color extracted image')
    parser.add_argument('-o', '--output', dest='output', type=str, default='.', help='Output folder')
    parser.add_argument('-f', '--file', dest='file', type=str, required=True,
                        help="Path to database file (found in '/mnt/data/rockrobo/robot.db' on vacuum)")

    args, external = parser.parse_known_args()

    file = args.file
    do_coloring = args.color
    output_folder = args.output

    with sqlite3.connect(file) as conn:
        for row in conn.cursor().execute('SELECT * FROM cleanmaps'):
            parse(row[0], io.BytesIO(row[2]), do_coloring, output_folder)


if __name__ == '__main__':
    main()
