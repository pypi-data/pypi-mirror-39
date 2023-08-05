
# Tagger

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
[![pypi](https://img.shields.io/pypi/v/torch-tagger.svg)](https://pypi.python.org/pypi/torch-tagger)
[![travis-ci](https://travis-ci.org/infinity-future/torch-tagger.svg?branch=master)](https://travis-ci.org/infinity-future/torch-tagger/)
[![codecov](https://codecov.io/gh/infinity-future/torch-tagger/branch/master/graph/badge.svg)](https://codecov.io/gh/infinity-future/torch-tagger)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://infinity-future.github.io/torch-tagger/)
[![ToDo and InProgress Status](https://badge.waffle.io/infinity-future/torch-tagger.svg?columns=To%20Do,In%20Progress)](https://waffle.io/infinity-future/torch-tagger)

Tagger could use as named entity recognized(NER), part of speech tagging(POS), word segmentation

This repo use torch and RNN-CRF to do tag job

这个项目是Infinity-Future Chatbot、Dialog System、NLP 等项目的一个子项目，目的在于构建通用、易用的中英文Tagger工具，主要工作可能是命名实体识别 (NER)

## Document

[Document Online](https://infinity-future.github.io/torch-tagger/)

## Score

`tests/ner_glove_charcnn.py` could reach CONLL2003 testb F1 >= 90.05, using GloVe.6B 100 dimension pretrained-vector

`tests/segmentation_glove.py` could reach MSR dataset test F1 >= 95.3, using Chinese character GloVe, pretrained-vector by author of this repo

### Generate

Install documentation dependencies

`pip3 install sphinx sphinx_rtd_theme --upgrade --user`

run the script to generate docs

`scripts/gen_doc.sh`

## Test

```sh
python3 -m tests
```
