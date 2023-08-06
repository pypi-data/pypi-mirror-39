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

"""TODO"""

########### IMPORTS ########### {{{1
import warnings
from operator import eq
from collections.abc import MutableSet, Sequence, Iterable, Hashable
import math
from functools import reduce
import operator
import numpy as np


########### UTILS ########### {{{1

def _is_iterable(obj):
    """TODO""" # TODO
    return isinstance(obj, Iterable)

def _in_bounds(val, domain):
    """TODO""" # TODO
    return val >= domain[0] and val <= domain[1]
    #return all(val >= domain[0] and val <= domain[1] for val in vals)

def _hashify(item):
    """Verify if *item* is hashable, if not, try and return it as a tuple."""
    if isinstance(item, Hashable):
        return item
    else:
        return tuple(item)


########### BASE COLLECTION CLASSES ########### {{{1

class Container(MutableSet, Sequence):
    """TODO""" # TODO

    def __init__(self, iterable=None, storage_type=list, attr_names = ['fitness', 'features'], **kwargs):
        self.attr_names = set(attr_names)
        for attr in self.attr_names:
            setattr(self, attr, [])
        self._capacity = math.inf
        self._size = 0
        self.items = storage_type()
        if iterable is not None:
            self |= iterable

    capacity = property(lambda self: self._get_capacity()) # Late binding to allow polymorphic getters (https://stackoverflow.com/questions/237432/python-properties-and-inheritance)
    def _get_capacity(self):
        """Return the capacity of the container (i.e. maximal number of items/spots/bins/etc)."""
        return self._capacity

    free = property(lambda self: self._get_free()) # Late binding to allow polymorphic getters
    def _get_free(self):
        """Return the number of free spots in the container."""
        return self.capacity - self.size

    size = property(lambda self: self._get_size()) # Late binding to allow polymorphic getters
    def _get_size(self):
        """Return the size of the container (i.e. number of items, spots, bins, etc)."""
        return self._size

    def size_str(self):
        """Return a string describing the fullness of the container."""
        if math.isinf(self._get_capacity()):
            return str(self._get_size())
        else:
            return "%i/%i" % (self._get_size(), self._get_capacity())

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __contains__(self, key):
        return key in self.items

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def add(self, individual):
        """TODO""" # TODO
        old_len = len(self)
        if isinstance(self.items, MutableSet):
            index = self.items.add(individual)
            if index == old_len:
                for attr in self.attr_names:
                    getattr(self, attr).append(getattr(individual, attr, None))
                self._size += 1
            return index
        elif isinstance(self.items, Sequence):
            try:
                index = self.items.index(individual)
            except ValueError:
                self.items.append(individual)
                index = len(self.items) - 1
            if index == old_len:
                for attr in self.attr_names:
                    getattr(self, attr).append(getattr(individual, attr, None))
                self._size += 1
            return index
        else:
            raise ValueError("storage_type must be an ordered set implementing MutableSet or a Sequence")

    def discard(self, individual):
        """TODO""" # TODO
        try:
            index = self.index(individual)
        except ValueError:
            return
        for attr in self.attr_names:
            del getattr(self, attr)[index]
        self.items.remove(individual)
        self._size -= 1

    def update(self, population):
        """Add the individuals in *population*, if they are not already present in the container.
        Ignore individuals with an index outside of bounds (i.e. when *self.add* raise an IndexError exception), but print a warning when this happens.
        Returns the index of the last element inserted."""
        item_index = None
        try:
            for item in population:
                try:
                    item_index = self.add(item)
                except IndexError as e:
                    warnings.warn("Adding individual failed (index out of bounds): %s" % str(e))
                except ValueError as e:
                    warnings.warn("Adding individual failed (attribute out of bounds): %s" % str(e))
        except TypeError:
            raise ValueError("Argument needs to be an iterable, got %s" % type(population))
        return item_index




