# coding: UTF-8
'''
text to paras (from string to sents)
'''
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def text_to_paras(text, aux=''):
    '''
    :in: str text
    list of str: paras = text_to_paras(text, aux='')

    aux = '.' for use in baidutr batch translate
    seg text to paras
    newline delimiters a para
    empty lines ignored
    '''

    # lines = text.split('\n')
    lines = text.splitlines()
    lines = [element.strip() for element in lines if element.strip()]
    terminators = ['.', '!', '?']
    # crude, add aux to para end if not ended with terminators
    lines = [elm + (aux if elm[-1] not in terminators else '') for elm in lines]  # noqa

    return lines
