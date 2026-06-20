# ClinicFlow Terminology Alignment: Clinician UX vs. System Architecture

This guide documents system terminology guidelines, outlining the separation between **user-facing clinician language (UX)** and **internal domain models (Architecture)**.

---

## 1. The Core Philosophy

When building complex clinical and veterinary operating systems, a common mistake is matching the technical database domain models directly with the user interface labels. 

To ensure high usability for veterinarians, nurses, and receptionists:
* **The User Interface must speak the natural language of the clinic** (e.g., "Visits", "Consultations", "Prescriptions").
* **The System Architecture must utilize generic, scalable medical boundaries** (e.g., "Encounters", "Observations", "Orders").

---

## 2. Terminology Mapping Table

The table below contrasts what the clinical staff sees in the ClinicFlow UI versus what is represented in the database registry/code base:

| Clinician-Facing UI Term (UX) | Database/Code representation | Purpose & Scope |
| :--- | :--- | :--- |
| **Patients** | `clinicflow.pet` | Animal profile (species, breed, microchip, weight). |
| **Appointments** | `calendar.event` | Scheduling block representing expected patient arrivals. |
| **Consultations** / **Visits** | `clinicflow.visit` (Architectural *Encounter*) | The root clinical container. Contains all consultation SOAP notes, instructions, and diagnostics. |
| **Hospitalizations** | `clinicflow.admission` | Hospital stays (admissions/discharges/procedures). |
| **Prescriptions** | `clinicflow.prescription` (Architectural *Order*) | Clinical medication instructions (linked to inventory items). |
| **Vaccinations** | `clinicflow.vaccination` (Architectural *Order*) | Immunization log and due reminders. |
| **Billing** / **Invoices** | `account.move` | Financial invoices linked directly to the patient's owner.<br/>*Note: Odoo uses the term "move" because, in accounting, an invoice is a double-entry "journal entry" or "accounting move" that transfers balances. The `move_type` (e.g. `out_invoice`) determines if it is an Invoice, Bill, or general journal entry.* |

---

## 3. The "Encounter" Concept

An **Encounter** is defined as any clinical interaction between a provider and a patient. While systems like Epic, Cerner, or OpenMRS use "Encounter" internally, clinicians are never exposed to this word. Instead, they interact with "Visits" or "Consultations".

For ClinicFlow:
* **UI Constraint**: Do not expose the word "Encounter" anywhere in the user interface. Continue using **Visit** or **Consultation** terminology.
* **Architectural Integration**: Treat `clinicflow.visit` as the implementation vehicle for an Encounter. Prescriptions, vaccinations, laboratory requests, invoices, and clinical documents must attach to this root visit. This modular structure allows the model to evolve into a generic `clinicflow.encounter` in the future without causing any UI disruption or database migration friction.
