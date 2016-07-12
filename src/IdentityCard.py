# -*- coding: utf-8 -*-

import sys
import datetime
import calendar
import xml.etree.ElementTree as ET
import random
import math
from optparse import OptionParser
from AreaInfo import XML_STRING

__VERSION = '0.0.2'

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class IdentityCard(object):
    """docstring for GenerateID"""

    def __init__(self, num=1, min_age=0, max_age=100, sex=0, birth=None):
        self.__areas = []

    def initialize_areas(self):
        root = ET.fromstring(XML_STRING)
        for child in root:
            self.__areas.append(child.attrib)

    def __random_card_number(self, min_age=0, max_age=100, sex=0, year=0, month=0, day=0):
        area = ''
        while True:
            rd = random.randint(1, len(self.__areas))
            area = self.__areas[rd - 1]['code']
            if area[-2:] != "00":
                break

        code = ''
        order_code = '0'
        code_number = ''

        if sex == 0:
            code = str(random.randint(1000, 9999))
        else:
            while True:
                code = str(random.randint(1000, 9999))
                order_code = code[0:3]
                if (sex == 1 and int(order_code) % 2 == 0) or (sex == 2 and int(order_code) % 2 != 0):
                    break

        now = datetime.datetime.now()
        _year = year if year else now.year - random.randint(min_age, max_age)
        flag = (_year == now.year or _year == now.year - min_age)
        _month = month if month else random.randint(1, now.month) if flag else random.randint(1, 12)
        _day = day if day else (random.randint(1, now.day) if flag else random.randint(
            1, calendar.monthrange(_year, _month)[1]))

        birthday = datetime.datetime(_year, _month, _day)

        code_number = area + datetime.datetime.strftime(birthday, '%Y%m%d') + code

        sum = 0.0
        check_code = None
        for i in range(2, 19):
            sum += int(code_number[18 - i], 16) * (math.pow(2, i - 1) % 11)

        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        check_code = check_codes[int(sum % 11)]
        idcard_number = code_number[0:17] + check_code

        return idcard_number

    def generator(self, num=1, *args, **kwargs):
        idcards = []

        while len(idcards) < num:
            idcard = self.__analysis(self.__random_card_number(*args, **kwargs))
            if idcard not in idcards:
                idcards.append(idcard)

        return idcards

    def __analysis(self, idcard_number):
        prov_code = idcard_number[0:2].ljust(6).replace(' ', '0')
        area_code = idcard_number[0:4].ljust(6).replace(' ', '0')
        city_code = idcard_number[0:6].ljust(6).replace(' ', '0')
        address = []
        for a in self.__areas:
            if prov_code == a['code']:
                address.append(a['name'])
            if area_code == a['code']:
                address.append(a['name'])
            if city_code == a['code']:
                address.append(a['name'])
            if len(address) == 3:
                break
        addr = ''.join(
            reduce(lambda x, y: x if y in x else x + [y], [[], ] + address))
        age_code = idcard_number[6:14]
        try:
            year = age_code[0:4]
            month = age_code[4:6]
            day = age_code[-2:]
            age = self.__get_age(datetime.datetime(
                int(year), int(month), int(day)))
        except:
            raise

        order_code = idcard_number[14:17]
        sex = u'女' if int(order_code) % 2 == 0 else u'男'

        return (self.__gen_name(), idcard_number, '{0}-{1}-{2}'.format(year, month, day), str(age), str(sex), addr)

    def __get_age(self, born):
        today = datetime.datetime.today()
        try:
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day - 1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def __gen_name(self):
        x = u"王陈张李周杨吴黄刘徐朱胡沈潘章程方孙郑金叶汪何马赵林蒋俞姚许丁施高余谢董汤钱卢江蔡宋曹邱罗杜郭戴洪唐袁夏童肖姜傅范顾梅盛吕诸邵陆彭韩倪雷郎梁楼万龚储鲍严葛华应冯项崔魏毛阮邹喻曾邓熊任陶费凌虞裘涂苏翁莫卞史季康管黎孔田单娄宣钟饶鲁廖于韦甘石孟柳祝胥殷舒褚薛白向邬尚竺查谈贾温游谭开伍庄成沙柏郝秦尉麻詹赖裴颜尹巴乐厉谷易段钮骆笪阎缪臧樊操卜丰文水兰包平乔伊有牟邢劳来求沃芮闵欧郏柯贺闻桂耿戚符蓝路阚滕霍上卫干支牛计车左申艾仲刑匡印吉宇安戎毕池纪过佘冷时束花迟邰卓宓宗官庞於明练苗茅郁冒洑相郤郦钦奚席晋晏柴聂宿密屠常鄂惠琚窦简蒿阙穆濮"
        m = u"华明芳琴红萍文丽金荣国英珍月云平美海林志玉建伟春玲晓爱秀霞燕根新凤德成敏生民小亚梅强忠军良永飞雪芬莲宝娣斌水兰祥学勇福娟峰菊青桂卫富龙贵娥莉彩兴安慧珠庆旭法艳惠群秋世有佳立家清义丹正宏炳银贤培锋中仁元香长如花才友刚利连东江洪胜君昌俊星光波顺婷一和康吉亮喜琳颖仙发杰鸣勤蓉静传欢兵振维晶辉双方礼松彬淑来涛素莹超木芸武浩道天冬巧先宗泽娜虹能善瑛鑫开加汉全远坤炎树泉珏继高鸿景为叶宇年孝寿苗虎洁益智森琼雅源鹏士山丰乐冰克杏定承绍政倩健锡锦黎耀三阳佩剑姣珊章铭瑞碧翠瑾土少行伯坚阿其奇妹怡炜南品盛菲雄意璐人久大风仲向达启时欣茂钦卿翔九广心代亦存师纪芝李灵纯苏迎秉诚奎娇显祖哲荷基珺琦熙蕾万子火以圣宁兆权竹自观贞妙怀妮育彦恒栋堂婕湘照瑜韵毓豪毅潮力之五从升太引业本田名守扬汝百妍岚男财进凯周宜放旺经雨保信娅庭思钢钧凌圆宽宾笑骏跃斐朝煜增震鹤衡艺尔申尧作园声陆卓孟昉治知祎郁钖修复威柏洲相科晋润航莎铁乾晨望梦涵象逸媛敬腊滨雷蔚磊露乃于女工书公六历日贝仕令北四石再农则吕延聿亨余呈应社芹运依姐姗季岩玥诗厚垚宣宪峥映柱炼茹贻轶容悦梧泰积耕莺谊逢铃梓渊爽绪敦淼琪登程越雁雯雲嵩满筠蓓路旗熊瑶璋聪镕薇赟鹰麟亿川允夫毛功可央幼必旦未由白伊众优伦同囡孙臣至齐吾希张改更灿甫纬芙言轩钊咏姑官宙尚岳征昇昊昕枝枫河玮迪驹亭俐俭冠奕帮挺柳标洋济珉盈省觉选闻娴展恩息晔晟桃真竞舫通钰啓堃婧寅崇晗深焕理甜绮绵绿野铨隆傅博嵘普棋渭焱然琛禄缘萱葆葱裕鼎楚筱解靖魁嘉睿韬影蕊蕴蝶儒樵镛镜霏燮繁巍懿又上巾彐门马内支斗丝主仪占古台史对巨市汀玄甲艾记丞乔争任伍伏关列在圭地多好庄扣执次池汤玎玑祁羊舟许迈位冶初助吴均妞妤孚岑序库形彤我扶抒攸材杜步求汪汶芦芽评谷身邱里际陈京佶侹典刻垂备居幸性房抱招昆昔杭枚泷玠玫现画畅空竺罗苓苔苹表视诞贯轮郑俞俨勉勋咣咸哞城姝娃将峡带度彪待总战持昱柯洼洽炯狮界畏盼眉祚禹统胤胪茗茜茶荟赴赵逊重钜钟闽音候原唐夏峻换效敖晖校桔桢桧殷流浙浦涌烈烨玺珩祯秦秩称粉致舰莞起都铎阅隽颂婉婵孰寄尉屠常庸得惊惜授敛旋曹梁涯淦烽猗猛球琅皎硕移羚辅逵铜领喆堡媚尊弼惑斯晰最棠棣植滋琨琰紫联舒舜葛装谟谦遂遇链靓鲁嫄微愚慈慎数椿楠楷楸楹槐歆殿溢溪滢煌瑀瑰盟碎蒙裘键雾颐龄嫣稳舆蔷蔺蕖蜀蜜蝉裴褔谱霆韶墀嬉慰樑樟樱潜澄澜璇稼稽豫遵醉镇镐霄题颜冀器壁操潞濒璘璞璟禧翰翱赞霖黔壑曙磻魏黛藩馥攀霭麒鑑"
        num = random.randint(1, 2)
        ln = x[random.randint(1, len(x)) - 1]
        rn = ''
        for n in range(0, num):
            rn += m[random.randint(1, len(m)) - 1]

        return ln + rn


def main():
    parser = OptionParser(
        usage="usage: %prog [options] arg1 arg2", version="%prog {}".format(__VERSION))
    parser.add_option('--num', action='store', dest='num',
                      type='int', default=1, help='Number of idcardnumber [default: %default]')
    parser.add_option('--min', action='store', dest='min',
                      type='int', default=0, help='Minimum age [default: %default]')
    parser.add_option('--max', action='store', dest='max',
                      type='int', default=100, help='Maximum age [default: %default]')
    parser.add_option('--sex', action='store', dest='sex',
                      type='int', default=0, help='Random 0, Female 1 or Male 2 [default: %default]')
    parser.add_option('--year', action='store', dest='year',
                      type='int', default=0, help='Birth year [default: %default]')
    parser.add_option('--month', action='store', dest='month',
                      type='int', default=0, help='Birth month [default: %default]')
    parser.add_option('--day', action='store', dest='day',
                      type='int', default=0, help='Birth day [default: %default]')
    (options, args) = parser.parse_args()

    cls = IdentityCard()
    cls.initialize_areas()
    ret = cls.generator(options.num, options.min, options.max, options.sex, options.year, options.month, options.day)
    for r in ret:
        print ', '.join(r)

if __name__ == '__main__':
    main()
