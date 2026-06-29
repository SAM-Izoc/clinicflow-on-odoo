# Veterinary Hospital Module - Directory Structure

## 📁 Module Structure

```
vet_hospital/
├── __init__.py                          # Module initialization
├── __manifest__.py                      # Module metadata
├── README.md                            # Installation & usage guide
│
├── models/
│   ├── __init__.py                      # Models initialization
│   ├── owner.py                         # Owner & Veterinarian models
│   ├── patient.py                       # Patient, Species, Breed models
│   ├── appointment.py                   # Appointment & AppointmentType models
│   ├── medical_record.py                # Medical Record, Diagnosis, LabResult models
│   ├── vital_sign.py                    # VitalSign model with validation
│   └── prescription.py                  # Prescription & MedicineProduct models
│
├── views/
│   ├── menu.xml                         # Main menu structure
│   ├── owner_views.xml                  # Owner/Veterinarian views
│   ├── patient_views.xml                # Patient, Species, Breed views
│   ├── appointment_views.xml            # Appointment & Type views
│   ├── medical_record_views.xml         # Medical Record & Diagnosis views (SOAP)
│   ├── vital_sign_views.xml             # Vital Signs & Prescription views
│   ├── prescription_views.xml           # (placeholder)
│   └── dashboard_views.xml              # Dashboard view
│
├── security/
│   └── ir.model.access.csv              # Access control rules
│
├── data/
│   ├── appointment_type_data.xml        # Pre-loaded appointment types & sequences
│   └── species_data.xml                 # Pre-loaded animal species & breeds
│
└── reports/
    ├── medical_record_report.xml        # Medical record PDF report
    ├── appointment_report.xml           # Appointment report
    └── invoice_report.xml               # Invoice report

```

## 📚 Models Breakdown

### 1. **owner.py** - Contact Management
Classes:
- `Owner` (inherits res.partner)
  - Pet owner information
  - Notification preferences
  - Patient relationships
  - Statistics (total patients, total spent)
  
- `Veterinarian` (inherits res.partner)
  - License information
  - Specialization
  - Working hours (7-day schedule)
  - Appointment and medical record links

### 2. **patient.py** - Patient Records
Classes:
- `Patient`
  - Complete patient profile
  - Microchip tracking
  - Species/Breed relationships
  - Medical history
  - Vital statistics
  - Relationships: Appointments, Medical Records, Vital Signs, Prescriptions
  
- `Species`
  - Animal species catalog
  - Scientific names
  - Breed associations
  
- `Breed`
  - Breed information
  - Average weight & life expectancy
  - Species association

### 3. **appointment.py** - Scheduling System
Classes:
- `Appointment`
  - Appointment booking & management
  - Status workflow (scheduled → completed)
  - Automatic conflict detection
  - Reminder system
  - Medical record linkage
  - Invoice integration
  
- `AppointmentType`
  - Type definitions (wellness, surgery, etc.)
  - Duration and default pricing
  - Categories for organization

### 4. **medical_record.py** - Medical Documentation
Classes:
- `MedicalRecord` (SOAP Format)
  - Subjective: Chief complaint & history
  - Objective: Physical exam findings
  - Assessment: Diagnosis information
  - Plan: Treatment recommendations
  - Vital signs recording
  - Lab results
  - Prescription linkage
  - Invoice generation
  - Follow-up tracking
  
- `Diagnosis`
  - Diagnosis code system
  - Category classification
  - Searchable diagnosis database
  
- `LabResult`
  - Lab test records
  - Results with reference values
  - Status tracking (normal/abnormal/critical)
  - Report attachment support

### 5. **vital_sign.py** - Health Metrics
Classes:
- `VitalSign`
  - Comprehensive vital recording
  - Automatic validation:
    - Temperature normality
    - Heart rate (species-specific)
    - Respiration normality
    - Blood pressure check
    - Weight change calculation
  - Abnormality alerting
  - Hydration assessment
  - Body condition scoring
  - Behavioral observation

### 6. **prescription.py** - Medication Management
Classes:
- `Prescription`
  - Complete prescription system
  - Dosage & frequency tracking
  - Route of administration
  - Refill management
  - Expiry tracking
  - Side effects/warnings
  - Controlled substance flagging
  - Medication label generation
  
