import re


def reduceThePrecision(latex_string, precision=2):
    pattern = r"([-+]?\d*\.\d+|\d+)"

    def round_decimal(match):
        return str(round(float(match.group(0)), precision))

    result = re.sub(pattern, round_decimal, latex_string)
    return result
