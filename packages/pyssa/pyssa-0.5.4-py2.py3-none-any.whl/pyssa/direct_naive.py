"""
    Naive implementation of the Gillespie algorithm (direct method) in Numba
"""

from typing import Tuple

from numba import njit
import numpy as np

from .utils import get_kstoc, roulette_selection


@njit(nogil=True, cache=False)
def direct_naive(
    react_stoic: np.ndarray,
    prod_stoic: np.ndarray,
    init_state: np.ndarray,
    k_det: np.ndarray,
    max_t: float,
    max_iter: int,
    volume: float,
    seed: int,
    chem_flag: bool,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """
        Parameters
        ---------
        react_stoic : (nr, ns) ndarray
            A 2D array of the stoichiometric coefficients of the reactants.
            Reactions are rows and species are columns.
        prod_stoic : (nr, ns) ndarray
            A 2D array of the stoichiometric coefficients of the products.
            Reactions are rows and species are columns.
        init_state : (ns,) ndarray
            A 1D array representing the initial state of the system.
        k_det : (nr,) ndarray
            A 1D array representing the deterministic rate constants of the
            system.
        volume : float
            The volume of the reactor vessel which is important for second
            and higher order reactions. Defaults to 1 arbitrary units.
        seed : int
            The seed for the numpy random generator used for the current run
            of the algorithm.
        chem_flag : bool
            If True, divide by Na while calculating stochastic rate constants.
            Defaults to False.

        Returns
        -------
        t : ndarray
            Numpy array of the times.
        x : ndarray
            Numpy array of the states of the system at times in in `t`.
        status : int
            Indicates the status of the simulation at exit.
            1 : Succesful completion, terminated when `max_iter` iterations reached.
            2 : Succesful completion, terminated when `max_t` crossed.
            3 : Succesful completion, terminated when all species went extinct.
            -1 : Failure, order greater than 3 detected.
            -2 : Failure, propensity zero without extinction.
    """

    ite = 1  # Iteration counter
    t_curr = 0  # Time in seconds
    nr = react_stoic.shape[0]
    ns = react_stoic.shape[1]
    v = prod_stoic - react_stoic  # nr x ns
    xt = init_state.copy()  # Number of species at time t_curr
    x = np.zeros((max_iter, ns))
    t = np.zeros((max_iter))
    x[0, :] = init_state.copy()
    xtemp = init_state.copy()  # Temporary X for updating
    status = 0
    np.random.seed(seed)  # Set the seed
    # Determine kstoc from kdet and the highest order or reactions
    prop = np.copy(
        get_kstoc(react_stoic, k_det, volume, chem_flag)
    )  # Vector of propensities
    kstoc = prop.copy()  # Stochastic rate constants
    while ite < max_iter:
        # Calculate propensities
        for ind1 in range(nr):
            for ind2 in range(ns):
                # prop = kstoc * product of (number raised to order)
                prop[ind1] *= np.power(xt[ind2], react_stoic[ind1, ind2])
        # Roulette wheel
        choice, status = roulette_selection(prop, xt)
        if status == 0:
            xtemp = xt + v[choice, :]
        else:
            return t[:ite], x[:ite, :], status

        # If negative species produced, reject step
        if np.min(xtemp) < 0:
            continue
        # Update xt and t_curr
        else:
            xt = xtemp
            r2 = np.random.rand()
            t_curr += 1 / np.sum(prop) * np.log(1 / r2)
            if t_curr > max_t:
                status = 2
                print("Reached maximum time (t_curr = )", t_curr)
                return t[:ite], x[:ite, :], status
        prop = np.copy(kstoc)
        x[ite, :] = xt
        t[ite] = t_curr
        ite += 1
    status = 1
    return t[:ite], x[:ite, :], status
