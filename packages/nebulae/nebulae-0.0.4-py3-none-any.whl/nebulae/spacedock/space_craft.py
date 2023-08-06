#!/usr/bin/env python
'''
space_craft
Created by Seria at 23/11/2018 10:31 AM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-

import tensorflow as tf
import numpy as np
from .component import Pod

class SpaceCraft(object):
    def __init__(self, scope='', reuse=None, layout_sheet=None):
        if scope:
            self.scope = scope + '/'
        else:
            self.scope = scope
        if reuse is None:
            self.reuse = tf.AUTO_REUSE
        self.miles = tf.Variable(0, trainable=False)
        self.valid_dtypes = ['uint8', 'uint16', 'uint32', 'int8', 'int16', 'int32', 'int64',
                             'float16', 'float32', 'float64', 'str', 'bool']
        self.operands = {'+': tf.add, '-': tf.subtract, '*': tf.multiply, '@': tf.matmul, '&': tf.concat}
        self.layout = {}
        if layout_sheet is None:
            self.verbose = False
        else:
            self.layout_sheet = layout_sheet
            self.verbose = True

    def fuelLine(self, name, shape, dtype, default=None):
        if dtype not in self.valid_dtypes:
            raise Exception('%s is not a valid data type.' % dtype)
        if not default is None:
            self.layout[name] = tf.placeholder_with_default(tf.constant(default, dtype=dtype),
                                                            shape, 'FL/DEFAULT' + name)
        else:
            self.layout[name] = tf.placeholder(tf.as_dtype(dtype), shape, 'FL/' + name)

    def _getHull(self, component):
        tshape = component.get_shape()
        if tshape.dims is None or tshape.ndims == 0:
            return ' 1    '
        shape = tshape[1:].as_list()
        len_wo_bs = len(shape) - 1
        hull = ' '
        for dim in range(len_wo_bs):
            hull += '%-4d x ' % shape[dim]
        hull += '%-5d' % shape[-1]
        return hull

    def assemble(self, left_comp, right_comp=None, gear='fit', assemblage=None, sub_scope='', is_external=True):
        if not isinstance(left_comp, Pod):
            raise TypeError('Only the members from Component can be assembled.')
        if sub_scope:
            sub_scope += '/'
        if self.scope[:3] == 'FL/':
            raise ValueError('FL is the reserved words for fuel lines in spacecraft. Please change your scope name.')
        len_prefix = len(self.scope)
        if not is_external:
            scope = ''
        else:
            scope = self.scope
        with tf.variable_scope(scope, reuse=self.reuse):
            with tf.variable_scope(sub_scope, reuse=self.reuse):
                left_symbol = left_comp.symbol
                if gear == 'fit':
                    if not isinstance(left_symbol, str) or not left_symbol: # this is an individual component
                        if assemblage is None:
                            assert not isinstance(left_symbol, str)
                            self.layout[sub_scope+left_comp.name] = left_comp.component()
                            if self.verbose: # draw layout sheet
                                hull = self._getHull(left_symbol)
                                if left_symbol.name.startswith('FL/'): # if the input is a fuel line
                                    self.layout_sheet._drawNode(left_symbol.op.name[3:], sub_scope+left_comp.name,
                                                                hull, init=True)
                                else:
                                    self.layout_sheet._drawNode(left_symbol.op.name[len_prefix:],
                                                                sub_scope + left_comp.name, hull)
                        else:
                            if isinstance(left_symbol, int):
                                self.layout[sub_scope+left_comp.name] = left_comp.component(mile_meter=self.miles,
                                                                                    input=self.layout[assemblage])
                            else:
                                self.layout[sub_scope+left_comp.name] = left_comp.component(input=self.layout[assemblage])
                            if self.verbose:  # draw layout sheet
                                hull = self._getHull(self.layout[assemblage])
                                self.layout_sheet._drawNode(assemblage, sub_scope + left_comp.name, hull)
                                if not isinstance(left_symbol, str):
                                    hull = self._getHull(left_symbol)
                                    if left_symbol.name.startswith('FL/'):  # if the input is a fuel line
                                        self.layout_sheet._drawNode(left_symbol.op.name[3:], sub_scope+left_comp.name,
                                                                    hull, init=True)
                                    else:
                                        hull = self._getHull(self.layout[assemblage])
                                        self.layout_sheet._drawNode(left_symbol.op.name[len_prefix:],
                                                                    sub_scope + left_comp.name, hull)
                        return left_comp.name
                    elif left_symbol == '>':
                        for comp in left_comp.component:
                            assemblage = self.assemble(comp, assemblage=assemblage,
                                                           sub_scope=sub_scope, is_external=False)
                        return assemblage
                    elif left_symbol in ['+', '-', '*', '@', '&']:
                        operator = None
                        assemblage_name = left_comp.name
                        assemblage_list = []
                        hull_list = []
                        init_assemblage = assemblage
                        for comp in left_comp.component:
                            assemblage = self.assemble(comp, assemblage=init_assemblage,
                                                           sub_scope = sub_scope, is_external=False)
                            assemblage_name += '-'+assemblage
                            assemblage_list.append(assemblage)
                            if self.verbose:
                                hull = self._getHull(self.layout[assemblage])
                                hull_list.append(hull)
                            if operator is None:
                                operator = self.layout[assemblage]
                            else:
                                if left_symbol == '&':
                                    operator = self.operands[left_symbol]([operator, self.layout[assemblage]],
                                                                           axis=-1, name=assemblage_name)
                                else:
                                    operator = self.operands[left_symbol](operator,
                                                                       self.layout[assemblage],
                                                                       name=assemblage_name)
                        self.layout[sub_scope+assemblage_name] = operator
                        if self.verbose:
                            self.layout_sheet._combineNodes(assemblage_list, hull_list,
                                                            sub_scope+assemblage_name, left_symbol)
                        return assemblage_name
                    else:
                        raise TypeError('unsupported operand type for %s: "Pod" and "Pod".' % left_comp.symbol)
                # elif gear == ''