import math

'''使用 math 库进行向上、向下取整'''
print(f'对 2.675 向上取整：{math.ceil(2.675)}')
print(f'对 2.135 向上取整：{math.ceil(2.135)}')
print(f'对 2.675 向下取整：{math.floor(2.675)}')
print(f'对 2.135 向下取整：{math.floor(2.135)}')
print('========================================================================================================')

'''使用 round 函数对浮点数进行不精确四舍五入'''
print(f'使用 round 函数对 2.675 取小数点后 2 位：{round(2.675,2)}')
print(f'使用 round 函数对 2.135 取小数点后 2 位：{round(2.135,2)}')
print('========================================================================================================')

'''使用 decimal 库对浮点数进行精确四舍五入'''
from decimal import *

x = Decimal('2.675')
y = Decimal('2.135')
print('使用 decimal 库的 ROUND_HALF_UP 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_HALF_UP)))
print('使用 decimal 库的 ROUND_HALF_UP 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_HALF_UP)))
print('========================================================================================================')

'''decimal 库 quantize() 方法的 rounding 参数'''
# ROUND_CEILING：舍入方向为正无穷
# ROUND_DOWN ：舍入方向为零
# ROUND_FLOOR ：舍入方向为负无穷
# ROUND_HALF_DOWN ：舍入到最接近的数，同样接近则舍入方向为零
# ROUND_HALF_EVEN ：舍入到最接近的数，同样接近则舍入到最接近的偶数（默认值）
# ROUND_HALF_UP ：舍入到最接近的数，同样接近则舍入到零的反方向
# ROUND_UP ：舍入到零的反方向
# ROUND_05UP ：如果最后一位朝零的方向舍入后为 0 或 5 则舍入到零的反方向；否则舍入方向为零
print('使用 decimal 库的 ROUND_CEILING 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_CEILING)))
print('使用 decimal 库的 ROUND_CEILING 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_CEILING)))
print('使用 decimal 库的 ROUND_DOWN 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_DOWN)))
print('使用 decimal 库的 ROUND_DOWN 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_DOWN)))
print('使用 decimal 库的 ROUND_FLOOR 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_FLOOR)))
print('使用 decimal 库的 ROUND_FLOOR 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_FLOOR)))
print('使用 decimal 库的 ROUND_HALF_DOWN 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_HALF_DOWN)))
print('使用 decimal 库的 ROUND_HALF_DOWN 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_HALF_DOWN)))
print('使用 decimal 库的 ROUND_HALF_EVEN 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_HALF_EVEN)))
print('使用 decimal 库的 ROUND_HALF_EVEN 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_HALF_EVEN)))
print('使用 decimal 库的 ROUND_UP 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_UP)))
print('使用 decimal 库的 ROUND_UP 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_UP)))
print('使用 decimal 库的 ROUND_05UP 参数对 2.675 取小数点后 2 位：{}'.format(x.quantize(Decimal('1.00'),rounding=ROUND_05UP)))
print('使用 decimal 库的 ROUND_05UP 参数对 2.135 取小数点后 2 位：{}'.format(y.quantize(Decimal('1.00'),rounding=ROUND_05UP)))
print('========================================================================================================')

'''使用 format 进行指定位数截断'''
print('保留 2.675 小数点后 2 位：{:.2f}'.format(2.675))
print('保留 2.135 小数点后 2 位：{:.2f}'.format(2.135))
print('========================================================================================================')

'''使用 / 进行除法'''
print('对 2.675 进行除法：{}'.format(2.675 / 2))
print('对 2.135 进行除法：{}'.format(2.135 / 2))
print('========================================================================================================')

'''使用 // 进行整除'''
print('对 2.675 进行整除：{}'.format(int(2.675 // 2)))
print('对 2.135 进行整除：{}'.format(int(2.135 // 2)))
print('========================================================================================================')

'''使用 % 进行取余'''
print('对 2.675 进行取余：{:.2f}'.format(2.675 % 2))
print('对 2.135 进行取余：{:.2f}'.format(2.135 % 2))
print('========================================================================================================')
