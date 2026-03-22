#!/usr/bin/env python3
"""
Enumerate and verify all 760 generalizable Claude-like decompositions from
Don Knuth's "Claude's Cycles" (Feb/Mar 2026), then test whether the exact
cyclic chirality split

    {0, -3, -3m(m-1)}

holds for every decomposition (up to permutation of the three cycles).

What this script does
---------------------
1. Enumerates all 11,502 Hamiltonian cycles of the m=3 digraph.
2. Filters the 996 cycles that generalize to Hamiltonian cycles for m=5 and m=7.
   By Knuth's theorem, those are exactly the cycles that generalize to all odd m>1.
3. Solves the exact-cover problem on the 81 directed arcs to recover all 760
   valid Claude-like decompositions.
4. Optionally verifies the cyclic chirality multiset for every decomposition on
   one or more odd m values.

Notes
-----
* Cyclic chirality is startpoint-independent: it includes the wrap-around
  transition from the last direction back to the first.
* Linearized chirality is NOT used here, because it depends on where you choose
  to print the cycle.
* The decomposition count 760 is for unordered triples of cycles.

Typical usage
-------------
    python enumerate_760_claude_like_decompositions.py
    python enumerate_760_claude_like_decompositions.py --test-ms 3,5,7,9,11
    python enumerate_760_claude_like_decompositions.py --skip-chirality-check
    python enumerate_760_claude_like_decompositions.py --write-json results.json

Expected core counts
--------------------
Hamiltonian cycles on m=3 graph:         11502
Generalizable cycles (m=5 and m=7 pass):   996
Generalizable Claude-like decompositions:   760
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


# ============================================================
# Basic graph data for m = 3
# ============================================================

M3 = 3
VERTS3: List[Tuple[int, int, int]] = [
    (i, j, k) for i in range(M3) for j in range(M3) for k in range(M3)
]
IDX3: Dict[Tuple[int, int, int], int] = {v: n for n, v in enumerate(VERTS3)}
N3 = len(VERTS3)
ALL3_MASK = (1 << N3) - 1
START3 = IDX3[(0, 0, 0)]

OUT3: List[List[int]] = [[] for _ in range(N3)]
IN3: List[List[int]] = [[] for _ in range(N3)]
for i, j, k in VERTS3:
    v = IDX3[(i, j, k)]
    nbrs = [
        IDX3[((i + 1) % 3, j, k)],
        IDX3[(i, (j + 1) % 3, k)],
        IDX3[(i, j, (k + 1) % 3)],
    ]
    OUT3[v] = nbrs
for v in range(N3):
    for w in OUT3[v]:
        IN3[w].append(v)


def bar(x: int, m: int) -> int:
    """Collapse an m-coordinate to the {0,1,2} alphabet used by Knuth.

    0       -> 0
    m-1     -> 2
    other   -> 1
    """
    if x == 0:
        return 0
    if x == m - 1:
        return 2
    return 1


# ============================================================
# Hamiltonian cycle enumeration on the m = 3 graph
# ============================================================


def enumerate_hamiltonian_cycles_m3() -> List[Tuple[int, ...]]:
    """Enumerate all Hamiltonian cycles of the m=3 digraph, rooted at 000.

    Each returned cycle is a tuple of vertex-indices of length 28, with the
    first and last entry both equal to START3. Because every Hamiltonian cycle
    visits 000 exactly once, fixing the first vertex at 000 removes rotational
    duplicates.
    """
    sys.setrecursionlimit(10000)
    path: List[int] = [START3]
    cycles: List[Tuple[int, ...]] = []

    def dfs(v: int, visited_mask: int) -> None:
        if visited_mask == ALL3_MASK:
            if START3 in OUT3[v]:
                cycles.append(tuple(path + [START3]))
            return

        # Cheap but strong necessary-condition pruning.
        remaining = ALL3_MASK ^ visited_mask
        u = 0
        mm = remaining
        while mm:
            if mm & 1:
                # Some future outgoing edge must still be available.
                ok_out = False
                for w in OUT3[u]:
                    if w == START3 or not ((visited_mask >> w) & 1):
                        ok_out = True
                        break
                if not ok_out:
                    return

                # Some future incoming edge must still be available.
                ok_in = False
                for p in IN3[u]:
                    if p == v or not ((visited_mask >> p) & 1):
                        ok_in = True
                        break
                if not ok_in:
                    return
            mm >>= 1
            u += 1

        # Warnsdorff-style ordering: visit the tightest next vertex first.
        moves = [w for w in OUT3[v] if not ((visited_mask >> w) & 1)]
        moves.sort(key=lambda w: sum(1 for z in OUT3[w] if not ((visited_mask >> z) & 1)))

        for w in moves:
            path.append(w)
            dfs(w, visited_mask | (1 << w))
            path.pop()

    dfs(START3, 1 << START3)
    return cycles


# ============================================================
# Rule tables and generalization to odd m
# ============================================================

Rule = Tuple[int, ...]  # length 27, one direction per m=3 vertex/state


def rule_from_cycle_m3(cycle: Sequence[int]) -> Rule:
    """Convert an m=3 Hamiltonian cycle into the 27-state rule table."""
    rule = [None] * 27
    for a, b in zip(cycle[:-1], cycle[1:]):
        va = VERTS3[a]
        vb = VERTS3[b]
        di = (vb[0] - va[0]) % 3
        dj = (vb[1] - va[1]) % 3
        dk = (vb[2] - va[2]) % 3
        direction = 0 if di == 1 else 1 if dj == 1 else 2
        rule[a] = direction
    assert all(x is not None for x in rule)
    return tuple(rule)  # type: ignore[arg-type]


@dataclass(frozen=True)
class GeneralizedCycle:
    m: int
    cycle: Tuple[Tuple[int, int, int], ...]  # closed, so first = last
    directions: Tuple[int, ...]              # one per step, includes final edge



def generalize_cycle(rule: Rule, m: int) -> GeneralizedCycle | None:
    """Generalize an m=3 rule table to odd m using Knuth's bar-map recipe.

    Returns None if the generalized walk is not Hamiltonian.
    """
    if m % 2 == 0 or m < 3:
        raise ValueError("m must be odd and >= 3")

    I = J = K = 0
    cycle: List[Tuple[int, int, int]] = []
    directions: List[int] = []
    seen = set()

    for t in range(m ** 3 + 1):
        cycle.append((I, J, K))
        if t == m ** 3:
            break
        if (I, J, K) in seen:
            return None
        seen.add((I, J, K))

        i = bar(I, m)
        j = bar(J, m)
        s = bar((I + J + K) % m, m)
        k = (s - i - j) % 3
        direction = rule[IDX3[(i, j, k)]]
        directions.append(direction)

        if direction == 0:
            I = (I + 1) % m
        elif direction == 1:
            J = (J + 1) % m
        else:
            K = (K + 1) % m

    if cycle[0] != cycle[-1]:
        return None
    if len(set(cycle[:-1])) != m ** 3:
        return None

    return GeneralizedCycle(m=m, cycle=tuple(cycle), directions=tuple(directions))


# ============================================================
# Chirality
# ============================================================


def cyclic_chirality_from_directions(directions: Sequence[int]) -> int:
    """Return CW - CCW, counting the final transition back to the first."""
    n = len(directions)
    cw = 0
    ccw = 0
    for t in range(n):
        d1 = directions[t]
        d2 = directions[(t + 1) % n]
        if d1 == d2:
            continue
        if (d2 - d1) % 3 == 1:
            cw += 1
        else:
            ccw += 1
    return cw - ccw


# ============================================================
# Exact cover on the 81 arcs
# ============================================================


def arc_columns_for_rule(rule: Rule) -> Tuple[int, ...]:
    """Represent the cycle's 27 chosen m=3 arcs as columns 0..80.

    Column 3*v + d corresponds to: at m=3 vertex v, take direction d.
    """
    return tuple(sorted(3 * v + rule[v] for v in range(27)))



def exact_cover_solutions(rows: List[Tuple[int, ...]], ncols: int = 81) -> List[Tuple[int, int, int]]:
    """Algorithm X specialized to this 3-row exact-cover instance."""
    col_to_rows: Dict[int, List[int]] = defaultdict(list)
    for r, row in enumerate(rows):
        for c in row:
            col_to_rows[c].append(r)

    used = [False] * len(rows)
    solutions: List[Tuple[int, int, int]] = []

    def search(covered: set[int], chosen: List[int]) -> None:
        if len(covered) == ncols:
            solutions.append(tuple(sorted(chosen)))
            return

        uncovered_col = min(
            (c for c in range(ncols) if c not in covered),
            key=lambda c: sum(1 for r in col_to_rows[c] if not used[r]),
        )

        for r in col_to_rows[uncovered_col]:
            if used[r]:
                continue
            row = rows[r]
            if any(c in covered for c in row):
                continue
            used[r] = True
            chosen.append(r)
            search(covered.union(row), chosen)
            chosen.pop()
            used[r] = False

    search(set(), [])
    return solutions


# ============================================================
# Main verification pipeline
# ============================================================


def parse_ms(text: str) -> List[int]:
    vals = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = int(chunk)
        if m < 3 or m % 2 == 0:
            raise argparse.ArgumentTypeError(f"m must be odd and >= 3: {m}")
        vals.append(m)
    return vals


@dataclass
class Summary:
    hamiltonian_m3: int
    generalizable_cycles: int
    decompositions: int
    chirality_holds_for_all: bool | None
    tested_ms: List[int]



def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--test-ms",
        type=parse_ms,
        default=[3, 5, 7],
        help="Odd m values used when checking chirality across all 760 decompositions (default: 3,5,7)",
    )
    ap.add_argument(
        "--skip-chirality-check",
        action="store_true",
        help="Stop after enumerating the 760 decompositions.",
    )
    ap.add_argument(
        "--write-json",
        default="",
        help="Optional path for a JSON summary/output dump.",
    )
    args = ap.parse_args()

    t0 = time.time()
    print("[1/5] Enumerating all Hamiltonian cycles on the m=3 digraph...")
    cycles_m3 = enumerate_hamiltonian_cycles_m3()
    print(f"      Found {len(cycles_m3)} cycles (expected 11502).")

    print("[2/5] Filtering generalizable cycles via m=5 and m=7...")
    generalizable_rules: List[Rule] = []
    for cyc in cycles_m3:
        rule = rule_from_cycle_m3(cyc)
        if generalize_cycle(rule, 5) is not None and generalize_cycle(rule, 7) is not None:
            generalizable_rules.append(rule)
    # Deduplicate just in case (it should already be unique)
    generalizable_rules = list(dict.fromkeys(generalizable_rules))
    print(f"      Found {len(generalizable_rules)} generalizable cycles (expected 996).")

    print("[3/5] Solving the exact-cover problem on the 81 directed arcs...")
    rows = [arc_columns_for_rule(rule) for rule in generalizable_rules]
    decompositions = exact_cover_solutions(rows, ncols=81)
    print(f"      Found {len(decompositions)} decompositions (expected 760).")

    chirality_ok: bool | None = None
    bad_examples = []

    if args.skip_chirality_check:
        print("[4/5] Chirality check skipped.")
    else:
        print(f"[4/5] Checking cyclic chirality on all decompositions for m = {args.test_ms} ...")
        chirality_ok = True
        for m in args.test_ms:
            target = sorted([0, -3, -3 * m * (m - 1)])
            for dec in decompositions:
                chis = []
                for ridx in dec:
                    gc = generalize_cycle(generalizable_rules[ridx], m)
                    if gc is None:
                        chirality_ok = False
                        bad_examples.append({
                            "m": m,
                            "decomposition": dec,
                            "reason": "generalization failed unexpectedly",
                        })
                        break
                    chis.append(cyclic_chirality_from_directions(gc.directions))
                if chis and sorted(chis) != target:
                    chirality_ok = False
                    bad_examples.append({
                        "m": m,
                        "decomposition": dec,
                        "found": sorted(chis),
                        "expected": target,
                    })
                    break
            if bad_examples:
                break
        if chirality_ok:
            print("      Chirality split verified for every tested decomposition and every tested m.")
        else:
            print("      Chirality split FAILED for at least one tested case.")
            print("      First counterexample:")
            print(json.dumps(bad_examples[0], indent=2))

    elapsed = time.time() - t0
    print("[5/5] Done.")
    print()
    print("Summary")
    print("-------")
    print(f"Hamiltonian cycles on m=3 graph: {len(cycles_m3)}")
    print(f"Generalizable cycles:           {len(generalizable_rules)}")
    print(f"Decompositions:                 {len(decompositions)}")
    if chirality_ok is not None:
        print(f"Chirality check passed:         {chirality_ok}")
    print(f"Elapsed time:                   {elapsed:.2f} s")

    if args.write_json:
        payload = {
            "summary": {
                "hamiltonian_m3": len(cycles_m3),
                "generalizable_cycles": len(generalizable_rules),
                "decompositions": len(decompositions),
                "chirality_holds_for_all": chirality_ok,
                "tested_ms": args.test_ms,
                "elapsed_seconds": elapsed,
            },
            "bad_examples": bad_examples,
            "decompositions": [list(dec) for dec in decompositions],
        }
        with open(args.write_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote JSON report to: {args.write_json}")


if __name__ == "__main__":
    main()
