# ClinicFlow UX Refactor – Patient-Centric Veterinary Workflow

## Background

After reviewing the current ClinicFlow implementation and comparing it to DaySmart Vet, we have identified a fundamental UX issue.

The current ClinicFlow navigation is model-centric:

* Patients
* Visits
* Hospitalizations
* Vaccinations
* Prescriptions

This reflects the database structure rather than how veterinary staff actually work.

Veterinarians, receptionists, and clinic managers think in terms of the patient journey, not individual database entities.

Our goal is to evolve ClinicFlow into a patient-centric Veterinary Operating System where the patient record becomes the primary workspace.

---

# Objective

Refactor the information architecture and UI so that:

* Patient becomes the primary entity.
* Most daily actions occur from within the patient record.
* Related information is grouped and interconnected.
* Users can navigate the complete medical history of an animal from a single screen.

The target experience should be inspired by DaySmart Vet and other modern veterinary PMS systems, while remaining fully aligned with Odoo architecture.

---

# Information Architecture Changes

## Current Navigation

Patients
Visits
Hospitalizations
Vaccinations
Prescriptions

## New Navigation

Patients
Appointments
Hospitalizations
Billing
Reports
Configuration

### Notes

Visits, Vaccinations, Prescriptions, Medical Records, Documents, and Invoices should no longer be primary navigation items.

These become components of the Patient 360 View.

---

# Patient 360 View

The Patient screen (clinicflow.pet) must become the primary operational workspace.

When opening a patient, users should have access to all relevant information without navigating through multiple menus.

Implement notebook tabs/pages on the patient form.

---

## Tab: Profile

Display:

* Photo
* Name
* Species
* Breed
* Gender
* Date of Birth
* Age
* Weight
* Microchip
* Owner
* Emergency Contact
* Alerts

Purpose:

Quick clinical overview.

---

## Tab: Medical History

Display:

* Chronic Conditions
* Allergies
* Surgical History
* Clinical Alerts
* Notes

Purpose:

Persistent health information.

---

## Tab: Visits

Display related clinicflow.visit records.

Columns:

* Date
* Veterinarian
* Reason
* Status

Opening a visit should display full SOAP details.

---

## Tab: Vaccinations

Display:

* Vaccine
* Date Administered
* Due Date
* Status

Future support:

* Vaccine protocols
* Automatic due schedules

---

## Tab: Prescriptions

Display:

* Medication
* Dosage
* Quantity
* Instructions
* Date

Purpose:

Medication history.

---

## Tab: Hospitalizations

Display:

* Admission Date
* Discharge Date
* Status
* Assigned Vet

Purpose:

Track inpatient care.

---

## Tab: Billing

Integrate with native Odoo accounting.

Display:

* Invoice Number
* Date
* Amount
* Payment Status
* Outstanding Balance

Pull data directly from account.move.

No custom billing models.

---

## Tab: Documents

Integrate with Odoo Documents.

Display:

* Lab Reports
* X-Rays
* Ultrasounds
* Clinical Photos
* Consent Forms

Allow drag-and-drop upload.

---

## Tab: Timeline

Create a chronological patient activity stream.

Example:

2026-06-19 Visit Created
2026-06-19 Prescription Issued
2026-06-19 Invoice Generated
2026-05-15 Vaccination Administered
2026-04-10 Surgery Completed

This should become the fastest way to understand a patient's history.

This is a high-priority differentiator.

---

# Model Adjustments

## Keep

clinicflow.pet
clinicflow.visit
clinicflow.vaccination
clinicflow.prescription
clinicflow.admission

## Maintain Odoo Integrations

res.partner
calendar.event
product.product
account.move
documents.document

Do not duplicate native Odoo functionality.

---

# Appointment Strategy

Do NOT merge clinicflow.visit into calendar.event.

Instead:

clinicflow.visit
Many2one(calendar.event)

Reason:

An appointment is scheduling data.

A visit is a medical record.

They are different concepts.

Maintain separation.

---

# Future Features

Prepare architecture for:

* Weight history tracking
* Vaccine protocols
* AI SOAP generation
* Owner portal
* WhatsApp reminders
* Lab integrations

Do not implement immediately unless required.

Ensure design does not block these future enhancements.

---

# Deliverables

Produce:

1. Updated menu architecture.
2. Revised XML views for Patient 360.
3. Model relationship review.
4. Timeline implementation proposal.
5. Wireframe/mockup descriptions for Patient 360 View.
6. Migration plan from current navigation to patient-centric navigation.

The Patient 360 View should become the primary daily workspace for veterinarians and receptionists.

Success criterion:

A veterinarian should be able to access 80–90% of all patient-related information without leaving the patient record screen.
