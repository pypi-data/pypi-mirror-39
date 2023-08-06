import random
import numpy as np
import numbers
import collections
import torch
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.interpolation import map_coordinates
from skimage import transform, filters, util
import cv2
# Ignore skimage convertion warnings
import warnings
warnings.filterwarnings("ignore")

def _is_numpy_image(t):
    return isinstance(t, np.ndarray) and (t.ndim in {2, 3})

def _is_tensor_image(t):
    return torch.is_tensor(t) and t.ndimension() == 3

class Compose():
    """Composes several transforms together
    Args:
        transforms (list of ``Transform`` objects): list of transforms to compose.
    """
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, x, y=None):
        for t in self.transforms:
            x, y = t(x, y)
        return x, y


class Lambda():
    """Apply a user-defined lambda as a transform.
    Args:
        lambd (function): Lambda/function to be used for transform.
    """
    def __init__(self, lambd):
        assert callable(lambd), repr(type(lambd).__name__) + " object is not callable"
        self.lambd = lambd

    def __call__(self, x, y=None):
        return self.lambd(x, y)


class ToTensor():
    """
    Converts a numpy.ndarray (H x W x C) in the range [0, 255]
    to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0].
    """
    def to_tensor(self, t):
        if t is None:
            return t
        if not _is_numpy_image(t):
            raise TypeError('input is not a numpy image.')
        if t.dtype == np.float64:
            t = t.astype(np.float32)
        if t.ndim == 2:
            t = np.expand_dims(t, -1)
        t = t.transpose((2, 0, 1))
        try:
            t = torch.from_numpy(t)
        except ValueError:
            # workaround: PyTorch not handle memory well after numpy array flip/rotate
            t = torch.from_numpy(t.copy())
        if isinstance(t, torch.ByteTensor):
            return t.float().div(255)
        return t

    def __call__(self, x, y=None):
        return self.to_tensor(x), self.to_tensor(y)


class ToNumpy():
    """
    Convert a tensor to ndarray
    """
    def to_numpy(self, t):
        if t is None:
            return t
        if not _is_tensor_image(t):
            raise TypeError('tensor is not a torch image.')
        if isinstance(t, torch.FloatTensor):
            t = t.mul(255).byte()
        t = np.transpose(t.numpy(), (1, 2, 0))
        if t.shape[-1] == 1:
            t = np.squeeze(t)
        return t

    def __call__(self, x, y=None):
        return self.to_numpy(x), self.to_numpy(y)

class Normalize():
    """Normalize an tensor image with mean and standard deviation.
    will normalize each channel of the torch.*Tensor, i.e.
    channel = (channel - mean) / std
    Args:
        mean (sequence): Sequence of means for each channels respecitvely.
        std (sequence): Sequence of standard deviations for each channels
            respecitvely.
    """
    def __init__(self, mean=0.5, std=0.5):
        self.mean = mean
        self.std = std

    def normalize(self, t):
        if t is None:
            return t
        if not _is_tensor_image(t):
            raise TypeError('tensor is not a torch image.')
        mean, std = self.mean, self.std
        if isinstance(mean, numbers.Number):
            mean = [mean] * t.shape[0]
        if isinstance(std, numbers.Number):
            std = [std] * t.shape[0]
        # This is faster than using broadcasting, don't change without benchmarking
        for a, m, s in zip(t, mean, std):
            a.sub_(m).div_(s)
        return t

    def __call__(self, x, y=None):
        return self.normalize(x), y


class DeNormalize():
    """DeNormalize an tensor image with mean and standard deviation.
    will denormalize each channel of the torch.*Tensor, i.e.
    channel = (channel * std) + mean
    Args:
        mean (sequence): Sequence of means for each channels respecitvely.
        std (sequence): Sequence of standard deviations for each channels
            respecitvely.
    """
    def __init__(self, mean=0.5, std=0.5):
        self.mean = mean
        self.std = std

    def denormalize(self, t):
        if t is None:
            return t
        if not _is_tensor_image(t):
            raise TypeError('tensor is not a torch image.')
        mean, std = self.mean, self.std
        if isinstance(mean, numbers.Number):
            mean = [mean] * t.shape[0]
        if isinstance(std, numbers.Number):
            std = [std] * t.shape[0]
        # This is faster than using broadcasting, don't change without benchmarking
        for a, m, s in zip(t, mean, std):
            a.mul_(s).add_(m)
        return t

    def __call__(self, x, y=None):
        return self.denormalize(x), y


