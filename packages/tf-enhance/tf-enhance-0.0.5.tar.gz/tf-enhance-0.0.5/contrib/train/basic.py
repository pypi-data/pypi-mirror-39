#!/usr/bin/python
# -*- coding=UTF-8 -*-
import tensorflow as tf

from contrib.train.log import TrainLog


class BasicTrainOperation(object):

    def __init__(self):

        self.train_op = None
        self.loss_op = None
        self.acc_op = None
        self.init_op = None
        self.sess_init_op = None
        self.inputs = None
        self.labels = None
        self.train_name = None
        self.epochs = None
        self.model_saver = None

        self.sess = None

        self.graph = None

        self.step_pre_epoch = None
        self.log = None

        self.params_done = False

    def set_params(self,
                   train_name,
                   train_op,
                   epochs,
                   model_saver,
                   inputs,
                   init_op=tf.global_variables_initializer(),
                   labels=None,
                   graph=None,
                   sess_init_op=None,
                   loss_op=None,
                   acc_op=None):

        self.train_op = self.unpack_op(train_op, 'train_op')
        self.loss_op = loss_op
        self.acc_op = acc_op
        self.init_op = init_op
        self.train_name = train_name
        self.epochs = epochs
        self.model_saver = model_saver
        self.inputs = inputs
        self.labels = labels
        self.graph = graph if graph is not None \
            else tf.get_default_graph()

        self.step_pre_epoch = None
        self.log = None

        self.params_done = True

        self.sess_init_op = sess_init_op

    def start_training(self,
                       save_log=True,
                       save_log_path=None,
                       process_bar_len=20):
        if not self.params_done:
            raise ValueError('Please call set_params() before starting training!')

        self.log = TrainLog(self.train_name, self.epochs,
                            self.step_pre_epoch, save_log,
                            save_log_path, process_bar_len)
        self.log.start_train()

        self.sess = tf.Session(graph=self.graph)
        self.initialize()

        for epoch in range(self.epochs):
            self.log.start_epoch()
            self.each_epoch()
            self.log.end_epoch()

        self.save_model()
        self.end_training()

    def initialize(self):
        self.sess.run(self.init_op)

    def each_epoch(self):
        pass

    def save_model(self):
        self.model_saver.save(self.sess)

    def end_training(self):
        self.sess.close()

    def each_step(self, train_x, valid_x=None,
                  train_y=None, valid_y=None,
                  other_params=None):
        train_feed_dict = self.create_feed_dict(train_x, train_y, other_params)

        valid_feed_dict = self.create_feed_dict(valid_x, valid_y, other_params) \
            if valid_x is not None else None  # create valid feed dict only when valid_x exist.

        loss = self.get_metric(self.loss_op, train_feed_dict, valid_feed_dict)
        acc = self.get_metric(self.acc_op, train_feed_dict, valid_feed_dict)

        for op in self.train_op:
            self.sess.run(op, feed_dict=train_feed_dict)

        return loss, acc

    @staticmethod
    def unpack_op(op, op_name):
        if op is None:
            return None
        if type(op) == list:
            return op
        elif type(op) == tuple:
            return [op]
        else:
            raise ValueError('Operation must be tuple or list.'
                             'Found {} for {}'.format(type(op), op_name))

    def create_feed_dict(self, x, y=None, other_params=None):
        feed_dict = {self.inputs: x}
        if y is not None:
            feed_dict[self.labels] = y
        if other_params is not None:
            for k, v in other_params.items():
                feed_dict[k] = v
        return feed_dict

    def get_metric(self, op, train_feed_dict, valid_feed_dict):
        if op is not None:
            metric = [self.sess.run(op, feed_dict=train_feed_dict)]
            if valid_feed_dict is not None:
                metric.append(self.sess.run(op, feed_dict=valid_feed_dict))

            return metric
        else:
            return None


