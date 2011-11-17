#!/bin/env python
import os, shutil, sys

# detekcja systemu operacyjnego
system = 'windows'
if sys.platform.startswith('linux'):
    system = 'linux'

def resize(photo_src, photo_dsc, resize_val):
    os.system('convert -filter lanczos -quality %s %s %s' % (str(resize_val)+'%', photo_src, photo_dsc) )

def test(photo):
    test_val = 40
    while test_val > 10:
        resize(photo, photo+'.test', test_val)
        size = os.path.getsize(photo+'.test')
        print 'test %s %s %s' % (photo, str(test_val), str(size))
        #if size > 950000 and size < 1100000:
        if size < 1100000:
            break
        test_val = test_val - 5
    try:
        os.remove(photo + '.test') #os.system('rm %s' % photo+'.test')
    except:
        print 'problem z usuniecie %s' % (photo+'.test')
    return test_val

def trav(d):
    dirList=os.listdir(d)
    groups = {}
    for fileName in dirList:
        fullPath = d+'/'+fileName
        if os.path.isdir(fullPath):
            trav(fullPath)
        else:
            if fullPath[:-4] == 'dupa':
                continue
            size = os.path.getsize(fullPath)
            sizeg = size/100000
            if sizeg not in groups:
                groups[sizeg] = []
            groups[sizeg].append(fullPath)
    for key in groups:
        group = groups[key]
        print 'Testuje grupe %s' % key
        first = group[0]
        resize_val = test(first)
        for photo in group:
            print 'quality down %s %s' % (str(resize_val)+'%', photo)
            resize(photo, photo+'.jpg', resize_val)
            shutil.move(photo+'.jpg', photo)

trav('.')
