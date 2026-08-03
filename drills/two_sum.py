"""LeetCode Easy #1 — Two Sum (narrated for interview practice).

Problem: given a list of ints `nums` and an int `target`, return the indices of
the two numbers that add up to `target`. Exactly one solution exists and you may
not reuse the same element.

Say this out loud in the interview:
  "I keep a hash map of value -> index as I scan once. For each number I check
   whether its complement (target - num) is already in the map. If so I've found
   the pair; otherwise I store the current number. One O(n) pass, O(n) space —
   beating the O(n^2) brute-force double loop."
"""

from __future__ import annotations

from typing import Dict, List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen: Dict[int, int] = {}              # value -> index seen so far
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []                              # problem guarantees a pair; safety net
