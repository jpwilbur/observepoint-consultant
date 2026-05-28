# REST API reference

A working reference for the ObservePoint REST API: authentication, the v3 endpoints you'll use most, common recipes, and how to wire it into CI/CD. Load this file whenever the user asks to write a Rule, hit the API, run an audit on demand, export a report, or integrate ObservePoint into a release pipeline.

## Versions & current state

ObservePoint exposes two API versions:

| Version | Status | Use it when |
|---|---|---|
| **v3** | Fully supported, recommended | All new integrations. Better pagination, filtering, and the most recent endpoints. |
| **v2** | Fully supported, no deprecation announced | Only if you need a specific endpoint that v3 hasn't covered yet. |

There is no v1. No deprecation timeline has been announced for either version, but assume new features will land in v3 first.

## Base URL & auth

```
Base URL:       https://api.observepoint.com
Auth method:    API key sent in the Authorization header
Auth header:    Authorization: api_key <YOUR_API_KEY>
Key source:     User profile in the ObservePoint app
Content type:   application/json
```

API access is included with every ObservePoint subscription at no extra cost.

Interactive Swagger docs live at https://api.observepoint.com/swagger-ui/index.html and the formal reference at https://api-docs.observepoint.com/.

## Rate limits

ObservePoint applies rate limits but does not publish the exact numbers. Treat the API as "generous for normal use, contact sales for high-volume." Build retry-with-backoff into any automation you wire up.

A pragmatic client policy:

- Retry on `429 Too Many Requests` and `5xx` with exponential backoff (1s, 2s, 4s, 8s, 16s, then give up).
- Cap concurrent requests at 5 unless you've coordinated with ObservePoint sales/support.
- Cache GETs locally when polling — re-fetching the same audit definition every second is wasteful.

## Endpoint cheat-sheet

| Domain | Common v3 endpoints |
|---|---|
| Web Audits | `GET /v3/web-audits`, `POST /v3/web-audits`, `POST /v3/web-audits/{id}/runs` |
| Audit runs | `GET /v3/web-audits/{id}/runs`, `GET /v3/web-audits/{id}/runs/{runId}` |
| Reports | `GET /v3/web-audits/{id}/runs/{runId}/reports/page-summary/pages` |
| Journeys | `GET /v3/web-journeys`, `POST /v3/web-journeys/{id}/runs` |
| Rules | `GET /v3/rules`, `POST /v3/rules`, `PATCH /v3/rules/{id}`, `DELETE /v3/rules/{id}` |
| Alerts | `GET /v3/alerts` |
| HAR processing | See "Recipe: Process a HAR file" below |
| Webhooks | See "Webhooks" section |

When a user asks for an endpoint not listed here, point them at https://api-docs.observepoint.com/sections/v3-index rather than inventing one.

## Recipe: trigger an audit from the command line

The most common automation: kick off a scheduled audit immediately, then wait for it to finish.

```bash
# Start a new run of an existing audit
curl -s -X POST \
  -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs" \
  -d '{}'
# Response includes a runId you'll use for polling.
```

Polling for completion:

```bash
RUN_ID=12345
while true; do
  STATUS=$(curl -s \
    -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
    "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs/${RUN_ID}" \
    | jq -r .status)
  echo "status: $STATUS"
  [[ "$STATUS" == "COMPLETED" || "$STATUS" == "FAILED" ]] && break
  sleep 30
done
```

Same in Python with `httpx` and exponential backoff baked in:

```python
import os, time, httpx

API = "https://api.observepoint.com"
HEADERS = {"Authorization": f"api_key {os.environ['OBSERVEPOINT_API_KEY']}"}

def start_audit_run(audit_id: int) -> int:
    r = httpx.post(f"{API}/v3/web-audits/{audit_id}/runs", headers=HEADERS, json={})
    r.raise_for_status()
    return r.json()["runId"]

def wait_for_run(audit_id: int, run_id: int, poll_seconds: int = 30) -> dict:
    delay = poll_seconds
    while True:
        r = httpx.get(f"{API}/v3/web-audits/{audit_id}/runs/{run_id}", headers=HEADERS)
        if r.status_code in (429, 502, 503, 504):
            time.sleep(min(delay, 60))
            delay *= 2
            continue
        r.raise_for_status()
        body = r.json()
        if body["status"] in ("COMPLETED", "FAILED"):
            return body
        time.sleep(poll_seconds)
```

## Recipe: pull the Page Summary report for a run

Once a run completes, fetch the per-page results:

```bash
curl -s \
  -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
  "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs/${RUN_ID}/reports/page-summary/pages?size=200&page=0"
```

Pagination is via `size` (max varies; 200 is safe) and `page` (zero-indexed). Iterate until the response page count is short of `size`.

Other reports follow the same shape, swapping `/reports/page-summary/pages` for `/reports/tag-variable-rules`, `/reports/cookies-privacy-compliance`, etc.

## Recipe: create a Tag & Variable Rule