class RandomVerticalFlip():
    def __init__(self, p=0.5):
        self.p = p

    def flip(self, t):
        if t is None:
            return t
        return np.flipud(t)

    def __call__(self, x, y=None):
        if random.random() < self.p:
            return self.flip(x), self.flip(y)
        return x, y

class RandomHorizontalFlip():
    def __init__(self, p=0.5):
        self.p = p

    def flip(self, t):
        if t is None:
            return t
        return np.fliplr(t)

    def __call__(self, x, y=None):
        if random.random() < self.p:
            return self.flip(x), self.flip(y)
        return x, y


class RandomRotate():
    def rotate(self, t, k):
        if t is None:
            return t
        return np.rot90(t, k, (0, 1))

    def __call__(self, x, y=None):
        k = random.randint(-1, 2)
        return self.rotate(x, k), self.rotate(y, k)


class Pad():
    """Pad the given Image on all sides with the given "pad" value.
    Args:
        padding (int or tuple): padding on each border of the image.
        fill: Pixel fill value for constant fill. Default is 0.
        mode: Type of padding. Should be: constant, edge, reflect or symmetric. Default is constant.
             - constant: pads with a constant value, this value is specified with fill
             - edge: pads with the last value on the edge of the image
             - reflect: pads with reflection of image (without repeating the last value on the edge)
                padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode
                will result in [3, 2, 1, 2, 3, 4, 3, 2]
             - symmetric: pads with reflection of image (repeating the last value on the edge)
                padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode
                will result in [2, 1, 1, 2, 3, 4, 4, 3]
    """
    def __init__(self, padding, fill=0, mode='reflect'):
        self.padding = padding
        self.fill = fill
        self.mode = mode

    def pad(self, t, border):
        if t is None:
            return t
        assert _is_numpy_image(t)
        if self.mode == 'constant':
            return np.pad(t, border[:t.ndim], self.mode, constant_values=self.fill)
        else:
            return np.pad(t, border[:t.ndim], self.mode)

    def __call__(self, x, y=None):
        if isinstance(self.padding, numbers.Number):
            b = self.padding
            b = ((b, b), (b, b), (0, 0))
        elif isinstance(padding, tuple):
            bw = self.padding[0]
            bh = self.padding[1]
            b = ((bw, bw), (bh, bh), (0, 0))
        else:
            raise ValueError('padding type invalid')
        return self.pad(x, b), self.pad(y, b)


class RandomCrop(Pad):
    """Crop at a random location.
    Args:
        size (sequence or int): Desired output size of the crop. If size is an
            int instead of sequence like (h, w), a square crop (size, size) is
            made.
        padding (int or tuple): padding on each border of the image.
            Default is None, i.e no padding.
        pad_if_needed (boolean): It will pad the image if smaller than the
            desired size to avoid raising an exception.
        fill: Pixel fill value for constant fill. Default is 0.
        mode: Type of padding. Should be: constant, edge, reflect or symmetric. Default is constant.
             - constant: pads with a constant value, this value is specified with fill
             - edge: pads with the last value on the edge of the image
             - reflect: pads with reflection of image (without repeating the last value on the edge)
                padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode
                will result in [3, 2, 1, 2, 3, 4, 3, 2]
             - symmetric: pads with reflection of image (repeating the last value on the edge)
                padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode
                will result in [2, 1, 1, 2, 3, 4, 4, 3]
    """

    def __init__(self, size, padding=None, pad_if_needed=True):
        super().__init__(padding)
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.pad_if_needed = pad_if_needed

    def get_params(self, x, y, output_size):
        """Get parameters for ``crop`` for a random crop.
        Args:
            x: input array
            y: label array
            output_size (tuple): Expected output size of the crop.
        Returns:
            tuple: params (i, j, h, w) to be passed to ``crop`` for random crop.
        """
        h, w = x.shape[:2]
        th, tw = output_size
        if w == tw and h == th:
            return 0, 0, h, w

        i = random.randint(0, h - th)
        j = random.randint(0, w - tw)
        return i, j, th, tw

    def crop(self, t, param):
        if t is None:
            return t
        i, j, h, w = param
        if t.ndim == 2:
            return t[i:i+h, j:j+w]
        else:
            return t[i:i+h, j:j+w, :]

    def __call__(self, x, y=None):
        if self.padding is not None:
            x, y = super().__call__(x), super().__call__(y)

        # pad the width if needed
        if self.pad_if_needed and x.shape[1] < self.size[1]:
            b = self.size[1] - x.shape[1]
            b = ((0, 0), (b, b), (0, 0))
            x, y = self.pad(x, b), self.pad(y, b)

        # pad the height if needed
        if self.pad_if_needed and x.shape[0] < self.size[0]:
            b = self.size[0] - x.shape[0]
            b = ((b, b), (0, 0), (0, 0))
            x, y = self.pad(x, b), self.pad(y, b)

        param = self.get_params(x, y, self.size)

        return self.crop(x, param), self.crop(y, param)

