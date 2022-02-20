from math import pi
from PyQt5.Qt import QValidator

class angle_vadidator(QValidator):
    ## 验证器 要求的是角度在0和2*pi之间
    def validate(self,input_str,pos_int):
        try:
            if float(input_str) <= 2*pi and float(input_str) >= 0:
                return (QValidator.Acceptable,input_str,pos_int)
            else: return (QValidator.Invalid,input_str,pos_int)
        except:
            if len(input_str) == 0:
                return (QValidator.Intermediate,input_str,pos_int)
            return (QValidator.Invalid,input_str,pos_int)

    def fixup(self, p_str: str) -> str:
        try:
            if float(p_str) < 0:
                return "0"
            elif float(p_str) > 2*pi:
                return str(2*pi)
        except:
            return "0"
        ## todo int返回值是不是仅仅为int啊，还有长度限制

class position_vadidator(QValidator):
    ## 要求输入在-50~50之间
    def validate(self, input_str: str, pos_int: float):
        try:
            if float(input_str) >=-50 and float(input_str) <= 50:
                return (QValidator.Acceptable,input_str,pos_int)
            else:return (QValidator.Invalid,input_str,pos_int)
        except:
            if len(input_str) == 0:
                return (QValidator.Intermediate,input_str,pos_int)
            elif len(input_str) == 1 and input_str == '-':
                return (QValidator.Intermediate, input_str, pos_int)
            return (QValidator.Invalid,input_str,pos_int)

    def fixup(self, p_str: str) -> str:
        try:
            if float(p_str) < -50:
                return "-50"
            elif float(p_str) > 50:
                return "50"
        except:
            return "-50"
        ## todo int返回值是不是仅仅为int啊，还有长度限制

class attack_vadidator(QValidator):
    def validate(self, input_str: str, pos_int: float):
        try:
            if float(input_str) >= 0 and float(input_str) <= 10:
                return (QValidator.Acceptable, input_str, pos_int)
            else:
                return (QValidator.Invalid, input_str, pos_int)
        except:
            if len(input_str) == 0:
                return (QValidator.Intermediate, input_str, pos_int)
            return (QValidator.Invalid, input_str, pos_int)

    def fixup(self, p_str: str) -> str:
        try:
            if float(p_str) < 0:
                return "0"
            elif float(p_str) > 10:
                return "10"
        except:
            return "-50"
        ## todo int返回值是不是仅仅为int啊，还有长度限制