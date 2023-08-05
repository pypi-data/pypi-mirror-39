#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import sample
from string import lowercase, uppercase, letters, digits, punctuation


class PwGen(object):
    # upper = 65 - 90; lower = 97 - 122; num = 48 - 57
    lowerEnd = 122

    def __init__(self):
        self.letterExcept = {'I', 'O', 'Q', 'l', 'o', 'Z', 'z', }
        self.digitExcept = {'0', '1', '2', '4', }
        self.punctuationInclude = {'!', }
        self.punctuationExcept = {'"', "'", '@', }
        self.group = self.set_group()
        self.first_letter = True
        self.distinct = True

    def set_group(self, has_lower=True, has_upper=True, has_digits=True, punc_in=True, punc_ex=False):
        group = ""
        if has_lower:
            group += lowercase
        if has_upper:
            group += uppercase
        if has_lower or has_upper:
            group += "".join(set(group) - self.letterExcept)
        if has_digits:
            group += "".join(set(digits) - self.digitExcept)
        if punc_in:
            group += "".join(self.punctuationInclude)
        if punc_ex:
            group += "".join(set(punctuation) - self.punctuationExcept)
        return group

    def _gen_char(self, length=1):
        return sample(self.group, length)

    def _gen_letter(self, length=1):
        group = ''.join(set(letters) - self.letterExcept)
        return sample(group, length)

    def _gen_digit(self, length=1):
        group = ''.join(set(digits) - self.digitExcept)
        return sample(group, length)

    def _sum_digits(self, tmp):
        count = 0
        for char in tmp:
            if char.isdigit():
                count += 1
        return count

    def generate(self, length, digits_least=None):
        tmp = sample(self.group, length - 1)
        while len(tmp) < length:
            if digits_least is not None:
                count = digits_least - self._sum_digits(tmp)
                if count > 0:
                    tmp = tmp[count::]
                    tmp += self._gen_digit(count)
            if self.first_letter:
                tmp[0] = self._gen_letter()[0]
            tmp += sample(self.group, 1)
            if self.distinct:
                tmp = list(set(tmp))
        return ''.join(tmp)


if __name__ == '__main__':
    gen = PwGen()
    gen.group = gen.set_group(punc_in=False)
    for i in range(1, 10):
        pw = gen.generate(15, 6) + "!"
        print(pw)
