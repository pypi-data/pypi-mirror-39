import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__POETRY_URL = __PREFIX + ybc_config.uri + '/poetry'


def shici(title='春晓', author='孟浩然'):
    """
    功能：根据诗词标题和作者，搜索诗词内容。

    参数：title:诗词标题，默认为'春晓'
         author:诗词作者，默认为'孟浩然'

    返回：返回搜索到的诗词内容，若未搜索到返回提示"未搜索到这首诗词"
    """
    # 参数类型正确性检查
    error_msg = ""
    error_flag = 1
    if not isinstance(title, str):
        error_flag = -1
        error_msg = "'title'"
    if not isinstance(author, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'author'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    if title == "":
        error_flag = -1
        error_msg = "'title'"
    if author == "":
        if error_flag == -1:
            error_msg += "、"
        error_msg += "'author'"
    if error_flag == -1:
            raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    try:
        url = __POETRY_URL + '?title=%s&author=%s' % (title, author)

        for i in range(3):
            r = requests.get(url)
            if r.status_code == 200:
                if r.content:
                    res = r.json()
                    content = ''.join(res)
                    return content
                else:
                    return '未搜索到这首诗词'
        raise ConnectionError('搜索诗词服务调用失败', r.content)
    except Exception as e:
        raise InternalError(e, 'ybc_poetry')


def main():
    res = shici()
    print(res)

    res = shici('早发白帝城', '李白')
    print(res)

    res = shici('声声慢', '李清照')
    print(res)

    res = shici('早发白帝城', '李')
    print(res)


if __name__ == '__main__':
    main()