class RandomTargetCrop(RandomCrop):
    """Crop at a random location, guarantee to crop foreground pixels of label .
    """
    def __init__(self, size):
        super().__init__(size)

    def get_params(self, x, y, output_size):
        if y is None:
            return super().get_params(x, y, output_size)

        h, w = x.shape[:2]
        th, tw = output_size
        if w == tw and h == th:
            return 0, 0, h, w

        # pick any foreground pixels, support various dim of y array
        points = list(map(list, zip(*np.nonzero(y))))
        if len(points) > 0:
            pi, pj = random.choice(points)[:2]
            # crop based on foreground pixel
            i = random.randint(max(0, pi-th), min(pi, h-th))
            j = random.randint(max(0, pj-tw), min(pj, w-tw))
        else:
            i = random.randint(0, h - th)
            j = random.randint(0, w - tw)
        return i, j, th, tw

class RandomUniformCrop(RandomCrop):
    """Crop at a random location, which will be distributed uniformed on whole image
    """
    def __init__(self, size):
        super().__init__(size)

    def get_params(self, x, y, output_size):
        h, w = x.shape[:2]
        th, tw = output_size
        if w == tw and h == th:
            return 0, 0, h, w

        # partition into grids, randomly pick a grid uniformly
        max_row = h // th if (h % th > 0.5 * th) else (h // th - 1)
        max_col = w // tw if (w % tw > 0.5 * tw) else (w // tw - 1)
        row, col = random.randint(0, max_row), random.randint(0, max_col)
        # randomly move around slightly
        i = round((row + random.triangular(-0.5, 0.5, 0)) * th)
        j = round((col + random.triangular(-0.5, 0.5, 0)) * tw)
        # within image bounary (might be unnecessary?)
        i = max(0, min(i, h - th))
        j = max(0, min(j, w - tw))
        return i, j, th, tw

class RandomChoice():
    """Apply single transformation randomly picked from a list
    Args:
        transforms (list or tuple): list of transformations
    """
    def __init__(self, transforms):
        assert isinstance(transforms, (list, tuple))
        self.transforms = transforms

    def __call__(self, x, y):
        t = random.choice(self.transforms)
        return t(x, y)

class Resize():
    """Resize to the given size.
    Args:
        size (sequence or int): Desired output size. If size is a sequence like
            (h, w), output size will be matched to this. If size is an int,
            smaller edge of the image will be matched to this number.
            i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
    """
    def __init__(self, size, fast=True):
        assert isinstance(size, int) or (isinstance(size, collections.Iterable) and len(size) == 2)
        self.size = size
        self.fast = fast

    def resize(self, t):
        if t is None:
            return t
        if self.fast:
            if t.dtype == np.bool:
                t = t.astype(np.uint8) # cv2.resize not support bool type
            t = cv2.resize(t, self.size[::-1], interpolation=cv2.INTER_LANCZOS4)
        else:
            t = transform.resize(t, self.size)
        return t

    def __call__(self, x, y=None):
        return self.resize(x), self.resize(y)

