"""There is an interesting thing:  
A math expression that contains both ` `(multiply) and `|`(abs) may be ambiguous.  
for example: `|x-2| x-2 |x-2|` can mean:
  - |x-2|*x-2*|x-2|
  - |x-2*|x-2|*x-2|
Given this, 
in the current implementation, we use `assert` to present it
"""
import re

preabs = re.compile(r"\|(?=[\w\(])")
nexabs = re.compile(r"(?<=[\w\)])\|")


def replace2abs(s):
    # NOTE: called after _replacemul
    assert re.search(r"[\w\(]\|[\w\(]", s) == None
    return preabs.sub("abs(", nexabs.sub(")", s))


def _test_replace2abs():
    teststr = """
|3*x+1|*|5+x|+8
""".strip()
    out = replace2abs(teststr)
    print(teststr, "->", out)


_opchr = r"+-*/"


def replace2mul(s):
    l = s.split()
    ns = l[0]
    # ") +"
    for i in range(1, len(l)):
        if nows := l[i]:  # if isn't Empty-String
            before_ = l[i - 1][-1]
            if nows == "|":
                if (
                    before_.isalnum()
                    and i + 1 != len(l)
                    and l[i + 1][0].isalnum()  # handle ones like "+ |"
                ):
                    ns += "*" + nows
                else:  # handle ones like "x | )"
                    ns += nows
                continue
            if nows == "(":  # handle ones like "x | ( x"
                ns += "*" + nows
                continue

            _after = nows[0]
            if before_ == "|":
                try:
                    before_ = l[i - 1][-2]
                except IndexError:
                    pass
            if _after == "|":
                _after = nows[1]

            if all(
                [
                    before_ == ")" or before_.isalnum(),
                    (_after == "(" or _after.isalnum()),
                ]
            ):
                ns += "*" + nows
            else:
                ns += nows

    return ns


if __name__ == "__main__":
    _test_replace2abs()

    s = "|x+1|+|x|+3 |2 x+1|+5 |x+2 |x+1||" "5 (x+1)+x |x (3+x)|"
    ws = " ".join(filter(lambda x: not x.isspace(), s))
    ns = replace2abs(replace2mul(s))
    nws = replace2abs(replace2mul(ws))
    assert s.replace(" ", "") == ws.replace(" ", "")
    assert ns == nws
