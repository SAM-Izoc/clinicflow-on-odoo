# Veterinary Hospital Management System - Odoo 19 Community Edition

## 📋 Overview

A complete Veterinary Hospital Management Module for Odoo 19 Community Edition that includes:

- **Patient Management** - Complete patient records with medical history
- **Appointment Scheduling** - Calendar-based appointment system
- **Medical Records** - SOAP format (Subjective, Objective, Assessment, Plan)
- **Vital Signs Tracking** - Comprehensive vital signs monitoring with abnormality alerts
- **Prescription Management** - Medication prescriptions with dosage and refills
- **Owner/Client Management** - Contact management integrated with patients
- **Billing & Invoicing** - Automatic invoice generation from medical services
- **Reports** - Medical records, appointment, and financial reports

---

## 🚀 Installation

### 1. **Prerequisites**
- Odoo 19 Community Edition
- Database access
- Administrator privileges

### 2. **Download Module**
Copy the `vet_hospital` folder to your Odoo addons directory:
```
/path/to/odoo/addons/vet_hospital/
```

### 3. **Update Module List**
```bash
# Via Odoo CLI
odoo -d database_name -u base --update-module-list

# Or through Odoo Web Interface:
# 1. Go to Settings → Apps
# 2. Click "Update Apps List"
```

### 4. **Install Module**
1. Go to **Settings → Apps**
2. Search for "Veterinary Hospital Management"
3. Click **Install**

### 5. **Initial Setup**
After installation, you need to configure:

#### a) Create Species & Breeds
- Go to **Veterinary Hospital → Configuration → Species & Breeds**
- Add animal species and their breeds
- Pre-loaded data includes: Canine, Feline, Rabbit, Bird, Small Rodents, Reptiles

#### b) Create Appointment Types
- Go to **Veterinary Hospital → Schedule & Appointments → Appointment Types**
- Pre-loaded types: Wellness, Vaccination, Dental, Surgery, Treatment, Follow-up, Emergency

#### c) Add Veterinarians
- Go to **Contacts**
- Create new contacts and check "Is Veterinarian"
- Set specialization, license information, and working hours

#### d) Add Pet Owners
- Go to **Contacts** 
- Create new contacts and check "Is Pet Owner"
- Set emergency contact and notification preferences

---

## 📊 Module Features

### 1. **Patient Management**
- Complete patient profiles with photo, microchip ID
- Track species, breed, age, weight, medical conditions
- Link patients to owners
- View appointment history and medical records
- Track allergies and medications

**Menu:** Veterinary Hospital → Patient Management → Patients

### 2. **Appointment Scheduling**
- Create appointments with date, time, duration
- Assign to veterinarian
- Track appointment type (wellness, surgery, etc.)
- Support for appointment reminders via email
- Status tracking: Scheduled, Confirmed, In Progress, Completed, Cancelled, No Show
- Calendar view for easy scheduling

**Menu:** Veterinary Hospital → Schedule & Appointments → Appointments

### 3. **Medical Records (SOAP Format)**
The heart of the system - complete medical documentation:

**S - SUBJECTIVE:** Patient history and owner-reported symptoms
**O - OBJECTIVE:** Physical examination findings and observations
**A - ASSESSMENT:** Diagnosis/differential diagnoses
**P - PLAN:** Treatment plan and recommendations

Features:
- Automatic linkage to appointments
- Vital signs recording
- Lab results attachment
- Prescriptions link
- Automatic invoice generation
- Follow-up tracking

**Menu:** Veterinary Hospital → Medical Records → Medical Records

### 4. **Vital Signs Monitoring**
Track and monitor:
- Temperature (normal: 37.5-39°C)
- Heart Rate (dogs: 60-100 bpm, cats: 110-140 bpm)
- Respiration Rate (normal: 10-30 breaths/min)
- Blood Pressure
- Weight tracking with change calculation
- Body condition score
- Mucous membrane color
- Capillary refill time
- Hydration status

