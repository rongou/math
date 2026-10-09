#!/usr/bin/env python3
"""Independent, bounded SU(2) rough-link replacement diagnostics.

Run from the repository root (Python >= 3.9; standard library only):
    python3 -B research_notes/yang_mills_2026_10_09/rough_region/checks/check_replacement.py
Capture both streams in the assigned transcript:
    > research_notes/yang_mills_2026_10_09/rough_region/checks/output.txt 2>&1

Conventions: U_xy -> g_x U_xy g_y^*, row-major complex 2x2 matrices,
s(U) = 1 - Re Tr(U)/2, d(U,V) = ||U-V||_op, n = |J|, and E below
means ONLY the conditional sum over ALL plaquettes touching J, not an
energy difference. Caps are GEODESIC: theta <= rho <= 1, as in the parent
note; their chordal radii are <= rho. Forests and J depend only on geometry.

Quaternion multiplication and a generic 2x2 singular-value calculation
provide independent checks on the matrix calculations. No sibling imports,
dependencies, downloads, filesystem writes, or disabled-under--O assertions.
Every random stream is seeded; set iteration never determines random draws.

Finite samples (including the 'all U' obstruction tests) are DIAGNOSTICS,
NOT PROOFS. The parent supplies analytic quantifiers and measure arguments.
No density/partition-function integration, typical-boundary probability,
continuum, or mass-gap claim is made. Optional Hessian checks are omitted.
"""

from collections import Counter, deque
from itertools import combinations, product
from math import cos, fsum, pi, sin, sqrt
import random
import sys


SEED = 20261009
GRIDS = ((4, 4, 4, 4), (4, 5, 4, 5))
PAIRS = tuple(combinations(range(4), 2))
I = (1 + 0j, 0j, 0j, 1 + 0j)
MINUS_I = (-1 + 0j, 0j, 0j, -1 + 0j)
QI = (1.0, 0.0, 0.0, 0.0)
TOL = 2e-11
ENERGY_TOL = 2e-9


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, tolerance, message):
    error = abs(actual - expected)
    require(error <= tolerance, f"{message}: {actual!r} != {expected!r}; error={error!r}")
    return error


def rejected(call, exception, message):
    try:
        call()
    except exception:
        return
    raise AssertionError(f"negative control was not detected: {message}")


def mul(a, b):
    return (a[0]*b[0] + a[1]*b[2], a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2], a[2]*b[1] + a[3]*b[3])


def adj(a):
    return (a[0].conjugate(), a[2].conjugate(),
            a[1].conjugate(), a[3].conjugate())


def chain(*matrices):
    result = I
    for matrix in matrices:
        result = mul(result, matrix)
    return result


def matrix_error(a, b):
    return max(abs(x-y) for x, y in zip(a, b))


def op_norm_sq(m):
    """Largest eigenvalue of M* M, valid for generic complex 2x2 M.

    Deliberately does NOT use the SU(2) trace/action identity under test.
    """
    # Avoid squaring abs(complex), whose intermediate sqrt needlessly rounds
    # exactly representable squared moduli (e.g. |1-i|^2 = 2).
    def squared_modulus(z):
        return z.real*z.real + z.imag*z.imag
    a = squared_modulus(m[0]) + squared_modulus(m[2])
    d = squared_modulus(m[1]) + squared_modulus(m[3])
    b = m[0].conjugate()*m[1] + m[2].conjugate()*m[3]
    return (a + d + sqrt((a-d)**2 + 4*squared_modulus(b))) / 2


def distance(a, b=I):
    return sqrt(op_norm_sq(tuple(x-y for x, y in zip(a, b))))


def action(u):
    trace = u[0] + u[3]
    close(trace.imag, 0.0, TOL, "real SU(2) trace")
    return 1 - trace.real/2


def qmul(u, v):
    a, b, c, d = u
    e, f, g, h = v
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def qadj(q):
    return (q[0], -q[1], -q[2], -q[3])


def qmatrix(q):
    a, b, c, d = q
    return (complex(a, b), complex(c, d), complex(-c, d), complex(a, -b))


def sphere(rng, dimension):
    while True:
        v = [rng.gauss(0, 1) for _ in range(dimension)]
        norm = sqrt(fsum(x*x for x in v))
        if norm:
            return tuple(x/norm for x in v)


def haar(rng):
    return qmatrix(sphere(rng, 4))


