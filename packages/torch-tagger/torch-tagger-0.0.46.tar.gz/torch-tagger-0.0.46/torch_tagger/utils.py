# -*- coding: utf-8 -*-
"""Utils tools for tagger
Created by InfinityFuture
"""

import re
import sys
from collections import Counter
from typing import Optional, Tuple

import numpy as np

import torch
from sklearn.utils import shuffle

if torch.cuda.is_available():
    print('CUDA is online', file=sys.stderr)
else:
    print('CUDA is offline', file=sys.stderr)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
START_TAG = '<START>'
STOP_TAG = '<STOP>'
PAD_TAG = '<PAD>'
UNK_TAG = '<UNK>'


def prepare_sequence(seq: list, to_ix: list) -> torch.LongTensor:
    """Convert sequence to torch variable"""
    idxs = [to_ix[w] if w in to_ix else to_ix[UNK_TAG] for w in seq]
    return idxs


def normalize_word(word: str) -> str:
    """normalize number"""
    word = re.sub(r'\d', '0', word)
    return word


def text_reader(path: str) -> Tuple[list, list]:
    """Read a text file, and return data
    data should follow this format:

    I O
    want O
    to O
    New B-City
    York I-City
    """
    with open(path, 'r') as fobj:
        parts = fobj.read().split('\n\n')
        parts = [part.strip() for part in parts]
        parts = [part for part in parts if len(part) > 0]
    assert parts, 'text file empty "{}"'.format(path)

    x_data = []
    y_data = []
    for part in parts:
        lines = part.split('\n')
        lines = [line.split() for line in lines]
        words = [x[0] for x in lines]
        tags = [x[-1] for x in lines]
        words = [normalize_word(word) for word in words]
        x_data.append(words)
        y_data.append(tags)
        assert len(words) == len(tags), \
            'line "{}" and "{}" do not match "{}" vs "{}"'.format(
                len(words), len(tags), words, tags)
    return x_data, y_data


def build_vocabulary(x_data: list, y_data: list, limit: int = 1) -> dict:
    """ Use data to build vocabulary"""
    sentence_word = Counter()
    sentence_word_char = Counter()
    tags_word = Counter()
    for sentence in x_data:
        sentence_word.update(sentence)
    for tags in y_data:
        tags_word.update(tags)

    word_to_ix = {PAD_TAG: 0, UNK_TAG: 1}
    for word, count in sentence_word.items():
        sentence_word_char.update(list(word))
        if word not in word_to_ix and count >= limit:
            indx = len(word_to_ix)
            word_to_ix[word] = indx

    char_to_ix = {PAD_TAG: 0, UNK_TAG: 1}

    for char, count in sentence_word_char.items():
        if count >= limit:
            indx = len(char_to_ix)
            char_to_ix[char] = indx

    ix_to_char = {v: k for k, v in char_to_ix.items()}

    ix_to_word = {v: k for k, v in word_to_ix.items()}

    tag_to_ix = {}

    tag_words = [PAD_TAG] + list(tags_word.keys()) + [START_TAG, STOP_TAG]
    for tag in tag_words:
        indx = len(tag_to_ix)
        tag_to_ix[tag] = indx

    ix_to_tag = {v: k for k, v in tag_to_ix.items()}

    return {
        'word_to_ix': word_to_ix,
        'ix_to_word': ix_to_word,
        'tag_to_ix': tag_to_ix,
        'ix_to_tag': ix_to_tag,
        'char_to_ix': char_to_ix,
        'ix_to_char': ix_to_char
    }


def pad_seq(seq: list, max_len: int, pad: int = 0,
            method: str = 'right') -> list:
    """Padding data to max_len length"""
    if method == 'right':
        if len(seq) < max_len:
            seq = seq + [pad] * (max_len - len(seq))
    elif method == 'left':
        if len(seq) < max_len:
            seq = [pad] * (max_len - len(seq)) + seq
    elif method == 'both':
        if len(seq) < max_len:
            for i in range(max_len - len(seq)):
                if i % 2 == 0:
                    seq = seq + [pad]
                else:
                    seq = [pad] + seq
    return seq


def extract_char_features(x_batch: list, char_max_len: int, char_to_ix: dict,
                          max_len: int) -> Tuple[list, list]:
    """extract char features"""
    char_batch = []
    char_len_batch = []
    for xseq in x_batch:
        sentence_char = []
        len_char = []
        for char in xseq:
            if re.match(r'^[\u4e00-\u9fff]+$', char):
                # Process Chinese
                from pypinyin import lazy_pinyin
                char = ' '.join([x[0] for x in lazy_pinyin(char)])
            char = char[:char_max_len]
            len_char.append(len(char))
            char = prepare_sequence(char, char_to_ix)
            char = pad_seq(char, char_max_len, method='both')
            sentence_char.append(char)
        while len(sentence_char) < max_len:
            sentence_char.append([0] * char_max_len)
        while len(len_char) < max_len:
            len_char.append(0)
        char_batch.append(sentence_char)
        char_len_batch.append(len_char)
    char_batch = np.asarray(char_batch)
    char_len_batch = np.asarray(char_len_batch)
    return char_batch, char_len_batch


