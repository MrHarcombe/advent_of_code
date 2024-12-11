def build_combinations(k, n):
  assert n > k > 1
  to_process = [[i] for i in range(1, n+1)]
  while to_process:
      l = to_process.pop()
      s = sum(l)
      le = len(l)
      # There are three main variations you can use for the loop, from here.
      # To distinguish permutations: range(1, n - s + 1)
      # To avoid repeated cases    : range(l[-1], n - s + 1)
      # Or to number repetitions   : range(l[-1] + 1, n - s + 1)
      for i in range(l[-1], n-s+1):
          news = s + i
          if news <= n:
              newl = list(l)
              newl.append(i)
              if le == k-1 and news == n:
                  yield tuple(newl)
              elif le <= k-2 and news < n:
                  to_process.append(newl)

def manhattan_distance(p1, p2):
  return sum(abs(pa - pb) for pa, pb in zip(p1, p2))
