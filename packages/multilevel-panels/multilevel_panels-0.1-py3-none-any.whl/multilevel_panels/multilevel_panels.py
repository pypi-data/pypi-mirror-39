import logging
from functools import reduce
from operator import or_
from typing import List, Sequence, Tuple

import numpy as np


def setop2d_functor(op):
    """Return a binary function that will perform the passed 1-dimensional set operation on 2-dimensional array arguments.
    """
    if op not in (np.intersect1d, np.union1d, np.setdiff1d):
        raise ValueError

    def setop2d(a, b):
        # inspired by https://stackoverflow.com/questions/8317022/get-intersecting-rows-across-two-2d-numpy-arrays
        result = op(
            a.view([('', a.dtype)] * a.shape[1]).ravel(),
            b.view([('', b.dtype)] * b.shape[1]).ravel(),
        )

        return result.view(a.dtype).reshape(-1, a.shape[1])

    return setop2d


def setop2d_variadic_functor(op):
    """Return a variadic version of the function returned by setop2d_functor.
    """
    def setop2d_variadic(*args):
        return reduce(
            setop2d_functor(op),
            args
        )

    return setop2d_variadic


intersect2d = setop2d_variadic_functor(np.intersect1d)
union2d = setop2d_variadic_functor(np.union1d)
setdiff2d = setop2d_variadic_functor(np.setdiff1d)


def get_gap_patterns(n: int) -> Tuple:
    """Return a tuple of integers whose binary representation is like the following regular expression: ^10{m}1$
    and m = n - 2.
    """
    if n < 3:
        return tuple()
    else:
        return get_gap_patterns(n - 1) + ((1 << (n - 1)) + 1, )


def hasgaps(bool_lst: List) -> bool:
    """Determine if the passed list of boolean values matches any possible gap pattern for a list of such length.
    """
    # assume the input represents a bit array and convert it to an integer
    val = int(sum(v << i for i, v in enumerate(reversed(bool_lst))))

    gap_patterns = get_gap_patterns(val.bit_length())

    while val:
        for i, n in enumerate(range(3, val.bit_length() + 1)):
            # if the value's lower bits matches the gap pattern of corresponding length
            if (val & ((2 ** n) - 1)) ^ gap_patterns[i] == 0:
                return True
        else:
            val = val >> 1

    return False


def get_hi_lo_join(hi, lo):
    """Return the result of intersecting the higher order columns in hi and lo and filtering lo with this intersection.
    """
    logging.debug(f'hi: {hi}')
    logging.debug(f'lo: {lo}')

    intersection = intersect2d(hi, lo[:, :-1].copy())
    logging.debug(f'intersection: {intersection}')

    lo_dtype = [('', lo.dtype)] * (lo.shape[1] - 1)
    hi_dtype = [('', hi.dtype)] * hi.shape[1]

    # convert each 2-dimensional array to a 1-dimensional array of tuples for ease of filtering
    join_bool_idx = np.isin(
        lo[:, :-1].copy().view(dtype=lo_dtype).ravel(),
        hi.view(dtype=hi_dtype).ravel(),
    )

    join_lo = lo[join_bool_idx]
    logging.debug(f'join_lo: {join_lo}')

    return join_lo


def intersectml_colwise_reduction(a: Sequence, b: Sequence):
    """Perform a recursive multilevel intersect of pairs of 2-dimensional arrays from the sequences a and b.
    """
    logging.debug(f'a: {a}')
    logging.debug(f'b: {b}')

    if len(a) == 1:
        # note that this returns a 1-tuple
        return intersect2d(*a, *b),
    else:
        join_a_b = get_hi_lo_join(a[-2], b[-1])
        join_b_a = get_hi_lo_join(b[-2], a[-1])

        intersection_lo = intersect2d(a[-1], b[-1])
        logging.debug(f'intersection_lo: {intersection_lo}')

        concat_lo = np.concatenate(
            (
                intersection_lo,
                join_a_b.view(int).reshape((join_a_b.shape[0], intersection_lo.shape[1])),
                join_b_a.view(int).reshape((join_b_a.shape[0], intersection_lo.shape[1])),
            ),
            axis=0,
        )
        if len(concat_lo) > 0:
            concat_lo = np.unique(concat_lo, axis=0)
        logging.debug(f'concat_lo: {concat_lo}')

        intersection_hi = intersectml_colwise_reduction(a[:-1], b[:-1])
        logging.debug(f'intersection_hi: {intersection_hi}')

        return (*intersection_hi, concat_lo)


