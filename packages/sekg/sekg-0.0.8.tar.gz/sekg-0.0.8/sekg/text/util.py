#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

from bs4 import BeautifulSoup


class CodeTextPreprocessor:
    pattern = re.compile(r'\s+')

    def __clean_format(self, text):
        """
        clean text format for text extract from html
        :param text:
        :return:
        """
        return re.sub(self.pattern, " ", text.replace('\n', ' ').replace(u'\u00a0', " "))

    def clean_html_text(self, html_text):
        if html_text is None or html_text == "":
            return ""
        soup = BeautifulSoup(html_text, "lxml")
        codeTags = soup.find_all(name=["pre", 'blockquote'])

        for tag in codeTags:
            if tag.string:
                tag.string = tag.string + " . \n "

        cleanText = soup.get_text()
        cleanText = self.__clean_format(cleanText)
        return cleanText
