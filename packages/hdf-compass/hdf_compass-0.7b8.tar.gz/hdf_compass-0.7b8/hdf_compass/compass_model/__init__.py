##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of the HDF Compass Viewer. The full HDF Compass          #
# copyright notice, including terms governing use, modification, and         #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

from hdf_compass.compass_model.model import get_stores, push, Store, Node, \
    Container, KeyValue, GeoArray, GeoSurface, Array, Text, Xml, Image, Unknown

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
