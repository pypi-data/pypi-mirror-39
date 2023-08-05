import os
import re
import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__IDIOM_URL = __PREFIX + ybc_config.uri + '/idiom'

data_path = os.path.abspath(__file__)
data_path = os.path.split(data_path)[0]+'/idioms.txt'


def meaning(keyword=''):
    """
    功能：查询成语释义。

    参数 keyword 是需要查询的成语，

    返回：成语详解、读音、同义词、反义词等信息。
    """
    if not isinstance(keyword, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'keyword'")
    if not keyword:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'keyword'")

    try:
        url = __IDIOM_URL
        data = {
            'keyword': keyword
        }

        for i in range(3):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                res = r.json()['result']
                # 查询不到成语时返回 null
                if res:
                    return {
                        '名称': keyword,
                        '读音': '无' if res['pinyin'] == None else res['pinyin'],
                        '解释': '无' if res['chengyujs'] == None else res['chengyujs'],
                        '出自': '无' if res['from_'] == None else res['from_'],
                        '近义词': '无' if res['tongyi'] == None else ','.join(res['tongyi']),
                        '反义词': '无' if res['fanyi'] == None else ','.join(res['fanyi']),
                        '举例': '无' if res['example'] == None else res['example'].replace(' ','')
                    }
                else:
                    raise ParameterValueError(sys._getframe().f_code.co_name, "'keyword'")
        raise ConnectionError('查询成语解释失败', r._content)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_idiom')


def search(keyword=''):
    """
    功能：根据关键字模糊搜索成语。

    参数 keyword 成语关键字，

    返回：搜索到的成语列表(最多10个)。
    """
    if not isinstance(keyword, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'keyword'")
    if not keyword:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'keyword'")
    try:
        if keyword == '':
            return -1

        f = open(data_path, encoding='UTF-8')
        content = f.read()
        f.close()
        s = re.findall('.*' + keyword + '.*', content)

        # 返回生僻成语较多，是否返回结果列表中的随机10个成语？
        if s:
            return s[0:10]
        else:
            return -1
    except Exception as e:
        raise InternalError(e, 'ybc_idiom')


def main():
    print(meaning('叶公好龙'))
    print(search('一'))


if __name__ == '__main__':
    main()