**Automatic Alerts:**
- Color-coded abnormal values (red highlighting)
- Summary of abnormalities in medical record

**Menu:** Veterinary Hospital → Medical Records → Vital Signs

### 5. **Prescription Management**
Complete prescription system:
- Link to medications
- Dosage and frequency specification
- Route of administration (oral, injection, topical, etc.)
- Special instructions
- Refill tracking
- Expiry date management
- Side effects and drug interactions
- Support for controlled substances

**Menu:** Veterinary Hospital → Prescriptions & Medications → Prescriptions

### 6. **Owner/Client Management**
Track:
- Contact information
- Emergency contact details
- Preferred veterinarian
- Notification preferences (email/SMS)
- All owned patients
- Total spent on veterinary services

**Menu:** Veterinary Hospital → Patient Management → Owners

### 7. **Billing & Invoicing**
- Automatic invoice generation from medical records
- Service charges for appointments
- Prescription costs
- Invoice tracking and payment status
- Owner billing history

**Menu:** Veterinary Hospital → Billing & Invoices

---

## 🔧 Configuration

### Working Hours Setup
For each veterinarian, configure working hours:
1. Go to **Contacts**
2. Select veterinarian
3. Scroll to "Working Hours" section
4. Set hours for each day (24-hour format)

### Appointment Types
Configure different appointment types with:
- Name
- Duration (in minutes)
- Default price
- Category (wellness, surgery, etc.)

### Species & Breeds
Add species with:
- Scientific name
- Description
- Associated breeds
- Average weight
- Life expectancy

---

## 📱 User Guide

### Creating a New Patient
1. Go to **Patient Management → Patients**
2. Click **Create**
3. Fill in:
   - Pet Name
   - Species & Breed
   - Owner
   - Physical characteristics (age, gender, weight, color)
   - Medical information (allergies, conditions)
4. Save

### Creating an Appointment
1. Go to **Schedule & Appointments → Appointments**
2. Click **Create**
3. Select:
   - Date & Time
   - Appointment Type
   - Patient
   - Veterinarian
   - Reason for visit
4. Click **Save & Confirm** (if confirmed)

### Recording Medical Record
1. From appointment, click **Create Medical Record**
2. Fill SOAP sections:
   - S: Owner's description of symptoms
   - O: Your physical exam findings
   - A: Your diagnosis
   - P: Treatment plan
3. Record vital signs
4. Add prescriptions
5. Add lab results if applicable
6. Click **Complete**
7. Click **Create Invoice** to generate billing

### Tracking Vital Signs
1. In Medical Record, go to **Vital Signs** tab
2. Click **Add a line**
3. Enter:
   - Date & Time
   - Vital measurements
   - Body condition score
4. Abnormal values auto-highlight in red

### Managing Prescriptions
1. In Medical Record, go to **Prescriptions** tab
2. Click **Add a line**
3. Select medication (must be marked as "Is Medicine")
4. Set:
   - Dosage
   - Frequency
   - Duration
   - Special instructions
5. System tracks refills and expiry

---

## 📈 Reports

### Medical Record Report
- Complete patient summary
- SOAP documentation
- Vital signs chart
- Prescriptions
- Lab results

**Access:** Right-click medical record → Print

### Appointment Report
- Appointment details
- Patient & owner info
- Veterinarian assigned
- Time slot information

**Access:** Right-click appointment → Print

### Billing Reports
- Invoice details
- Payment status
- Owner billing history

---

## 🔐 Security & Access Control

Default access levels:
- **Manager:** Full read/write/delete access
- **User:** Read/create/write (no delete) access
- **Read-only:** Limited to viewing records

### Customizing Access
1. Go to **Settings → Users & Companies → Users**
2. Select user
3. Modify group access:
   - Veterinary Hospital User (default)
   - System Administrator (full access)

---

