"""Testing for Naive Bayes regression """

# Authors: Remi Louf <remilouf@gmail.com>, <remi@sounds.am>
#          Daniel Emaasit <daniel.emaasit@gmail.com>
#
# License: BSD 3 clause

import pytest
import numpy.testing as npt
import pandas.testing as pdt
import shutil
import tempfile

import numpy as np
import pymc3 as pm
from pymc3 import summary
from sklearn.naive_bayes import GaussianNB as skGaussianNB
from sklearn.model_selection import train_test_split


from pmlearn.exceptions import NotFittedError
from pmlearn.naive_bayes import GaussianNB


class TestGaussianNB(object):

    def setup_method(self):
        self.num_pred = 1
        self.num_training_samples = 300

        self.length_scale = 1.0
        self.signal_variance = 0.1
        self.noise_variance = 0.1

        X = np.linspace(start=0, stop=10,
                        num=self.num_training_samples)[:, None]

        cov_func = self.signal_variance ** 2 * pm.gp.cov.ExpQuad(
            1, self.length_scale)
        mean_func = pm.gp.mean.Zero()

        f_true = np.random.multivariate_normal(
            mean_func(X).eval(),
            cov_func(X).eval() + 1e-8 * np.eye(self.num_training_samples),
            1).flatten()
        y = f_true + \
            self.noise_variance * np.random.randn(self.num_training_samples)

        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.3)

        self.advi_gnb = GaussianNB()

        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Tear down
        """
        shutil.rmtree(self.test_dir)


class TestGaussianNBFit(TestGaussianNB):
    def test_advi_fit_returns_correct_model(self):
        # This print statement ensures PyMC3 output won't overwrite
        # the test name
        print('')
        self.advi_gnb.fit(self.X_train, self.y_train,
                          inference_args={"n": 25000})

        npt.assert_equal(self.num_pred, self.advi_gnb.num_pred)
        npt.assert_almost_equal(
            self.signal_variance,
            self.advi_gnb.summary['mean']['signal_variance__0'],
            0)
        npt.assert_almost_equal(
            self.length_scale,
            self.advi_gnb.summary['mean']['length_scale__0_0'],
            0)
        npt.assert_almost_equal(
            self.noise_variance,
            self.advi_gnb.summary['mean']['noise_variance__0'],
            0)