class Grid(Container):
    """TODO""" # TODO

    def __init__(self, iterable=None, shape=(1), items_per_bin=1, fitness_attr='fitness', fitness_domain=(0., 1.), fitness_weight=1., features_attr='features', features_domain=((0., 1.),), **kwargs):
        kwargs['attr_names'] = list(set(kwargs['attr_names']) - set([fitness_attr, features_attr])) if 'attr_names' in kwargs else ()
        if _is_iterable(shape):
            self._shape = shape
        else:
            self._shape = (shape,)
        self.items_per_bin = items_per_bin
        self.fitness_attr = fitness_attr
        self.fitness_domain = fitness_domain
        self.fitness_weight = fitness_weight
        self.features_attr = features_attr
        self.features_domain = features_domain
        if len(self.features_domain) != len(self.shape):
            raise ValueError("*features_domain* must have the same shape as *shape*")
        for f in self.features_domain:
            if len(f) != 2:
                raise ValueError("*features_domain* must be a sequence of 2-tuples.")
        self._init_grid()
        super().__init__(iterable, **kwargs)


    def _init_grid(self):
        """Initialise the grid attributes *self.solutions*, *self.fitness* and *self.features*, to correspond to the shape *self.shape*."""
        self.solutions = {x: [] for x in self._index_grid_iterator()}
        self.fitness = {x: [] for x in self._index_grid_iterator()}
        self.features = {x: [] for x in self._index_grid_iterator()}
        self.best_fitness = {x: math.nan for x in self._index_grid_iterator()}
        self.best_fitness_array = np.full(self._shape, np.nan)
        self._bins_size = [(self.features_domain[i][1] - self.features_domain[i][0]) / float(self.shape[i]) for i in range(len(self.shape))]
        self._filled_bins = 0

    shape = property(lambda self: self._get_shape()) # Late binding to allow polymorphic getters (https://stackoverflow.com/questions/237432/python-properties-and-inheritance)
    def _get_shape(self):
        """Return the shape of the grid."""
        return self._shape

    def _get_capacity(self):
        """Return the capacity of the container (i.e. maximal number of items/spots/bins/etc)."""
        return reduce(operator.mul, self.shape)

    def _get_size(self):
        """Return the size of the container (i.e. number of filled bins)."""
        return self._filled_bins


    def index_grid(self, features):
        """Get the index in the grid of a given individual with features *features*, raising an IndexError if it is outside the grid. """
        index = []
        if len(features) != len(self.shape):
            raise IndexError("length of parameter *features* (%i) does not corresponds to the number of dimensions of the grid (%i)" % (len(features), len(self.shape)))
        for i in range(len(features)):
            normalised_feature = features[i] - self.features_domain[i][0]
            if normalised_feature == self.features_domain[i][1] - self.features_domain[i][0]:
                partial = self.shape[i] - 1
            elif normalised_feature > self.features_domain[i][1] - self.features_domain[i][0]:
                raise IndexError("*features* (%s) out of bounds (%s)" % (str(features), str(self.features_domain)))
            else:
                partial = int(normalised_feature / self._bins_size[i])
            index.append(partial)
        return tuple(index)


    def _index_grid_iterator(self):
        """Return an iterator of the index of the grid, based on *self.shape*."""
        val = [0] * len(self._shape)
        yield tuple(val)
        while True:
            for i in reversed(range(len(self._shape))):
                val[i] += 1
                if val[i] >= self._shape[i]:
                    if i == 0:
                        return
                    val[i] = 0
                else:
                    yield tuple(val)
                    break

    def _update_best_fitness(self, ig):
        if self.fitness_weight < 0.:
            val = min(self.fitness[ig], default=None)
        elif self.fitness_weight > 0.:
            val = max(self.fitness[ig], default=None)
        self.best_fitness[ig] = val
        if val == None:
            self.best_fitness_array[ig] = math.nan
        else:
            self.best_fitness_array[ig] = val


    def add(self, individual):
        """TODO""" # TODO
        ind_features = getattr(individual, self.features_attr)
        ind_fitness = getattr(individual, self.fitness_attr)
        ind_fitness_vals = ind_fitness.values[0] if hasattr(ind_fitness, "values") else ind_fitness[0]
        if not _in_bounds(ind_fitness_vals, self.fitness_domain):
            raise ValueError("fitness (%s) out of bounds (%s)" % (str(ind_fitness_vals), str(self.fitness_domain)))
        ig = self.index_grid(ind_features) # Raise exception if features are out of bounds

        if len(self.fitness[ig]) == 0:
            self._filled_bins += 1

        # Add individual in grid, if there are enough empty spots
        if len(self.fitness[ig]) < self.items_per_bin:
            pass
        elif (self.fitness_weight < 0. and max(self.fitness[ig], default=self.fitness_domain[1]) > ind_fitness_vals):
            index_max = max(range(len(self.fitness[ig])), key=self.fitness[ig].__getitem__)
            Container.discard(self, self.solutions[ig][index_max])
            del self.solutions[ig][index_max]
            del self.fitness[ig][index_max]
            del self.features[ig][index_max]
        elif (self.fitness_weight > 0. and min(self.fitness[ig], default=self.fitness_domain[0]) < ind_fitness_vals):
            index_min = min(range(len(self.fitness[ig])), key=self.fitness[ig].__getitem__)
            Container.discard(self, self.solutions[ig][index_min])
            del self.solutions[ig][index_min]
            del self.fitness[ig][index_min]
            del self.features[ig][index_min]
        else:
            return None

        # Add individual in container
        old_len = len(self)
        index = Container.add(self, individual)
        if index == old_len: # Individual was not already present in container
            self.solutions[ig].append(individual)
            self.fitness[ig].append(ind_fitness_vals)
            self.features[ig].append(ind_features)

        # Update best_fitness
        self._update_best_fitness(ig)
        return index


    def discard(self, individual):
        """TODO""" # TODO
        # Verify that the individual is in container
        if not individual in self:
            return
        # Remove individual from grid
        ind_features = getattr(individual, self.features_attr)
        ind_fitness = getattr(individual, self.fitness_attr)
        ig = self.index_grid(ind_features) # Raise exception if features are out of bounds
        index_in_bin = self.solutions[ig].index(individual)
        del self.solutions[ig][index_in_bin]
        del self.fitness[ig][index_in_bin]
        del self.features[ig][index_in_bin]
        # Update best_fitness
        self._update_best_fitness(ig)
        # Remove individual from container
        Container.discard(self, individual)
        # Update number of filled bins
        if len(self.solutions[ig]) == 0:
            self._filled_bins -= 1


#
## TODO
#class Archive(Container):
#    """TODO"""
#    pass
#





# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
