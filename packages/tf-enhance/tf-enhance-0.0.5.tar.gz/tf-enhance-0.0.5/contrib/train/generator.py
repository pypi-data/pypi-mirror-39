#!/usr/bin/python
# -*- coding: UTF-8 -*-
from contrib.train.basic import BasicTrainOperation


class GeneratorTrainOperation(BasicTrainOperation):

    def __init__(self, train_generator, step_pre_epoch,
                 valid_generator=None, valid_pre_step=0):
        BasicTrainOperation.__init__(self)

        self.train_generator = train_generator
        self.step_pre_epoch = step_pre_epoch
        self.valid_generator = valid_generator
        self.valid_pre_step = valid_pre_step

    def each_epoch(self):

        step = 0
        for x, y in self.train_generator.next():
            self.log.start_step()

            valid_x, valid_y = None, None
            if step % self.valid_pre_step == 0:
                valid_x, valid_y = self.valid_generator.next()

            loss, acc = self.each_step(train_x=x, train_y=y,
                                       valid_x=valid_x, valid_y=valid_y)

            self.log.end_step(loss, acc)
