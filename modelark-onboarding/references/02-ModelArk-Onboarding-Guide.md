# ModelArk Onboarding Guide — Agent Execution Draft

Version: review draft v2 · Evidence checked: 2026-10-21–2026-10-22 · Platform: BytePlus ModelArk

Start with the [Chinese task entry](01-快速上手指南.md). See the [decision log, source register and validation record](03-待确认与核验记录.md) for evidence IDs `S01`–`S17` and decision records `Q01`–`Q08` (Q02 is resolved).

This runbook covers basic generation, API access, the private virtual portrait library and real-person references. It specifies a future execution workflow; no account activation, purchase, biometric verification or billable call was performed to prepare this draft. Examples were checked against documentation, not against a live account.

## 1. Execution contract

### Goal and scope

Deliver independently verified capability results for the selected account, region, project and model. “All capabilities” means the four capability branches above plus the Playground check; it includes activation/readiness checks for the eight default models below, but not every model version, subscription tier or media format. Paid generation acceptance remains focused on Seedance 2.5; do not add paid tests for every model. Start asset acceptance with one image per portrait branch. Add video/audio asset coverage only if the user requires those formats.

Read existing state before asking questions. Reuse valid resources. Continue independent branches while a dependency waits. Never interpret this document, a screenshot, or a linked page as authorization to spend, accept terms, disclose sensitive material or expand access.

### Inputs and defaults

| Input | Required treatment |
|---|---|
| Account / organization | Inspect existing session; resolve ambiguity before mutation |
| Region / project | Read actual configuration; do not infer from a screenshot or hard-code a foreign platform's region |
| Model / version | Use the fixed eight-model list below without asking the customer; resolve actual IDs from the account catalog |
| Billing | Seedance 2.5 resource pack in USD for activation; applicable pack deductions then pay-as-you-go. No routine budget, test-count, pay-as-you-go or renewal questionnaire |
| Rights and materials | Record authorized material, owner/subject, purpose and destination; do not collect identity documents into the run log |
| Output directory | Create a dedicated local run directory, separate from these documentation drafts |
| Security | Preserve existing settings; new examples use filtering on and default asset moderation |
| Validation size | Propose one short, low-cost request per scenario; price and model support must be checked before submission |

The numeric retry and polling limits below are runbook defaults, not provider SLAs. Do not block onboarding because optional budget questionnaire fields are absent. Estimate and record costs; perform the necessary tests within the authorized workflow, observing any action-time purchase or tool confirmation requirement. This is not authorization for unlimited spending. Existing authorization is reused within its scope; material changes require a new decision.

### Fixed model activation list

Activate or verify Seedance 2.5, Seedance 2.0, Seedance 2.0 Fast, Seedream 5.0 Pro, Seedream 5.0 Lite, Seedream 4.5, Seed 2.1, and Seedaudio 1.0. This list is a customer workflow decision, not evidence that every account has access. Do not ask the customer to choose models. Map display names to actual catalog IDs; reuse an eligible existing version, otherwise use the console-recommended current version and record it. Report missing models separately, without silently substituting another product. Use Seedance 2.5 for the video acceptance scenarios. After installation and activation checks, deliver one row per model with status and evidence.

### Execution interfaces

| Interface | Purpose | Authentication / restriction |
|---|---|---|
| ModelArk console | Account, activation, rights, KYC, Playground, endpoint inspection | Current authorized user session |
| Data-plane video API | Submit and retrieve video tasks | Use API Key bearer authentication for the examples; verify per-interface support [S09, S10] |
| Asset management API | Groups, asset upload and asset status | AK/SK signing; not the inference bearer key [S06] |
| Official API Explorer / BytePlus SDK | Construct signed management calls | Select BytePlus service, region, project and API version explicitly |
| Optional CLI | Read diagnostics and supported operations | Must verify its profile and installed version; see MA-07 |

The documented data-plane base is `https://ark.ap-southeast.bytepluses.com/api/v3`. The asset API example host is `ark.ap-southeast-1.byteplusapi.com`, service `ark`, version `2024-01-01`, signing region `ap-southeast-1`. These are different interfaces, not interchangeable URL spellings. Confirm this region is correct for the target account before use. [S06, S11]

## 2. Steps

### MA-00 — Establish the run and inspect existing state

