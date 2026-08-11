# Monitor: Site Evaluation

Shipped 2026-07-20.
DB: `mysql` MCP, read replica. Logs: `aws` CLI, log group `/ecs/site-eval`.

## How it works

A 5-step pipeline evaluating publisher sites. Rows in `site_evaluations` carry
`status` (pending, running, complete, failed) and a `step` counter 1-5. The
worker logs to the `site-eval` service. Normally 200-400/day, ~90s each.

## Checks

### 1. Stuck evaluations
```sql
SELECT id, site_id, step, updated_at FROM site_evaluations
WHERE status = 'running' AND updated_at < now() - interval 30 minute
ORDER BY updated_at LIMIT 50;
```
Normal: 0-2 rows. Above 5 means the worker is wedged or a step hangs.

### 2. Failure rate by step
```sql
SELECT step, count(*) AS total, sum(status = 'failed') AS failed
FROM site_evaluations WHERE created_at > now() - interval 24 hour
GROUP BY step ORDER BY step;
```
Normal: under 5% overall; step 3 (external fetch) runs hottest at ~8%. A step
rising above its own usual rate is the signal, not the absolute number.

### 3. Worker errors
```logql
{service="site-eval"} |= "level=error" | json
```
Last 24h. Normal: step 3 timeouts, a handful per hour. Anything with a stack
trace, or an error string not already in the log below, is new.

### 4. Throughput
```sql
SELECT count(*) AS evaluations FROM site_evaluations
WHERE created_at > now() - interval 24 hour;
```
Normal: 200-400. Near zero means nothing is being enqueued — worse than
errors, because it's silent.

### 5. Time to complete
```sql
SELECT count(*) AS n,
       avg(timestampdiff(second, created_at, updated_at)) AS avg_s,
       max(timestampdiff(second, created_at, updated_at)) AS max_s
FROM site_evaluations
WHERE status = 'complete' AND updated_at > now() - interval 24 hour;
```
Normal: ~90s average, tail under 10 minutes. Report a shift in the shape, not
only a breach — a step creeping up is what becomes a timeout next month.

## Log

### 2026-07-20 — created
Checks 1-5 verified against production; normal ranges are observed values.
