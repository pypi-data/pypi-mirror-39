#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`~qdpy.utils` module is a collection of small functions and classes handling common patterns."""

__all__ = ["jit"]

########### NUMBA ########### {{{1
def _dummyJit(*args, **kwargs):
    """
    Dummy version of jit decorator, does nothing
    """
    if len(args) == 1 and callable(args[0]):
        return args[0]
    else:
        def wrap(func):
            return func
        return wrap
try:
    import numba
    from numba import jit
except ImportError:
    jit = _dummyJit


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
