'''
module paragraphe, provides cap and iscap methods for str
'''

class MultiplicationError(Exception):
    '''MultiplicationError class'''

class Paragraphe(str):
    '''
    class Paragraphe, provides cap and iscap methods for str
    '''
    def cap(self):
        '''cap(self) -> str'''
        if '.' not in self:
            lstriped_chaine = self.lstrip()
            capitalized_chaine = lstriped_chaine.capitalize()
            result = capitalized_chaine.rjust(len(self))
        else:
            phrases = self.split('.')
            caped_phrases = [Paragraphe(ph).cap() for ph in phrases]
            result = '.'.join(caped_phrases)
        return Paragraphe(result)

    def iscap(self):
        '''iscap(self) -> bool'''
        return self.cap() == self

    def __add__(self, other):
        return Paragraphe(str.__add__(self, other.cap()))

    def __mul__(self, value):
        if isinstance(value, int) and value > 2:
            try:
                raise Warning('multiplication par %d > 2' %value)
            except Warning as wrn:
                print('%s: %s' %(wrn.__class__.__name__, wrn))
        return Paragraphe(str.__mul__(self, value))
