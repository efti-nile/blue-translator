#!/usr/bin/python
# -*- coding: utf-8 -*-

import goslate
import codecs
import time

# japanese unicodes
FULL_STOP = u'\u3002'
EXCLAMATION_MARK = u'\uff01'
QUESTION_MARK = u'\uff1f'
QUOTE_OPEN = u'\u300c'
QUOTE_CLOSE = u'\u300d'

# state machine constants
UNDEFINED = 0
IN_SENTENCE = 1
IN_QUOTE = 2

gs = goslate.Goslate()

orig = unicode(open('blue-chapter-original/blue-chapter-original.txt').read(), "utf-8")
orig_sentences = codecs.open('orig-sentences.txt', 'w', 'utf-8')
translation = codecs.open('translation.txt', 'w', 'utf-8')
sentences = [];
sentence = unicode("", "utf-8")

sentences_num = 0
sentences_translated_num = 0

state = UNDEFINED

for uc in orig:
    if uc == u'\u000a': continue # skip new line charachters
    
    if state == UNDEFINED:
        if uc == QUOTE_OPEN:
            sentence = sentence + uc;
            state = IN_QUOTE;
            continue
        else:
            sentence = sentence + uc
            state = IN_SENTENCE
            continue
        
    if state == IN_SENTENCE:
        if uc == FULL_STOP:
            sentence = sentence + uc
            sentences.append(sentence)
            sentences_num += 1
            sentence = unicode("", "utf-8")
            state = UNDEFINED;
            continue
        else:
            sentence = sentence + uc
            continue

    if state == IN_QUOTE:
        if uc == QUOTE_CLOSE:
            sentence = sentence + uc
            sentences.append(sentence)
            sentences_num += 1
            sentence = unicode("", "utf-8")
            state = UNDEFINED;
            continue
        else:
            sentence = sentence + uc
            continue        
 
for s in sentences:
    orig_sentences.write(s + u'\u000a')
    translation.write(s + u'\u000a')
    translation.write(gs.translate(s, 'en', 'ja') + u'\u000a')
    sentences_translated_num += 1
    print 'translated %s from %s' % (sentences_translated_num, sentences_num)
    time.sleep(5)
    
orig_sentences.close()
translation.close()