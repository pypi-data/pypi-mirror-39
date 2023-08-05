#!/usr/bin/env python3

from ewmh import *

class EWMH_:

    def getWmName(self, win):
        """
        Get the property _NET_WM_NAME for the given window as a string.

        :param win: the window object
        :return: str
        """
        return self._getProperty('_NET_WM_NAME', win).decode()

    def getFrameExtents(self, win):
        """
        Get the property _NET_FRAME_EXTENTS for the given window.

        :param win: the window object
        :return: [left, right, top, bottom]
        """
        return self._getProperty('_NET_FRAME_EXTENTS', win)

EWMH.getWmName = EWMH_.getWmName
EWMH.getFrameExtents = EWMH_.getFrameExtents

