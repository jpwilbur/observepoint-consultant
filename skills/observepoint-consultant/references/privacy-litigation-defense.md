# Privacy litigation defense — technical evidence for tort claims

> **Important framing.** This file is technical evidence guidance, not legal advice. ObservePoint produces audit data; lawyers decide what that data means for a specific claim. The statutes covered here drive active class-action waves with substantial damages exposure — when a customer receives a demand letter or class-action filing, the right next step is coordinating with their counsel, not relying on this file in isolation.

Load this file when a user describes a litigation scenario rather than a compliance-program scenario. Different audience (in-house counsel, litigation-support engineers), different use pattern (responding to a complaint, preparing for discovery), different evidence shape (proof of reasonable controls + change history, not ongoing compliance attestation).

## Contents

- [How to use this file](#how-to-use-this-file)
- [CIPA — California Invasion of Privacy Act](#cipa--california-invasion-of-privacy-act)
- [VPPA — Video Privacy Protection Act](#vppa--video-privacy-protection-act)
- [BIPA — Illinois Biometric Information Privacy Act](#bipa--illinois-biometric-information-privacy-act)
- [ECPA / federal Wiretap Act](#ecpa--federal-wiretap-act)
- [State wiretap statutes](#state-wiretap-statutes)
- [Healthcare-tracking pixel claims (HIPAA + state torts)](#healthcare-tracking-pixel-claims-hipaa--state-torts)
- [Session-replay claims (cross-cutting)](#session-replay-claims-cross-cutting)
- [Producing the evidence pack for litigation](#producing-the-evidence-pack-for-litigation)

## How to use this file

When a user describes any of the following, this file is the right reference:

- "We just received a demand letter alleging CIPA violations from session-replay vendors on our site"
- "A class action was filed alleging VPPA violations from the Meta Pixel on our video pages"
- "Our healthcare site is being sued over PHI leakage to Google Analytics"
- "Counsel needs technical evidence showing we had reasonable controls in place"
- "How do we prove what was firing on a specific date in the past?"

Walk the user through:

1. **What's alleged.** The statutory hook and the specific technical theory. Plaintiffs in these waves usually plead a standard set of allegations — knowing the pattern speeds the conversation.
2. **What ObservePoint detects.** The specific Rules and reports that produce evidence relevant to the claim.
3. **How to assemble the evidence pack for counsel.** Audit configurations, Rule history, run history with timestamps, exception log, change log — see the [Producing the evidence pack for litigation](#producing-the-evidence-pack-for-litigation) section at the end.
4. **What the evidence does and doesn't prove.** Honest framing — ObservePoint can produce strong "we detected and remediated" evidence, but it cannot defeat liability on its own.

Cross-reference the **regulation** skill for the comprehensive privacy laws that may run parallel to a tort claim (e.g., CCPA / CPRA on top of CIPA), and `references/mcp-tools.md` for the specific MCP wrappers — especially `scan_audit_pii`, `scan_journey_pii`, `compare_consent_states`, `find_anomalies`, and `find_first_observed`.

## CIPA — California Invasion of Privacy Act

**Statutory hook.** Cal. Penal Code §§ 631 (unauthorized eavesdropping or recording), 632 (eavesdropping on confidential communications), and the dominant 2024–2026 theory under § 638.51 (pen registers and trap-and-trace devices).

**The pen-register theory in plain language.** A pen register is a device that captures dialing or routing information about communications. Plaintiffs allege that third-party trackers on websites (session-replay vendors, chat widgets, fingerprinting libraries) function as digital pen registers when they capture identifying signals about visitors without consent. The legal theory has produced 1,000+ class-action filings annually in 2024–2026, often against retailers, healthcare providers, financial services, and other consumer-facing businesses.

**Common allegations.**

- A specific third-party vendor (most often a session-replay platform, chat widget, or analytics tool with fingerprinting) is installed on the website.
- The vendor captures identifying information (IP address, device fingerprint, browser fingerprint, mouse movements, scroll patterns) that plaintiffs analogize to dialing/routing information.
- Consent is missing or inadequate — the cookie banner doesn't explicitly mention the practice, or fires only after the data is already collected.
- The plaintiff visited the site, was tracked, and seeks statutory damages (CIPA provides up to $5,000 per violation).

**What ObservePoint detects.**

- **Vendor inventory.** The Domains & Geo Privacy Report enumerates every third-party domain receiving data from the audited pages. Session-replay vendors, chat widgets, and fingerprinting libraries appear here. This is the foundational evidence for "what's actually on the site."
- **Timing.** `find_first_observed` produces the date a specific vendor first appeared in the audit history — useful when the complaint alleges tracking during a period before the customer claims it was deployed.
- **Pre-consent firing.** A Web Audit run in the default (no-consent) state with Rules asserting no third-party tracker fires before explicit consent. This is the central evidence for "did the tracker fire before consent was given?"
- **Consent-state diff.** `compare_consent_states(domain=..., leftState="default", rightState="opt-out")` produces a side-by-side: tags that fire on default but not on opt-out. The vendors in scope for CIPA usually appear in the "only on default" list.
- **PII leak detection.** `scan_audit_pii` and `scan_journey_pii` detect whether identifying values (visitor IP, typed identifiers, masked values from form inputs) are actually being captured by the named vendor — strengthens or weakens specific allegations about what was captured.
- **Change history.** When a vendor was added, modified, or removed from the site — pulled from the audit run history.

**Specific Rules to write.**

```
WHEN vendor in ["<session-replay vendor>", "<chat widget>", "<fingerprinting library>"]
EXPECT
  consent_state != "default"   (does not fire before consent)
  AND request_destination in approved-vendor-list
```

**Evidence-pack notes for CIPA defense.**

- Demonstrate that consent was sought (the CMP banner is configured, served, and tracked).
- Demonstrate that the named vendor did not fire pre-consent on the customer's pages (the audit history showing Rule passes).
- Demonstrate that when an issue was detected, it was remediated within a defined SLA (the exception log).
- Don't oversell — ObservePoint evidence shows technical controls; legal arguments about consent adequacy, CIPA's applicability to a specific data flow, and damages calculation are counsel's work.

**What this file does NOT do.** Predict CIPA case outcomes; advise on settlement strategy; opine on whether a specific consent flow satisfies CIPA's "two-party consent" framework. Those are legal calls for the customer's litigation counsel.

## VPPA — Video Privacy Protection Act

**Statutory hook.** 18 U.S.C. § 2710. Originally enacted in 1988 after a Supreme Court nominee's video rental history was published. Modernized in 2012, but the core prohibition — disclosing personally identifiable information about a "consumer's" video viewing without informed consent — remains.

**The current litigation wave.** Plaintiffs allege that website operators with video content disclose viewing data to third parties (most commonly Meta Pixel, TikTok Pixel, Google Analytics) without obtaining the specific consent VPPA requires. Sites that host video content — streaming services, sports leagues, news outlets, e-commerce product videos — have been the primary targets. Statutory damages: up to $2,500 per violation, with potential punitive damages.

**Common allegations.**

- A specific tracking pixel (most often Meta Pixel) is installed on video-bearing pages.
- The pixel sends the URL of the video the user is watching (or a video identifier) to the third party.
- The third party can link that URL to the user's identity via existing cookies or account associations.
- Consent under VPPA's specific standard (written, informed, distinct from general terms of service) was not obtained.

**What ObservePoint detects.**

- **Video-page audit scope.** Define a Web Audit scoped to video-bearing URLs (`/watch*`, `/videos/*`, `/play/*`, etc.) with Rules asserting no advertising tracker fires when consent isn't expressly granted for video-data sharing.
- **Pixel payload inspection.** `get_page_requests` and `query_report` against the network-requests entity surface the specific requests Meta Pixel and other named vendors make. If the request URL or payload contains the video URL, that's the evidentially-relevant signal.
- **PII scanning on video pages.** `scan_audit_pii` on video URLs catches direct user-identifier leakage.
- **Consent-state diff specifically for video pages.** `compare_consent_states` between the consent variants on the video subset — confirms what fires under each state.

**Specific Rules.**

```
WHEN page URL matches "<video-page pattern>"
AND tag = "Meta Pixel"
EXPECT
  no event payload contains the video URL OR video identifier
```

**Evidence-pack notes for VPPA defense.**

- Show what was firing on the named video pages during the alleged period (audit history).
- Show the consent gating — what the user was shown and what they had to do for video pixels to fire.
- Show any change history — if the vendor configuration was modified mid-period, the activity log captures who, when, and why.

## BIPA — Illinois Biometric Information Privacy Act

**Statutory hook.** 740 ILCS 14. In force since 2008. Damages: $1,000 per negligent violation, $5,000 per intentional or reckless violation, attorney's fees, no cap.

**Scope.** Regulates the collection, use, storage, and disclosure of "biometric identifiers" (retina/iris scans, fingerprints, voiceprints, scans of hand or face geometry) and "biometric information" (any information based on biometric identifiers used to identify an individual). Photographs and standard video are typically excluded — but face-scan technology applied to those images is in scope.

**Web-tracking intersection.** Most BIPA litigation targets in-person biometric capture (workplace fingerprint clocks, retail face-recognition). The web-tracking intersection is narrower but real: face-detection libraries embedded in marketing pages, voice-print capture in customer-service chat, fingerprint-style browser fingerprinting that goes beyond what most courts consider "biometric."

**What ObservePoint detects.**

- **Vendor inventory.** Identify pixels and libraries known to perform face / voice / fingerprint capture. The Domains & Geo Privacy Report inventories every third-party endpoint receiving data; cross-reference against known biometric-capture vendor lists.
- **Capture-attempt detection.** Audit pages that use camera or microphone access (camera-permission JavaScript prompts, getUserMedia calls). Capture is visible in `get_browser_logs` and `get_page_requests`.
- **Consent evidence.** Whether explicit consent for biometric capture was sought before capture — same audit pattern as CIPA, with stricter consent requirements.

**Specific Rules.**

```
WHEN page contains script from "<known biometric-capture vendor>"
EXPECT
  explicit biometric consent obtained AND captured in event log
```

**Evidence-pack notes for BIPA defense.** BIPA is the highest-damages tort statute among these — $5,000 per intentional violation with no cap means class certification can produce catastrophic exposure. Conservative evidence: prove the capture didn't happen, or prove explicit BIPA-compliant consent was obtained before it did.

## ECPA / federal Wiretap Act

**Statutory hook.** 18 U.S.C. § 2511 (federal Wiretap Act, part of the Electronic Communications Privacy Act). Prohibits the unauthorized "interception" of "electronic communications." Civil remedies: statutory damages ($10,000 or $100/day, whichever is greater), actual damages, punitive damages.

**Web-tracking theory.** Plaintiffs allege that third-party trackers (session-replay vendors, chat-pixel handoffs, analytics tools) "intercept" the user's communications with the website — the user types into a form or moves their mouse, and the third party captures it in real time. ECPA's "party exception" (one party to the communication consents) is the central defense battleground.

**Relationship to CIPA.** CIPA is California's tougher state analog with broader plaintiff-friendly provisions. Federal ECPA claims often accompany CIPA claims in California suits; non-California suits typically rely on ECPA alone or pair with that state's wiretap statute.

**What ObservePoint detects.** Same surface as CIPA — vendor inventory, pre-consent firing, consent-state diff, PII scanning. The evidentiary signal is the same; the legal framework differs.

## State wiretap statutes

**Statutory hooks.** Many states have wiretap statutes paralleling CIPA, with varying consent regimes and damages. The plaintiff-friendly ones (cited in pixel litigation):

- **Massachusetts.** M.G.L. c. 272 § 99. Two-party-consent state. Significant pixel-related filings in 2024–2026.
- **Pennsylvania.** 18 Pa. C.S. § 5703. Two-party-consent state.
- **Florida.** Fla. Stat. § 934.03. Two-party-consent state.
- **Washington.** RCW 9.73.030. Two-party-consent state.

**What ObservePoint detects.** Same as CIPA — the technical evidence transfers across state wiretap regimes. The legal frame and damages exposure differ.

## Healthcare-tracking pixel claims (HIPAA + state torts)

**Statutory hooks.**

- HIPAA (45 C.F.R. Parts 160-164) — federal healthcare privacy law. Enforced by HHS Office for Civil Rights (OCR). The December 2022 OCR bulletin (and 2024-2026 updates) addresses tracking technologies on healthcare websites specifically.
- State torts — invasion of privacy, breach of confidence, breach of fiduciary duty, plus the consumer-protection statutes of the relevant state.
- Add CIPA / VPPA / state wiretap as additional layered claims where applicable.

**The wave.** Hundreds of class actions filed against hospital systems, healthcare-adjacent retailers, telehealth platforms, and pharmacy chains since 2023. The pattern: Meta Pixel or Google Analytics on a patient-facing page (appointment booking, prescription refill, symptom checker, condition information, find-a-doctor) transmits the URL — which constitutes PHI when paired with an IP address — to the third party. OCR has issued substantial settlements; private litigation has produced multi-million-dollar settlements as well.

**What ObservePoint detects.** This is the strongest current ObservePoint defensive use case. See the HIPAA section in the **regulation** skill for the audit setup. Additional litigation-specific signals:

- **Historical pixel firing.** Audit run history showing what fired on which patient-facing URLs on what date. When the complaint alleges a specific date range, this is the central rebuttal data.
- **`scan_audit_pii` with healthcare-context customRegex.** Detect not just generic PII patterns but customer-specific identifiers (member IDs, MRNs, appointment confirmation numbers).
- **Vendor removal timeline.** When a problematic vendor was removed from the site — proves remediation timing.

**Evidence-pack notes for healthcare-pixel defense.** Frame the evidence as: (a) we audit these pages regularly, (b) here's what we found and when, (c) here's how quickly we remediated, (d) here's our ongoing process for catching this. The "reasonable practices" narrative is what counsel needs to construct around the technical evidence.

## Session-replay claims (cross-cutting)

Session-replay vendors (FullStory, Hotjar-style products, custom session-recording libraries) appear across CIPA, ECPA, and state-wiretap claims. The technical defense is the same across jurisdictions — the legal framing differs.

**What plaintiffs allege.** The session-replay vendor records the user's interactions (mouse movements, scrolls, keystrokes, form inputs) and transmits them to the vendor. Plaintiffs frame this as interception under wiretap statutes or as pen-register/trap-and-trace activity under CIPA.

**What ObservePoint detects.**

- **Vendor presence.** Domains & Geo Privacy Report shows the vendor's endpoint domain.
- **What's captured.** `get_page_requests` shows the actual requests the vendor makes; `scan_audit_pii` shows whether identifying data is in those requests.
- **Consent-state firing.** Audit with Reject-All and GPC variants; assert the session-replay vendor doesn't fire when the user opted out.
- **Form-field masking.** Session-replay vendors offer masking features for sensitive form fields. Pages can be audited for whether the masking attributes are correctly applied to in-scope inputs.

**Specific Rule.**

```
WHEN vendor = "<session-replay vendor>"
EXPECT
  consent_state in ["accept-all", "essential-only-with-explicit-replay-consent"]
  AND all form fields with class "ssn|cc|password|...."  have data-private="true"
```

## Producing the evidence pack for litigation

When counsel asks for the technical record, assemble:

1. **Audit definitions.** The configurations of the relevant audits — URL scope, consent states tested, schedule cadence. Show this is a regular, defined process, not ad-hoc inspection.
2. **Rules library.** The `WHEN/EXPECT` Rules attached to each relevant audit, with their version history. The rules are the codified controls.
3. **Run history.** The audit run history for the alleged period — date, status (pass/fail), and what specifically failed. Use `get_audit_runs` followed by `query_report` against the rule-summary entity. `mcp__ObservePoint__export_report` produces the CSV.
4. **Exception log.** Every Rule failure during the period, when it was acknowledged, when it was remediated, and by whom. The activity log in the app captures this.
5. **Change log.** Modifications to the audit definitions, Rules, or attached consent categories during the alleged period — pulled from the activity log. This addresses any "you changed your defenses after we sued" arguments.
6. **PII scan output (where relevant).** `scan_audit_pii` or `scan_journey_pii` results for the relevant pages and period. Output is already masked — no raw PII in the evidence pack.
7. **Vendor inventory.** Domains & Geo Privacy Report for the alleged period. Shows every third-party endpoint receiving data.

**Format the pack for counsel as:**

- An executive summary (1 page) — what was audited, what the audits found, what was remediated, current status.
- An evidence appendix (PDF + CSV bundle) — the raw artifacts above, dated and labeled.
- A "reasonable practices" narrative (drafted by counsel, supported by the appendix) — how the customer's audit + remediation process compares to industry practice.

The package goes to counsel. ObservePoint produces the technical record; counsel uses it as part of a broader litigation defense.

---

*Last verified: 2026-06-03*

*This file is technical evidence guidance, not legal advice. The statutes covered drive active class-action waves with substantial damages exposure; coordinate with counsel before relying on any audit data in litigation. "ObservePoint" and product names referenced here are trademarks of ObservePoint, LLC.*
