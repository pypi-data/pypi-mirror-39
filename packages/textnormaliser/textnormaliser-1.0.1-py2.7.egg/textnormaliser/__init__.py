# !/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import codecs
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import operator
import os
import pickle
import re
import string
import sys
import threading
from langdetect import detect_langs
from langdetect import DetectorFactory
import nltk
import tqdm
import spacy
import langdetect
from bs4 import BeautifulSoup


nlp = None
lock = threading.Lock()


def _is_anything(text):
    stripped = text.strip()
    letters = re.sub('[^a-zA-Z]+', '', stripped)
    return len(letters) > 1


def _is_probably_english(text):
    global lock
    try:
        lock.acquire()
        langs = detect_langs(text)
        lock.release()
        lang_dict = {}
        for lang in langs:
            lang_dict[lang.lang] = lang.prob
        if 'en' not in lang_dict:
            return False
        most_likely_lang = max(lang_dict.iteritems(), key=operator.itemgetter(1))[0]
        if most_likely_lang == 'en':
            return True
        return abs(lang_dict['en'] - lang_dict[most_likely_lang]) < 0.1
    except langdetect.lang_detect_exception.LangDetectException:
        print 'EXCEPTION HAR'
        lock.release()
        return False


def _should_normalise_text(text):
    if not _is_anything(text):
        return False
    if not _is_probably_english(text):
        print 'This is not english'
        return False
    return True


def _resolve_html_entities(text):
    soup = BeautifulSoup(text, features="html.parser")
    return unicode(soup.encode(formatter=None))


def _normalise_text(text, nlp):
    text = _resolve_html_entities(text)
    doc = nlp(text)
    replaced_text = []
    entity_text = text
    for entity in doc.ents:
        if not _is_anything(entity.text):
            continue
        new_text = '_'.join([entity.label_, entity.text.replace(' ', '_')])
        new_text = re.sub(r'[^\w\s]', ' ', new_text)
        entity_text = entity_text.replace(entity.text, new_text)
        replaced_text.append(new_text)
    tokenize = nltk.word_tokenize(entity_text)
    pos_tags = nltk.pos_tag(tokenize)
    pos_tokens = []
    for pos_tag in pos_tags:
        if not _is_anything(pos_tag[0]) or pos_tag[0] in replaced_text:
            pos_tokens.append(pos_tag[0])
            continue
        pos_tokens.append(u'{}_{}'.format(pos_tag[1], pos_tag[0]))
    lower_text = ' '.join(pos_tokens).lower()
    if lower_text[-1] != '\n':
        lower_text += '\n'
    return lower_text


def _run_text(text):
    global nlp
    if not _should_normalise_text(text):
        return ''
    return _normalise_text(text, nlp)


def _run_pool(corpus_input, output_handle):
    pool = ThreadPool()
    results = pool.map(_run_text, corpus_input)
    pool.close() 
    pool.join()
    for result in results:
        if result:
            output_handle.write(result)


def _run_normaliser(corpus_file, output_file):
    global nlp
    # Setup determinism
    DetectorFactory.seed = 0
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nlp = spacy.load('en_core_web_sm')
    # Read and write the normalised corpus
    with codecs.open(output_file, 'w', encoding='utf8') as output_handle:
        corpus_input = []
        with codecs.open(corpus_file, 'r', encoding='utf8') as corpus_handle:
            for text in tqdm.tqdm(corpus_handle):
                corpus_input.append(text)
                if len(corpus_input) == 1000000:
                    _run_pool(corpus_input, output_handle)
                    corpus_input = []
            _run_pool(corpus_input, output_handle)


def _main():
    # Read arguments
    parser = argparse.ArgumentParser(description='Normalise a corpus of text.');
    parser.add_argument('corpus', help='The path to the corpus file.')
    parser.add_argument('output', help='The path to the output file.')
    args = parser.parse_args()
    _run_normaliser(args.corpus, args.output)


if __name__ == "__main__":
    _main()