class RandomScale():
    """Scale to random size, yet keep origin aspect ratio.
    Args:
        scale (tuple): Desired scale range. Default is (0.2, 2.0).
        mode (string): either tri-angular distribution or uni-form distribution. Default 'tri'
    """
    def __init__(self, scale=(0.2, 2.0), mode='tri', fast=True):
        assert isinstance(scale, collections.Iterable) and len(scale) == 2
        self.scale = scale
        self.mode = mode
        self.fast = fast

    def rescale(self, t, scale):
        if t is None:
            return t
        if self.fast:
            if t.dtype == np.bool:
                t = t.astype(np.uint8) # cv2.resize not support bool type
            # note: INTER_AREA not support 4+ channels
            interpolation = cv2.INTER_LANCZOS4 if scale <= 1 else cv2.INTER_CUBIC
            t = cv2.resize(t, None, fx=scale, fy=scale, interpolation=interpolation)
        else:
            t = transform.rescale(t, scale, mode='reflect')
        return t

    def __call__(self, x, y=None):
        if self.mode == 'tri':
            scale = random.triangular(self.scale[0], self.scale[1], 1.0)
        elif self.mode == 'uni':
            scale = random.uniform(self.scale[0], self.scale[1])
        else:
            raise ValueError(f'mode {self.mode} invalid')
        return self.rescale(x, scale), self.rescale(y, scale)

class RandomNoise():
    def __init__(self, p=0.75, mode='speckle'):
        self.mode = mode
        self.p = p

    def noise(self, t):
        if t is None:
            return t
        t = util.random_noise(t, self.mode)
        return t

    def __call__(self, x, y=None):
        if random.random() < self.p:
            return self.noise(x), y
        return x, y


class RandomGaussianBlur():
    def __init__(self, p=0.75, fast=True):
        self.p = p
        self.fast = fast

    def gaussian(self, t):
        if t is None:
            return t
        if self.fast:
            t = cv2.GaussianBlur(t, (5,5), 0)
        else:
            t = filters.gaussian(t, mode='reflect', multichannel=True)
        return t

    def __call__(self, x, y=None):
        if random.random() < self.p:
            return self.gaussian(x), y
        return x, y

"""
Quote: These results might indicate that these types of data augmentations work best when the training set is small.

Reference:
1. [Evaluation of Data Augmentation of MR Images for Deep Learning](http://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=8952747&fileOId=8952748)
2. https://www.di.ens.fr/~josef/publications/Rocco17.pdf
3. https://www.kaggle.com/bguberfain/elastic-transform-for-data-augmentation
"""

class ElasticDistortion():
    """Elastic deformation of image as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
    """
    def __init__(self, p=0.75):
        self.p = p

    def get_params(self, size, alpha=2000, sigma=30):
        h, w = size
        dx = gaussian_filter((np.random.rand(*(h, w)) * 2 - 1),
                            sigma, mode="constant", cval=0) * alpha
        dy = gaussian_filter((np.random.rand(*(h, w)) * 2 - 1),
                            sigma, mode="constant", cval=0) * alpha
        x, y = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
        indices = [np.reshape(x + dx, (-1, 1)), np.reshape(y + dy, (-1, 1))]
        return indices

    def distort(self, t, indices, spline_order=1, mode='reflect'):
        if t is None:
            return t
        if t.ndim == 2:
            t = np.expand_dims(t, -1)
        shape = t.shape[:2]
        result = np.empty_like(t)
        for i in range(t.shape[2]):
            result[:, :, i] = map_coordinates(
                t[:, :, i], indices, order=spline_order, mode=mode).reshape(shape)
        if result.shape[-1] == 1:
            result = np.squeeze(result)
        return result

    def __call__(self, x, y=None):
        if random.random() < self.p:
            param = self.get_params(x.shape[:2])
            return self.distort(x, param), self.distort(y, param)
        return x, y


class RandomAffine(object):
    """Random affine transformation of the image keeping center invariant
    """
    def __call__(self, img):
        raise NotImplementedError()


class ColorJitter(object):
    """Randomly change the brightness, contrast and saturation of an image.
    """
    def __call__(self, x, y=None):
        raise NotImplementedError()