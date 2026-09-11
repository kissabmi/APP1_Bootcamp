n, m = map(int, input().split())
g = [list(map(int, input().split())) for _ in range(n)]

dp = [[0] * m for _ in range(n)]
dp[0][0] = g[0][0]

for i in range(1, n):
    dp[i][0] = dp[i - 1][0] + g[i][0]

for j in range(1, m):
    dp[0][j] = dp[0][j - 1] + g[0][j]

for i in range(1, n):
    for j in range(1, m):
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + g[i][j]

print(dp[n - 1][m - 1])
