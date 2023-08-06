import fire
import re

def search(exp,s):
    reg = re.compile(exp)
    m = reg.search(s)
    r = s[m.regs[0][0]:m.regs[0][1]]
    return r

if __name__ == '__main__':
    fire.Fire()
