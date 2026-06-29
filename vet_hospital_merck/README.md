# Merck Vet Manual Integration Module for Odoo Veterinary Hospital

## 🔍 Overview

This module integrates **Merck Vet Manual** (https://www.merckvetmanual.com/) directly into your Odoo Veterinary Hospital system, allowing veterinarians to quickly search medical information without leaving Odoo.

**Merck Vet Manual** is the world's most trusted source of veterinary medicine information used by veterinary professionals globally.

---

## ✨ Features

### 🎯 One-Click Search Buttons

**Medical Records (SOAP):**
- 🔍 **Search Diagnosis** - Search primary diagnosis from SOAP note
- 🔍 **Search Symptoms** - Search chief complaints and symptoms
- 🔍 **Search Treatment** - Search treatment plan in Merck
- 🔍 **Search Assessment** - Search assessment/diagnosis details

**Prescriptions:**
- 🔍 **Search Drug Info** - Look up medication details
- 🔍 **Search Indication** - Search drug indication and uses

**Vital Signs:**
- 🔍 **Search Abnormality** - Search abnormal vital signs information

**Patients:**
- 🔍 **Search Breed Info** - Get breed-specific health information
- 🔍 **Search Conditions** - Search medical conditions

**Diagnosis:**
- 🔍 **Search in Merck** - Quick diagnosis lookup

---

## 📦 Installation

### Prerequisites
- Odoo 19 Community Edition
- Veterinary Hospital Module (vet_hospital) installed

### Installation Steps

1. **Extract the module:**
   ```bash
   tar -xzf vet_hospital_merck.tar.gz
   cp -r vet_hospital_merck /path/to/odoo/addons/
   ```

2. **Restart Odoo:**
   ```bash
   systemctl restart odoo
   ```

3. **Update Apps List:**
   - Go to Settings → Apps
   - Click "Update Apps List"

4. **Install Module:**
   - Search for "Veterinary Hospital - Merck"
   - Click Install

---

## 🚀 Usage Guide

### Searching from Medical Records

1. **Open Medical Record**
   - Go to Medical Records → Select a record

2. **Look for Merck Buttons in Header**
   - 🔍 **Merck: Diagnosis** - Search the diagnosis
   - 🔍 **Merck: Symptoms** - Search patient symptoms
   - 🔍 **Merck: Treatment** - Search treatment plan
   - 🔍 **Merck: Assessment** - Search assessment

3. **Click Any Button**
   - Merck Vet Manual opens in new tab
   - Search results match your term
   - Review information and return to Odoo

### Searching from Prescriptions

1. **Open Prescription**
   - Go to Prescriptions → Select a prescription

2. **Click Merck Buttons**
   - 🔍 **Merck: Drug Info** - Search medication details
   - 🔍 **Merck: Indication** - Search drug indication/use

3. **Reference Information**
   - Verify dosage, interactions, contraindications
   - Return to prescription with information

### Searching from Vital Signs

1. **Open Vital Signs Record**
   - Go to Vital Signs → Select a record

2. **If Abnormalities Detected**
   - Click 🔍 **Merck: Abnormality** button
   - Research abnormal findings
   - Reference in medical record

### Searching from Patients

1. **Open Patient**
   - Go to Patients → Select a patient

2. **Click Search Buttons**
   - 🔍 **Merck: Breed Info** - Get breed health info
   - 🔍 **Merck: Conditions** - Search medical conditions

3. **Use Information**
   - Understand breed-specific issues
   - Reference for health decisions

### Searching from Diagnosis

1. **Open Diagnosis Record**
   - Go to Medical Records → Diagnosis Codes

2. **Click 🔍 Search in Merck**
   - Quick diagnosis lookup
   - Verify classification and details

---

## 🔗 How It Works

The module uses Merck Vet Manual's search functionality via URL parameters:

```
https://www.merckvetmanual.com/search?query=[your_search_term]
```

**Process:**
1. Click a Merck button
2. Module extracts relevant information (diagnosis, medication, etc.)
3. Information is URL-encoded
4. Merck search URL is generated
5. Merck opens in new browser tab
6. Search results display in Merck
7. Veterinarian reviews and returns to Odoo

---

## 📋 Search Scope

### What Gets Searched

| Module | Search Content | Source |
|--------|----------------|--------|
| Medical Record | Primary diagnosis name | `primary_diagnosis_id.name` |
| Medical Record | Chief complaint/symptoms | First line of `subjective` field |
| Medical Record | Treatment plan | First line of `plan` field |
| Medical Record | Assessment | First line of `assessment` field |
| Prescription | Medication name | `product_id.name` |
| Prescription | Indication/use | First line of `instructions` |
| Vital Signs | Abnormality details | `abnormalities` field |
| Patient | Breed health info | `breed_id.name + " health"` |
| Patient | Medical conditions | First listed condition |
| Diagnosis | Diagnosis description | `name` field |

### Search Limitations

- **Term Length:** Limited to 100 characters (auto-truncated)
- **Content:** Only text fields are searched (no binary data)
- **Language:** English only (Merck database limitation)
- **Connection:** Requires internet access to Merck website

---

## 🎯 Use Cases

### 1. **Verify Diagnosis**
```
Medical Record → Click "Merck: Diagnosis"
→ Verify diagnosis classification and symptoms
→ Confirm correct treatment approach
```

### 2. **Check Drug Information**
```
Prescription → Click "Merck: Drug Info"
→ Review dosage guidelines for species/weight
→ Check interactions and contraindications
→ Verify side effects
```

### 3. **Research Abnormal Vitals**
```
Vital Signs (with abnormalities) → Click "Merck: Abnormality"
→ Understand what abnormality means
→ Find treatment information
→ Identify related conditions
```

### 4. **Breed-Specific Care**
```
Patient → Click "Merck: Breed Info"
→ Learn breed predispositions
→ Understand health concerns
→ Prepare preventive care
```

### 5. **Treatment Planning**
```
Medical Record → Click "Merck: Treatment"
→ Review treatment options
→ Verify recommended protocols
→ Access clinical guidelines
```

---

## 💡 Tips & Best Practices

### 1. **Use in Context**
- Open Merck while editing medical records
- Keep Merck tab available during consultation
- Reference information for documentation

### 2. **Search Refinement**
- If first search doesn't yield results, try more general terms
- Example: "Diabetes" instead of "Diabetes mellitus"
- Try species name: "Feline diabetes"

### 3. **Cross-Reference**
- Compare information across multiple searches
- Verify information from multiple Merck sources
- Document findings in medical record

### 4. **Time Management**
- Quick searches during appointment breaks
- Not meant to replace formal diagnosis
- Use for quick reference and verification

### 5. **Documentation**
- Include Merck sources in medical notes if applicable
- Record search results and clinical decisions
- Create audit trail for compliance

---

## 🔧 Configuration

### No Configuration Needed!

The module works out-of-the-box with:
- Pre-configured Merck search URLs
- Automatic term encoding
- One-click access

### Optional: Custom Search Terms

If you want to add custom searches:

1. **Extend the module:**
   ```python
   class PatientCustom(models.Model):
       _inherit = 'vet.patient'
       
       def action_custom_search(self):
           search_term = self.your_field
           return self._search_merck(search_term)
   ```

2. **Add button in view:**
   ```xml
   <button name="action_custom_search" type="object" string="🔍 Custom Search"/>
   ```

---

## 🌐 Merck Vet Manual Resources

### Popular Search Topics

- **Diseases:** Diabetes, arthritis, otitis, dermatitis
- **Medications:** Antibiotics, pain relievers, vaccines
- **Species:** Canine, feline, equine, exotic animal health
- **Breed Info:** Breed predispositions, genetic conditions
- **Procedures:** Surgery pre-op, diagnostics, treatments
- **Anatomy:** Organ systems, physiology, pathology

### Direct Links

- **Merck Vet Manual Main:** https://www.merckvetmanual.com/
- **Canine Section:** https://www.merckvetmanual.com/dog-owners
- **Feline Section:** https://www.merckvetmanual.com/cat-owners
- **Professional Version:** https://www.merckvetmanual.com/ (login required for some content)

---

## ⚙️ How Buttons Appear

### Medical Record Form
```
Header Buttons:
🔍 Merck: Diagnosis  |  🔍 Merck: Symptoms  |  🔍 Merck: Treatment  |  🔍 Merck: Assessment
```

### Prescription Form
```
Header Buttons:
🔍 Merck: Drug Info  |  🔍 Merck: Indication
```

### Patient Form
```
Header Buttons:
🔍 Merck: Breed Info  |  🔍 Merck: Conditions
```

### Vital Signs Form
```
Header Buttons:
🔍 Merck: Abnormality
```

Buttons automatically **hide** if relevant data is not available.

---

## 🔍 What Happens When You Click

1. **Button Click**
   - Extracts relevant data from current record
   - Encodes text for URL
   - Generates Merck search URL

2. **New Tab Opens**
   - Merck Vet Manual website loads
   - Search results display automatically
   - Your search term shown in search box

3. **You Can**
   - Browse search results
   - Click on articles
   - Read full information
   - Switch tabs between Odoo and Merck

4. **Return to Odoo**
   - Use Merck information for decisions
   - Document findings in medical record
   - Continue with treatment planning

---

## 🛡️ Privacy & Security

### Important Notes

1. **No Data Sent to Odoo**
   - Searches go directly to Merck
   - Only search term is transmitted
   - No patient data leaves your Odoo

2. **No Account Required**
   - Merck searches don't require login
   - Free access to information
   - Anonymous searches

3. **External Website**
   - Merck runs independently
   - Subject to their privacy policy
   - Follow their terms of service

---

## 📊 Compatibility

| Component | Requirement | Status |
|-----------|-------------|--------|
| Odoo | 19.0 Community | ✅ Compatible |
| Veterinary Module | vet_hospital | ✅ Required |
| Internet Connection | Needed for Merck | ✅ Required |
| Browser | Modern browser | ✅ Chrome, Firefox, Safari, Edge |
| Python | 3.8+ | ✅ Compatible |

---

## 🐛 Troubleshooting

### Issue: Buttons Don't Appear

**Solution:** 
- Ensure module is installed (Settings → Apps → Search "Merck")
- Refresh page (Ctrl+F5)
- Check that parent data exists (diagnosis, medication, etc.)

### Issue: Merck Site Doesn't Load

**Solution:**
- Check internet connection
- Verify browser allows pop-ups
- Check Merck website is accessible (https://www.merckvetmanual.com/)

### Issue: Search Returns No Results

**Solution:**
- Try more general search term
- Use species name (add "canine" or "feline")
- Try synonym (e.g., "UTI" instead of "urinary tract infection")

### Issue: URL Encoding Issues

**Solution:**
- Avoid special characters in search fields
- Keep search terms under 100 characters
- Use simple, common medical terms

---

## 📝 Examples

### Example 1: Diabetes Diagnosis

**Workflow:**
1. Open Medical Record with diabetes diagnosis
2. Click 🔍 **Merck: Diagnosis**
3. Merck opens: "diabetes in dogs"
4. Review:
   - Symptoms
   - Diagnostic procedures
   - Treatment options
   - Management protocols
5. Return to Odoo and document findings

### Example 2: Medication Review

**Workflow:**
1. Open Prescription for Insulin
2. Click 🔍 **Merck: Drug Info**
3. Merck opens with insulin information
4. Verify:
   - Dosage (mg/kg/day)
   - Administration route
   - Interactions
   - Side effects
5. Confirm prescription is appropriate

### Example 3: Abnormal Temperature

**Workflow:**
1. Open Vital Signs showing high temperature (41°C)
2. Click 🔍 **Merck: Abnormality**
3. Merck opens with fever information
4. Learn:
   - Differential diagnoses
   - Related symptoms
   - Treatment approaches
5. Return and update medical record

---

## 🚀 Advanced Usage

### Custom Module Extension

To add more search capabilities:

```python
# vet_hospital_merck_custom/models.py
from odoo import models

class MedicalRecordCustom(models.Model):
    _inherit = 'vet.medical_record'
    
    def action_search_merck_species_condition(self):
        """Search species + condition"""
        species = self.patient_id.species_id.name
        condition = self.primary_diagnosis_id.name
        search_term = f"{species} {condition}"
        return self._open_merck_search(search_term)
```

---

## 📞 Support & Documentation

### Resources

- **Merck Vet Manual:** https://www.merckvetmanual.com/
- **Merck Professional Version:** https://www.merckvetmanual.com/professional (for veterinarians)
- **Odoo Documentation:** https://www.odoo.com/documentation/19.0/

### Getting Help

1. Check this README
2. Review troubleshooting section
3. Verify module installation
4. Clear browser cache (Ctrl+Shift+Delete)
5. Contact your Odoo administrator

---

## 📋 Version History

### v1.0.0 (Initial Release)
- Medical record diagnosis search
- Prescription drug information search
- Vital signs abnormality search
- Patient breed information search
- Diagnosis quick search
- Integrated menu items

---

## 📄 License & Credits

**License:** LGPL-3  
**Author:** Vaterny Hospital Team  
**Odoo Version:** 19.0 Community Edition  
**Category:** Healthcare Integration  

---

## ✅ Checklist

After installation:

□ Module appears in Settings → Apps  
□ Merck buttons visible in Medical Record form  
□ Merck buttons visible in Prescription form  
□ Merck buttons visible in Patient form  
□ Merck buttons visible in Vital Signs form  
□ Clicking button opens Merck in new tab  
□ Search term pre-populated in Merck  
□ Results display correctly  
□ Menu item "Merck Vet Manual" appears in sidebar  

---

## 🎯 Next Steps

1. **Install the module**
2. **Open a medical record**
3. **Click a Merck button**
4. **Browse Merck Vet Manual**
5. **Return and document findings**

---

## 🌟 Key Benefits

✅ **Time-Saving:** One-click access to Merck information  
✅ **Reference-Friendly:** Don't leave Odoo  
✅ **Integrated:** Seamless workflow  
✅ **Free:** Uses Merck's public search  
✅ **Reliable:** Merck is trusted by veterinarians worldwide  
✅ **Easy:** No configuration needed  
✅ **Secure:** No data shared with Merck  

---

## 🎓 Educational Value

Perfect for:
- **Learning:** Expand veterinary knowledge
- **Verification:** Confirm diagnoses and treatments
- **Reference:** Quick lookup during consultations
- **Compliance:** Document evidence-based decisions
- **Training:** Support continuing education

---

## 📮 Feedback

If you have suggestions for improvements:
1. Document your request
2. Include use case
3. Submit to your Odoo administrator
4. We'll evaluate for future updates

---

**Version:** 19.0.1.0.0  
**Last Updated:** June 2026  
**Status:** ✅ Ready for Production Use  

🐾 **Happy Veterinary Practice!**

---

For the most current information, visit:
- **Merck Vet Manual:** https://www.merckvetmanual.com/
- **Odoo Veterinary Hospital:** Your Odoo installation
