import re
from lib.exception import IllegalCharacter,GrammarError

INDEX = 0
TOKEN_LIST = []
TOKEN = None

def get_next_token():
    global INDEX,TOKEN
    INDEX += 1
    if INDEX > len(TOKEN_LIST) - 1:
        TOKEN = {"type":"end","str":"end"}
    else:
        TOKEN = TOKEN_LIST[INDEX]
    return TOKEN

def digit_status(string):
    """
    分析数字开头的字符串，整数或小数
    :param string: 字符串
    :return:
    """
    token = {
        "type": "",
        "str": "",
    }
    decimal = re.match("\d+(\.\d+)", string)
    if decimal:
        token["type"] = "小数"
        token["str"] = decimal.group()
        index = decimal.span()[1]
    else:
        integer = re.match("\d+", string)
        token["type"] = "整数"
        token["str"] = integer.group()
        index = integer.span()[1]

    return string[index:],token

def delimiter_status(string):
    """
    界符判断
    :param string:
    :return:
    """
    token = {
        "type": "界符",
        "str": string[0],
    }
    return string[1:],token

def math_status(string):
    """
    运算符判断
    :param string:
    :return:
    """
    token = {
        "type": "运算符",
        "str": string[0],
    }
    index = 1
    # 加减号 除号
    if string[0] in ["+","-","/"]:
        token["type"] = "算数运算符"
        token["str"] = string[0]
        index = 1

    # 乘号 或 **
    elif string[0] == "*":
        if len(string) > 1 and string[1] == "*":
            token["type"] = "算数运算符"
            token["str"] = string[0:2]
            index = 2
        else:
            token["type"] = "算数运算符"
            token["str"] = string[0]
            index = 1

    return string[index:], token

def token_merge(token_list):
    """
    合并数字前的正负号
    :param token_list:
    :return:
    """
    i = 0
    while i < len(token_list)-2:
        # print(token_list[i])
        if token_list[i].get("str") in ["-","+"] and token_list[i].get("type") == "算数运算符":
            if 0 < i < len(token_list):
                if token_list[i+1].get("type") in ["整数","小数"] and token_list[i-1].get("type") not in ["整数","小数"]:
                    token_list[i+1]["str"] = token_list[i].get("str") + token_list[i+1]["str"]
                    token_list.pop(i)
                    continue
            elif i == 0:
                if token_list[i+1].get("type") in ["整数","小数"]:
                    token_list[i+1]["str"] = token_list[i].get("str") + token_list[i+1]["str"]
                    token_list.pop(i)
                    continue
        i = i + 1

    return token_list

    # exp -> addtive_exp exp_more;
    # exp_more -> additive_exp exp_more | ε
    # addtive_exp -> term addtive_exp_more
    # addtive_exp_more -> (('+' | '-')  term addtive_exp_more) | ε
    # term -> factor term_more
    # term_more -> (('*' | '/' | '**')  factor term_more) | ε
    # factor -> '('exp')' | number

def exp_stm():
    if TOKEN["str"] == "(" or (TOKEN["type"] in ["整数", "小数"]):
        addtive_exp()
        exp_more()
    else:
        raise GrammarError(detail="表达式语法错误！")

def exp_more():
    if TOKEN["str"] == "**":
        get_next_token()
        addtive_exp()
        exp_more()

def addtive_exp():
    term()
    addtive_exp_more()

def addtive_exp_more():
    if TOKEN["str"] in ["+",'-']:
        get_next_token()
        term()
        addtive_exp_more()

def term():
    factor()
    term_more()

def term_more():
    if TOKEN["str"] in ["*","/"]:
        get_next_token()
        factor()
        term_more()

def factor():
    if TOKEN and TOKEN["str"] == "(":
        get_next_token()
        exp_stm()
        if TOKEN and TOKEN["str"] != ")":
            raise GrammarError("缺少 ）")
        get_next_token()
    elif TOKEN and TOKEN["type"] in ["整数","小数"]:
        get_next_token()
    else:
        raise GrammarError("表达式语法错误")


def check_expression(input_str):
    """
    检查表达式
    :param input_str:
    :return:
    """
    token_list = []
    input_str = input_str.replace(" ","")

    # 词法分析，获取token
    while len(input_str) > 0:
        if input_str[0].isdigit():
            input_str, token = digit_status(input_str)
            token_list.append(token)
        elif input_str[0] in ["(",")"]:
            input_str, token = delimiter_status(input_str)
            token_list.append(token)
        elif input_str[0] in ["+","-","*","/"]:
            input_str, token = math_status(input_str)
            token_list.append(token)
        else:
            raise IllegalCharacter(detail="不合法的字符：{}".format(input_str[0]))

    global TOKEN,TOKEN_LIST,INDEX
    TOKEN_LIST = token_merge(token_list)
    TOKEN = TOKEN_LIST[0]
    INDEX = 0
    print(TOKEN_LIST)

    # 语法分析
    exp_stm()
    if INDEX < len(TOKEN_LIST):
        raise GrammarError("表达式语法错误,剩余token无法分析")
    return True