Rules can be created in-app, but the API is what you use for change control or bulk provisioning.

```python
rule = {
  "name": "GA4 purchase event has numeric value",
  "description": "Ensure ecommerce.value is populated on purchase events.",
  "conditions": [
    {"variable": "tag.name", "operator": "equals", "value": "Google Analytics 4"},
    {"variable": "event_name", "operator": "equals", "value": "purchase"}
  ],
  "expectations": [
    {"variable": "ecommerce.value", "operator": "is_numeric"},
    {"variable": "ecommerce.value", "operator": "greater_than", "value": "0"}
  ]
}

r = httpx.post(f"{API}/v3/rules", headers=HEADERS, json=rule)
r.raise_for_status()
rule_id = r.json()["id"]
```

The exact field names (`conditions`, `expectations`, operator strings) vary between API versions — confirm against the live Swagger before writing production code. The shape above matches the v3 pattern as documented.

PATCH a rule to update; DELETE to remove. Listing rules supports filtering by name and assigned-audit.

## Recipe: process a HAR file

Upload a HAR file and run your existing rules against it.

```bash
curl -s -X POST \
  -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
  -F "har=@./capture.har" \
  -F "ruleIds=101,102,103" \
  "https://api.observepoint.com/v3/har-analyzer/process"
```

The response contains a job ID you can poll the same way as an audit run. See https://api-docs.observepoint.com/sections/api-recipes/har-file-processing for the canonical version.

## Recipe: CI/CD gate with GitHub Actions

A reusable workflow: on every push to `main`, run a specific audit, fail the build if any Rule failed.

```yaml
name: ObservePoint audit gate

on:
  push:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    env:
      OBSERVEPOINT_API_KEY: ${{ secrets.OBSERVEPOINT_API_KEY }}
      AUDIT_ID: ${{ vars.OBSERVEPOINT_AUDIT_ID }}
    steps:
      - name: Trigger and wait
        run: |
          RUN_ID=$(curl -fsS -X POST \
            -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs" \
            -d '{}' | jq -r .runId)
          echo "Started run $RUN_ID"
          while true; do
            STATUS=$(curl -fsS \
              -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
              "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs/${RUN_ID}" \
              | jq -r .status)
            echo "status: $STATUS"
            [[ "$STATUS" == "COMPLETED" || "$STATUS" == "FAILED" ]] && break
            sleep 30
          done
          [[ "$STATUS" == "COMPLETED" ]] || exit 1
      - name: Fail on rule violations
        run: |
          FAILS=$(curl -fsS \
            -H "Authorization: api_key $OBSERVEPOINT_API_KEY" \
            "https://api.observepoint.com/v3/web-audits/${AUDIT_ID}/runs/${RUN_ID}/reports/tag-variable-rules?status=failed&size=1" \
            | jq '.totalElements // 0')
          echo "Failed rules: $FAILS"
          [[ "$FAILS" == "0" ]] || exit 1
```

The same pattern works on Jenkins, GitLab CI, Azure DevOps, Bamboo, and Circle CI — anywhere you can run shell commands and `jq`.

## Webhooks

ObservePoint can POST to a URL of your choice when an audit run finishes. Configure webhooks in the app or via the API; the body identifies the audit, the run, and the run status. Use webhooks instead of polling when you can — they cut API calls and latency.

If your webhook receiver is in a private network, ObservePoint supports VPN/whitelisting; coordinate with their support team.

## Error handling

Errors come back as JSON with a status code and a message. Common ones:

| Code | Meaning | What to do |
|---|---|---|
| 400 | Bad request body or query | Validate against Swagger; check field names. |
| 401 | Missing or invalid API key | Confirm the `api_key` prefix in the `Authorization` header. |
| 403 | Authenticated but lacks permission | Different roles see different audits; talk to your admin. |
| 404 | Audit or run not found | Double-check IDs; v2-to-v3 IDs are not interchangeable. |
| 409 | Conflict (e.g., starting a run while one is already running) | Wait, then retry. |
| 429 | Rate limited | Back off with exponential delay; cap concurrency. |
| 5xx | ObservePoint-side issue | Retry with backoff; if persistent, [status page](https://status.observepoint.com/) or support. |

Always read the response body on errors — the message field usually tells you exactly which field was wrong.

## Things the API will NOT do

- Run a Web Audit against a site behind an IP-restricted firewall without first whitelisting ObservePoint's egress IPs.
- Test a native mobile app. (HAR upload is the only path. See `references/limitations.md`.)
- Execute server-side tags. (Same: client-side requests only.)
- Discover API keys for you — they live in the user profile, not the admin API.

## Picking up MCP later

When the ObservePoint MCP server reaches GA and exposes tools named `mcp__observepoint__*`, prefer those over raw REST for the same operations. The REST recipes here remain valid as the fallback and as the contract the MCP server wraps. See `references/mcp-tools.md`.

---

*Last verified: 2026-05-28*
