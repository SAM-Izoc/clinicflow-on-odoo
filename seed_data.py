# seed_data.py
import datetime
from odoo import fields

# Create or find products
def get_or_create_product(name, ptype, list_price):
    product = env['product.product'].search([('name', '=', name)], limit=1)
    if not product:
        product = env['product.product'].create({
            'name': name,
            'type': ptype,
            'list_price': list_price,
            'sale_ok': True,
            'purchase_ok': False,
        })
        print(f"Created product: {name}")
    return product

# Products
consultation = get_or_create_product("General Consultation", "service", 50.0)
rabies = get_or_create_product("Rabies Vaccine", "consu", 25.0)
dhpp = get_or_create_product("DHPP Vaccine", "consu", 30.0)
dewormer = get_or_create_product("Deworming Medication", "consu", 15.0)
antibiotic = get_or_create_product("Antibiotic Injection (Convenia)", "service", 45.0)
amoxicillin = get_or_create_product("Amoxicillin Oral (100mg)", "consu", 20.0)

# Create owners (partners)
def get_or_create_partner(name, email, phone):
    partner = env['res.partner'].search([('name', '=', name)], limit=1)
    if not partner:
        partner = env['res.partner'].create({
            'name': name,
            'email': email,
            'phone': phone,
            'is_pet_owner': True,
            'is_company': False,
        })
        print(f"Created partner: {name}")
    return partner

owner_john = get_or_create_partner("John Doe", "john.doe@example.com", "+1-555-0199")
owner_mary = get_or_create_partner("Mary Smith", "mary.smith@example.com", "+1-555-0188")

# Create pets
def get_or_create_pet(name, species, breed, gender, dob, owner):
    pet = env['clinicflow.pet'].search([('name', '=', name), ('owner_id', '=', owner.id)], limit=1)
    if not pet:
        pet = env['clinicflow.pet'].create({
            'name': name,
            'species': species,
            'breed': breed,
            'gender': gender,
            'dob': fields.Date.from_string(dob),
            'owner_id': owner.id,
            'emergency_contact': f"{owner.name} ({owner.phone})",
            'alerts': "Slight heart murmur (Grade 1)" if name == "Max" else "",
            'chronic_conditions': "Arthritis" if name == "Max" else "None",
            'allergies': "Penicillin" if name == "Bella" else "None",
            'surgical_history': "Neutered on 2024-05-12" if name == "Max" else "Spayed on 2025-01-10",
        })
        print(f"Created pet: {name}")
    return pet

pet_max = get_or_create_pet("Max", "dog", "Golden Retriever", "neutered_male", "2021-03-15", owner_john)
pet_bella = get_or_create_pet("Bella", "cat", "Siamese", "spayed_female", "2023-08-20", owner_mary)

# Add weight records
def add_weight(pet, date, weight, notes=""):
    existing = env['clinicflow.weight.record'].search([('pet_id', '=', pet.id), ('date', '=', fields.Date.from_string(date))], limit=1)
    if not existing:
        env['clinicflow.weight.record'].create({
            'pet_id': pet.id,
            'date': fields.Date.from_string(date),
            'weight': weight,
            'notes': notes,
        })
        print(f"Added weight for {pet.name}: {weight}kg on {date}")

# Max weights
add_weight(pet_max, "2025-01-15", 32.5, "Initial checkup")
add_weight(pet_max, "2025-04-10", 33.1, "Healthy weight")
add_weight(pet_max, "2025-06-19", 34.2, "Recent visit")

# Bella weights
add_weight(pet_bella, "2025-02-20", 3.8, "First checkup")
add_weight(pet_bella, "2025-06-19", 4.1, "Annual wellness exam")

