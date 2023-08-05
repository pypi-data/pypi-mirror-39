__author__ = 'sibirrer'

import numpy as np
import lenstronomy.Util.util as util
import lenstronomy.Util.constants as const


class LikelihoodModule(object):
    """
    this class contains the routines to run a MCMC process
    the key components are:
    - imSim_class: an instance of a class that simulates one (or more) images and returns the likelihood, such as
    ImageModel(), Multiband(), MulitExposure()

    - param_class: instance of a Param() class that can cast the sorted list of parameters that are sampled into the
    conventions of the imSim_class

    Additional arguments are supported for adding a time-delay likelihood etc (see __init__ definition)
    """
    def __init__(self, imSim_class, param_class, image_likelihood=True, check_bounds=True, check_solver=False,
                 point_source_likelihood=False, position_uncertainty=0.004, check_positive_flux=False,
                 solver_tolerance=0.001, force_no_add_image=False, source_marg=False, restrict_image_number=False,
                 max_num_images=None, bands_compute=None, time_delay_likelihood=False, time_delays_measured=None,
                 time_delays_uncertainties=None):
        """
        initializing class

        :param imSim_class: instance of a class that simulates one (or more) images and returns the likelihood, such as
        ImageModel(), Multiband(), MulitExposure()
        :param param_class: instance of a Param() class that can cast the sorted list of parameters that are sampled into the
        conventions of the imSim_class
        :param image_likelihood: bool, option to compute the imaging likelihood
        :param check_bounds:  bool, option to punish the hard bounds in parameter space
        :param check_solver: bool, option to check whether point source position solver finds a solution to match all
         the image positions in the same source plane coordinate
        :param point_source_likelihood: bool, additional likelihood term of the predicted vs modelled point source position
        :param flaot, position_uncertainty: 1-sigma Gaussian uncertainty on the point source position
        (only used if point_source_likelihood=True)
        :param check_positive_flux: bool, option to punish models that do not have all positive linear amplitude parameters
        :param solver_tolerance: float, punishment of check_solver occures when image positions are predicted further
        away than this number
        :param force_no_add_image: bool, if True: computes ALL image positions of the point source. If there are more
        images predicted than modelled, a punishment occures
        :param source_marg: marginalization addition on the imaging likelihood based on the covariance of the infered
        linear coefficients
        :param restrict_image_number: bool, if True: computes ALL image positions of the point source. If there are more
        images predicted than indicated in max_num_images, a punishment occures
        :param max_num_images: int, see restrict_image_number
        :param bands_compute: list of bools with same length as data objects, indicates which "band" to include in the fitting
        :param time_delay_likelihood: bool, if True computes the time-delay likelihood of the FIRST point source
        :param time_delays_measured: relative time delays (in days) in respect to the first image of the point source
        :param time_delays_uncertainties: time-delay uncertainties in same order as time_delay_measured
        """

        self.imSim = imSim_class
        self.param = param_class
        self._lower_limit, self._upper_limit = self.param.param_limits()
        # this part is not yet fully implemented
        self._time_delay_likelihood = time_delay_likelihood
        if self._time_delay_likelihood is True:
            if time_delays_measured is None:
                raise ValueError("time_delay_measured need to be specified to evaluate the time-delay likelihood.")
            if time_delays_uncertainties is None:
                raise ValueError("time_delay_uncertainties need to be specified to evaluate the time-delay likelihood.")
            self._delays_measured = np.array(time_delays_measured)
            self._delays_errors = np.array(time_delays_uncertainties)

        self._image_likelihood = image_likelihood
        self._check_bounds = check_bounds
        self._point_source_likelihood = point_source_likelihood
        self._position_sigma = position_uncertainty
        self._check_solver = check_solver
        self._check_positive_flux = check_positive_flux
        self._solver_tolerance = solver_tolerance
        self._force_no_add_image = force_no_add_image
        self._source_marg = source_marg  # whether to fully invert the covariance matrix for marginalization
        self._restrict_number_images = restrict_image_number
        if max_num_images is None:
            max_num_images = self.param.num_point_source_images
        self._max_num_images = max_num_images
        self._num_bands = self.imSim.num_bands
        if bands_compute is None:
            bands_compute = [True] * self._num_bands
        self._compute_bool = bands_compute
        if not len(self._compute_bool) == self._num_bands:
            raise ValueError('compute_bool statement has not the same range as number of bands available!')

    @property
    def param_limits(self):
        return self._lower_limit, self._upper_limit

    def logL(self, args):
        """
        routine to compute X2 given variable parameters for a MCMC/PSO chainF
        """
        #extract parameters
        kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_ps, kwargs_cosmo = self.param.args2kwargs(args)
        #generate image and computes likelihood
        self.imSim.reset_point_source_cache()
        logL = 0
        if self._check_bounds is True:
            penalty, bound_hit = self.check_bounds(args, self._lower_limit, self._upper_limit)
            logL -= penalty
            if bound_hit:
                return logL, None
        if self._image_likelihood is True:
            logL += self.imSim.likelihood_data_given_model(kwargs_lens, kwargs_source, kwargs_lens_light, kwargs_ps,
                                                           source_marg=self._source_marg, compute_bool=self._compute_bool)
        if self._point_source_likelihood is True:
            logL += self.likelihood_image_pos(kwargs_lens, kwargs_ps, self._position_sigma)
        if self._time_delay_likelihood is True:
            logL += self.logL_delay(kwargs_lens, kwargs_ps, kwargs_cosmo)
        if self._check_solver is True:
            logL -= self.solver_penalty(kwargs_lens, kwargs_ps, self._solver_tolerance)
        if self._force_no_add_image:
            bool = self.check_additional_images(kwargs_ps, kwargs_lens)
            if bool is True:
                logL -= 10**10
        if self._restrict_number_images is True:
            ra_image_list, dec_image_list = self.imSim.image_positions(kwargs_ps=kwargs_ps, kwargs_lens=kwargs_lens)
            if len(ra_image_list[0]) > self._max_num_images:
                logL -= 10**10
        if self._check_positive_flux is True:
            bool = self.param.check_positive_flux(kwargs_source, kwargs_lens_light, kwargs_ps)
            if bool is False:
                logL -= 10**10
        return logL, None

    def solver_penalty(self, kwargs_lens, kwargs_ps, tolerance):
        """
        test whether the image positions map back to the same source position
        :param kwargs_lens:
        :param kwargs_ps:
        :return: add penalty when solver does not find a solution
        """
        dist = self.param.check_solver(kwargs_lens, kwargs_ps)
        if dist > tolerance:
            return dist * 10**10
        return 0

    def check_additional_images(self, kwargs_ps, kwargs_lens):
        """
        checks whether additional images have been found and placed in kwargs_ps
        :param kwargs_ps: point source kwargs
        :return: bool, True if more image positions are found than originally been assigned
        """
        ra_image_list, dec_image_list = self.imSim.image_positions(kwargs_ps=kwargs_ps, kwargs_lens=kwargs_lens)
        if len(ra_image_list) > 0:
            if len(ra_image_list[0]) > self.param.num_point_source_images:
                return True
        else:
            return False

    def likelihood_image_pos(self, kwargs_lens, kwargs_ps, sigma):
        """

        :param x_lens_model: image position of lens model
        :param y_lens_model: image position of lens model
        :param x_image: image position of image data
        :param y_image: image position of image data
        :param sigma: likelihood sigma
        :return: log likelihood of model given image positions
        """
        # TODO think of where to put it, it used specific keyword arguments
        # TODO does this work with source position defined point source and required arguemnts 'ra_image'?
        if not 'ra_image' in kwargs_ps[0]:
            return 0
        x_image = kwargs_ps[0]['ra_image']
        y_image = kwargs_ps[0]['dec_image']
        ra_image_list, dec_image_list = self.imSim.image_positions(kwargs_ps=kwargs_ps, kwargs_lens=kwargs_lens)
        num_image = len(ra_image_list[0])
        if num_image != len(x_image):
            return -10**15
        dist = util.min_square_dist(ra_image_list[0], dec_image_list[0], x_image, y_image)
        logL = -np.sum(dist/sigma**2)/2
        return logL

    def check_bounds(self, args, lowerLimit, upperLimit):
        """
        checks whether the parameter vector has left its bound, if so, adds a big number
        """
        penalty = 0
        bound_hit = False
        for i in range(0, len(args)):
            if args[i] < lowerLimit[i] or args[i] > upperLimit[i]:
                penalty = 10**15
                bound_hit = True
        return penalty, bound_hit

    def logL_delay(self, kwargs_lens, kwargs_ps, kwargs_cosmo):
        """
        routine to compute the log likelihood of the time delay distance
        :param args:
        :return:
        """
        delay_arcsec = self.imSim.fermat_potential(kwargs_lens, kwargs_ps)
        D_dt_model = kwargs_cosmo['D_dt']
        delay_days = const.delay_arcsec2days(delay_arcsec[0], D_dt_model)
        logL = self._logL_delays(delay_days, self._delays_measured, self._delays_errors)
        return logL

    def _logL_delays(self, delays_model, delays_measured, delays_errors):
        """
        log likelihood of modeled delays vs measured time delays under considerations of errors

        :param delays_model: n delays of the model (not relative delays)
        :param delays_measured: relative delays (1-2,1-3,1-4) relative to the first in the list
        :param delays_errors: gaussian errors on the measured delays
        :return: log likelihood of data given model
        """
        delta_t_model = np.array(delays_model[1:]) - delays_model[0]
        logL = np.sum(-(delta_t_model - delays_measured) ** 2 / (2 * delays_errors ** 2))
        return logL

    def effectiv_numData_points(self):
        """
        returns the effective number of data points considered in the X2 estimation to compute the reduced X2 value
        """
        n = self.imSim.numData_evaluate(compute_bool=self._compute_bool)
        num_param, _ = self.param.num_param()
        num_linear = 0
        for bool in self._compute_bool:
            if bool is True:
                num_linear += self.param.num_param_linear()
        return n - num_param - num_linear

    def __call__(self, a):
        return self.logL(a)

    def likelihood(self, a):
        return self.logL(a)

    def computeLikelihood(self, ctx):
        logL, _ = self.logL(ctx.getParams())
        return logL

    def setup(self):
        pass
