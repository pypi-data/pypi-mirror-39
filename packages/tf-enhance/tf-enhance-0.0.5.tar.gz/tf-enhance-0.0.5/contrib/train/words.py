#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from contrib.train.basic import BasicTrainOperation


class WordsTrainOperation(BasicTrainOperation):

    def __init__(self, batches, state_op, n_steps):
        BasicTrainOperation.__init__(self)

        self.state_op = state_op
        self.batches = batches

        self.n_steps = n_steps

    def each_epoch(self):

        total_losses = 0.0
        ite = 0
        state = self.sess.run(self.state_op)

        for x, y in self.batches:
            self.log.start_step()
            loss, state, _ = self.sess.run([self.loss_op, self.state_op, self.train_op],
                                           feed_dict={self.inputs: x, self.labels: y,
                                                      self.state_op: state})
            total_losses += loss
            ite += self.n_steps

            self.log.end_step(np.exp(total_losses / ite))