def batch_flow(x_data: list,
               y_data: list,
               word_to_ix: dict,
               tag_to_ix: dict,
               char_to_ix: dict = None,
               char_max_len: int = None,
               batch_size: int = 32,
               sample_shuffle: bool = True,
               max_limit: int = 300):
    """Automatic generate batch data"""
    assert len(x_data) >= batch_size, 'len(x_data) > batch_size'
    assert len(x_data) == len(y_data), \
        'len(x_data) == len(y_data), {} != {}'.format(len(x_data), len(y_data))

    x_batch, y_batch = [], []
    inds = list(range(len(x_data)))
    if sample_shuffle:
        inds = shuffle(inds)
    while True:
        for ind in inds:
            if len(x_batch) == batch_size:
                len_batch = [len(t) for t in x_batch]
                max_len = np.max(len_batch)

                char_batch = None
                char_len_batch = None
                if char_to_ix is not None:
                    char_batch, char_len_batch = extract_char_features(
                        x_batch, char_max_len, char_to_ix, max_len)

                x_batch = [prepare_sequence(x, word_to_ix) for x in x_batch]
                y_batch = [prepare_sequence(y, tag_to_ix) for y in y_batch]
                x_batch = [pad_seq(x, max_len) for x in x_batch]
                y_batch = [pad_seq(y, max_len) for y in y_batch]

                batches = list(
                    zip(x_batch, y_batch, len_batch, char_batch,
                        char_len_batch))
                batches = sorted(batches, key=lambda x: x[2], reverse=True)
                (x_batch, y_batch, len_batch, char_batch,
                 char_len_batch) = zip(*batches)

                tcx, tcy, tcl, tcc, tccl = (torch.from_numpy(
                    np.asarray(x_batch)), torch.from_numpy(
                        np.asarray(y_batch)),
                                            torch.from_numpy(
                                                np.asarray(len_batch)),
                                            torch.from_numpy(
                                                np.asarray(char_batch)),
                                            torch.from_numpy(
                                                np.asarray(
                                                    char_len_batch,
                                                    dtype=np.int32)))
                x_batch, y_batch = [], []
                yield tcx, tcy, tcl, tcc, tccl

            x_batch.append(x_data[ind][:max_limit])
            y_batch.append(y_data[ind][:max_limit])


def sequence_mask(lens: torch.Tensor,
                  max_len: Optional[int] = None) -> torch.FloatTensor:
    """InfinityFutures: This function is copy from:

    https://github.com/epwalsh/pytorch-crf

    The author is epwalsh, and its license is MIT too

    Compute sequence mask.

    Parameters

    lens : torch.Tensor
        Tensor of sequence lengths ``[batch_size]``.
    max_len : int, optional (default: None)
        The maximum length (optional).

    Returns

    torch.ByteTensor
        Returns a tensor of 1's and 0's of size ``[batch_size x max_len]``.
    """
    batch_size = lens.size(0)

    if max_len is None:
        max_len = lens.max().item()

    ranges = torch.arange(0, max_len, device=lens.device).long()
    ranges = ranges.unsqueeze(0).expand(batch_size, max_len)
    ranges = torch.autograd.Variable(ranges)

    lens_exp = lens.unsqueeze(1).expand_as(ranges)
    mask = ranges < lens_exp

    return mask.float()


def extract_entities(seq: list, x=None) -> list:
    """Extract entities from a sequences

    ---
    input: ['B', 'I', 'I', 'O', 'B', 'I']
    output: [(0, 3, ''), (4, 6, '')]
    ---
    input: ['B-loc', 'I-loc', 'I-loc', 'O', 'B-per', 'I-per']
    output: [(0, 3, '-loc'), (4, 6, '-per')]
    ---
    input:
        seq=['B-loc', 'I-loc', 'I-loc', 'O', 'B-per', 'I-per']
        x='我爱你欧巴桑'
    output:
        [(0, 3, '-loc', '我爱你'), (4, 6, '-per', '巴桑')]
    """
    ret = []
    start_ind, start_type = -1, None
    for i, tag in enumerate(seq):
        if tag.startswith('S'):
            if x is not None:
                ret.append((i, i + 1, tag[1:], x[i:i + 1]))
            else:
                ret.append((i, i + 1, tag[1:]))
            start_ind, start_type = -1, None
        if tag.startswith('B') or tag.startswith('O'):
            if start_ind >= 0:
                if x is not None:
                    ret.append((start_ind, i, start_type, x[start_ind:i]))
                else:
                    ret.append((start_ind, i, start_type))
                start_ind, start_type = -1, None
        if tag.startswith('B'):
            start_ind = i
            start_type = tag[1:]
    if start_ind >= 0:
        if x is not None:
            ret.append((start_ind, len(seq), start_type, x[start_ind:]))
        else:
            ret.append((start_ind, len(seq), start_type))
        start_ind, start_type = -1, None
    return ret
