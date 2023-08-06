import numba
import numpy as np
import pytest
from profiling import profiling_data
from profiling import tools

from profiles import geometry_profiles


class EllipticalIsothermal(geometry_profiles.EllipticalProfile):

    def __init__(self, centre=(0.0, 0.0), axis_ratio=0.9, phi=0.0, einstein_radius=1.0):
        """
        Represents an elliptical isothermal density distribution, which is equivalent to the elliptical power-law
        density distribution for the value slope=2.0

        Parameters
        ----------
        centre: (float, float)
            The image_grid of the origin of the profiles
        axis_ratio : float
            Elliptical mass profile's minor-to-major axis ratio (b/a)
        phi : float
            Rotation angle of mass profile's ellipse counter-clockwise from positive x-axis
        einstein_radius : float
            Einstein radius of power-law mass profiles
        """

        super(EllipticalIsothermal, self).__init__(centre, axis_ratio, phi)
        self.einstein_radius = einstein_radius
        self.slope = 2.0

    @property
    def einstein_radius_rescaled(self):
        """Rescale the einstein radius by slope and axis_ratio, to reduce its degeneracy with other mass-profiles
        parameters"""
        return ((3 - self.slope) / (1 + self.axis_ratio)) * self.einstein_radius ** (self.slope - 1)

    @geometry_profiles.transform_grid
    def deflections_from_grid(self, grid):
        """
        Calculate the deflection angles at a given set of gridded coordinates.

        Parameters
        ----------
        grid : masks.ImageGrid
            The grid of coordinates the deflection angles are computed on.
        """

        try:
            factor = 2.0 * self.einstein_radius_rescaled * self.axis_ratio / np.sqrt(1 - self.axis_ratio ** 2)

            psi = np.sqrt(np.add(np.multiply(self.axis_ratio ** 2, np.square(grid[:, 0])), np.square(grid[:, 1])))

            deflection_x = np.arctan(np.divide(np.multiply(np.sqrt(1 - self.axis_ratio ** 2), grid[:, 0]), psi))
            deflection_y = np.arctanh(np.divide(np.multiply(np.sqrt(1 - self.axis_ratio ** 2), grid[:, 1]), psi))

            return self.rotate_grid_from_profile(np.multiply(factor, np.vstack((deflection_x, deflection_y)).T))
        except ZeroDivisionError:
            return self.grid_radius_to_cartesian(grid, np.full(grid.shape[0], 2.0 * self.einstein_radius_rescaled))

    @geometry_profiles.transform_grid
    def deflections_from_grid_jitted(self, grid):
        return self.rotate_grid_from_profile(
            self.deflections_from_grid_jit(grid, self.axis_ratio, self.einstein_radius_rescaled))

    @staticmethod
    @numba.jit(nopython=True)
    def deflections_from_grid_jit(grid, axis_ratio, einstein_radius_rescaled):

        factor = 2.0 * einstein_radius_rescaled * axis_ratio / np.sqrt(1 - axis_ratio ** 2)
        q1 = np.sqrt(1 - axis_ratio ** 2)

        deflections = np.zeros(grid.shape)
        for i in range(deflections.shape[0]):
            psi = np.multiply(np.divide(1.0, q1),
                              np.sqrt(np.add(np.multiply(np.square(axis_ratio), np.square(grid[i, 0])),
                                             np.square(grid[i, 1]))))

            deflections[i, 0] = np.multiply(factor, np.arctan(np.divide(grid[i, 0], psi)))
            deflections[i, 1] = np.multiply(factor, np.arctanh(np.divide(grid[i, 1], psi)))

        return deflections


sie = EllipticalIsothermal(centre=(0.0, 0.0), axis_ratio=0.8, phi=90.0, einstein_radius=1.4)

subgrd_size = 4

lsst = profiling_data.setup_class(name='LSST', pixel_scale=0.2, sub_grid_size=subgrd_size)
euclid = profiling_data.setup_class(name='Euclid', pixel_scale=0.1, sub_grid_size=subgrd_size)
hst = profiling_data.setup_class(name='HST', pixel_scale=0.05, sub_grid_size=subgrd_size)
hst_up = profiling_data.setup_class(name='HSTup', pixel_scale=0.03, sub_grid_size=subgrd_size)
ao = profiling_data.setup_class(name='AO', pixel_scale=0.01, sub_grid_size=subgrd_size)

assert (sie.deflections_from_grid(grid=lsst.coords.sub_grid_coords) ==
        pytest.approx(sie.deflections_from_grid_jitted(grid=lsst.coords.sub_grid_coords), 1e-4))


@tools.tick_toc_x10
def lsst_solution():
    sie.deflections_from_grid_jitted(grid=lsst.coords.sub_grid_coords)


@tools.tick_toc_x10
def euclid_solution():
    sie.deflections_from_grid_jitted(grid=euclid.coords.sub_grid_coords)


@tools.tick_toc_x10
def hst_solution():
    sie.deflections_from_grid_jitted(grid=hst.coords.sub_grid_coords)


@tools.tick_toc_x10
def hst_up_solution():
    sie.deflections_from_grid_jitted(grid=hst_up.coords.sub_grid_coords)


@tools.tick_toc_x10
def ao_solution():
    sie.deflections_from_grid_jitted(grid=ao.coords.sub_grid_coords)


if __name__ == "__main__":
    lsst_solution()
    euclid_solution()
    hst_solution()
    hst_up_solution()
    ao_solution()
