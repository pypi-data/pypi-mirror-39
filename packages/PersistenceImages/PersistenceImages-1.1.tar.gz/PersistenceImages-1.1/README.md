# Persistence Images: A Stable Vector Representation of Persistent Homology
## Description
This module defines the Python class PersistenceImager used to vectorize persistence diagrams into persistence images (see [PI] http://www.jmlr.org/papers/volume18/16-337/16-337.pdf for details).

## Dependencies
* Interpreter
```
Python 3.6.0
```

* Modules
```
numpy 1.11.3
matplotlib 2.0.0
```

## Installation

You may download PersistenceImages package from the gitlab repo and install locally:
From gitbash or terminal:
```
$ git clone git@gitlab.com:csu-tda/PersistenceImages.git
$ cd PersistenceImages/
$ pip install .
```
Once installed, you may access PersistenceImages methods by importing the package
```
>>> import PersistenceImages.persistence_images as pi
```
## PersistenceImager()
The PersistenceImager() class is the workhorse of the PersistenceImages package and is used to transform a diagram. An instantiation of a PersistenceImager() object must first be created, and will contain the attributes which define the persistence image hyper-parameters:
* **birth_range**: tuple specifying the left and right image boundaries
* **pers_range**: tuple specifying the lower and upper image boundaries
* **pixel_size**: a float specifying the width and height of each image pixels
* **weight**: weight function that scales the contribution of each persistence pair to the final image 
* **weight_args**: arguments needed to specify the weight function
* **kernel**: cumulative distribution function of the kernel which replaces each persistence pair
* **kernel_args**: arguments needed to specify the kernel CDF

Currently, only the CDF of a general bivariate normal distribution is implemented in `cdfs.py`.  The shape of this distribution is controlled by the parameter 'sigma' which is expected to be a valid 2x2, positive-definite covariance matrix. 

**NOTE**: For mathematical reasons, a standard isotropic bivariate normal i.e. $`\Sigma=[[\sigma, 0],[0, \sigma]]`$, will be *much* faster to compute than a non-isotropic distribution kernel. 

## Example
First instantiate a PersistenceImager() object:
```
>>> pers_imger = pi.PersistenceImager()
```
Printing a PersistenceImager() object will print its hyperparameters (defaults in this case):
```
>>> print(pers_imger)

PersistenceImager object:
  pixel size: 0.2
  resolution: (5, 5)
  birth range: (0, 1)
  persistence range: (0, 1)
  weight: linear_ramp
  kernel: bvncdf
  weight parameters: {}
  kernel parameters: {sigma: [[ 1.  0.]
                              [ 0.  1.]]}
```
The `transform()` method can then be called on a (N,2) numpy array to generate a persistence image from the input diagram:
```
>>> pers_dgm = np.array([[0.5, 0.8], [.7, 1.2], [2.5, 4]])
>>> pers_img = pers_imager.transform(pers_dgm, skew=True)
```
The option `skew=True` specifies that the diagram is currently in birth-death coordinates and must be first transformed to birth-persistence coordinates. 

The `plot_diagram()` and `plot_image()` methods can be used to generate plots of a diagram and the corresponding image:

```
>>> pers_imager.plot_diagram(pers_dgm, skew=True)
>>> pers_imager.plot_image(pers_dgm, skew=True)
```
A finer resolution image is made by decreasing the `pixel_size` attribute:
```
>>> pers_imager.pixel_size = 0.02
>>> print(pers_imager)

PersistenceImager object:
  pixel size: 0.02      <----
  resolution: (50, 50)  <----
  birth range: (0, 1)
  persistence range: (0, 1)
  weight: linear_ramp
  kernel: bvncdf
  weight parameters: {}
  kernel parameters: {sigma: [[ 1.  0.]
                              [ 0.  1.]]}
```
Updating attributes of a PersistenceImager() object will automatically update other dependent image attributes: 
```
>>> pers_imager.birth_range = (0,2)
>>> print(pers_imager)

PersistenceImager object: 
  pixel size: 0.2 
  resolution: (10, 5)     <----
  birth range: (0, 2)     <----
  persistence range: (0, 1) 
  weight: linear_ramp 
  kernel: bvncdf 
  weight parameters: {} 
  kernel parameters: {sigma: [[ 1.  0.]
                              [ 0.  1.]]}
```
Other weighting functions can also be used and are implemented in in the `PersistenceImages.weighting_fxns` modules. Here we weight pairs by their persistence squared:
```
>>> pers_imager.weight = pi.weighting_fxns.persistence
>>> pers_imager.weight_params = {'n': 2}
```
## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.