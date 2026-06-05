#!/usr/bin/env python3
"""Compute an ObservePoint value summary (customer-side value; never OP pricing).

Reads JSON from stdin with optional keys: incidents_caught, avg_incident_cost,
manual_qa_hours_saved, hourly_rate, wasted_adspend_reduced. Prints a structured
value summary. This frames VALUE, not cost; it never quotes ObservePoint pricing.
"""
import json
import sys


def main():
    data = json.loads(sys.stdin.read() or "{}")
    incidents = data.get("incidents_caught", 0) * data.get("avg_incident_cost", 0)
    qa = data.get("manual_qa_hours_saved", 0) * data.get("hourly_rate", 0)
    adspend = data.get("wasted_adspend_reduced", 0)
    categories = {
        "incident_avoidance": incidents,
        "qa_efficiency": qa,
        "adspend_efficiency": adspend,
    }
    out = {
        "categories": categories,
        "total_estimated_value": sum(categories.values()),
        "disclaimer": "Value framing only — this never quotes ObservePoint pricing. Direct pricing questions to the account team.",
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
