#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_propersubtract.py
#
#  Copyright 2018 Bruno S <bruno@oac.unc.edu.ar>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
test_propersubtract module from ProperImage,
for subtracting astronomical images.

Written by Bruno SANCHEZ

PhD of Astromoy - UNC
bruno@oac.unc.edu.ar

Instituto de Astronomia Teorica y Experimental (IATE) UNC
Cordoba - Argentina

Of 301
"""

import os
import tempfile
import shutil
import unittest

import numpy as np
from astropy.io import fits

from properimage import propersubtract as ps
from properimage import single_image as si
from properimage.tests import simtools


class PropersubtractBase(object):

    def setUp(self):
        print('setting up')
        self.tempdir = tempfile.mkdtemp()
        self.paths = []
        # mock data
        psf = simtools.Psf(11, 2.5, 3.)

        self.mock_image_data = np.random.random((256, 256))*10.
        for i in range(50):
            x = np.random.randint(7, 220)
            y = np.random.randint(7, 120)
            # print x, y
            self.mock_image_data[x:x+11, y:y+11] += psf*float(i+1)*2000.

        psf = simtools.Psf(11, 3., 1.9)
        for i in range(50):
            x = np.random.randint(7, 220)
            y = np.random.randint(122, 220)
            # print x, y
            self.mock_image_data[x:x+11, y:y+11] += psf*float(i+1)*2000.

        # generate 2 images to subtract

        # a reference
        refimage_data = self.mock_image_data*10. + \
            np.random.random((256, 256))*50. + 350

        refimage_data[123, 123] = np.nan

        # a fits file
        refmockfits_path = os.path.join(self.tempdir, 'refmockfits.fits')
        fits.writeto(refmockfits_path, refimage_data, overwrite=True)
        self.paths.append(refmockfits_path)

        # a new image
        newimage_data = self.mock_image_data*3. + \
            np.random.random((256, 256))*50. + 750

        newimage_data[123, 123] = np.nan

        # a fits file
        newmockfits_path = os.path.join(self.tempdir, 'newmockfits.fits')
        fits.writeto(newmockfits_path, newimage_data, overwrite=True)
        self.paths.append(newmockfits_path)

    def tearDown(self):
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        try:
            self.si_ref._clean()
            self.si_new._clean()
        except OSError:
            pass


class TestSubtract(PropersubtractBase, unittest.TestCase):
    def setUp(self):
        super(TestSubtract, self).setUp()
        self.si_ref = si.SingleImage(self.paths[0])
        self.si_new = si.SingleImage(self.paths[1])

    def testSubtractNoBeta(self):
        D, P, S_corr, mix_mask = ps.diff(self.si_ref, self.si_new,
                                         beta=False)
        self.assertIsInstance(D, np.ndarray)
        self.assertIsInstance(P, np.ndarray)
        self.assertIsInstance(S_corr, np.ndarray)
        self.assertIsInstance(mix_mask, np.ndarray)

    def testSubtractBetaIterative(self):
        D, P, S_corr, mix_mask = ps.diff(self.si_ref, self.si_new,
                                         beta=True, iterative=True)
        self.assertIsInstance(D, np.ndarray)
        self.assertIsInstance(P, np.ndarray)
        self.assertIsInstance(S_corr, np.ndarray)
        self.assertIsInstance(mix_mask, np.ndarray)

    def testSubtractBetaShift(self):
        D, P, S_corr, mix_mask = ps.diff(self.si_ref, self.si_new,
                                         beta=True, iterative=False,
                                         shift=True)
        self.assertIsInstance(D, np.ndarray)
        self.assertIsInstance(P, np.ndarray)
        self.assertIsInstance(S_corr, np.ndarray)
        self.assertIsInstance(mix_mask, np.ndarray)

    def testSubtractOnlyBeta(self):
        D, P, S_corr, mix_mask = ps.diff(self.si_ref, self.si_new,
                                         beta=True, iterative=False,
                                         shift=False)
        self.assertIsInstance(D, np.ndarray)
        self.assertIsInstance(P, np.ndarray)
        self.assertIsInstance(S_corr, np.ndarray)
        self.assertIsInstance(mix_mask, np.ndarray)