def cap(rng, rho):
    """Haar restricted to theta <= rho, via rejection against theta^2.

    theta=rho*U^(1/3), acceptance (sin(theta)/theta)^2, uniform S^2 axis.
    This is not uniform in theta and not a chordal-radius cap sampler.
    """
    require(0 <= rho <= 1, "geodesic cap radius must lie in [0,1]")
    if rho == 0:
        return I
    while True:
        theta = rho * rng.random()**(1/3)
        sinc = sin(theta)/theta if theta else 1.0
        if rng.random() <= sinc*sinc:
            axis = sphere(rng, 3)
            return qmatrix((cos(theta), *(sin(theta)*x for x in axis)))


class Lattice:
    def __init__(self, periods):
        if len(periods) != 4 or any(p < 4 for p in periods):
            raise ValueError("four periods >= 4 required")
        self.periods = tuple(periods)
        self.sites = tuple(product(*(range(p) for p in periods)))
        self.links = tuple((x, mu) for x in self.sites for mu in range(4))
        self.plaquettes = tuple((x, mu, nu) for x in self.sites for mu, nu in PAIRS)
        self.support = {p: tuple(e for e, _ in self.boundary(p)) for p in self.plaquettes}
        require(all(len(set(es)) == 4 for es in self.support.values()),
                "a plaquette repeated an independent link")

    def shift(self, x, mu, step=1):
        y = list(x)
        y[mu] = (y[mu] + step) % self.periods[mu]
        return tuple(y)

    def end(self, edge):
        return self.shift(*edge)

    def boundary(self, p):
        x, mu, nu = p
        return (((x, mu), 1), ((self.shift(x, mu), nu), 1),
                ((self.shift(x, nu), mu), -1), ((x, nu), -1))

    def plaquette(self, links, p):
        # Direct matrix formula, independent of the support/incidence counters.
        x, mu, nu = p
        return chain(links[x, mu], links[self.shift(x, mu), nu],
                     adj(links[self.shift(x, nu), mu]), adj(links[x, nu]))

    def incident(self, edge):
        x, mu = edge
        return {(base, min(mu, nu), max(mu, nu))
                for nu in range(4) if nu != mu
                for base in (x, self.shift(x, nu, -1))}

    def counts(self, edited):
        return {p: q for p, es in self.support.items()
                if (q := sum(e in edited for e in es))}

    def walk(self, start, steps):
        x, edges = start, []
        for mu, sign in steps:
            require(sign in (-1, 1), "walk orientation")
            if sign == 1:
                edges.append(((x, mu), 1))
                x = self.shift(x, mu)
            else:
                x = self.shift(x, mu, -1)
                edges.append(((x, mu), -1))
        require(x == start, "test loop must close")
        return tuple(edges)


def holonomy(links, edges):
    result = I
    for edge, sign in edges:
        result = mul(result, links[edge] if sign == 1 else adj(links[edge]))
    return result


def energy(lattice, links, touched):
    return fsum(action(lattice.plaquette(links, p)) for p in touched)


def star(lattice, x):
    return {(base, mu) for mu in range(4)
            for base in (x, lattice.shift(x, mu, -1))}