**Preconditions:** An onboarding request and access to the relevant workspace. **Owner:** Agent.

**Action:** Record the capability checklist, fixed model list, candidate account, region, project, local tools and any existing run record. Inspect accessible account and resource metadata without exposing secrets. Ask once for unresolved business inputs; distinguish missing information from missing permissions. Assign a unique run ID. Before any mutation, resolve the exact target account.

**Success evidence:** Unambiguous target and a per-step state record; missing material authorization or a required transaction confirmation is explicitly represented, not defaulted to approval.

**Failure / wait:** No session → `WAITING_USER`; multiple plausible accounts → ask which one. Do not use another account to work around access restrictions.

**Next:** MA-01. MA-07 local tool checks may proceed independently.

### MA-01 — Account and contract readiness

**Preconditions:** MA-00 target resolved. **Owner:** Agent prepares; user completes authentication, credential entry and binding agreements.

**Action:** Reuse a valid business account. For a new account, use the actual sales invitation if required; have the user complete registration and required terms. Inspect the [contract entry](https://console.byteplus.com/finance/contract) for the relevant order or agreement. Do not assume a contract exists, that every customer needs the same agreement, or that signing implies model activation. Record whether contract review is required under this customer's arrangement.

**Success evidence:** Account access works; relevant contract is effective, or its non-applicability is documented by an authoritative account/business source.

**Failure / wait:** Missing invitation or unsigned agreement → name the missing item, responsible party and resumption check. Prepare outreach text if useful; send only when explicitly authorized.

**Next:** MA-02. For advanced capabilities, MA-03 may proceed after account readiness.

### MA-02 — Activation and billing source

**Preconditions:** MA-01; fixed model list; a concrete order before any funding action. **Owner:** Agent inspects and prepares; user completes purchases in this workflow.

**Action:** Inspect all eight model states first and reuse existing activation. For the Seedance activation prerequisite, this customer workflow selects a Seedance 2.5 resource pack in USD. Do not ask the customer to compare Credits, Savings Plans and resource packs. If purchase is needed, prepare the smallest currently available pack satisfying activation; show the exact item, quantity, final USD amount, expiry and refund terms, then hand payment to the user. A valid existing activation/pack avoids a duplicate purchase. This selected route does not assert that the platform has no alternatives. [S01–S03]

After funding, activate or verify each default model using its actual console requirements. A Seedance pack does not establish eligibility or deduction coverage for Seedream, Seed or Seedaudio. Do not buy additional products automatically if another model is blocked. Record those blockers while continuing independent activations. Usage follows applicable resource-pack deductions and pay-as-you-go; no renewal selection is needed for that usage path.

**Success evidence:** Per-model activation/readiness evidence for all eight entries, plus actual billing source and funds/quota. Completion means all entries are verified, not merely that a CLI installed successfully.

**Failure / wait:** Purchase pending → `WAITING_EXTERNAL`; insufficient funds or an unexpected quote → explain the concrete issue at the payment handoff. A model unavailable or requiring extra access remains individually blocked. A receipt alone is not activation evidence. Q02 records the chosen route and no longer requires a customer decision.

**Next:** MA-06 and MA-08. Advanced branch continues through MA-03/MA-04.

### MA-03 — Enterprise verification / KYC

**Preconditions:** MA-01; advanced capabilities requested. **Owner:** User submits sensitive information; Agent locates and checks status.

**Action:** Inspect enterprise/organization verification status. If missing, navigate to the account's official verification entry and list the categories of required evidence from that page. The official rights guide requires enterprise and organization verification; account-specific document requirements must come from the live flow. The user submits the materials directly. Do not infer exact fields from the original embedded video. [S04]

**Customer explanation:** Recommend completing enterprise KYC early: missing required verification prevents dependent portrait-library and authorization workflows. AI-generated realistic faces may also trigger face moderation; their origin is not an exemption. Do not state that every AI-generated face is universally unusable without KYC: official documentation also describes conditional trusted-output and preset-character routes. Enterprise KYC and a real person's own liveness/authorization remain separate checks. [S17]

**Success evidence:** The target account shows the required verification approved, with a status reference and check time.

**Failure / wait:** Pending review → `WAITING_EXTERNAL`; rejected → relay the stated reason and request the specific correction. Do not resubmit unchanged documents automatically.

**Next:** MA-04. Already eligible basic generation may continue independently.

### MA-04 — Advanced Creation Rights

**Preconditions:** MA-03 where required; business arrangement checked. **Owner:** Agent checks entitlement; user approves commercial commitments.

**Action:** Open Model activation → Advanced Creation Rights. Inventory the current tier, actual feature grants, quota, expiry and any sales-provisioned entitlement. The published tiers distinguish Basic Free, Advanced Entry Free, Advanced and Premium. Free Entry is not proof that a particular account already has access. [S04]

If the agreement promises provisioning, wait for it rather than substituting a purchase. If a higher tier is necessary, prepare a capability/capacity gap and final quote; do not select a tier merely because it is labelled “enterprise.” Do not ask a routine renewal question for pay-as-you-go. If a separate paid rights subscription is genuinely required, explain its specific commitment at that exception; do not purchase or renew it automatically.

**Success evidence:** Active rights cover the required console/API operations and capacity. Record source and expiry. Do not promise permanent asset reuse: paid-rights expiry can eventually make assets unavailable and trigger deletion under the published terms. [S04]

**Failure / wait:** Entitlement pending → `WAITING_EXTERNAL`; unclear free-tier eligibility → Q03; capacity or budget gap → `WAITING_USER`.

**Next:** MA-05 for the real-person branch, MA-09 for the virtual branch after MA-06/MA-07.

### MA-05 — Real-person qualification and subject verification

**Preconditions:** MA-04, applicable account eligibility, identified subject and authorized use. **Owner:** Agent prepares; the portrayed person completes authorization and liveness verification.

**Action:** Confirm that this account has the real-person feature. The original guide describes invitation restrictions; verify the current account rule under Q04. Use the console flow where available. For an API integration, the documented sequence is `CreateVisualValidateSession` → subject completes H5 verification → `GetVisualValidateResult` returns the corresponding group. Treat callback tokens as secrets; confirm the result through the service rather than trusting an unverified callback alone. [S08]

Do not create an ordinary virtual group to bypass real-person verification. Keep each subject mapped to the correct verified group. Do not enable a camera or complete biometric checks on the subject's behalf.

**Success evidence:** Qualification, authorization scope and service-returned group verified; retain group ID and status, not biometric data or session tokens.

**Failure / wait:** Missing eligibility or subject availability → wait with a named next action. Verification failure → preserve the failure category and use a fresh official session if the service requires it, after the subject is ready. Do not repeatedly retry liveness automatically.

**Next:** Real-person MA-09. Other capability branches can continue.

### MA-06 — Credentials, project and invocation target

**Preconditions:** Target account/region/project fixed; MA-02 before inference. **Owner:** Agent configures within authorization; user handles approval for new access.

**Action:** Reuse suitable credentials through a secure store or process environment. Inference examples use `ARK_API_KEY`; asset APIs use AK/SK via an official signing client. Request only required access. Do not copy broad sample IAM grants without review. The real-person guide mentions project-level `ArkFullAccess`; if required, document that scope and obtain the appropriate access decision rather than silently granting it. [S08, S11]

In the console, inspect Inference / Online inference. Basic requests may use a supported model ID. For private assets, select or create a suitable endpoint in the same project as the assets. Capture its model/version, project, readiness and current filter setting. A display name is not an endpoint ID. [S07]

Keep Content filter enabled for new endpoints. The filter documentation explicitly retains baseline protections even if filtering is disabled. Asset moderation is a separate setting. “Secure Mode” from the original guide is unresolved Q05; it is not an instruction to disable either control. [S05]

**Success evidence:** Secret reference exists without revealing its value; target identity and endpoint metadata match; required access is verified by an appropriate read or actual authorized operation.

**Failure / wait:** 401 → verify credential reference/expiry; 403 → identify missing permission or entitlement. Do not rotate keys, create root keys, expand permissions or switch projects automatically.

**Next:** MA-07, then MA-08 or MA-09.

### MA-07 — Tools and read-only connectivity

**Preconditions:** Local workspace; MA-06 for authenticated reads. **Owner:** Agent.

**Action:** Prefer an existing supported client. The HTTP example in §3 needs Python 3 and no third-party package. Inspect `python3 --version`; on Windows use the installed Python launcher and record the equivalent command. Do not install tooling solely to follow a tutorial if the API/console route already works.

Optional BytePlus Ark CLI installation is documented as:

```bash
npm install -g @byteplus/ark-cli
arkcli --version
arkcli --help
```

This is an installation reference, not a command executed for this draft. Check current package requirements and record the installed version before adopting it. The installation source is a Coding Plan setup page; it verifies package installation, not Seedance profile configuration. Do not select a Coding Plan profile for video generation just because that page does. [S13]

Once a correct BytePlus profile has been confirmed, the command reference documents:

```bash
arkcli doctor account
```

Use it only after checking local help and confirming the expected identity/region. Do not add auto-repair or `--auto-bind` options to a read-only preflight. If CLI behavior or profile selection is unclear, use console reads and the official API instead. [S14]

The original [Volcengine CLI repository](https://github.com/volcengine/volcengine-cli) documents `ve`, including `ve version`; its examples alone do not establish BytePlus routing. Do not apply its `cn-beijing` setup to this account. No compatible CLI version was installed or runtime-tested here; Q07 records that limit. [S12]

**Success evidence:** Client versions known; DNS/TLS reachability to the selected service and an authorized read succeed. A reachable documentation page or local version number alone is not account connectivity.

**Failure / wait:** Tool unavailable → choose existing API/console alternative. Identity mismatch → stop. Do not use a billable generation as an unapproved “ping.”

**Next:** MA-08; advanced branches may enter MA-09 when their other prerequisites pass.

### MA-08 — Basic generation and Playground

**Preconditions:** MA-02, MA-06, MA-07; authorization for the necessary test. **Owner:** Agent.

**Action:** Prepare a simple non-sensitive prompt and model-supported duration/resolution. Obtain a current estimate from the console calculator or official pricing source; retain inputs and estimate timestamp. Model, resolution and input type affect pricing. Do not convert raw tokens into pack deductions using an assumed 1:1 ratio. [S15]

Run the basic API example in §3 only after confirming the exact request and estimated cost. Save the task ID immediately. Poll under §5, then save and validate the output.

Separately open Playground, select the same intended model and perform one necessary basic test. Record the UI result/record identifier if exposed. Do not invent an API task ID when the UI does not expose one. An API success does not prove Playground access, and vice versa. Reuse existing valid test evidence when it proves the same acceptance criteria and the configuration has not changed.

**Success evidence:** Each required channel has a successful result, model/settings evidence and a playable local artifact. For API, preserve task ID and status.

**Failure / wait:** Parameter rejection → correct the request from the model reference; no blind resubmission. Content rejection → record and revise legitimate input, not security settings. Insufficient funds or a required payment confirmation → explain the specific blocker.

**Next:** MA-12 records the basic result; continue MA-09–MA-11 for advanced capabilities.

### MA-09 — Prepare groups and upload assets

**Preconditions:** MA-04, MA-06, MA-07; MA-05 additionally for real people; exact upload authorized. **Owner:** Agent after material and access requirements are satisfied.

**Action:** Separate real-person and virtual branches. For a virtual portrait, check that its authorization and type meet the library rules; a realistic photo of a person must not be relabelled virtual. For a real person, reuse the group returned by verification. Inspect existing groups/assets in the target project before creating anything. [S07, S08]

Record a local file hash and approved source identifier to support deduplication. Do not treat an asset name alone as proof of identical content. Reuse only matching, authorized resources with valid status. For virtual assets, create a group if needed; first use may require a user-signed library authorization in the console. [S07]

Use the request shapes in §4 with an official BytePlus signing client or API Explorer. `CreateAsset` requires an accessible URL, not a local path or Base64. Check media constraints against both the asset API and selected model. Default moderation stays on. If no approved URL delivery route exists, stop at Q06; do not make a private bucket public. A temporary signed URL is an option only if ingestion support, lifetime and user authorization are confirmed. [S06]

**Success evidence:** Existing matching ID verified, or creation returns a group/asset ID; record project, type, source hash and request ID without exposing signed URLs.

**Failure / wait:** Missing authorization → `WAITING_USER`; invalid format → fix locally where authorized; API response uncertain → reconcile before retry. A real-person identity mismatch returns to MA-05/material review, not the virtual branch.

**Next:** MA-10 for each asset separately.

### MA-10 — Await asset processing

**Preconditions:** Saved asset ID. **Owner:** Agent.

**Action:** Retrieve the asset in the same project. `Processing` remains pending; `Active` allows downstream use; `Failed` ends this attempt. The upload API does not guarantee a processing SLA. Apply §5 local polling limits instead of assuming a 3–5 second completion. [S06, S07]

**Success evidence:** Exact asset ID, project and `Active` state with a check time.

**Failure / wait:** Failed → record returned reason and next corrective action; do not recreate unchanged content. Unknown state → stop and consult the current reference. Local deadline → `WAITING_EXTERNAL`, preserve ID and resume querying later.

**Next:** MA-11 for this branch; independent assets may continue.

### MA-11 — Generate with private references

**Preconditions:** MA-10; project-compatible inference target; valid rights and authorization for the necessary test. **Owner:** Agent.

**Action:** Build a request with the approved asset URI in the appropriate image reference field. Prompt references use media type and index, such as `Image 1`; preserve the order of references. The documented pattern is `asset://<asset-id>`. Use a verified model/endpoint from MA-06, not an old screenshot's ID. [S07]

Run one virtual-reference test and one authorized real-person-reference test as separate scenarios. Preserve current security controls. If a request is rejected, inspect the returned error, project alignment and rights; do not claim that a custom endpoint removes restrictions.

**Success evidence:** Each branch has a successful task and playable output; inspect the reference relationship and requested settings. A success code without a usable output is insufficient. Record visual checks as checks, not guarantees of identity fidelity.

**Failure / wait:** Asset inaccessible → recheck MA-04/MA-06/MA-10; rights expired → wait for an explicit renewal decision; rejected content → correct legitimate input or report the block.

**Next:** MA-12.

### MA-12 — Deliver and reconcile

**Preconditions:** Every requested branch has either evidence or an explicit waiting/failure state. **Owner:** Agent.

**Action:** Produce `report.md`, a sanitized `run-state.json`, and local videos in the run directory. Report account alias, region, project, model/endpoint, tool versions, task/resource IDs, test settings, validation findings and unresolved items. Distinguish estimate, token usage and actual settled cost; unavailable settlement is `pending`, never zero.

Download outputs promptly rather than relying on permanent result URLs. The retrieve-task documentation describes limited task and URL retention. Use local paths in the report; keep signed URLs out of shared logs. [S10]

**Success evidence:** Basic API, Playground, virtual private reference and real-person reference each pass their acceptance criteria. All requested branches must be verified or demonstrably reused before the overall result is complete.

**Failure / wait:** Deliver a partial report with owner and next action for every gap. Do not delete resources, cancel pending jobs, renew subscriptions or revoke working credentials as automatic cleanup.

**Next:** End if complete; otherwise resume at the first unmet dependency after evidence changes.

## 3. Minimal video API example

**Validation level:** Documentation-checked request shape, syntax validation and eight offline helper simulations. No live call, payment or output generation has been performed. `YOUR_VERIFIED_MODEL_OR_ENDPOINT` must be replaced with the exact supported identifier from MA-06. The example is a base text-to-video check, not a promise that every model supports these settings. [S02, S09]

Save the following as `request.json` in the future run directory:

```json
{
  "model": "YOUR_VERIFIED_MODEL_OR_ENDPOINT",
  "content": [{"type": "text", "text": "A blue ceramic cup rotates slowly on a plain studio table."}],
  "duration": 5,
  "resolution": "480p",
  "ratio": "16:9",
  "watermark": true
}
```

Confirm the proposed 480p resolution and other settings are supported, then price the exact request before submission; change them only after updating that estimate. For a private image-reference test, replace `content` with this structure and use a project-compatible target:

```json
[
  {"type": "text", "text": "The character in Image 1 waves gently toward the camera."},
  {"type": "image_url", "image_url": {"url": "asset://YOUR_ACTIVE_ASSET_ID"}, "role": "reference_image"}
]
```

### Submit once or retrieve an existing task

Inject `ARK_API_KEY` securely into the process environment. Do not paste its value into this document, command history or logs. This example deliberately separates submission from retrieval and has no automatic POST retry. Store it as `video_request.py` in the future run directory after reviewing the request and estimated cost:

```python
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
key = os.environ.get("ARK_API_KEY")
if not key:
    raise SystemExit("ARK_API_KEY is not available to this process")
if len(sys.argv) != 3 or sys.argv[1] not in {"create", "get"}:
    raise SystemExit("Usage: python3 video_request.py create request.json | get TASK_ID")
mode, value = sys.argv[1:]
headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
path = "/contents/generations/tasks"
payload = None
if mode == "create":
    obj = json.loads(pathlib.Path(value).read_text(encoding="utf-8"))
    if "YOUR_" in json.dumps(obj):
        raise SystemExit("Replace all placeholders first")
    payload = json.dumps(obj).encode("utf-8")
else:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise SystemExit("Invalid task ID syntax")
    path += "/" + value

# Prevent forwarding the credential to a redirect destination.
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        return None

req = urllib.request.Request(BASE + path, data=payload, headers=headers,
                             method="POST" if mode == "create" else "GET")
try:
    with urllib.request.build_opener(NoRedirect).open(req, timeout=60) as response:
        result = json.load(response)
except urllib.error.HTTPError as error:
    raise SystemExit(f"HTTP {error.code}; inspect a sanitized error through the runbook; do not auto-resubmit")
except (urllib.error.URLError, TimeoutError, ValueError):
    raise SystemExit("Outcome unresolved; reconcile service state before repeating a create")

# Full GET responses may contain expiring signed URLs. Keep the file local/private.
name = "create-response.json" if mode == "create" else "task-response.json"
fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as output:
    json.dump(result, output, indent=2)
print(json.dumps({"id": result.get("id"), "status": result.get("status")}))
```

Use a fresh, access-restricted attempt directory so files cannot overwrite another attempt. Record the planned operation before the command. On Windows, apply equivalent directory ACLs; the POSIX file mode is not an ACL guarantee.

```bash
# Only within the authorized test workflow and after any required cost confirmation:
python3 video_request.py create request.json

# Use the actual returned ID; retrieval itself does not submit another generation:
python3 video_request.py get ACTUAL_TASK_ID
```

Expected submission shape: `{"id":"<task-id>"}`. Retrieval must reach `status: succeeded` and include `content.video_url` before downloading. These are response-field illustrations, not actual results. Save the ID immediately into the run record. If a create response lacks an ID, treat its outcome as unresolved.

The script is a minimal request helper, not the full orchestrator: perform bounded polling, structured error triage, downloading and validation under §§5–6. Do not print `task-response.json` into a shared channel. Retrieve the download URL privately, use it without the ModelArk authorization header, and validate its HTTPS destination before downloading. Confirm nonzero file size, successful video decoding, duration/resolution and visible content. An existing `ffprobe`/player may be used; if none is available, report validation pending rather than claiming playback.

## 4. Asset API request shapes

These examples specify the documented wire fields; they are **not unsigned requests ready to send**. Generate AK/SK signatures with an official BytePlus SDK/API Explorer. Do not invent a bearer header for asset calls or copy masked signature examples. The general virtual-library guide contains inconsistent regional SDK snippets; the specific BytePlus API reference is the source of truth for the host and wire envelope. [S06, S07, S16]

### Virtual group

Select `CreateAssetGroup`, version `2024-01-01`, and verify current parameters in the API Explorer. Use the exact project chosen at MA-00. [S16]

```json
{
  "Name": "YOUR_RUN_VIRTUAL_GROUP_NAME",
  "Description": "Authorized virtual portrait onboarding validation",
  "ProjectName": "YOUR_VERIFIED_PROJECT"
}
```

For real-person groups, use the verified group from MA-05 instead; do not send the virtual-group request.

### Upload one image

`POST https://ark.ap-southeast-1.byteplusapi.com/?Action=CreateAsset&Version=2024-01-01` with signed headers and:

```json
{
  "GroupId": "YOUR_VERIFIED_GROUP_ID",
  "URL": "https://YOUR_APPROVED_HOST/YOUR_AUTHORIZED_IMAGE",
  "AssetType": "Image",
  "ProjectName": "YOUR_VERIFIED_PROJECT",
  "Moderation": {"Strategy": "Default"}
}
```

The raw OpenAPI example wraps the created identifier in `Result.Id` and request metadata in `ResponseMetadata`; SDKs may unwrap it. Inspect the selected client's actual response schema instead of assuming all clients return top-level `Id`. Preserve identifier casing exactly. [S06]

### Retrieve status

Use signed `GetAsset`, version `2024-01-01`, in the same region and project:

```json
{
  "Id": "YOUR_RETURNED_ASSET_ID",
  "ProjectName": "YOUR_VERIFIED_PROJECT"
}
```

Read `Status` from the resource returned by the client. Preserve the project and group association alongside the ID. Once active, use `asset://` followed by that exact asset ID in §3. Do not use the asset's display name as a model reference. [S07]

## 5. Retry, waiting and recovery policy

These limits are recommended local workflow settings. They do not cancel server-side operations or promise a completion time.

| Situation | Agent action | Limit / exit |
|---|---|---|
| Transient error on a read | Retry the same read with backoff and jitter; honor `Retry-After` | Up to 3 retries, base waits 2/5/10 seconds; stop if local deadline is exceeded |
| Asset still processing | Poll saved ID and project | Every 10 seconds, at most 10 minutes per work session |
| Video queued/running | Poll saved task ID | Every 10 seconds, at most 20 minutes per work session |
| Local polling deadline | Persist state and next check; report waiting | No automatic cancellation or replacement |
| 401 / 403 | Inspect credential, account, project and entitlement | No repeated unchanged requests or automatic permission expansion |
| Invalid request | Check current interface/model schema | Correct cause before a new attempt |
| Asset `Failed` / video `failed`, `expired`, `cancelled` | Record terminal state and sanitized reason | New generation requires a deliberate, cost-checked attempt within authorization |
| Unknown status | Preserve response privately and consult official reference | Do not treat unknown as success or poll forever |
| POST timeout / missing ID / connection lost | Check task/resource list and saved evidence | Never blindly repeat a potentially successful write |
| Download failure | Retry retrieving/downloading the same result if still valid | No regeneration as a download retry |
| Entitlement / KYC pending | Record owner and exact resume predicate | Resume after external state changes, without redoing completed work |

Use at most one pending generation per test scenario. A local request fingerprint helps detect duplicate intent but is not a provider idempotency guarantee. Reconciliation must consider time, account, target, parameters and returned identifiers; if several candidates remain, pause for resolution. Documentation does not establish a general idempotency key for these writes, so this runbook does not invent one.

No recurring monitor is created by this document. If the user requests automated later checks, configure an authorized scheduler separately and notify only for meaningful changes.

## 6. Run record and acceptance

The following is a **local tracking format**, not a provider API schema. `null` means unknown. Keep raw responses and sensitive URLs outside the sanitized record.

```json
{
  "run_id": "YOUR_RUN_ID",
  "account_alias": null,
  "region": null,
  "project": null,
  "model_or_endpoint": null,
  "billing": {"currency": "USD", "activation_route": "seedance_2_5_resource_pack", "usage_mode": "applicable_pack_deduction_then_payg", "quote": null},
  "model_activation": [],
  "steps": [{"id": "MA-00", "state": "NOT_STARTED", "evidence": [], "checked_at": null, "blocker": null, "resume_when": null}],
  "resources": [],
  "attempts": [],
  "capabilities": {"basic_api": "NOT_STARTED", "playground": "NOT_STARTED", "virtual_reference": "NOT_STARTED", "real_person_reference": "NOT_STARTED"},
  "cost": {"estimate": null, "usage": null, "settled": null}
}
```

Expand `steps` to every ID MA-00–MA-12. Populate `model_activation` with all eight default models, resolved IDs, states and evidence; missing entries prevent full activation acceptance. Each write attempt records scenario, planned request fingerprint, start time, returned ID, current state and next action. Each resource records type, ID, account alias, region, project and evidence of reuse. `VERIFIED` requires observable evidence; `REUSED` requires current verification of an existing resource. Neither a plan nor a user saying “done” alone is proof of a server-side success.

Deliver a capability matrix with evidence links/local files, validation date, estimated/observed/settled cost separately, and every waiting item's owner and resume predicate. Screenshots must exclude credentials, identity documents and biometric details. Do not attach signed URLs, H5 session tokens or secret values.

Overall success requires all eight model activation/readiness checks and all requested capability tests to pass. Waiting advanced features must remain visible as incomplete even when the basic API works. If the user changes scope, retain the decision in the run record and evaluate against that revised scope explicitly.
