from collections import defaultdict
import io

import cvxpy as cp
import numpy as np
from titus_optimize.utils import stdout_redirector


def optimize_ip(requested_cus, total_available_cus, num_sockets, previous_allocation=None, verbose=False):
    """
    This function will find the optimal placement of workloads on the compute units of the instance,
    potentially starting from an initial allocation state (in which case it will also try to minimize
    the changes required to the current placement to satisfy the new request).

    Arguments:
        - requested_cus: array of integers representing the number of compute units requested by each workload. Ex: [2,4,8,4]
        - total_available_cus: total # of compute units on the instance
        - num_sockets: # of NUMA sockets on the instance
        - previous allocation: array of assignment vectors from a previous placement
        - verbose: flag to return the (very!) verbose stdout of the internal xpress solver

    Returns:
    An array of binary assignment vectors. For example: [[0, 1, 0, 0], [1, 0, 1, 0]] could be a possible
    return value for a call where requested_cus=[1, 2] and total_available_cus=4
    This would mean that the first workload was assigned the compute unit with index 1, and that
    the second workload was assigned the compute units with indices 0 and 3
    """

    d = total_available_cus
    n = num_sockets
    c = d // 2  # number of physical cores
    b = total_available_cus // n  # number of CUs per socket
    k = len(requested_cus)

    if sum(requested_cus) > d:
        raise ValueError("The total # of compute units requested is higher than the total available on the instance.")
    if total_available_cus % 2 != 0:
        raise ValueError("Odd number of compute units on the instance not allowed."
                         " we assume that there always are 2 hyper-threads per physical core.")

    ALPHA_NU = 1000.0
    ALPHA_LLC = 1.0
    ALPHA_L12 = 10000.0
    ALPHA_ORDER = 0.00000001
    ALPHA_PREV = 0.00001

    r = np.array(requested_cus)

    ij = np.zeros((d, k), dtype=np.int32)
    for i in range(d):
        for j in range(k):
            ij[i, j] = (i + 1) * (j + 1) * (i // b + 1)

    prev_M = None
    if previous_allocation is not None:
        prev_M = np.zeros((d, k), dtype=np.int32)
        for j, v in enumerate(previous_allocation):
            if j == k:  # means that previous one was bigger, we removed a task
                break
            for i in range(d):
                if v[i] > 0.5:
                    prev_M[i, j] = 1

    # Optimal boolean assignment matrix we wish to find
    M = cp.Variable((d, k), boolean=True)

    # Auxiliary variables needed
    X = cp.Variable((n, k), integer=True)
    Z = cp.Variable(n, integer=True)
    Y = cp.Variable(c, integer=True)

    # 1) Penalize placements where workloads span multiple sockets
    cost_NU = -(ALPHA_NU / (n * k)) * cp.sum(X)

    # 2) Penalize empty sockers (because it means more LLC trashing)
    cost_LLC = - (ALPHA_LLC / n) * cp.sum(Z)

    # 3) Penalize empty cores (because it means more L1/L2 trashing)
    cost_L12 = (ALPHA_L12 / c) * cp.sum(Y)

    # 4) Favor contiguous indexing for:
    # - better affinity of hyperthreads to jobs on the same core
    # - more organized placement
    cost_ordering = ALPHA_ORDER * cp.sum(cp.multiply(ij, M))

    cost = cost_NU + cost_LLC + cost_L12 + cost_ordering

    # 5) [optional] if starting from a previous allocation,
    # penalize placements that move assignements too much
    # compared to reference placement.
    if prev_M is not None:
        cost += ALPHA_PREV * cp.sum(cp.abs(M - prev_M))

    # The placement has to satisfy the requested # of units for workload
    CM1 = [M.T * np.ones((d,)) == r]
    # Each compute unit can only be assigned to a single workload
    CM2 = [M * np.ones((k, 1)) <= np.ones((d, 1))]

    # Extra variables constraints (coming from linearization of min/-max operators)
    CX1 = [X[t, j] <= (1.0 / max(r[j], 1)) * cp.sum(M[t * b: (t + 1) * b, j]) for t in range(n) for j in range(k)]
    CX2 = [X <= 1]

    CZ1 = [Z[t] <= cp.sum(M[t * b: (t + 1) * b, :]) for t in range(n)]
    CZ2 = [Z <= 1]

    CY1 = [Y[l] >= -1 + cp.sum(M[2 * l, :]) + cp.sum(M[2 * l + 1, :]) for l in range(c)]
    CY2 = [Y >= 0]

    constraints = CM1 + CM2 + CY1 + CY2 + CX1 + CX2 + CZ1 + CZ2

    prob = cp.Problem(cp.Minimize(cost), constraints)

    if not verbose:
        xpress_stdout = io.BytesIO()
        with stdout_redirector(xpress_stdout):
            prob.solve(solver='XPRESS', verbose=False)
    else:
        prob.solve(solver='XPRESS', verbose=False)

    if prob.status != 'optimal':
        raise Exception("Could not solve the integer program: `%s`" % (prob.status,))

    res = [None] * len(requested_cus)
    for i, e in enumerate(M.value.T):
        res[i] = [1 if u > 0.5 else 0 for u in e]
    return res


def optimize_greedy(requested_cus, total_available_cus, num_sockets):
    """
    This function simulates the greedy algorithm implemented in titus-isolate.
    Only used for benchmarking purposes.
    """
    try:
        from titus_isolate.isolate.cpu import assign_threads
        from titus_isolate.model.processor.cpu import Cpu
        from titus_isolate.model.processor.package import Package
        from titus_isolate.model.processor.core import Core
        from titus_isolate.model.processor.thread import Thread
        from titus_isolate.model.workload import Workload
        from titus_isolate.docker.constants import STATIC
    except ImportError:
        raise Exception("You need titus-isolate for this function.")

    workloads = []

    for i, req in enumerate(requested_cus):
        w = Workload(str(i), req, STATIC)
        workloads.append(w)

    workloads.sort(key=lambda workload: workload.get_thread_count(), reverse=True)

    b = total_available_cus // num_sockets
    c = b // 2
    sockets = []
    for i in range(num_sockets):
        cores = []
        for j in range(c):
            core = Core(j, [Thread(b * i + 2 * j), Thread(b * i + 2 * j + 1)])
            cores.append(core)
        sockets.append(Package(i, cores))
    cpu = Cpu(sockets)
    cpu.clear()

    for w in workloads:
        assign_threads(cpu, w)

    ids_per_workload = defaultdict(list)

    for t in cpu.get_threads():
        if t.is_claimed():
            ids_per_workload[t.get_workload_id()] = ids_per_workload[t.get_workload_id()] + [t.get_id()]

    allocations = []
    for i in range(len(requested_cus)):
        assignments = [0] * total_available_cus
        for j in ids_per_workload[str(i)]:
            assignments[j] = 1
        allocations.append(assignments)

    return allocations
