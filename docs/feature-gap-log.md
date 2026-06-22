# ClinicFlow Feature Gap Log

Use this document to log all requested features, gaps, and improvements identified by Tomken clinic staff during the pilot phase. Do not build these features immediately; track them here to prioritize after workflows stabilize.

## Gap Log Table

| Feature Description | Requested By | Frequency / Impact | Priority (High/Med/Low) | Status (Backlog/Review/In-Progress) | Target Sprint | Notes / Workaround |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WhatsApp Notifications** | Receptionist | High - DaySmart sends auto-reminders via SMS/WhatsApp | High | Backlog | Sprint 4+ (Future) | Currently handled manually or via native Odoo Email templates. |
| **Owner Portal** | Clients / Managers | Medium - Owners like downloading vaccine certificates | Medium | Backlog | Sprint 9 | Currently, reception staff prints/emails PDF certificates directly. |
| **Automated SOAP Templates** | Vets | High - Pre-filled text templates based on visit reason | High | Review | Sprint 8+ | See detailed planning note below. Templates menu scaffold already in place. |
| **Multi-Doctor Scheduling Colors** | Clinic Manager | Medium - Color-coding calendar events by Veterinarian | Med | Backlog | Sprint 2 (Ops) | Calendar view currently colors events by doctor name, but needs refined styling. |
| **Reorder Warnings on Pharmacy** | Vets / Inventory | Low - Alerts when drug stock drops below threshold | Med | Review | Sprint 3 (Stock) | Odoo Inventory reordering rules can handle this natively. |

---

## Planned Feature: SOAP Note Templates (Detailed)

> **Status**: Architecture planned, not yet built. The `Templates` sidebar menu is already scaffolded in `clinicflow_outreach` — future template types will appear as additional sub-items under it.

### Overview

Veterinarians frequently use the same SOAP structure for common visit types (routine checkup, post-surgery review, vaccination visit, dental, etc.). Rather than typing from scratch each time, doctors should be able to define reusable templates that pre-fill SOAP fields when starting a new visit.

### Template Scopes (Ownership Model)

| Scope | Visible To | Editable By |
|-------|-----------|-------------|
| **Personal** | Owning doctor only | Owning doctor |
| **Team / Role** | Users with the same role/group | Managers or the creator |
| **Organisation-wide** | All staff | Clinic Managers / Admins only |

### Proposed Model: `clinicflow.soap.template`

```
name              Char        — Template name (e.g. "Routine Checkup", "Post-Op Review")
visit_reason      Char        — Suggested reason for visit this template applies to
scope             Selection   — personal | team | org
owner_id          Many2one(res.users)   — null if org-wide
group_id          Many2one(res.groups)  — optional, for team scope
soap_s            Text        — Pre-filled Subjective block
soap_o            Text        — Pre-filled Objective block
soap_a            Text        — Pre-filled Assessment block
soap_p            Text        — Pre-filled Plan block
active            Boolean     — Archive without deletion
```

### UX Flow

1. Doctor opens **New Visit** form.
2. A **"Load Template"** button appears on the SOAP tab.
3. Clicking it opens a selection dialog showing templates scoped to that doctor (personal → team → org, in priority order).
4. Selecting a template pre-fills the SOAP fields. Doctor edits as needed.
5. If SOAP already has content, user is warned before overwriting.

### Access Control

- Personal templates: only the `owner_id` can view/edit.
- Org-wide templates: only `base.group_system` or a future `clinicflow.group_manager` can create/edit.
- All staff can read org-wide templates for selection purposes.

### Menu Placement

Will appear under `ClinicFlow > Templates > SOAP Templates` — consistent with the existing `Outreach Templates` sub-item already under `Templates`.

### Dependencies

- Requires `clinicflow_clinical` (visit + SOAP model).
- Can be built standalone as `clinicflow_clinical` already owns SOAP fields.
- No new module needed — add to `clinicflow_clinical` unless template complexity justifies a `clinicflow_templates` module later.

### Target Sprint

Not yet scheduled. Candidate for **Sprint 8** or after Voice Dictation is evaluated (Sprint 8 is currently Voice Dictation — may push to Sprint 8.5 or Sprint 9 depending on priority).

---

## Log Guidelines

When a feature is requested:
1. **Log it immediately**: Add it to this list.
2. **Assign priority**:
   - **High**: Blocks standard daily workflow or significantly slows down operations compared to DaySmart.
   - **Medium**: Annoying/cumbersome but has a clear workaround.
   - **Low**: Nice-to-have aesthetic or luxury feature.
3. **Review weekly**: Vets and the development team should review this list to promote critical fixes to active sprints.
