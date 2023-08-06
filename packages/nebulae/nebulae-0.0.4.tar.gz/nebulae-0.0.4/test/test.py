#!/usr/bin/env python
'''
test
Created by Seria at 05/11/2018 9:13 PM
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

import nebulae
import tensorflow as tf

# fg = nebulae.toolkit.FuelGenerator(file_dir='/Users/Seria/Desktop/nebulae/test',
#                                   file_list='label.csv',
#                                   dtype=['uint8', 'int8'],
#                                   channel=3,
#                                   height=224,
#                                   width=224,
#                                   encode='png')
# fg.editProperty(encode='jpeg')
# fg.generateFuel('/Users/Seria/Desktop/nebulae/test/img/testimg.hdf5')

# fd = nebulae.fuel.FuelDepot()
# fd.loadFuel(name='test-img',
#             batch_size=4,
#             key_data='image',
#             data_path='/Users/Seria/Desktop/nebulae/test/mer/pae.hdf5',
#             width=200, height=200,
#             resol_ratio=0.5,
#             spatial_aug='brightness,gamma_contrast',
#             p_sa=(0.5, 0.5), theta_sa=(0.1, 1.2))
# config = {'name':'test', 'batch_size':128}
# fd.editProperty(dataname='test-img', config=config)
# for s in range(fd.stepsPerEpoch('test')):
#     batch = fd.nextBatch('test')
#     print(fd.currentEpoch('test'), batch['label'].shape)
# fd.unloadFuel('test')
#
# label = ['1 2','1 3', '0']
# print(nebulae.toolkit.toOneHot(label, 5))



fg = nebulae.toolkit.FuelGenerator(file_dir='/Volumes/Dataset/hand143_panopticdb',
                                  file_list='hands_v143_14817.csv',
                                  dtype=['uint8'] + 42*['float32'],
                                  channel=3,
                                  height=368,
                                  width=368,
                                  encode='jpeg')
fg.generateFuel('/Volumes/Dataset/hand143_panopticdb/handkpt.hdf5')
# fd = nebulae.fuel.FuelDepot()
# fname = 'por'
# fd.loadFuel(name=fname+'-t',
#             batch_size=32,
#             channel=1,
#             data_path='/Users/Seria/Desktop/nebulae/test/porosity_train.hdf5',
#             data_key='image',
#             spatial_aug='flip',
#             p_sa=(0.5,), theta_sa=(0,))
# fd.loadFuel(name=fname+'-v',
#             batch_size=32,
#             channel=1,
#             data_path='/Users/Seria/Desktop/nebulae/test/porosity_val.hdf5',
#             data_key='image')
#
# ls = nebulae.aerolog.LayoutSheet('/Users/Seria/Desktop/nebulae/test/por_ls')
#
# COMP = nebulae.spacedock.Component()
# scope = 'sc'
# sc = nebulae.spacedock.SpaceCraft(scope, layout_sheet=ls)
# sc.fuelLine('input', (None, 32, 32, 1), 'float32')
# sc.fuelLine('label', (None), 'int64')
# sc.fuelLine('is_train', (), 'bool', default=False)
# comp_conv1 = (COMP.CONV(name='conv1', input=sc.layout['input'], kernel_size=[3, 3], in_out_chs=[1, 4])
#             >> COMP.RELU(name='relu1')
#             >> COMP.MAX_POOL(name='max_pool1'))
# comp_conv2 = (COMP.CONV(name='conv2', kernel_size=[3, 3], in_out_chs=[4, 8], w_init='rand_norm')
#             >> COMP.RELU(name='relu2')
#             >> COMP.BATCH_NORM(name='bn1', is_train=sc.layout['is_train']))
#             # >> COMP.MAX_POOL(name='max_pool2'))
# comp_conv3 = (COMP.CONV(name='conv3', input=sc.layout['input'], kernel_size=[3, 3], in_out_chs=[1, 8])
#             >> COMP.RELU(name='relu3')
#             >> COMP.BATCH_NORM(name='bn2', is_train=sc.layout['is_train'])
#             >> COMP.MAX_POOL(name='max_pool3'))
# outnode = sc.assembleComp((comp_conv1 >> comp_conv2) + comp_conv3)
#
# comp_out = (COMP.FLAT(name='flat1', input=sc.layout[outnode])
#             >> COMP.DENSE(name='fc1', out_chs=2)
#             >> COMP.SFTM_XENTROPY(name='sftm_xe1', labels=sc.layout['label'], one_hot=False))
# totloss = sc.assembleComp(comp_out+COMP.WEIGHT_DECAY(name='wd', penalty=4e-5))
# outnode = sc.assembleComp(COMP.MOMENTUM(name='momentum', input=sc.layout[totloss], mile_meter=sc.miles,
#                                         lr=0.005, update_scope=scope, lr_decay='exp_stair',
#                                         lr_miles=500, decay_param=0.8, grad_limit=4.))
# prob = sc.assembleComp(COMP.SOFTMAX(name='sftm1', input=sc.layout['fc1']))
# ls._generateLS()
#
#
#
# config = tf.ConfigProto(allow_soft_placement=True)
# sess = tf.Session(config=config)
#
# # correct = tf.equal(tf.cast(tf.round(sc.layout[prob]), tf.int64), sc.layout['label'])
# correct = tf.equal(tf.argmax(sc.layout[prob], 1), sc.layout['label'])
# accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
# sess.run(tf.global_variables_initializer())
#
# for s in range(fd.milesPerEpoch(fname+'-t')):
#     batch = fd.nextBatch(fname+'-t')
#     _, acc, loss = sess.run([sc.layout[outnode], accuracy, sc.layout[totloss]],
#                             feed_dict={sc.layout['input']: batch['image'],
#                                        sc.layout['label']: batch['label'],
#                                        sc.layout['is_train']: True})
#     if s % 64 == 0:
#         print('epoch #%d: acc: %.2f%%, loss: %.4f' % (fd.currentEpoch(fname+'-t'), acc * 100, loss))
# print(50*'=')
# acc_tot = 0
# loss_tot = 0
# steps = fd.milesPerEpoch(fname+'-v')
# for s in range(steps):
#     batch = fd.nextBatch(fname+'-v')
#     acc, loss = sess.run([accuracy, sc.layout[totloss]], feed_dict={sc.layout['input']: batch['image'],
#                                                                     sc.layout['label']: batch['label'],
#                                                                     sc.layout['is_train']: False})
#     acc_tot += acc
#     loss_tot += loss
# print('epoch #%d: acc: %.2f%%, loss: %.4f' % (fd.currentEpoch(fname+'-v'), acc_tot/steps * 100, loss_tot/steps))
#
# fd.unloadFuel(fname+'-t')
# fd.unloadFuel(fname+'-v')