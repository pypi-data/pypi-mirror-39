# -*- coding: utf-8 -*-
"""Python VISL Parser.

This module uses the VISL parser for Portuguese to perform the
morphosyntactic parsing of a given text via Python code. The VISL Parser
is available online where information on its use, notation, labels and
used symbols can be found.

.. _VISL Parser Website:
   http://visl.sdu.dk/en/parsing/automatic/parse.php
"""
import re
import requests
import lxml.html

def parse(text):
    """This method return the morphosyntactic information about the
    given text.

    Args:
        text (str): The text for which you want the information.

    Returns:
        list: A list where each item is a dictionary containing the
            keys: 'word', 'stem', 'semantic_tags', 'word_class_tag',
            'other_tags' and 'syntatic_tag'.
    """

    url = u'https://visl.sdu.dk/visl/pt/parsing/automatic/parse.php'
    data = {
        u'text': text,
        u'parser': u'parse',
        u'visual': u'niceline'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

    content = response.content.decode(u'utf-8')
    page = lxml.html.fromstring(content)
    text_result = page.xpath(u'//dt')[0].text_content()
    regex_inf = re.compile(
        '(?P<w>.*?) \n\n\[(?P<stem>.*?)\]  (?P<sem_tag>(<.*?> )*) ?'
        '(?P<wc_tag>.*?) (?P<o_tag>.*?)  (?P<sin_tag>.*?)\n'
    )

    words = []
    for regex_word in regex_inf.finditer(text_result):
        word_dict = regex_word.groupdict()
        sem_tags = word_dict[u'sem_tag'].replace('*', '').replace('<', '')
        sem_tags = sem_tags.replace('>', '').split()
        word_inf = {
            u'word': word_dict[u'w'],
            u'stem': word_dict[u'stem'],
            u'semantic_tags': sem_tags,
            u'word_class_tag': word_dict[u'wc_tag'],
            u'other_tags': word_dict[u'o_tag'],
            u'syntatic_tag': word_dict[u'sin_tag'],
        }
        words.append(word_inf)

    return words
