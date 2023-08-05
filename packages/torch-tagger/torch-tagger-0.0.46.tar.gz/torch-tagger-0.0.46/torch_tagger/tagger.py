# -*- coding: utf-8 -*-
"""Main tagger class
"""

import math
import os
import pickle

import numpy as np

import torch
from sklearn.base import BaseEstimator
from torch import nn, optim
from tqdm import tqdm

from .tagger_model import TaggerModel
from .utils import (DEVICE, batch_flow, build_vocabulary,
                    extract_char_features, extract_entities, pad_seq,
                    prepare_sequence)


class Tagger(BaseEstimator):
    """Scikit-learn compatible Tagger
    """

    def __init__(self,
                 embedding_dim=100,
                 hidden_dim=200,
                 weight_decay=0.0,
                 epochs=100,
                 verbose=1,
                 batch_size=32,
                 device='auto',
                 embedding_dropout_p=0.0,
                 rnn_dropout_p=0.0,
                 bidirectional=True,
                 rnn_type='lstm',
                 num_layers=1,
                 optimizer='Adam',
                 momentum=0,
                 learning_rate=None,
                 learning_rate_decay=0,
                 embedding_trainable=True,
                 use_crf=True,
                 use_char='rnn',
                 char_max_len=50,
                 char_embedding_dim=30,
                 char_hidden_dim=50,
                 char_dropout_p=0.5,
                 char_bidirectional=True,
                 clip_grad_norm=None,
                 average_loss=False,
                 _model=None,
                 _optimizer=None,
                 _word_to_ix=None,
                 _ix_to_word=None,
                 _tag_to_ix=None,
                 _ix_to_tag=None,
                 _char_to_ix=None,
                 _ix_to_char=None):
        """init"""
        assert optimizer.lower() in ('sgd', 'adam')
        assert device.lower() in ('cpu', 'gpu', 'cuda', 'auto')
        self.params = {
            'embedding_dim': embedding_dim,
            'hidden_dim': hidden_dim,
            'weight_decay': weight_decay,
            'epochs': epochs,
            'verbose': verbose,
            'batch_size': batch_size,
            'device': device,
            'embedding_dropout_p': embedding_dropout_p,
            'rnn_dropout_p': rnn_dropout_p,
            'bidirectional': bidirectional,
            'rnn_type': rnn_type,
            'num_layers': num_layers,
            'optimizer': optimizer,
            'momentum': momentum,
            'learning_rate': learning_rate,
            'learning_rate_decay': learning_rate_decay,
            'embedding_trainable': embedding_trainable,
            'use_crf': use_crf,
            'use_char': use_char,
            'char_max_len': char_max_len,
            'char_embedding_dim': char_embedding_dim,
            'char_hidden_dim': char_hidden_dim,
            'char_dropout_p': char_dropout_p,
            'char_bidirectional': char_bidirectional,
            'clip_grad_norm': clip_grad_norm,
            'average_loss': average_loss,
        }
        self._model = _model
        self._optimizer = _optimizer
        self._word_to_ix = _word_to_ix
        self._ix_to_word = _ix_to_word
        self._tag_to_ix = _tag_to_ix
        self._ix_to_tag = _ix_to_tag
        self._char_to_ix = _char_to_ix
        self._ix_to_char = _ix_to_char

    def _get_learning_rate(self):
        """default learning rate"""
        optimizer = self.params['optimizer']
        learning_rate = self.params['learning_rate']
        if learning_rate is not None:
            return learning_rate
        if optimizer.lower() == 'sgd':
            return 1e-2
        if optimizer.lower() == 'adam':
            return 1e-3

    def get_params(self, deep=True):
        """Get params for scikit-learn compatible"""
        params = self.params
        if deep:
            params['_model'] = self._model.state_dict(
            ) if self._model is not None else None
            params['_optimizer'] = self._optimizer.state_dict() \
                if self._optimizer is not None else None
            params['_word_to_ix'] = self._word_to_ix
            params['_ix_to_word'] = self._ix_to_word
            params['_tag_to_ix'] = self._tag_to_ix
            params['_ix_to_tag'] = self._ix_to_tag
            params['_char_to_ix'] = self._char_to_ix
            params['_ix_to_char'] = self._ix_to_char
        return params

    def set_params(self, **parameters):
        """Set params for scikit-learn compatible"""
        for key, value in parameters.items():
            if key in self.params:
                self.params[key] = value
        return self

    def __getstate__(self):
        """Get state for pickle"""
        state = {
            'params':
            self.params,
            '_model':
            self._model.state_dict() if self._model is not None else None,
            '_optimizer':
            self._optimizer.state_dict()
            if self._optimizer is not None else None,
            '_word_to_ix':
            self._word_to_ix,
            '_ix_to_word':
            self._ix_to_word,
            '_tag_to_ix':
            self._tag_to_ix,
            '_ix_to_tag':
            self._ix_to_tag,
            '_char_to_ix':
            self._char_to_ix,
            '_ix_to_char':
            self._ix_to_char
        }
        return state

    def __setstate__(self, state):
        """Get state for pickle"""
        self.params = state['params']
        if state['_model'] is not None:
            self._word_to_ix = state['_word_to_ix']
            self._ix_to_word = state['_ix_to_word']
            self._tag_to_ix = state['_tag_to_ix']
            self._ix_to_tag = state['_ix_to_tag']
            self._char_to_ix = state['_char_to_ix']
            self._ix_to_char = state['_ix_to_char']
            self.apply_params()
            self._model.load_state_dict(state['_model'])
            self._optimizer.load_state_dict(state['_optimizer'])

    def _get_device(self):
        """Get device to predict or train"""
        device = self.params['device']
        if device == 'auto':
            return DEVICE
        if device in ('cpu', ):
            return torch.device('cpu')
        if device in ('gpu', 'cuda'):
            return torch.device('cuda')

    def apply_params(self):
        """Apply params and build RNN-CRF model"""

        embedding_dim = self.params['embedding_dim']
        hidden_dim = self.params['hidden_dim']
        weight_decay = self.params['weight_decay']
        embedding_dropout_p = self.params['embedding_dropout_p']
        rnn_dropout_p = self.params['rnn_dropout_p']
        bidirectional = self.params['bidirectional']
        rnn_type = self.params['rnn_type']
        num_layers = self.params['num_layers']
        optimizer = self.params['optimizer']
        momentum = self.params['momentum']
        embedding_trainable = self.params['embedding_trainable']
        use_crf = self.params['use_crf']
        use_char = self.params['use_char']
        char_max_len = self.params['char_max_len']
        char_embedding_dim = self.params['char_embedding_dim']
        char_hidden_dim = self.params['char_hidden_dim']
        char_dropout_p = self.params['char_dropout_p']
        char_bidirectional = self.params['char_bidirectional']
        average_loss = self.params['average_loss']

        word_to_ix = self._word_to_ix
        tag_to_ix = self._tag_to_ix
        char_to_ix = self._char_to_ix

        model = TaggerModel(
            len(word_to_ix),
            tag_to_ix,
            embedding_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=bidirectional,
            device=self._get_device(),
            embedding_dropout_p=embedding_dropout_p,
            rnn_dropout_p=rnn_dropout_p,
            rnn_type=rnn_type,
            embedding_trainable=embedding_trainable,
            use_crf=use_crf,
            use_char=use_char,
            char_max_len=char_max_len,
            char_embedding_dim=char_embedding_dim,
            char_vocab_size=len(char_to_ix),
            char_hidden_dim=char_hidden_dim,
            char_dropout_p=char_dropout_p,
            char_bidirectional=char_bidirectional,
            average_loss=average_loss).to(self._get_device())

        if optimizer.lower() == 'adam':
            optimizer = optim.Adam(
                model.parameters(),
                lr=self._get_learning_rate(),
                weight_decay=weight_decay)
        elif optimizer.lower() == 'sgd':
            optimizer = optim.SGD(
                model.parameters(),
                lr=self._get_learning_rate(),
                weight_decay=weight_decay,
                momentum=momentum)

        self._model = model
        self._optimizer = optimizer

    def fit(self,
            X,
            y,
            X_dev=None,
            y_dev=None,
            patient_dev=None,
            save_best=None,
            pretrained_embedding=None,
            predict_batch_size=32):
        """Fit the model"""

        assert len(X) >= self.params['batch_size'], 'X must size >= batch_size'
        assert len(y) >= self.params['batch_size'], 'y must size >= batch_size'
        assert len(X) == len(y), 'X must size equal to y'

        # Autommatic build vocabulary
        vocabulary = build_vocabulary(X, y)
        self._char_to_ix = vocabulary['char_to_ix']
        self._ix_to_char = vocabulary['ix_to_char']
        if self._word_to_ix is None and self._tag_to_ix is None:
            self._word_to_ix = vocabulary['word_to_ix']
            self._ix_to_word = vocabulary['ix_to_word']
            self._tag_to_ix = vocabulary['tag_to_ix']
            self._ix_to_tag = vocabulary['ix_to_tag']
        elif self._word_to_ix is None:
            self._word_to_ix = vocabulary['word_to_ix']
            self._ix_to_word = vocabulary['ix_to_word']
        elif self._tag_to_ix is None:
            self._tag_to_ix = vocabulary['tag_to_ix']
            self._ix_to_tag = vocabulary['ix_to_tag']

        epochs = self.params['epochs']
        verbose = self.params['verbose']
        batch_size = self.params['batch_size']
        learning_rate_decay = self.params['learning_rate_decay']
        char_max_len = self.params['char_max_len']
        clip_grad_norm = self.params['clip_grad_norm']
        average_loss = self.params['average_loss']

        predict_batch_size = max(predict_batch_size, batch_size)

        word_to_ix = self._word_to_ix
        tag_to_ix = self._tag_to_ix
        char_to_ix = self._char_to_ix

        self.apply_params()
        model, optimizer = self._model, self._optimizer
        if pretrained_embedding is not None:
            model.load_embedding(pretrained_embedding)

        dev_best = float('inf')
        dev_best_round = 0
        # Make sure prepare_sequence from earlier in the LSTM section is loaded
        for epoch in range(epochs):
            model.train()
            model.zero_grad()
            lnrt = self._get_learning_rate()
            if learning_rate_decay > 0:
                lnrt = lnrt / (1 + epoch * learning_rate_decay)
                for param_group in optimizer.param_groups:
                    param_group['lr'] = lnrt
            pbar = range(len(X) // batch_size + 1)
            flow = batch_flow(
                X,
                y,
                word_to_ix,
                tag_to_ix,
                batch_size=batch_size,
                char_max_len=char_max_len,
                char_to_ix=char_to_ix)
            losses = []
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0)
                pbar.set_description('epoch: {}/{} loss: {:.4f}'.format(
                    epoch + 1, epochs, 0))
            for _ in pbar:
                x_b, y_b, l_b, l_c, ll_c = next(flow)
                x_b = x_b.to(self._get_device())
                y_b = y_b.to(self._get_device())
                l_b = l_b.to(self._get_device())
                if l_c is not None:
                    l_c = l_c.to(self._get_device())
                    ll_c = ll_c.to(self._get_device())
                loss = model.compute_loss(
                    x_b, y_b, l_b, chars=l_c, charlens=ll_c)
                losses.append(loss.item())
                loss.backward()
                if clip_grad_norm is not None:
                    nn.utils.clip_grad_norm_(model.parameters(),
                                             clip_grad_norm)
                optimizer.step()
                model.zero_grad()
                if verbose > 0:
                    pbar.set_description(
                        'epoch: {}/{} loss: {:.4f} lr: {:.4f}'.format(
                            epoch + 1, epochs, np.mean(losses), lnrt))
            train_score = self.score(X, y, batch_size=predict_batch_size)
            dev_score = None
            if X_dev is None:
                if verbose > 0:
                    print('train: {:.4f}'.format(train_score))
            else:
                model.eval()
                with torch.no_grad():
                    dev_score = self.score(
                        X_dev, y_dev, batch_size=predict_batch_size)
                    flow = batch_flow(
                        X_dev,
                        y_dev,
                        word_to_ix,
                        tag_to_ix,
                        batch_size=predict_batch_size,
                        char_max_len=char_max_len,
                        char_to_ix=char_to_ix)
                    dev_losses = []
                    for _ in range(math.ceil(len(X_dev) / predict_batch_size)):
                        x_b, y_b, l_b, l_c, ll_c = next(flow)
                        x_b = x_b.to(self._get_device())
                        y_b = y_b.to(self._get_device())
                        l_b = l_b.to(self._get_device())
                        if l_c is not None:
                            l_c = l_c.to(self._get_device())
                            ll_c = ll_c.to(self._get_device())
                        loss = model.compute_loss(
                            x_b, y_b, l_b, chars=l_c, charlens=ll_c)
                        dev_losses.append(loss.item())
                    dev_loss = np.mean(dev_losses)
                    if not average_loss:
                        dev_loss /= (predict_batch_size / batch_size)

                if verbose > 0:
                    print('dev loss: {:.4f}, train f1: {:.4f}, dev f1: {:.4f}'.
                          format(dev_loss, train_score, dev_score))
                if isinstance(save_best, str):
                    if dev_loss < dev_best:
                        print('save best {:.4f} > {:.4f}'.format(
                            dev_best, dev_loss))
                        dev_best = dev_loss
                        dev_best_round = 0
                        save_dir = os.path.realpath(os.path.dirname(save_best))
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        with open(save_best, 'wb') as fobj:
                            pickle.dump(self, fobj)
                    else:
                        dev_best_round += 1
                        print('no better {:.4f} <= {:.4f} {}/{}'.format(
                            dev_best, dev_loss, dev_best_round, patient_dev))
                        if isinstance(patient_dev,
                                      int) and dev_best_round >= patient_dev:
                            return
                print()

    def predict(self, X, batch_size=None, verbose=0, max_limit=300):
        """Predict tags"""
        model = self._model
        word_to_ix = self._word_to_ix
        ix_to_tag = self._ix_to_tag
        char_to_ix = self._char_to_ix
        model.eval()
        if batch_size is None:
            batch_size = self.params['batch_size']
        char_max_len = self.params['char_max_len']
        # Check predictions after training
        data = list(enumerate(X))
        data = sorted(data, key=lambda t: len(t[1]), reverse=True)
        inds = [i for i, _ in data]
        X = [x for _, x in data]
        ret = [None] * len(X)
        with torch.no_grad():
            batch_total = math.ceil(len(X) / batch_size)
            pbar = range(batch_total)
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0)
            for i in pbar:
                ind_batch = inds[i * batch_size:(i + 1) * batch_size]
                x_batch = X[i * batch_size:(i + 1) * batch_size]
                x_batch = [sent[:max_limit] for sent in x_batch]
                lens = [len(x) for x in x_batch]
                max_len = np.max(lens)

                char_batch = None
                char_len_batch = None
                if char_to_ix is not None:
                    char_batch, char_len_batch = extract_char_features(
                        x_batch, char_max_len, char_to_ix, max_len)

                x_batch = [
                    prepare_sequence(sent, word_to_ix) for sent in x_batch
                ]
                x_batch = [pad_seq(x, max_len) for x in x_batch]

                sent = torch.from_numpy(np.asarray(x_batch)).to(
                    self._get_device())
                lens = torch.Tensor(lens).long().to(self._get_device())
                char_batch = torch.from_numpy(np.asarray(char_batch)).to(
                    self._get_device())
                char_len_batch = torch.from_numpy(
                    np.asarray(char_len_batch,
                               dtype=np.int32)).to(self._get_device())
                _, predicts = model(sent, lens, char_batch, char_len_batch)
                for ind, tag_len, tags in zip(ind_batch, lens, predicts):
                    tags = [ix_to_tag[i] for i in tags[:tag_len]]
                    ret[ind] = tags
        return ret

    def score(self, X, y, batch_size=None, verbose=0, detail=False):
        """Calculate NER F1
        Based CONLL 2003 standard
        """

        def _get_sets():
            preds = self.predict(X, verbose=verbose, batch_size=batch_size)
            pbar = enumerate(zip(preds, y))
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0, total=len(y))

            apset = []
            arset = []
            for i, (pred, y_true) in pbar:
                pset = extract_entities(pred)
                rset = extract_entities(y_true)
                for item in pset:
                    apset.append(tuple([i] + list(item)))
                for item in rset:
                    arset.append(tuple([i] + list(item)))
            return apset, arset

        apset, arset = _get_sets()
        pset = set(apset)
        rset = set(arset)
        inter = pset.intersection(rset)
        precision = len(inter) / len(pset) if pset else 1
        recall = len(inter) / len(rset) if rset else 1
        f1score = 0
        if precision + recall > 0:
            f1score = 2 * ((precision * recall) / (precision + recall))
        if detail:
            return precision, recall, f1score
        return f1score
