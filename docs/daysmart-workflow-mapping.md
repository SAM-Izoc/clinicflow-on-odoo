# DaySmart Vet to ClinicFlow Workflow Mapping

This document maps DaySmart Vet workflows to the equivalent views and actions in ClinicFlow (Vet OS on Odoo). Use this as a reference guide during user training and the Tomken pilot.

## Core Workflow Comparison

| DaySmart Vet Action / Screen | ClinicFlow (Odoo CE) Location | Native / Custom | Workflow / Navigation Description |
| :--- | :--- | :--- | :--- |
| **Patient Overview** | `Patients` -> Form View -> persistent summary header & quick details | Custom (`clinicflow.pet`) | Central Patient 360 dashboard showing photo, species, breed, gender, age, owner, alerts, and emergency contact details. |
| **Patient Search** | `Patients` -> List View / Kanban View / Search Bar | Custom / Native | Use the top-right search box in Patients view to search by Pet Name, Owner, Species, Breed, etc. |
| **Medical History** | `Patients` -> Form View -> **Medical History** tab | Custom (`clinicflow.pet`) | Text grids containing persistent, editable records of chronic conditions, allergies, and surgical history. |
| **Weight Logs** | `Patients` -> Form View -> **Profile** tab -> Weight History table | Custom (`clinicflow.weight.record`) | Add weights directly with dates and notes in the list. Tracks changes over time. |
| **Clinician SOAP Notes** | `Operations -> Visits` OR `Patients -> Visits` tab | Custom (`clinicflow.visit`) | Structured clinical record with **Subjective, Objective, Assessment, and Plan (SOAP)** text boxes. |
| **Create Appointment** | `Appointments` -> Calendar | Native (`calendar.event`) | Native Odoo calendar interface. Double-click any cell to book a time slot and select the pet owner as partner. |
| **Issue Medication** | `Operations -> Visits` -> **Prescriptions** tab | Custom (`clinicflow.prescription`) | Create medication prescription lines linked directly to Odoo inventory (`product.product`). |
| **Administer Vaccine** | `Operations -> Vaccinations` OR `Patients -> Vaccinations` | Custom (`clinicflow.vaccination`) | Tracks administered and scheduled vaccines, linking products to Odoo catalog. |
| **Generate Invoice / Bill** | `Operations -> Visits` -> **Create Invoice** button | Native Integration (`account.move`) | Generates a native Odoo Invoice (`account.move`) containing all visit charges and prescription products, linking it directly to the customer. |
| **Review Invoices / Bills** | `Patients` -> Form View -> **Billing & Invoices** tab | Native / Custom | List of all draft and posted invoices showing numbers, total amounts, and payment states. |
| **Chronological Feed** | `Patients` -> Form View -> **Timeline** tab | Custom (`clinicflow.timeline.event`) | Automatically aggregates and logs all clinic activity (Visits, Vaccinations, Prescriptions, Admissions, Invoices) chronologically. |
| **Hospital Stays** | `Hospitalizations` OR `Patients -> Hospitalizations` tab | Custom (`clinicflow.admission`) | Track active hospital admissions, reasons for admission, and discharge statuses. |

---

## Detailed Step-by-Step Walkthroughs

### 1. Registering a Patient and Owner
1. Go to **Patients** menu and click **New**.
2. Fill out Pet Name, Species, Breed, Gender, DOB, and choose or create the **Owner** (Odoo Partner).
3. Fill in Emergency Contact and critical warnings (Allergies, Medical Alerts) which stay visible across all tabs.

### 2. Checking in a Patient
1. When a patient arrives, go to **Operations -> Visits** or click **Visits** and click **New**.
2. Select the Pet Patient (this auto-fills the Owner).
3. Set status to **Checked In** or **Waiting**. This registers a "Visit Created" event in the pet's timeline.

### 3. Consultation & Prescribing
1. During exam, change status to **Consultation**.
2. Document clinical notes in the **SOAP Clinical Notes** tab.
3. If prescribing medication, go to the **Prescriptions** tab, add a line, select the product/medication, set dosage frequency, and add instructions.
4. Set status to **Treatment** when administering treatments.

### 4. Billing the Client
1. When consultation is complete, update the status to **Billing Pending**.
2. Go to the **Charges & Invoicing** tab on the Visit form. Add any service charges (e.g., consultation fees, diagnostic fees).
3. Click **Create Invoice** button in the header. ClinicFlow automatically compiles the service charges and prescription products into a standard Odoo Customer Invoice.
4. Click into the generated Invoice to print, email, or register a payment.
