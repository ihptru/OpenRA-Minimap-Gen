#!/usr/bin/env python
#
# Copyright 2012-2014 ihptru (Igor Popov) and Holloweye (Christer U.L)
#
# This file is part of OpenRA-Minimap-Gen, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import hashlib
from map import *
import bmp

# script takes path to .oramap file as an argument
_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep

def mapToBMP(pmap):
    img = bmp.BitMap(pmap.Right,pmap.Bottom,bmp.Color(0,0,0));
    for x in range(pmap.Left,pmap.Right+pmap.Left):
        for y in range(pmap.Top,pmap.Bottom+pmap.Top):
            color = bmp.Color(0,0,0);
            d1 = 0
            if pmap.tilesTile[x][y] == 510:
                pmap.tilesTile[x][y] = 255 #Change 510 to clear (should probably never happen hint: byte size 255 function in .net line:130)
            for i in range(len(pmap.templates)):
                if int(pmap.templates[i].id) == pmap.tilesTile[x][y]:
                    index = pmap.tilesIndex[x][y]
                    c = ""
                    for j in range(len(pmap.templates[i].list)):
                        if pmap.templates[i].list[j].id == index:
                            c = pmap.templates[i].list[j].type
                            break;
                    if c == "":
                        c = c = pmap.templates[i].list[0].type
                        # accually error but we save it for now
                    for j in range(len(pmap.terrTypes)):
                        if pmap.terrTypes[j].type == c:
                            color = bmp.Color(pmap.terrTypes[j].r,pmap.terrTypes[j].g,pmap.terrTypes[j].b)
                            d1 = 1
                            break;
                    if d1 == 1:
                        break;
            d2 = 0
            for i in range(len(pmap.resTypes)):
                if pmap.resTypes[i].type == pmap.resTile[x][y]:
                    for j in range(len(pmap.terrTypes)):
                        if pmap.terrTypes[j].type == pmap.resTypes[i].terrType:
                            color = bmp.Color(pmap.terrTypes[j].r,pmap.terrTypes[j].g,pmap.terrTypes[j].b)
                            d2 = 1
                            break;
                if d2 == 1:
                    break
            d = 0
            if(d1 == 0 and d2 == 0):
                #nothing was found at all use 255 = clear to fill gap
                for i in range(len(pmap.templates)):
                    if int(pmap.templates[i].id) == 255:
                        index = pmap.tilesIndex[x][y]
                        c = ""
                        for j in range(len(pmap.templates[i].list)):
                            if pmap.templates[i].list[j].id == index:
                                c = pmap.templates[i].list[j].type
                                break;
                        if c == "":
                            c = c = pmap.templates[i].list[0].type
                            # accually error but we save it for now
                        for j in range(len(pmap.terrTypes)):
                            if pmap.terrTypes[j].type == c:
                                color = bmp.Color(pmap.terrTypes[j].r,pmap.terrTypes[j].g,pmap.terrTypes[j].b)
                                d = 1
                                break;
                        if d == 1:
                            break;
            img.setPenColor(color);
            img.plotPoint(x-pmap.Left,y-pmap.Top);
    return img

try:
    oramap = sys.argv[1]
except Exception as e:
    print("Requires a path to .oramap file")
    exit()

map1 = map(oramap)

# getting hash
concat_bytes = map1.raw_yamlData + map1.bin
h = hashlib.sha1()
h.update(concat_bytes)
hash = h.hexdigest()

#Generate info file
print "Creating info file..."
text_file = open(_PATH + "info.txt", "w")
lines = map1.getInfo();
text_file.writelines(lines)
text_file.close()

print("Map's hash: "+hash)

mapToBMP(map1).saveFile(_PATH + "minimap.bmp");
print("minimap is saved: "+_PATH+"minimap.bmp")
exit(0)
