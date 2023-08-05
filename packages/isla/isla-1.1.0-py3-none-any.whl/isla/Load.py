import numpy as np
from scipy.stats import norm

from .LoadComponent import LoadComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Load(LoadComponent):
    """Load module.

    Parameters
    ----------
    data : dict or ndarray
        Dataset. Pass a dict with 'load' as the key for the hourly load demand
        [kW] for one year. An ndarray can be passed as well.
    fail_prob : float
        Probability of failure of the component.
    stat_data : dict, str, or None
        Statistical data used for load variance. Set to None to remove load
        variability. Set to 'auto' to automatically make noise based on
        dataset. Pass a dict with 'var' as key and variance as value to
        manually adjust noise.

    Other Parameters
    ----------------
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.

    """

    def __init__(self, data, fail_prob=0.0, stat_data=None, **kwargs):
        """Initializes the base class."""

        # initialize component
        super().__init__(
            data, 0.0, 0.0, 0.0, 0.0,
            None, None, 'Load', '#666666',
            20.0, fail_prob, stat_data, False, **kwargs
        )

        # update initialized parameters if essential data is complete
        self.update_init()

    def _load_derive(self):
        """Derives energy parameters from dataset.

        Returns
        -------
        pow_max : ndarray
            Maximum power in the load.
        enr_tot : ndarray
            Total power in the load.

        Notes
        -----
        This function can be modified by the user.

        """
        # extract dataset
        if isinstance(self.data, dict):  # pass dict
            self.pow_ld = self.data['load']  # load [kW]
        elif isinstance(self.data, np.ndarray):  # pass ndarray
            self.pow_ld = self.data

        # convert dataset to 1D array
        self.pow_ld = np.ravel(self.pow_ld)

        return (np.max(self.pow_ld), np.sum(self.pow_ld))

    def _get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        Returns
        -------
        pow : ndarray
            Power [kW] at the current timestep.

        Notes
        -----
        This function can be modified by the user.

        """
        return self.pow_ld[hr]*np.ones(self.num_case)

    def _stat_derive(self):
        """Derive statistical parameters from dataset.

        Returns
        -------
        stat_dict : dict
            Dict with statistical parameters. Will be used in _noise_calc.

        Notes
        -----
        This function can be modified by the user.

        """
        # solve for variance between hours per day
        var_list = []  # list of variances
        norm_arr = self.pow_ld/np.max(self.pow_ld)  # normalize
        for i in range(24):
            loc_i, var_i = norm.fit(norm_arr[i::24])  # variance per hour
            var_list.append(var_i)  # append variance

        return {'var': np.array(var_list)}

    def _noise_calc(self, hr):
        """Generates noise based on statistical data.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        Returns
        -------
        noise : ndarray
            Factor to be multiplied to component power.

        Notes
        -----
        This function can be modified by the user.

        """
        var = self.stat_dict['var']
        if self.stat_data == 'auto':
            noise = 1+np.random.normal(
                0.0, var[hr % 24], self.num_case
            )
        else:
            noise = 1+np.random.normal(0.0, var, self.num_case)

        return noise

    def _update_init(self):
        """Initalize other parameters for the component."""

        pass