def fixed_sets(lattice, rng):
    origin = (0, 0, 0, 0)
    seam = tuple(p-1 for p in lattice.periods)
    square = lattice.support[seam, 0, 2]
    cases = [
        ("empty", set()), ("single-seam", {(seam, 3)}),
        ("plaquette-4", set(square)), ("star-8", star(lattice, origin)),
        ("two-stars", star(lattice, origin) | star(lattice, (2, 2, 2, 2))),
        ("winding", {(lattice.shift(origin, 1, k), 1) for k in range(lattice.periods[1])}),
        ("block", {(x, mu) for x in product(range(2), repeat=4) for mu in range(4)}),
        ("sparse-23", set(rng.sample(lattice.links, 23))),
        ("dense", set(rng.sample(lattice.links, 3*len(lattice.links)//4))),
        ("all", set(lattice.links)),
    ]
    cases.extend((f"square-mask-{mask}", {square[i] for i in range(4) if mask & (1 << i)})
                 for mask in range(16))
    return [(name, frozenset(es)) for name, es in cases]


def check_incidence(lattice, cases):
    scanned = {edge: set() for edge in lattice.links}
    for p, edges in lattice.support.items():
        for edge in edges:
            scanned[edge].add(p)
    for edge in lattice.links:
        require(scanned[edge] == lattice.incident(edge) and len(scanned[edge]) == 6,
                f"six-plaquette incidence failed at {edge}")
    seen_q = set()
    for name, edited in cases:
        counts = lattice.counts(edited)
        independent = Counter(p for edge in sorted(edited) for p in sorted(lattice.incident(edge)))
        require(counts == independent, f"independent touched-set enumeration: {name}")
        n = len(edited)
        require(len(counts) <= 6*n, f"|P(J)| <= 6n: {name}")
        require(sum(counts.values()) == 6*n, f"sum q = 6n: {name}")
        require(sum(q*q for q in counts.values()) <= 24*n, f"sum q^2 <= 24n: {name}")
        seen_q.update(counts.values())
        if name == "all":
            require(sum(q*q for q in counts.values()) == 24*n, "dense saturation")
    require(seen_q == {1, 2, 3, 4}, "all four edited multiplicities must be exercised")
    print(f"Incidence {lattice.periods}: all {len(lattice.links)} singleton incidences; "
          f"{len(cases)} fixed J; q=1,2,3,4; |P|<=6n, sum q=6n, sum q^2<=24n; dense equality")


def check_algebra(lattice, rng):
    close(op_norm_sq((0j, 2+0j, 0j, 0j)), 4, 0, "generic singular-value fixture")
    close(op_norm_sq((3+0j, 0j, 0j, 4+0j)), 16, 0, "non-SU(2) norm fixture")
    for u, expected in ((I, 0), (MINUS_I, 2), (qmatrix((0, 1, 0, 0)), 1)):
        close(action(u), expected, 0, "exact central/half-turn action")
        close(op_norm_sq(tuple(a-b for a, b in zip(I, u)))/2,
              expected, 0, "exact central/half-turn norm identity")
    quaternions = {e: sphere(rng, 4) for e in lattice.links}
    links = {e: qmatrix(q) for e, q in quaternions.items()}
    worst_group = worst_hol = worst_action = 0.0
    for u in links.values():
        worst_group = max(worst_group, matrix_error(mul(u, adj(u)), I),
                          abs(u[0]*u[3]-u[1]*u[2]-1))
    loops = [lattice.boundary(p) for p in lattice.plaquettes]
    seam = tuple(p-1 for p in lattice.periods)
    loops.extend(lattice.walk(seam, [(mu, 1)]*lattice.periods[mu]) for mu in range(4))
    loops.append(lattice.walk(seam, [(0, 1)]*2 + [(2, 1)]*3 + [(0, -1)]*2 + [(2, -1)]*3))
    for edges in loops:
        q = QI
        for edge, sign in edges:
            v = quaternions[edge]
            q = qmul(q, v if sign == 1 else qadj(v))
        u = holonomy(links, edges)
        worst_hol = max(worst_hol, matrix_error(u, qmatrix(q)))
        worst_action = max(worst_action, abs(action(u)-(1-q[0])),
                           abs(action(u)-distance(u)**2/2))
    for p in lattice.plaquettes:
        worst_hol = max(worst_hol, matrix_error(lattice.plaquette(links, p),
                                               holonomy(links, lattice.boundary(p))))
    require(max(worst_group, worst_hol, worst_action) < TOL, "SU(2)/quaternion/operator identity")
    print(f"SU(2): {len(loops)} quaternion/matrix loops (including wrapping and reversed edges); "
          f"unitarity/det error={worst_group:.3g}, holonomy error={worst_hol:.3g}, "
          f"s=||I-U||op^2/2 error={worst_action:.3g}")


class Forest:
    """Geometry-only BFS forest of frozen affected links, INCLUDING isolates."""
    def __init__(self, lattice, edited):
        self.lattice = lattice
        self.edited = frozenset(edited)
        require(self.edited <= set(lattice.links), "edited link outside lattice")
        self.counts = lattice.counts(self.edited)
        self.touched = tuple(sorted(self.counts))
        support = {e for p in self.touched for e in lattice.support[p]}
        self.frozen = tuple(sorted(support - self.edited))
        self.vertices = tuple(sorted({v for e in support for v in (e[0], lattice.end(e))}))
        graph = {v: [] for v in self.vertices}
        for e in self.frozen:
            x, y = e[0], lattice.end(e)
            graph[x].append((y, e, 1))
            graph[y].append((x, e, -1))
        self.roots, self.order, self.parent, self.root_of, tree = [], [], {}, {}, set()
        for root in self.vertices:
            if root in self.root_of:
                continue
            self.roots.append(root)
            self.root_of[root] = root
            queue = deque([root])
            while queue:
                parent = queue.popleft()
                for child, edge, sign in sorted(graph[parent]):
                    if child in self.root_of:
                        continue
                    self.root_of[child] = root
                    self.parent[child] = (parent, edge, sign)
                    self.order.append(child)
                    tree.add(edge)
                    queue.append(child)
        self.tree = frozenset(tree)
        require(len(self.tree) == len(self.vertices)-len(self.roots), "forest edge count")

    def frames(self, links, roots):
        require(set(roots) == set(self.roots), "one frame per component, including isolates")
        frames = dict(roots)
        for child in self.order:
            parent, edge, sign = self.parent[child]
            u = adj(links[edge]) if sign == 1 else links[edge]
            frames[child] = mul(u, frames[parent])
        return frames

    def path(self, vertex):
        path = []
        while vertex in self.parent:
            vertex, edge, sign = self.parent[vertex]
            path.append((edge, sign))
        return tuple(reversed(path))

    def residual(self, links, frames):
        return max((distance(chain(adj(frames[e[0]]), links[e], frames[self.lattice.end(e)]))
                    for e in self.frozen), default=0.0)


def framed_link(lattice, frames, edge, noise=I):
    return chain(frames[edge[0]], noise, adj(frames[lattice.end(edge)]))


def replace(forest, links, roots, noise):
    """Kernel realization, defined even for incompatible boundary data.

    Incompatibility prevents the SMALL-energy conclusion, not the kernel's
    definition. This function never silently erases frozen residuals.
    """
    require(set(noise) == forest.edited, "exactly one noise per edited link")
    frames = forest.frames(links, roots)
    output = dict(links)
    for edge in sorted(forest.edited):
        output[edge] = framed_link(forest.lattice, frames, edge, noise[edge])
    return output, frames


def unchanged_outside(before, after, edited):
    require(before.keys() == after.keys(), "replacement changed link keys")
    require(all(before[e] == after[e] for e in before if e not in edited),
            "replacement changed a frozen link outside J")


def compatible_fixture(forest, eta, rng):
    lattice = forest.lattice
    links = {e: haar(rng) for e in lattice.links}
    frames = {x: haar(rng) for x in forest.vertices}
    for edge in forest.frozen:
        residual = I if edge in forest.tree else cap(rng, eta)
        links[edge] = framed_link(lattice, frames, edge, residual)
    roots = {r: haar(rng) for r in forest.roots}
    recovered = forest.frames(links, roots)
    require(forest.residual(links, recovered) <= eta + TOL, "fixture is not forest-compatible")
    return links, roots


def frozen_loops(forest):
    lattice = forest.lattice
    loops = []
    for mu in range(4):
        for start in lattice.sites:
            if start[mu] != 0:
                continue
            edges = lattice.walk(start, [(mu, 1)]*lattice.periods[mu])
            if all(e not in forest.edited for e, _ in edges):
                loops.append((start, edges))
    # Fundamental frozen cycles also test boundary holonomy, not just windings.
    for edge in forest.frozen:
        if edge in forest.tree:
            continue
        left, right = forest.path(edge[0]), forest.path(lattice.end(edge))
        edges = left + ((edge, 1),) + tuple((e, -s) for e, s in reversed(right))
        loops.append((forest.root_of[edge[0]], edges))
    return loops


def check_output(forest, before, after, eta, rho):
    lattice = forest.lattice
    unchanged_outside(before, after, forest.edited)
    worst_ratio = 0.0
    for p in lattice.plaquettes:
        if p not in forest.counts:
            require(lattice.plaquette(before, p) == lattice.plaquette(after, p),
                    "a supposedly unaffected plaquette changed")
            continue
        q = forest.counts[p]
        bound = (4-q)*eta + q*rho
        u = lattice.plaquette(after, p)
        d = distance(u)
        require(d <= bound + TOL, f"curvature bound at {p}, q={q}: {d} > {bound}")
        close(action(u), d*d/2, TOL, "output action/operator-norm identity")
        worst_ratio = max(worst_ratio, d/bound if bound else 0.0)
    value = energy(lattice, after, forest.touched)
    local_bound = fsum(((4-q)*eta+q*rho)**2/2 for q in forest.counts.values())
    require(-ENERGY_TOL <= value <= local_bound + ENERGY_TOL, "sum of local energy bounds")
    count = nontrivial = 0
    for _, edges in frozen_loops(forest):
        old = holonomy(before, edges)
        require(old == holonomy(after, edges), "frozen-loop matrix holonomy changed")
        count += 1
        nontrivial += distance(old) > 1e-3
    if forest.edited and len(forest.edited) < 30:
        require(nontrivial > 0, "locality test must include nontrivial frozen holonomies")
    return value, worst_ratio, count, nontrivial


def check_replacements(lattice, cases, rng):
    selected = {name: Forest(lattice, edited) for name, edited in cases
                if name in {"empty", "single-seam", "plaquette-4", "two-stars", "sparse-23", "all"}}
    require(len(selected["two-stars"].roots) >= 3, "isolate/multiple-root fixture lost")
    loops = nontrivial = runs = 0
    for name, forest in selected.items():
        for h in (16, 1024):
            rho = 1/sqrt(h)
            for flat in (False, True):
                eta = 0.0 if flat else rho
                before, roots = compatible_fixture(forest, eta, rng)
                snapshot = dict(before)
                noise = {e: cap(rng, rho) for e in sorted(forest.edited)}
                require(all(distance(q) <= rho+TOL for q in noise.values()), "cap support")
                after, _ = replace(forest, before, roots, noise)
                require(before == snapshot, "replacement mutated its input")
                value, ratio, count, nt = check_output(forest, before, after, eta, rho)
                bound = (12 if flat else 48)*len(forest.edited)/h
                require(value <= bound + ENERGY_TOL, f"{'12' if flat else '48'}n/H energy bound")
                # Old edited links cannot influence the sampled output.
                altered_input = dict(before)
                for e in sorted(forest.edited):
                    altered_input[e] = MINUS_I
                repeated, _ = replace(forest, altered_input, roots, noise)
                require(after == repeated, "kernel incorrectly depends on original edited links")
                loops += count
                nontrivial += nt
                runs += 1
                print(f"Replacement {name}, H={h}, {'flat' if flat else 'eta=rho'}: "
                      f"n={len(forest.edited)}, roots={len(forest.roots)}, P={len(forest.touched)}, "
                      f"E={value:.8g} <= {bound:.8g}; max d/local_bound={ratio:.6f}")
    # Unequal radii distinguish the coefficients (4-q) and q.
    forest = selected["plaquette-4"]
    for eta, rho in ((0.02, 0.15), (0.15, 0.02), (0.1, 0.0)):
        before, roots = compatible_fixture(forest, eta, rng)
        noise = {e: cap(rng, rho) for e in sorted(forest.edited)}
        after, _ = replace(forest, before, roots, noise)
        value, ratio, count, nt = check_output(forest, before, after, eta, rho)
        loops += count
        nontrivial += nt
        runs += 1
        print(f"Mixed radii eta={eta:g}, rho={rho:g}: E={value:.8g}; max d/local_bound={ratio:.6f}")
    print(f"Locality: {runs} outputs, no changed links outside J, all unaffected plaquettes exact; "
          f"{loops} frozen loops unchanged ({nontrivial} nontrivial); old-J independence checked")
    return selected["two-stars"]


def gauge_transform(lattice, links, gauge):
    return {e: chain(gauge[e[0]], links[e], adj(gauge[lattice.end(e)])) for e in lattice.links}


def check_covariance(forest, rng):
    lattice, eta, rho = forest.lattice, 1/32, 1/8
    links, roots = compatible_fixture(forest, eta, rng)
    noise = {e: cap(rng, rho) for e in sorted(forest.edited)}
    output, frames = replace(forest, links, roots, noise)
    gauge = {x: haar(rng) for x in lattice.sites}
    transformed = gauge_transform(lattice, links, gauge)
    coupled_roots = {r: mul(gauge[r], roots[r]) for r in forest.roots}
    actual, transformed_frames = replace(forest, transformed, coupled_roots, noise)
    expected = gauge_transform(lattice, output, gauge)
    frame_error = max(matrix_error(transformed_frames[x], mul(gauge[x], frames[x]))
                      for x in forest.vertices)
    link_error = max(matrix_error(actual[e], expected[e]) for e in lattice.links)
    residual_error = close(forest.residual(links, frames),
                           forest.residual(transformed, transformed_frames), TOL,
                           "gauge-invariant boundary defect")
    # Also check the canonical h_x with root I: residuals conjugate by g_root.
    h = forest.frames(links, {r: I for r in forest.roots})
    hg = forest.frames(transformed, {r: I for r in forest.roots})
    canonical_error = max(matrix_error(hg[x], chain(gauge[x], h[x], adj(gauge[forest.root_of[x]])))
                          for x in forest.vertices)
    plaque_error = max(matrix_error(lattice.plaquette(actual, p),
                                     chain(gauge[p[0]], lattice.plaquette(output, p), adj(gauge[p[0]])))
                       for p in lattice.plaquettes)
    energy_error = close(energy(lattice, actual, forest.touched),
                         energy(lattice, output, forest.touched), ENERGY_TOL, "covariant energy")
    unchanged_outside(transformed, actual, forest.edited)
    loop_error = max(matrix_error(holonomy(actual, edges),
                                  chain(gauge[start], holonomy(output, edges), adj(gauge[start])))
                     for start, edges in frozen_loops(forest))
    # A COMMON right root-frame rotation is compensated by conjugating cap noise.
    # Independent left/right rotations of a cap are NOT asserted to preserve it.
    c = haar(rng)
    roots_c = {r: mul(roots[r], c) for r in forest.roots}
    noise_c = {e: chain(adj(c), noise[e], c) for e in sorted(noise)}
    cap_error = max(abs(distance(noise[e])-distance(noise_c[e])) for e in noise)
    same, _ = replace(forest, links, roots_c, noise_c)
    common_error = max(matrix_error(same[e], output[e]) for e in lattice.links)
    require(max(frame_error, link_error, canonical_error, plaque_error,
                loop_error, cap_error, common_error) < TOL, "forest/kernel covariance failed")
    wrong, _ = replace(forest, transformed, roots, noise)  # Deliberately omit g_root.
    wrong_error = max(matrix_error(wrong[e], expected[e]) for e in forest.edited)
    require(wrong_error > 1e-3, "forgotten-root-frame negative control was not detected")
    print(f"Forest covariance: {len(forest.roots)} components including isolates; "
          f"frame={frame_error:.3g}, canonical={canonical_error:.3g}, link={link_error:.3g}, "
          f"plaquette={plaque_error:.3g}, frozen-loop={loop_error:.3g}, "
          f"defect={residual_error:.3g}, energy={energy_error:.3g}")
    print(f"Invariant cap coupling: conjugation radius error={cap_error:.3g}, "
          f"common-frame output error={common_error:.3g}; forgotten g_root control={wrong_error:.6g} DETECTED")


def staples(lattice, links, edited_edge, touched):
    """S so that s(U_p)=1-Re Tr(U S)/2, handling inverse occurrences."""
    result = []
    for p in touched:
        boundary = lattice.boundary(p)
        indices = [i for i, (e, _) in enumerate(boundary) if e == edited_edge]
        require(len(indices) == 1, "one-link staple multiplicity")
        i = indices[0]
        rest = holonomy(links, boundary[i+1:] + boundary[:i])
        result.append(rest if boundary[i][1] == 1 else adj(rest))
    return result


def obstruction_samples(rng):
    axes = ((1, 0, 0), (0, 1, 0), (0, 0, 1), tuple(v/sqrt(14) for v in (1, 2, 3)))
    samples = [qmatrix((a, *(sqrt(max(0.0, 1-a*a))*v for v in axis)))
               for k in range(65) for a in (k/32-1,) for axis in axes]
    samples.extend(haar(rng) for _ in range(256))
    return samples


def check_obstruction(lattice, rng):
    origin, edge = (0, 0, 0, 0), ((0, 0, 0, 0), 0)
    forest = Forest(lattice, {edge})
    links = {e: I for e in lattice.links}
    for nu in (1, 2, 3):
        links[lattice.shift(origin, nu, -1), 0] = MINUS_I
    require(len(forest.frozen) == 18, "six internally edge-disjoint three-link staples")
    ss = staples(lattice, links, edge, forest.touched)
    require(ss.count(I) == 3 and ss.count(MINUS_I) == 3, "explicit 3+3 central staples")
    require(tuple(sum(s[i] for s in ss) for i in range(4)) == (0j,)*4, "central staple cancellation")
    samples = obstruction_samples(rng)
    worst_energy, least_large = 0.0, 6
    for u in samples:
        links[edge] = u
        values = [lattice.plaquette(links, p) for p in forest.touched]
        worst_energy = max(worst_energy, abs(fsum(action(v) for v in values)-6))
        large = sum(distance(v) >= sqrt(2)-TOL for v in values)
        least_large = min(least_large, large)
        require(large >= 3, "one-link obstruction lost three sqrt(2) curvatures")
        for p, v, s in zip(forest.touched, values, ss):
            close(action(v), action(mul(u, s)), TOL, f"staple orientation at {p}")
    require(worst_energy < TOL, "conditional obstruction E != 6")
    links[edge] = I
    print(f"One-link star obstruction: actual 18 frozen links, staples +I x3 / -I x3, sum=0; "
          f"{len(samples)} U samples incl +/-I and Tr U=0: E=6 error={worst_energy:.3g}, "
          f"minimum count d>=sqrt(2) is {least_large}")

    roots = {r: I for r in forest.roots}
    frames = forest.frames(links, roots)
    defect = forest.residual(links, frames)
    close(defect, 2, TOL, "incompatible forest defect")
    # The ACTUAL kernel remains defined, but must not pretend the boundary is compatible.
    honest, _ = replace(forest, links, roots, {edge: I})
    close(energy(lattice, honest, forest.touched), 6, TOL, "incompatible kernel still obstructed")
    rejected(lambda: require(defect <= 1/32, "incompatible boundary"), AssertionError,
             "accepting an incompatible boundary as small")
    frozen_loop = lattice.walk(origin, [(1, 1), (0, 1), (1, -1), (1, -1), (0, -1), (1, 1)])
    require(all(e not in forest.edited for e, _ in frozen_loop), "obstruction loop must be frozen")
    require(holonomy(links, frozen_loop) == MINUS_I, "explicit frustrated frozen loop")
    erased = dict(honest)
    for e in forest.frozen:
        erased[e] = framed_link(lattice, frames, e)  # Intentionally illegal projection.
    close(energy(lattice, erased, forest.touched), 0, TOL, "illegal boundary erasure appears flat")
    require(holonomy(erased, frozen_loop) == I, "erasure changed the frozen loop")
    rejected(lambda: unchanged_outside(links, erased, forest.edited), AssertionError,
             "erasing incompatible frozen boundary")
    outside_edits = sum(links[e] != erased[e] for e in lattice.links if e not in forest.edited)
    print(f"Negative control DETECTED: erasing incompatible boundary (eta_J={defect:g}) "
          f"fakes E=0 by editing {outside_edits} links OUTSIDE J; frozen-loop trace -2 -> +2")
    forgotten = tuple(p for p in forest.touched if p[0] == origin)
    require(len(forgotten) == 3, "wrong touched-set fixture")
    close(energy(lattice, links, forgotten), 0, 0, "wrong outgoing-only energy")
    close(energy(lattice, links, forest.touched), 6, 0, "true all-affected energy")
    rejected(lambda: require(set(forgotten) == set(forest.touched), "missing affected plaquettes"),
             AssertionError, "forgetting backward/seam affected plaquettes")
    print("Negative control DETECTED: counting only three outgoing plaquettes fakes E=0; "
          "all six affected plaquettes give E=6 (three backward/seam plaquettes omitted)")

    # Perturb ALL 18 frozen star links. Each link distance <= eps; the numerical
    # envelopes tested are staple distance <= 3eps, E >= 6-18eps, and at least
    # three curvatures >= sqrt(2)-3eps. Universal/open-set reasoning is in the parent.
    eps, trials = 1/64, 8
    min_energy, min_third, max_staple_shift, max_amplitude = 6.0, 2.0, 0.0, 0.0
    for trial in range(trials):
        perturbed = dict(links)
        for e in forest.frozen:
            perturbed[e] = mul(links[e], cap(rng, eps))
            require(distance(perturbed[e], links[e]) <= eps+TOL, "exterior perturbation radius")
        new_staples = staples(lattice, perturbed, edge, forest.touched)
        shift = max(distance(a, b) for a, b in zip(new_staples, ss))
        require(shift <= 3*eps+TOL, "three-link staple perturbation envelope")
        max_staple_shift = max(max_staple_shift, shift)
        total = tuple(sum(s[i] for s in new_staples) for i in range(4))
        amplitude = sqrt(op_norm_sq(total))
        max_amplitude = max(max_amplitude, amplitude)
        # Include the extremizing quaternion of the linear one-link action;
        # do not rely just on random U missing its worst direction.
        qtotal = ((total[0].real+total[3].real)/2, (total[0].imag-total[3].imag)/2,
                  (total[1].real-total[2].real)/2, (total[1].imag+total[2].imag)/2)
        require(matrix_error(qmatrix(qtotal), total) < TOL, "staple sum quaternion structure")
        require(amplitude > 1e-6, "perturbation must be nonconstant, not still central cancellation")
        minimizer = qmatrix(tuple(v/amplitude for v in qadj(qtotal)))
        perturbed[edge] = minimizer
        exact_min_sample = energy(lattice, perturbed, forest.touched)
        close(exact_min_sample, 6-amplitude, TOL, "one-link minimizing-direction diagnostic")
        require(amplitude <= 18*eps+TOL, "uniform one-link energy envelope")
        for u in samples + [minimizer, tuple(-v for v in minimizer)]:
            perturbed[edge] = u
            values = [lattice.plaquette(perturbed, p) for p in forest.touched]
            value = fsum(action(v) for v in values)
            third = sorted((distance(v) for v in values), reverse=True)[2]
            require(abs(value-6) <= 18*eps+TOL, f"robust energy envelope, trial {trial}")
            require(third >= sqrt(2)-3*eps-TOL, f"robust three-curvature envelope, trial {trial}")
            min_energy = min(min_energy, value)
            min_third = min(min_third, third)
    print(f"Open-obstruction diagnostic: {trials} noncentral perturbations of all 18 frozen links, "
          f"eps={eps:g}; max staple shift={max_staple_shift:.6g} <= {3*eps:g}")
    print(f"  Including minimizing/maximizing U: minimum E={min_energy:.8g} >= {6-18*eps:g}; "
          f"minimum third-largest curvature={min_third:.8g} >= {sqrt(2)-3*eps:.8g}; "
          f"nonconstant staple amplitude up to {max_amplitude:.6g}")


def check_cap_volume():
    """Optional, small quadrature diagnostic; no certified integration bound."""
    def quadrature(rho, panels):
        # Rescale theta=rho*t; stable even when rho is tiny.
        def value(i):
            theta = rho*i/panels
            sinc = sin(theta)/theta if theta else 1.0
            return (i/panels)**2 * sinc*sinc
        terms = [(1 if i in (0, panels) else (4 if i % 2 else 2))*value(i)
                 for i in range(panels+1)]
        return (2/pi)*rho**3*fsum(terms)/(3*panels)
    least_ratio, worst_grid = float("inf"), 0.0
    for rho in (1e-6, 0.001, 0.03125, 0.125, 0.5, 1.0):
        fine, coarse = quadrature(rho, 2048), quadrature(rho, 1024)
        require(fine >= rho**3/24, "sampled geodesic cap-volume lower bound")
        least_ratio = min(least_ratio, fine/(rho**3/24))
        worst_grid = max(worst_grid, abs(fine-coarse))
        if rho >= 0.03125:
            close(fine, (rho-sin(rho)*cos(rho))/pi, 2e-13, "cap closed-form quadrature")
    print(f"Cap-volume diagnostic ONLY: 6 geodesic radii in [1e-6,1], Simpson 1024/2048; "
          f"min b(rho)/(rho^3/24)={least_ratio:.8g}, grid difference={worst_grid:.3g}; NOT a proof")


def main():
    print("SU(2) rough-link replacement: bounded independent standard-library diagnostics")
    print(f"Python {sys.version.split()[0]}; seed={SEED}; streams seed+[0,1,2,3,4]; grids={GRIDS}")
    print("WARNING: finite tests are DIAGNOSTICS, NOT PROOFS; analytic 'every J/U/output' belongs to parent.")
    print("E=sum over ALL touched plaquettes; caps theta<=rho (geodesic); no density, continuum, or mass-gap claim.")
    for bad in ((3, 4, 4, 4), (4, 4, 4)):
        rejected(lambda b=bad: Lattice(b), ValueError, "period/domain guard")
    geometry_rng = random.Random(SEED)
    lattices = [Lattice(periods) for periods in GRIDS]
    cases = [fixed_sets(lattice, geometry_rng) for lattice in lattices]
    for lattice, sets in zip(lattices, cases):
        check_incidence(lattice, sets)
    check_algebra(lattices[0], random.Random(SEED+1))
    forest = check_replacements(lattices[1], cases[1], random.Random(SEED+2))
    check_covariance(forest, random.Random(SEED+3))
    check_obstruction(lattices[0], random.Random(SEED+4))
    check_cap_volume()
    print("ALL REPLACEMENT DIAGNOSTICS PASSED. Optional finite-difference Hessian omitted; no proof or mass-gap claim.")


if __name__ == "__main__":
    main()
