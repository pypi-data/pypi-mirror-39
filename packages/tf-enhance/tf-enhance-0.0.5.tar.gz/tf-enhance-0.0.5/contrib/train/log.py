#!/usr/bin/python
# -*- coding=UTF-8 -*-
import time
import sys
import numpy as np


class TrainLog(object):

    def __init__(self,
                 train_name,
                 epochs,
                 steps_pre_epoch,
                 save_log=True,
                 save_log_path=None,
                 process_bar_len=20):

        self.name = train_name
        self.save_log_path = save_log_path
        self.save_log = save_log
        self.start_train_time = None
        self.start_epoch_time = None
        self.start_step_time = None

        self.process_bar_len = process_bar_len

        self.total_losses = []
        self.total_acc = []

        self.epochs = epochs
        self.steps_pre_epoch = steps_pre_epoch
        self.epoch = 0
        self.step = 0

        self.valids = {}

    def start_train(self):
        self.start_train_time = time.time()
        print('Start training {}'.format(self.name),
              'on {}'.format(self.current_time_format()),
              'by TensorFlow-enhance')

    def start_epoch(self):
        self.start_epoch_time = time.time()
        self.epoch = 0

    def start_step(self):
        self.start_step_time = time.time()
        self.step = 0

    def end_step(self, loss=None, acc=None):
        if self.step >= self.steps_pre_epoch:
            n_arrows = self.process_bar_len
            n_lines = 0
        else:
            n_arrows = int(self.step * self.process_bar_len / self.steps_pre_epoch)
            n_lines = self.process_bar_len - n_arrows

        n_head = 0 if n_arrows == 0 else 1
        took_time = time.time() - self.start_step_time

        # 1. Epoch
        # 2. Step
        # 3. Process bar
        # 4. metrics(If provided)
        # 5. took time
        bar = 'Epoch {}/{}'.format(self.epoch, self.epochs) +\
              '{}/{}'.format(self.step, self.steps_pre_epoch) +\
              '|' + '=' * (n_arrows - 1) + '>' * n_head + '.' * n_lines

        def append_metrics(pbar, metric, metric_name, metric_container):
            if metric is not None:
                if type(metric) == list or type(metric) == tuple:
                    pbar += '{}={.3f} '.format(metric_name, metric[0])
                    if len(metric) == 2:
                        valid_metric = metric[1]
                        self.valids[metric_name] = valid_metric
                    else:
                        if metric_name in self.valids:
                            valid_metric = self.valids[metric_name]
                        else:
                            valid_metric = None
                    if valid_metric is not None:
                        pbar += 'valid_{}={:.3f} '.format(metric_name,
                                                          valid_metric)
                    metric_container.append(metric)
                else:
                    return append_metrics(pbar, [metric], metric_name, metric_container)
            return pbar

        bar = append_metrics(bar, loss, 'loss', self.total_losses)
        bar = append_metrics(bar, acc, 'acc', self.total_acc)
        bar += '{:.2f} s/step'.format(took_time)

        bar += '\r'

        sys.stdout.write(bar)
        sys.stdout.flush()

    def end_epoch(self):
        print('\n')

    def end_train(self):
        print('End training {}'.format(self.name),
              'On {}'.format(self.current_time_format()),
              'Took {:.2}s totally'.format(time.time() - self.start_train_time))

        if self.save_log:
            log = []
            if len(self.total_losses) != 0:
                log.append(self.total_losses)
            if len(self.total_acc) != 0:
                log.append(self.total_acc)

            if self.save_log_path is None:
                self.save_log_path = '{}_log.npy'.format(self.name)

            if len(log) != 0:
                np.save(self.save_log_path, log)
                print('Saved train log at', self.save_log_path)
            else:
                print('Nothing to save! Please provide metric when training!')

    @staticmethod
    def current_time_format():
        return time.strftime('%Y/%m/%d %H:%H:%S')