# Create a Visit, Prescription, Invoicing, etc.
def create_visit_flow(pet, date_str, vet_id, status, charges, prescription_products):
    visit_date = fields.Datetime.from_string(date_str)
    # Search if visit exists around that date
    visit = env['clinicflow.visit'].search([('pet_id', '=', pet.id), ('date', '>=', visit_date.replace(hour=0, minute=0, second=0)), ('date', '<=', visit_date.replace(hour=23, minute=59, second=59))], limit=1)
    if not visit:
        visit = env['clinicflow.visit'].create({
            'pet_id': pet.id,
            'vet_id': vet_id,
            'date': visit_date,
            'status': status,
            'soap_s': "Owner reports periodic limping in the hind left leg after exercise.",
            'soap_o': "Limping observed. Mild sensitivity on extension of left hip joint. No swelling.",
            'soap_a': "Suspected mild arthritis flare-up. Recommended joint supplements and rest.",
            'soap_p': "Administer Rimadyl injection today. Dispense joint tablets. Check back in 2 weeks.",
        })
        print(f"Created visit: {visit.name} for {pet.name}")
        
        # Add charge lines
        for product, qty in charges:
            env['clinicflow.visit.charge.line'].create({
                'visit_id': visit.id,
                'product_id': product.id,
                'quantity': qty,
            })
        print(f"Added charges to visit {visit.name}")
        
        # Add Prescription if products are specified
        if prescription_products:
            presc = env['clinicflow.prescription'].create({
                'pet_id': pet.id,
                'visit_id': visit.id,
                'date': visit_date.date(),
                'notes': "Give with food. Discontinue if vomiting occurs.",
            })
            for prod, qty, dose, instr in prescription_products:
                env['clinicflow.prescription.line'].create({
                    'prescription_id': presc.id,
                    'product_id': prod.id,
                    'quantity': qty,
                    'dosage': dose,
                    'instructions': instr,
                })
            print(f"Created prescription {presc.name} for visit {visit.name}")
            
        # If completed or billing, generate invoice
        if status in ['billing', 'completed']:
            invoice = visit.action_create_invoice()
            print(f"Created invoice {invoice.name} (ID: {invoice.id}) for visit {visit.name}")
            
            # Post the invoice to show it as Open/Paid
            invoice.action_post()
            print(f"Posted invoice {invoice.name}")
            
    return visit

# Let's run this flow for Max
vet_user = env.ref('base.user_admin').id
create_visit_flow(
    pet=pet_max,
    date_str="2026-06-18 10:00:00",
    vet_id=vet_user,
    status="billing",
    charges=[(consultation, 1), (antibiotic, 1)],
    prescription_products=[(amoxicillin, 1, '1-0-1', 'Give 1 tablet every 12 hours')]
)

# Administer vaccine to Bella
def add_vaccination(pet, vaccine, date_admin, date_due, status):
    date_admin_val = fields.Date.from_string(date_admin)
    date_due_val = fields.Date.from_string(date_due) if date_due else None
    existing = env['clinicflow.vaccination'].search([('pet_id', '=', pet.id), ('vaccine_product_id', '=', vaccine.id), ('date_administered', '=', date_admin_val)], limit=1)
    if not existing:
        env['clinicflow.vaccination'].create({
            'pet_id': pet.id,
            'vaccine_product_id': vaccine.id,
            'date_administered': date_admin_val,
            'date_due': date_due_val,
            'status': status,
            'remarks': "Administered subcutaneously in the right rear leg. No immediate reaction.",
        })
        print(f"Recorded vaccination {vaccine.name} for {pet.name}")

add_vaccination(pet_bella, rabies, "2026-06-19", "2027-06-19", "administered")

# Let's also do a hospitalization for Max
def add_admission(pet, reason, date_adm, state):
    adm_date = fields.Datetime.from_string(date_adm)
    existing = env['clinicflow.admission'].search([('pet_id', '=', pet.id), ('admission_date', '=', adm_date)], limit=1)
    if not existing:
        env['clinicflow.admission'].create({
            'pet_id': pet.id,
            'reason': reason,
            'admission_date': adm_date,
            'state': state,
        })
        print(f"Hospitalized {pet.name} for: {reason}")

add_admission(pet_max, "Overnight observation post dental clean", "2026-06-19 14:00:00", "admitted")

env.cr.commit()
print("Seeding finished successfully!")
