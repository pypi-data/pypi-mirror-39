#!/usr/bin/env python
'''
kpi
Created by Seria at 14/12/2018 12:11 PM
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
import os

# fg = nebulae.toolkit.FuelGenerator(file_dir='/home/ai/challenge/train_clean',
#                                   file_list='kpi18_ct.csv',
#                                   dtype=['uint8'] + ['int32'],
#                                   channel=3,
#                                   height=256,
#                                   width=256,
#                                   encode='jpeg')
# fg.generateFuel('/home/ai/seria/data/kpi18_ct.hdf5')

fd = nebulae.fuel.FuelDepot()
fname = 'kpi'
fd.loadFuel(name=fname + '-ct',
            batch_size=64,
            height=224,
            width=224,
            channel=3,
            data_path='/home/ai/seria/data/kpi18_ct.hdf5',
            data_key='image',
            spatial_aug='flip,crop',
            p_sa=(0.5, 0.5),
            theta_sa=(0, ((0.25, 1), (3/4, 4/3))))
fd.loadFuel(name=fname + '-cv',
            batch_size=32,
            height=224,
            width=224,
            channel=3,
            data_path='/home/ai/seria/data/kpi18_cv.hdf5',
            data_key='image',
            if_shuffle=False)

ls = nebulae.aerolog.LayoutSheet('/home/ai/seria/kpi_ls')


# fd = nebulae.fuel.FuelDepot()
# fname = 'kpi'
# fd.loadFuel(name=fname + '-tc',
#             batch_size=32,
#             height=224,
#             width=224,
#             channel=3,
#             data_path='/home/ai/seria/data/kpi18_trc.hdf5',
#             data_key='image',
#             spatial_aug='flip',
#             p_sa=(0.5,), theta_sa=(0,))
# # fd.loadFuel(name=fname + '-v',
# #             batch_size=32,
# #             channel=1,
# #             data_path='/Users/Seria/Desktop/nebulae/test/porosity_val.hdf5',
# #             data_key='image',
# #             if_shuffle=False)
# #
# ls = nebulae.aerolog.LayoutSheet('/home/ai/seria/por_ls')
#
COMP = nebulae.spacedock.Component()
scope = 'vgg_16'
sc = nebulae.spacedock.SpaceCraft(scope, layout_sheet=ls)
sc.fuelLine('input', (None, 224, 224, 3), 'float32')
sc.fuelLine('label', (None), 'int64')
# sc.fuelLine('is_train', (), 'bool', default=False)
COMP.addComp('conv_3x3', COMP.CONV(name='conv_3x3', k_size=[3, 3]))
conv1 = (COMP.CONV_3X3(name='conv1_1', input=sc.layout['input'], in_out_chs=[3, 64])
      >> COMP.CONV_3X3(name='conv1_2', in_out_chs=[64, 64])
      >> COMP.RELU(name='relu1')
      >> COMP.MAX_POOL(name='pool1'))
conv2 = (COMP.CONV_3X3(name='conv2_1', in_out_chs=[64, 128])
      >> COMP.CONV_3X3(name='conv2_2', in_out_chs=[128, 128])
      >> COMP.RELU(name='relu2')
      >> COMP.MAX_POOL(name='pool2'))
conv3 = (COMP.CONV_3X3(name='conv3_1', in_out_chs=[128, 256])
      >> COMP.CONV_3X3(name='conv3_2', in_out_chs=[256, 256])
      >> COMP.CONV_3X3(name='conv3_3', in_out_chs=[256, 256])
      >> COMP.RELU(name='relu3')
      >> COMP.MAX_POOL(name='pool3'))
conv4 = (COMP.CONV_3X3(name='conv4_1', in_out_chs=[256, 512])
      >> COMP.CONV_3X3(name='conv4_2', in_out_chs=[512, 512])
      >> COMP.CONV_3X3(name='conv4_3', in_out_chs=[512, 512])
      >> COMP.RELU(name='relu4')
      >> COMP.MAX_POOL(name='pool4'))
conv5 = ((COMP.CONV_3X3(name='conv5', in_out_chs=[512, 512]) ** 3)
      >> COMP.RELU(name='relu5')
      >> COMP.MAX_POOL(name='pool5'))
fc6 = (COMP.CONV(name='fc6', k_size=[7, 7], in_out_chs=[512, 4096], padding='valid')
      >> COMP.DROPOUT(name='drop6', p_drop=0.5))
fc7 = (COMP.CONV(name='fc7', k_size=[1, 1], in_out_chs=[4096, 4096])
      >> COMP.DROPOUT(name='drop7', p_drop=0.5))
fc8 = (COMP.FLAT(name='flat1')
      >> COMP.DENSE(name='fc8', out_chs=128))
obj = (COMP.SFTM_XENTROPY(name='sftm_xe1', label=sc.layout['label'], one_hot=False)
      + COMP.WEIGHT_DECAY(name='wd', input=4e-5))
cost = sc.assemble(conv1 >> conv2 >> conv3 >> conv4 >> conv5 >> fc6 >> fc7 >> fc8 >> obj)

# cost = sc.assemble(obj)

prob = sc.assemble(COMP.SOFTMAX(name='sftm1', input=sc.layout['fc8']))

mmnt = COMP.ADAM(name='adam', input=sc.layout[cost], mile_meter=sc.miles,
                     lr=6e-5, update_scope=scope, lr_decay='exp_stair',
                     lr_miles=900, decay_param=0.9, grad_limit=4.)
optz = sc.assemble(mmnt)

ls._generateLS()

config_proto = tf.ConfigProto(allow_soft_placement=True)
config_proto.gpu_options.per_process_gpu_memory_fraction = 0.6
config_proto.gpu_options.visible_device_list = '0'
sess = tf.Session(config=config_proto)

# correct = tf.equal(tf.cast(tf.round(sc.layout[prob]), tf.int64), sc.layout['label'])
correct = tf.equal(tf.argmax(sc.layout[prob], 1), sc.layout['label'])
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
sess.run(tf.global_variables_initializer())


mdir = '/home/ai/seria/model/vgg-d'
if not os.path.exists(mdir):
    os.mkdir(mdir)
# ckpt = tf.train.latest_checkpoint(mdir)
# variable = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='vgg_16')
# import pdb
# pdb.set_trace()
# restorer = tf.train.Saver(variable)
# restorer.restore(sess, ckpt)

# ckpt = tf.train.get_checkpoint_state(mdir)
# saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')

saver = tf.train.Saver(tf.global_variables(), max_to_keep=2)


for s in range(7*fd.milesPerEpoch(fname + '-ct')):
    batch = fd.nextBatch(fname + '-ct')
    _, acc, loss = sess.run([sc.layout[optz], accuracy, sc.layout[cost]],
                            feed_dict={sc.layout['input']: batch['image'],
                                       sc.layout['label']: batch['label']})
    if s % 25 == 0:
        print('epoch #%d - %d miles acc: %.2f%%, loss: %.4f' % (fd.currentEpoch(fname + '-ct'), s, acc * 100, loss))
        if s % 100 == 0:
            saver.save(sess, mdir, global_step=s, write_meta_graph=True)
    if s>0 and s%fd.milesPerEpoch(fname + '-ct') == 0:
        print(50 * '=')
        acc_tot = 0
        loss_tot = 0
        steps = fd.milesPerEpoch(fname + '-cv')
        for m in range(steps):
            batch = fd.nextBatch(fname + '-cv')
            acc, loss = sess.run([accuracy, sc.layout[cost]], feed_dict={sc.layout['input']: batch['image'],
                                                                         sc.layout['label']: batch['label']})
            acc_tot += acc
            loss_tot += loss
        print('epoch #%d: acc: %.2f%%, loss: %.4f' % (
        fd.currentEpoch(fname + '-cv'), acc_tot / steps * 100, loss_tot / steps))
        print(50 * '=')

fd.unloadFuel(fname + '-ct')
fd.unloadFuel(fname + '-cv')

# mdir = '/home/ai/seria/model/vgg-d'
# ckpt = tf.train.latest_checkpoint(mdir)
# restorer = tf.train.Saver(tf.get_collection(
#                     tf.GraphKeys.GLOBAL_VARIABLES, scope='vgg_16'))
# restorer.restore(sess, ckpt)
# restorer.restore(sess, '/home/ai/seria/model/vgg-d/vgg_16.ckpt')