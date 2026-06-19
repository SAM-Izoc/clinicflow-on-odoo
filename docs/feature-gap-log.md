# ClinicFlow Feature Gap Log

Use this document to log all requested features, gaps, and improvements identified by Tomken clinic staff during the pilot phase. Do not build these features immediately; track them here to prioritize after workflows stabilize.

## Gap Log Table

| Feature Description | Requested By | Frequency / Impact | Priority (High/Med/Low) | Status (Backlog/Review/In-Progress) | Target Sprint | Notes / Workaround |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WhatsApp Notifications** | Receptionist | High - DaySmart sends auto-reminders via SMS/WhatsApp | High | Backlog | Sprint 4+ (Future) | Currently handled manually or via native Odoo Email templates. |
| **Owner Portal** | Clients / Managers | Medium - Owners like downloading vaccine certificates | Medium | Backlog | Future | Currently, reception staff prints/emails PDF certificates directly. |
| **Automated SOAP Templates** | Vets | High - Pre-filled text templates based on visit reason | High | Review | Sprint 4+ (AI SOAP) | Vets currently copy-paste standard text templates manually. |
| **Multi-Doctor Scheduling Colors** | Clinic Manager | Medium - Color-coding calendar events by Veterinarian | Med | Backlog | Sprint 2 (Ops) | Calendar view currently colors events by doctor name, but needs refined styling. |
| **Reorder Warnings on Pharmacy** | Vets / Inventory | Low - Alerts when drug stock drops below threshold | Med | Review | Sprint 3 (Stock) | Odoo Inventory reordering rules can handle this natively. |

---

## Log Guidelines

When a feature is requested:
1. **Log it immediately**: Add it to this list.
2. **Assign priority**:
   - **High**: Blocks standard daily workflow or significantly slows down operations compared to DaySmart.
   - **Medium**: Annoying/cumbersome but has a clear workaround.
   - **Low**: Nice-to-have aesthetic or luxury feature.
3. **Review weekly**: Vets and the development team should review this list to promote critical fixes to active sprints.