def intersectml(a, b):
    """Intersect a pair of multilevel panels.
    """
    logging.debug(f'a: {a}')
    logging.debug(f'b: {b}')

    # produce the decompositions of a and b
    tup_a = tuple(a)
    tup_b = tuple(b)

    elementwise_or = map(or_, [np.any(i) for i in tup_a], [np.any(i) for i in tup_b])
    # level skipping issue is here
    if hasgaps(list(elementwise_or)):
        raise NotImplementedError

    return intersectml_colwise_reduction(tup_a, tup_b)


def get_lo_hi_setdiff(hi, lo):
    """Return the elements of lo whose higher order columns do not intersect with those in hi.
    """
    join_lo = get_hi_lo_join(hi, lo)

    setdiff_lo = setdiff2d(lo, join_lo)
    logging.debug(f'setdiff_lo: {setdiff_lo}')

    return setdiff_lo


def unionml_colwise_reduction(unions: Sequence):
    """Perform a recursive multilevel union of pairs of 2-dimensional arrays from the sequences a and b.
    """
    logging.debug(f'unionml_colwise_reduction: {unions}')
    if len(unions) == 1:
        return unions
    else:
        return unionml_colwise_reduction(unions[:-1]) + (get_lo_hi_setdiff(unions[-2], unions[-1]), )


def unionml(a, b):
    """Union a pair of multilevel panels.
    """
    logging.debug(f'a: {a}')
    logging.debug(f'b: {b}')

    # produce a tuple of the unions of each level of a and b
    unions = tuple(union2d(*tup) for tup in zip(a, b))
    # level skipping issue is here
    if hasgaps([np.any(u) for u in unions]):
        raise NotImplementedError

    return unionml_colwise_reduction(unions)


def decompose(arr: np.ndarray, assume_unique=True) -> Tuple:
    """Convert a 2-d array that may contain sequential row-wise right-hand-side NaNs into a n-tuple representation.
    Each tuple element is an array of shape (r, c), where c is the column index of the original array,
    and r is the number of rows in that column whose entries in further columns (i.e., c + 1, c + 2, etc.)
    contain only NaNs.

    >>> arr = np.array([[1, 1, 1], [2, 2, np.nan], [3, np.nan, np.nan]])
    >>> decompose(arr)
    (array([[3]]), array([[2, 2]]), array([[1, 1, 1]]))
    """
    if arr.shape[1] == 0:
        return tuple()
    else:
        nan_bool_idx = np.isnan(arr).any(axis=1)
        non_nan = arr[~ nan_bool_idx, :].astype(int)
        if not assume_unique:
            non_nan = np.unique(non_nan, axis=0)

        return decompose(arr[nan_bool_idx, :-1], assume_unique=assume_unique) + (non_nan, )


def recompose(tup) -> np.ndarray:
    """Convert the output of `decompose()` to a 2-d array that may contain sequential row-wise right-hand-side NaNs.
    Row order of the result is not guaranteed to match the original input order to `decompose()`.

    >>> arr = np.array([[1, 1, 1], [2, 2, np.nan], [3, np.nan, np.nan]])
    >>> recompose(decompose(arr))
    array([[ 3., nan, nan],
           [ 2.,  2., nan],
           [ 1.,  1.,  1.]])
    """
    pad_width = tup[-1].shape[1]

    return np.concatenate(
        tuple(
            np.pad(
                t.astype(float),
                ((0, 0), (0, pad_width - t.shape[1])),
                mode='constant',
                constant_values=np.nan
            ) for t in tup  # type: ignore
        )
    )


class MultilevelPanel:
    def __init__(self, arr: np.ndarray):
        self._decomposed = decompose(arr)

    def __getitem__(self, item):
        # this permits doing mlp[n], tuple(mlp), (*mlp), etc., and having the result come from `decompose()`
        return self._decomposed[item]

    def __eq__(self, other):
        # __ne__ is implicit in Python 3, but would need to be defined in Python 2
        # note that this does not guarantee the compared multilevel panels are in the same order,
        # only that they contain the same elements
        if not isinstance(other, type(self)):
            raise TypeError
        else:
            return all(np.all(s == o) for s, o in zip(self, other))

    def __repr__(self):
        return str(self.flatten())

    def flatten(self):
        return recompose(self._decomposed)

    def intersect(self, *others: 'MultilevelPanel'):
        return type(self)(
            recompose(
                reduce(
                    intersectml,
                    (self, *others)
                )
            )
        )

    def union(self, *others: 'MultilevelPanel'):
        return type(self)(
            recompose(
                reduce(
                    unionml,
                    (self, *others)
                )
            )
        )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
