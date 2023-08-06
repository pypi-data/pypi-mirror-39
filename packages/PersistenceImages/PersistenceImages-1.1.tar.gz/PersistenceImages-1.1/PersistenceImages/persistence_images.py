# PersistenceImager.py
# MIT license 2018
# Francis C. Motta

import numpy as np
import PersistenceImages.cdfs as kernels
import PersistenceImages.weighting_fxns as weighting_fxns
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


class PersistenceImager:
    def __init__(self, birth_range=None, pers_range=None, pixel_size=None,
                 weight=weighting_fxns.linear_ramp, weight_args=None, kernel=kernels.bvncdf, kernel_args=None):
        """
        class for transforming persistence diagrams into persistence images
        :param birth_range: tuple specifying lower and upper birth value of the persistence image
        :param pers_range: tuple specifying lower and upper persistence value of the persistence image
        :param pixel_size: size of square pixel
        :param weight: function to weight the birth-persistence plane
        :param weight_args: arguments needed to specify the weight function
        :param kernel: cumulative distribution function of kernel
        :param kernel_args: arguments needed to specify the kernel (cumulative distribution) function
        """
        # set defaults
        if birth_range is None:
            birth_range = (0.0, 1.0)
        if pers_range is None:
            pers_range = (0.0, 1.0)
        if pixel_size is None:
            pixel_size = np.min([pers_range[1] - pers_range[0], birth_range[1] - birth_range[0]]) * 0.2
        if weight_args is None:
            weight_args = {}
        if kernel_args is None:
            kernel_args = {'sigma': np.array([[1.0, 0.0], [0.0, 1.0]])}

        self.weight = weight
        self.weight_params = weight_args
        self.kernel = kernel
        self.kernel_params = kernel_args
        self._pixel_size = pixel_size
        self._birth_range = birth_range
        self._pers_range = pers_range
        self._width = birth_range[1] - birth_range[0]
        self._height = pers_range[1] - pers_range[0]
        self._resolution = (int(self._width / self._pixel_size), int(self._height / self._pixel_size))
        self._create_mesh()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def resolution(self):
        return self._resolution

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, val):
        self._pixel_size = val
        self._width = int(np.ceil((self.birth_range[1] - self.birth_range[0]) / self.pixel_size)) * self.pixel_size
        self._height = int(np.ceil((self.pers_range[1] - self.pers_range[0]) / self.pixel_size)) * self.pixel_size
        self._resolution = (int(self.width / self.pixel_size), int(self.height / self.pixel_size))
        self._create_mesh()

    @property
    def birth_range(self):
        return self._birth_range

    @birth_range.setter
    def birth_range(self, val):
        self._birth_range = val
        self._width = int(np.ceil((self.birth_range[1] - self.birth_range[0]) / self.pixel_size)) * self._pixel_size
        self._resolution = (int(self.width / self.pixel_size), int(self.height / self.pixel_size))
        self._create_mesh()

    @property
    def pers_range(self):
        return self._pers_range

    @pers_range.setter
    def pers_range(self, val):
        self._pers_range = val
        self._height = int(np.ceil((self.pers_range[1] - self.pers_range[0]) / self.pixel_size)) * self._pixel_size
        self._resolution = (int(self.width / self.pixel_size), int(self.height / self.pixel_size))
        self._create_mesh()

    def __repr__(self):
        repr_str = 'PersistenceImager object: \n' +\
                   '  pixel size: %g \n' % self.pixel_size +\
                   '  resolution: (%d, %d) \n' % self.resolution +\
                   '  birth range: (%g, %g) \n' % self.birth_range +\
                   '  persistence range: (%g, %g) \n' % self.pers_range +\
                   '  weight: %s \n' % self.weight.__name__ +\
                   '  kernel: %s \n' % self.kernel.__name__ +\
                   '  weight parameters: %s \n' % dict_print(self.weight_params) +\
                   '  kernel parameters: %s' % dict_print(self.kernel_params)
        return repr_str

    def _create_mesh(self):
        # padding around specified image ranges as a result of incommensurable ranges and pixel width
        db = self._width - (self._birth_range[1] - self._birth_range[0])
        dp = self._height - (self._pers_range[1] - self._pers_range[0])

        # adjust image ranges to accommodate incommensurable ranges and pixel width
        self._birth_range = (self._birth_range[0] - db / 2, self._birth_range[1] + db / 2)
        self._pers_range = (self._pers_range[0] - dp / 2, self._pers_range[1] + dp / 2)
        # construct linear spaces defining pixel locations
        self._bpnts = np.array(np.linspace(self._birth_range[0], self._birth_range[1] + self._pixel_size,
                                           self._resolution[0] + 1, endpoint=False, dtype=np.float64))
        self._ppnts = np.array(np.linspace(self._pers_range[0], self._pers_range[1] + self._pixel_size,
                                           self._resolution[1] + 1, endpoint=False, dtype=np.float64))

    def fit(self, pers_dgms, skew=True):
        """
        automatically choose persistence images parameters based on a collection of persistence diagrams
        :param pers_dgms: An iterable of (N,2) numpy arrays encoding persistence diagrams
        :param skew: boolean flag indicating if diagram needs to be converted to birth-persistence coordinates
                     (default: True)
        """
        min_birth = np.Inf
        max_birth = -np.Inf
        min_pers = np.Inf
        max_pers = -np.Inf

        # loop over diagrams to determine the maximum extent of the pairs contained in the birth-persistence plane
        for pers_dgm in pers_dgms:
            pers_dgm = np.copy(pers_dgm)
            if skew:
                pers_dgm[:, 1] = pers_dgm[:, 1] - pers_dgm[:, 0]

            min_b, min_p = pers_dgm.min(axis=0)
            max_b, max_p = pers_dgm.max(axis=0)

            if min_b < min_birth:
                min_birth = min_b

            if min_p < min_pers:
                min_pers = min_p

            if max_b > max_birth:
                max_birth = max_b

            if max_p > max_pers:
                max_pers = max_p

        self._birth_range = (min_birth, max_birth)
        self._pers_range = (min_pers, max_pers)

    def transform(self, pers_dgm, skew=True):
        """
        transform a persistence diagram to a persistence image using the parameters specified in the PersistenceImager
        object instance
        :param pers_dgm: (N,2) numpy array of persistence pairs encoding a persistence diagram
        :param skew: boolean flag indicating if diagram needs to be converted to birth-persistence coordinates
                     (default: True)
        :return: numpy array encoding the persistence image
        """
        pers_dgm = np.copy(pers_dgm)
        pers_img = np.zeros(self.resolution)
        n = pers_dgm.shape[0]
        general_flag = True

        # if necessary convert from birth-death coordinates to birth-persistence coordinates
        if skew:
            pers_dgm[:, 1] = pers_dgm[:, 1] - pers_dgm[:, 0]

        # compute weights at each persistence pair
        wts = self.weight(pers_dgm[:, 0], pers_dgm[:, 1], **self.weight_params)

        # handle the special case of a standard, isotropic Gaussian kernel
        if self.kernel == kernels.bvncdf:
            general_flag = False
            sigma = self.kernel_params['sigma']
            if sigma[0, 0] == sigma[1, 1] and sigma[0, 1] == 0.0:
                sigma = np.sqrt(sigma[0, 0])
                for i in range(n):
                    ncdf_b = kernels._norm_cdf((self._bpnts - pers_dgm[i, 0]) / sigma)
                    ncdf_p = kernels._norm_cdf((self._ppnts - pers_dgm[i, 1]) / sigma)
                    curr_img = ncdf_p[None, :] * ncdf_b[:, None]
                    pers_img += wts[i]*(curr_img[1:, 1:] - curr_img[:-1, 1:] - curr_img[1:, :-1] + curr_img[:-1, :-1])
            else:
                general_flag = True

        # handle the general case
        if general_flag:
            bb, pp = np.meshgrid(self._bpnts, self._ppnts)
            bb = bb.flatten(order='C')
            pp = pp.flatten(order='C')
            for i in range(n):
                self.kernel_params['mu'] = pers_dgm[i, :]
                curr_img = np.reshape(self.kernel(bb, pp, **self.kernel_params),
                                      (self.resolution[0]+1, self.resolution[1]+1), order='C')
                pers_img += wts[i] * (curr_img[1:, 1:] - curr_img[:-1, 1:] - curr_img[1:, :-1] + curr_img[:-1, :-1])

        return pers_img

    def fit_transform(self, pers_dgms, skew=True):
        """
        automatically choose persistence image parameters based on a collection of persistence diagrams and transform
        the collection of diagrams into images using the parameters specified in the PersistenceImager object instance
        :param pers_dgms: An iterable of (N,2) numpy arrays encoding persistence diagrams
        :param skew: boolean flag indicating if diagram needs to be converted to birth-persistence coordinates
                     (default: True)
        :return: Python list of numpy arrays encoding the persistence images
        """
        pers_dgms = np.copy(pers_dgms)

        # fit imager parameters
        self.fit(pers_dgms, skew=skew)

        # loop over each diagram and compute its image
        num_dgms = len(pers_dgms)
        pers_imgs = [None] * num_dgms
        for i in range(num_dgms):
            pers_imgs[i] = self.transform(pers_dgms[i], skew=skew)

        return pers_imgs

    def plot_diagram(self, pers_dgm, skew=True, out_file=None):
        pers_dgm = np.copy(pers_dgm)

        if skew:
            pers_dgm[:, 1] = pers_dgm[:, 1] - pers_dgm[:, 0]
            ylabel = 'persistence'
        else:
            ylabel = 'death'

        # setup plot range
        plot_buff_frac = 0.05
        bmin = np.min((np.min(pers_dgm[:, 0]), np.min(self._bpnts)))
        bmax = np.max((np.max(pers_dgm[:, 0]), np.max(self._bpnts)))
        b_plot_buff = (bmax - bmin) * plot_buff_frac
        bmin -= b_plot_buff
        bmax += b_plot_buff

        pmin = np.min((np.min(pers_dgm[:, 1]), np.min(self._ppnts)))
        pmax = np.max((np.max(pers_dgm[:, 1]), np.max(self._ppnts)))
        p_plot_buff = (pmax - pmin) * plot_buff_frac
        pmin -= p_plot_buff
        pmax += p_plot_buff

        fig = plt.figure()
        ax = plt.gca()
        ax.set_xlim(bmin, bmax)
        ax.set_ylim(pmin, pmax)

        # compute reasonable line width for pixel overlay (initially 1/50th of the width of a pixel)
        linewidth = (1/50 * self.pixel_size) * 72 * fig.bbox_inches.width * ax.get_position().width / \
                    np.min((bmax - bmin, pmax - pmin))

        # plot the persistence image grid
        hlines = np.column_stack(np.broadcast_arrays(self._bpnts[0], self._ppnts, self._bpnts[-1], self._ppnts))
        vlines = np.column_stack(np.broadcast_arrays(self._bpnts, self._ppnts[0], self._bpnts, self._ppnts[-1]))
        lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
        line_collection = LineCollection(lines, color='black', linewidths=linewidth)
        ax.add_collection(line_collection)

        # plot persistence diagram
        plt.scatter(pers_dgm[:, 0], pers_dgm[:, 1])

        # plot diagonal if necessary
        if not skew:
            min_diag = np.min((np.min(plt.xlim()), np.min(plt.ylim())))
            max_diag = np.min((np.max(plt.xlim()), np.max(plt.ylim())))
            plt.plot([min_diag, max_diag], [min_diag, max_diag])

        # fix and label axes
        ax.set_aspect('equal')
        plt.xlabel('birth')
        plt.ylabel(ylabel)

        # optionally save figure
        if out_file is None:
            plt.show()
        else:
            plt.savefig(out_file, bbox_inches='tight')

    def plot_image(self, pers_dgm, skew=True, out_file=None):
        pers_dgm = np.copy(pers_dgm)
        pers_img = self.transform(pers_dgm, skew=skew)
        if skew:
            ylabel = 'persistence'
        else:
            ylabel = 'death'

        ax = plt.gca()
        ax.matshow(pers_img.T, **{'origin': 'lower'})

        # plot diagonal if necessary
        if not skew:
            min_diag = np.min((np.min(plt.xlim()), np.min(plt.ylim())))
            max_diag = np.min((np.max(plt.xlim()), np.max(plt.ylim())))
            plt.plot([min_diag, max_diag], [min_diag, max_diag])

        # fix and label axes
        plt.xlabel('birth')
        plt.ylabel(ylabel)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

        # optionally save figure
        if out_file is None:
            plt.show()
        else:
            plt.savefig(out_file, bbox_inches='tight')


def dict_print(dict_in):
    # print dictionary contents in human-readable format
    if dict_in is None:
        str_out = 'None'
    else:
        str_out = []
        for key, val in dict_in.items():
            str_out.append('%s: %s' % (key, str(val)))
        str_out = '{' + ', '.join(str_out) + '}'

    return str_out
