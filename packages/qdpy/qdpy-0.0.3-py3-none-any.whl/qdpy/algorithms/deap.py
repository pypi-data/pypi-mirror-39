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

# TODO
"""TODO"""



from qdpy.collections import *

#from deap import algorithms
from deap import tools
from timeit import default_timer as timer


def qdSimple(init_batch, toolbox, container, batch_size, niter, stats = None, halloffame = None, verbose = False, start_time = None):
    """The simplest QD algorithm using DEAP.
    :param init_batch: Sequence of individuals used as initial batch.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution operators.
    :param batch_size: The number of individuals in a batch.
    :param niter: The number of iterations.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :param start_time: Starting time of the illumination process, or None to take the current time.
    :returns: The final batch
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution

    TODO
    """
    if start_time == None:
        start_time = timer()
    logbook = tools.Logbook()
    logbook.header = ["iteration", "containerSize", "evals"] + (stats.fields if stats else []) + ["elapsed"]

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in init_batch if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit[0]
        ind.features = fit[1]

    # Update halloffame
    if halloffame is not None:
        halloffame.update(init_batch)

    # Store batch in container
    container.update(init_batch)

    # Compile stats and update logs
    record = stats.compile(container) if stats else {}
    logbook.record(iteration=0, containerSize=container.size_str(), evals=len(invalid_ind), elapsed=timer()-start_time, **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for i in range(1, niter + 1):
        start_time = timer()
        # Select the next batch individuals
        batch = toolbox.select(container, batch_size)

        # Vary the pool of individuals
        offspring = []
        for o in batch:
            newO = toolbox.clone(o)
            ind, = toolbox.mutate(newO)
            del ind.fitness.values
            offspring.append(ind)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit[0]
            ind.features = fit[1]

        # Replace the current population by the offspring
        container.update(offspring)

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(container)

        # Append the current generation statistics to the logbook
        record = stats.compile(container) if stats else {}
        logbook.record(iteration=i, containerSize=container.size_str(), evals=len(invalid_ind), elapsed=timer()-start_time, **record)
        if verbose:
            print(logbook.stream)

    return batch, logbook



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
