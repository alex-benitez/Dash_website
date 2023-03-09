# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 00:01:33 2023

@author: alexb
"""
from PIL import Image, ImageFile
import pandas as pd

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True
# high_quality = Image.open('./macs0647_eazy.png')
# high_quality.save('./macs0647_final.jpg')

lower = Image.open('./macs0647_color.png')
lower.save('../macs0647_final.jpg',quality=50)
# # print(high_quality.size)
# df = pd.read_csv('./MACS0647/macs0647_phot-eazy.ecsv',sep='\s+',
#                  index_col='id',comment='#')


# idx = 4795
# x = df.iloc[idx -1]['x']
# y = high_quality.size[1] - df.iloc[idx -1]['y']
# print(x,y)
# diff = 300

# left = x - diff
# right = x + diff
# lower = y - diff
# upper = y + diff
# tempim = high_quality.crop((left,lower,right,upper))
# tempim.show()