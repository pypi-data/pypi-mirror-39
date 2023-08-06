import numpy as np
from profiling import profiling_data
from profiling import tools

from profiles import geometry_profiles


class SphericalProfile(geometry_profiles.Profile):

    def __init__(self, centre=(0.0, 0.0)):
        """ Generic elliptical profiles class to contain functions shared by light and mass profiles.

        Parameters
        ----------
        centre: (float, float)
            The coordinates of the origin of the profiles
        axis_ratio : float
            Ratio of profiles ellipse's minor and major axes (b/a)
        phi : float
            Rotational angle of profiles ellipse counter-clockwise from positive x-axis
        """
        super(SphericalProfile, self).__init__(centre)
        self.axis_ratio = 1.0
        self.phi = 0.0

    def transform_grid_to_reference_frame(self, grid):
        transformed = np.subtract(grid, self.centre)
        return transformed.view(geometry_profiles.TransformedGrid)


sub_grid_size = 4

lsst = profiling_data.setup_class(name='LSST', pixel_scale=0.2, sub_grid_size=sub_grid_size)
euclid = profiling_data.setup_class(name='Euclid', pixel_scale=0.1, sub_grid_size=sub_grid_size)
hst = profiling_data.setup_class(name='HST', pixel_scale=0.05, sub_grid_size=sub_grid_size)
hst_up = profiling_data.setup_class(name='HSTup', pixel_scale=0.03, sub_grid_size=sub_grid_size)
ao = profiling_data.setup_class(name='AO', pixel_scale=0.01, sub_grid_size=sub_grid_size)

geometry = SphericalProfile(centre=(0.0, 0.0))


@tools.tick_toc_x20
def lsst_solution():
    geometry.transform_grid_to_reference_frame(grid=lsst.coords.sub_grid_coords)


@tools.tick_toc_x20
def euclid_solution():
    geometry.transform_grid_to_reference_frame(grid=euclid.coords.sub_grid_coords)


@tools.tick_toc_x20
def hst_solution():
    geometry.transform_grid_to_reference_frame(grid=hst.coords.sub_grid_coords)


@tools.tick_toc_x20
def hst_up_solution():
    geometry.transform_grid_to_reference_frame(grid=hst_up.coords.sub_grid_coords)


@tools.tick_toc_x20
def ao_solution():
    geometry.transform_grid_to_reference_frame(grid=ao.coords.sub_grid_coords)


if __name__ == "__main__":
    lsst_solution()
    euclid_solution()
    hst_solution()
    hst_up_solution()
    ao_solution()