## 🔗 Integration Notes

### With Accounting Module
- Invoices automatically created from medical records
- Links to sales orders for medications
- Revenue tracking by appointment type

### With Contacts Module
- Uses standard Odoo contact system
- Extended with veterinary fields
- Owner and veterinarian flags

### With Calendar Module
- Appointments visible in calendar view
- Color-coded by veterinarian
- Appointment reminders

---

## 📝 Common Tasks

### Setup a New Veterinarian
1. Go to **Contacts**
2. Create new contact
3. Check **Is Veterinarian**
4. Fill:
   - License Number
   - License Expiry
   - Specialization
   - Working hours
5. Save

### Send Appointment Reminder
1. Open appointment
2. Click **Send Reminder** button
3. Email automatically sent to owner

### Generate Medical Record from Completed Appointment
1. Go to appointment (status: Completed)
2. Click **Create Medical Record**
3. Pre-filled with appointment details
4. Complete SOAP documentation

### Create Bulk Invoice from Multiple Medical Records
1. Go to **Medical Records**
2. Filter by status: Completed
3. Select multiple records
4. Use action: **Create Invoices**

---

## 🐛 Troubleshooting

### Appointment Conflict Error
**Error:** "Time slot already booked for [Veterinarian]"
**Solution:** Choose different time or veterinarian

### Missing Appointment Type
**Error:** Cannot create appointment without type
**Solution:** Create appointment types in Configuration first

### Prescription Without Product
**Error:** Cannot save prescription without medication
**Solution:** Create product records marked as "Is Medicine"

### Abnormal Vital Sign Not Triggering Alert
**Solution:** Ensure vital value is outside normal range for species type

---

## 📞 Support & Documentation

### Fields Reference
All database fields are documented in the model files:
- `models/patient.py` - Patient details
- `models/appointment.py` - Appointment system
- `models/medical_record.py` - Medical records & diagnoses
- `models/vital_sign.py` - Vital signs with automatic validation
- `models/prescription.py` - Prescriptions & medications
- `models/owner.py` - Owner/veterinarian management

### API Customization
The module uses standard Odoo ORM. To customize:
1. Create a new module inheriting from vet_hospital
2. Override models or views
3. Example: `vet_hospital_custom/models/vet_patient.py`

---

## 🎓 Training

### For Veterinary Staff
- Focus on: Appointments, Medical Records, Vital Signs, Prescriptions
- Train on SOAP documentation format
- Explain medication management workflow

### For Administrative Staff  
- Focus on: Patients, Owners, Appointments, Billing
- Train on creating appointments and sending reminders
- Explain invoice generation

### For Management
- Focus on: Reports, Billing, Analytics
- Show dashboard for quick insights
- Explain revenue tracking by appointment type

---

## 📋 License & Credits

- **License:** LGPL-3
- **Author:** Vaterny Hospital Team
- **Odoo Version:** 19.0 Community Edition
- **Category:** Healthcare Management

---

## 🔄 Version History

### v1.0.0 (Initial Release)
- Patient management
- Appointment scheduling
- SOAP medical records
- Vital signs tracking
- Prescription management
- Basic billing integration
- Reports

---

## ✅ Checklist for Setup

- [ ] Module installed and running
- [ ] Species & Breeds configured
- [ ] Appointment Types created
- [ ] Veterinarians added
- [ ] First pet owner created
- [ ] First patient created
- [ ] First appointment scheduled
- [ ] Medical record created
- [ ] Vital signs recorded
- [ ] Prescription added
- [ ] Invoice generated
- [ ] Users configured with proper permissions

---

## 🚀 Next Steps

1. Customize appointment types for your clinic
2. Add your staff as veterinarians
3. Import existing clients as pet owners
4. Start scheduling appointments
5. Begin recording medical records
6. Generate reports for analysis

---

For more information or to report issues, please contact the development team.

Happy veterinary practice! 🐾