- `MedicineProduct` (inherits product.product)
  - Medicine classification
  - Active ingredients
  - Veterinary approval status
  - Dosage guidelines
  - Drug interaction documentation

## 🔄 Workflow Integration

### Typical Patient Journey:

1. **Owner Creation**
   - Contact marked as "Is Pet Owner"
   - Sets notification preferences

2. **Patient Registration**
   - Link to owner
   - Species/Breed selection
   - Medical history

3. **Appointment Booking**
   - Veterinarian assignment
   - Time slot selection
   - Reason for visit

4. **Medical Documentation**
   - SOAP note creation
   - Vital signs recording
   - Lab results entry
   - Prescription generation

5. **Billing**
   - Invoice auto-generation
   - Service charges
   - Medication costs
   - Payment tracking

## 🔐 Security Model

### Access Groups:
- **Base User:** Read/Write on own records
- **Veterinary Hospital User:** Read/Write/Create on all
- **System Administrator:** Full access including delete

### Field-level Security:
- Read-only fields: Auto-calculated values
- Restricted deletion: Archived records
- Audit trail: Change logging via mail.thread

## 📊 Key Features by Model

### Patient
- ✅ Photo storage
- ✅ Microchip ID tracking
- ✅ Medical condition logging
- ✅ Allergy management
- ✅ Weight history
- ✅ Next appointment prediction
- ✅ Total invoiced tracking

### Appointment
- ✅ Automatic conflict detection
- ✅ Email reminders
- ✅ Status workflow
- ✅ Medical record linkage
- ✅ Calendar view integration
- ✅ Duration calculation

### Medical Record (SOAP)
- ✅ Structured SOAP format
- ✅ Diagnosis linking
- ✅ Lab result attachment
- ✅ Automatic invoice generation
- ✅ Follow-up scheduling
- ✅ Document archiving

### Vital Signs
- ✅ Automatic normality checking
- ✅ Species-specific ranges
- ✅ Weight change tracking
- ✅ Abnormality highlighting
- ✅ Body condition scoring

### Prescription
- ✅ Medication library
- ✅ Dosage validation
- ✅ Refill management
- ✅ Controlled substance flagging
- ✅ Drug interaction warnings
- ✅ Medication label generation

## 🔗 Database Relationships

```
res.partner (Owner)
    ↓ (is_owner)
    └─→ vet.patient
        ├─→ vet.appointment
        │   └─→ vet.medical_record
        │       ├─→ vet.vital_sign
        │       ├─→ vet.prescription
        │       │   └─→ product.product (is_medicine)
        │       ├─→ vet.diagnosis
        │       ├─→ vet.lab_result
        │       └─→ account.move (invoice)
        └─→ vet.species
            └─→ vet.breed

res.partner (Veterinarian)
    ↓ (is_vet)
    ├─→ vet.appointment
    └─→ vet.medical_record
```

## 🎯 Customization Points

### To Extend This Module:

1. **Add Custom Fields**
   ```python
   # In new module inheriting vet_hospital
   from odoo import models, fields
   
   class PatientCustom(models.Model):
       _inherit = 'vet.patient'
       custom_field = fields.Char()
   ```

2. **Override Views**
   ```xml
   <!-- In XML view file -->
   <record id="custom_patient_form" model="ir.ui.view">
       <field name="inherit_id" ref="vet_hospital.view_vet_patient_form"/>
       <!-- Your modifications -->
   </record>
   ```

3. **Add Custom Reports**
   - Add to reports/ directory
   - Reference in __manifest__.py

4. **Create Automated Actions**
   - Use Odoo's automation framework
   - Example: Auto-send reminder 24hrs before appointment

## 📈 Performance Considerations

- **Indexes:** Patient ID, Appointment Date, Diagnosis
- **Search Optimization:** Use filters for date ranges
- **Archive:** Move completed records to archived status
- **Report Caching:** Use Odoo's cache for repeated queries

## 🚀 Deployment

### Production Checklist:
- [ ] Backup database before installation
- [ ] Test in staging environment
- [ ] Configure email for reminders
- [ ] Set up backup appointments
- [ ] Train veterinary staff
- [ ] Import historical data
- [ ] Configure billing integration
- [ ] Set working hours for vets
- [ ] Create appointment types
- [ ] Load species/breeds

---

**Module Version:** 19.0.1.0.0
**Odoo Version:** Odoo 19 Community Edition
**License:** LGPL-3
