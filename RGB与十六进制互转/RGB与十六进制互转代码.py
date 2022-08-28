from xlwings.utils import rgb_to_int
from xlwings.utils import int_to_rgb

def rgb2hex(r,g,b):   # 定义一个 RG B颜色转 16 进制的函数
    try:    # 尝试获取 RGB 值的输入
        if int(r) < 0 or int(r) > 255 or int(g) < 0 or int(g) > 255 or int(b) < 0 or int(b) > 255:   # 如果 RGB 的值不在 0 - 255 之间，就打印一条提示语
            print('RGB请输入0-255之间的整数！\n')   # 提示语
        else:   # RGB 的值在 0 - 255 之间就继续执行
            pass
    except ValueError:   # 如果引发了类型错误也会打印一条提示语
        print('RGB请输入0-255之间的整数！\n')

    hex_r = hex(r)[2:].upper()   # 10 进制转 16 进制，并去掉 16 进制前面的“0x”，再把得出的结果转为大写
    hex_g = hex(g)[2:].upper()
    hex_b = hex(b)[2:].upper()
    hex_r0 = hex_r.zfill(2)   # 位数不足2位时补“0”
    hex_g0 = hex_g.zfill(2)
    hex_b0 = hex_b.zfill(2)

    result = hex_r0 + hex_g0 + hex_b0   # 得到最终结果（格式如“#ff0402”）
    return result


def hex2rgb(hex_color):   # 定义一个 16 进制转 RGB 颜色的函数
    if hex_color[0] != '#' or len(hex_color) != 7:   # 如果 16 进制颜色前面没有“#”或 16 进制字符串的长度不为 7 ，就打印一条提示语
        print('请输入标准的16进制颜色，以“#”开头，字符长度为7！\n')
    else:   # 如果 16 进制颜色符合标准
        try:   # 尝试进行 16 进制转 10 进制
            r = int('0x' + hex_color[1:3],16)   # 16 进制颜色格式如“#ff0402”，提取出其中的“ff”、“04”、“02”三个 16 进制数字，并在前面加上“0x”，表示 16 进制
            g = int('0x' + hex_color[3:5],16)
            b = int('0x' + hex_color[5:7],16)
        except ValueError:   # 如果引发了类型错误也会打印一条提示语
            print('请输入标准的16进制颜色，以“#”开头，字符长度为7！\n')

    result = '(' + str(r) + ',' + str(g) + ',' + str(b) + ')'   # 得到 RGB 值，用“,”分开
    return result


def main():
    hex = rgb2hex(255,0,0)
    rgb = hex2rgb('#FF0000')
    num = rgb_to_int((255,34,86))
    rgb2 = int_to_rgb(5645055)

    print(hex,rgb,num,rgb2)

if __name__ == '__main__':
    main()