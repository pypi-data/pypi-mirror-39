# -*- coding: utf-8 -*-

from .font_map import *
from ybc_exception import *
import sys

_DEFAULT_FONT = "standard"


def font_list():
    """
    功能：打印所有的字体
    """
    try:
        for item in sorted(list(font_map.keys())):
            print(str(item) + " : ")
            _tprint("test", str(item))
    except Exception as e:
        raise InternalError(e, 'ybc_art')


def _tprint(text, font=_DEFAULT_FONT, chr_ignore=True):
    """
    功能：内部函数，This function split function by \n then call text2art function
    参数：text 要转换的文本
         font：字体，默认为"standard"
         chr_ignore：是否忽略不能转换的字符，默认是
    """
    try:
        split_list = text.split("\n")
        result = ""
        for item in split_list:
            if len(item) != 0:
                result = result + text2art(item, font=font, chr_ignore=chr_ignore)
        print(result)
    except Exception as e:
        raise InternalError(e, 'ybc_art')


def text2art(text, font=_DEFAULT_FONT, chr_ignore=True):
    """
    功能：打印艺术字 This function print art text
    参数：text：输入文本
         font：字体
         chr_ignore：是否忽略不能转换的字符，默认是
    返回：艺术字
    """
    error_flag = 1
    error_msg = ""
    # 参数类型正确性判断
    if not isinstance(text, str):
        error_flag = -1
        error_msg = "'text'"
    if not isinstance(font, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'font'"
    if not isinstance(chr_ignore, bool):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'chr_ignore'"
    if error_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        split_list = []
        result_list = []
        letters = standard_dic
        text_temp = text
        if font.lower() in font_map.keys():
            letters = font_map[font.lower()][0]
            if font_map[font.lower()][1] == True:
                text_temp = text.lower()
        else:  # font参数取值错误
            error_flag = -1
            error_msg = "'font'"
        for i in text_temp:
            if (ord(i) == 9) or (ord(i) == 32 and font == "block"):
                continue
            if (i not in letters.keys()) and (chr_ignore == True):
                continue
            if len(letters[i]) == 0:
                continue
            split_list.append(letters[i].split("\n"))

        # text参数取值错误
        if len(split_list) == 0:
            if error_flag == -1:
                error_msg = "'text'、" + error_msg
            else:
                error_msg = "'text'"
        if error_flag == -1:
            raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

        for i in range(len(split_list[0])):
            temp = ""
            for j in range(len(split_list)):
                if j > 0 and (i == 1 or i == len(split_list[0]) - 2) and font == "block":
                    temp = temp + " "
                temp = temp + split_list[j][i]
            result_list.append(temp)
        return (("\n").join(result_list))

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_art')


def main():
    print(text2art('nihao 1234'))


if __name__ == "__main__":
    main()
