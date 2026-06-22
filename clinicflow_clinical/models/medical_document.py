from odoo import models, fields, api


DOCUMENT_CATEGORIES = [
    ('lab_result', 'Lab Result'),
    ('imaging', 'Imaging / X-Ray'),
    ('consent_form', 'Consent Form'),
    ('referral', 'Referral Letter'),
    ('clinical_photo', 'Clinical Photo'),
    ('discharge', 'Discharge Summary'),
    ('other', 'Other'),
]


class ClinicFlowMedicalDocument(models.Model):
    _name = 'clinicflow.medical.document'
    _description = 'Medical Document / Diagnostic File'
    _order = 'date desc, id desc'

    name = fields.Char(string="Document Title", required=True)
    category = fields.Selection(
        DOCUMENT_CATEGORIES,
        string="Category",
        required=True,
        default='other',
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.today,
    )

    # Clinical relationships
    pet_id = fields.Many2one(
        'clinicflow.pet',
        string="Patient",
        required=True,
        ondelete='cascade',
        index=True,
    )
    visit_id = fields.Many2one(
        'clinicflow.visit',
        string="Related Visit",
        domain="[('pet_id', '=', pet_id)]",
        ondelete='set null',
        help="The clinical visit during which this document was generated or collected.",
    )

    # The actual binary file
    attachment_id = fields.Many2one(
        'ir.attachment',
        string="File",
        ondelete='set null',
    )
    file_name = fields.Char(string="File Name", related='attachment_id.name', readonly=True)
    file_size = fields.Integer(string="File Size", related='attachment_id.file_size', readonly=True)
    mimetype = fields.Char(string="Mime Type", related='attachment_id.mimetype', readonly=True)

    # Convenience upload field — writes to ir.attachment on save
    file_upload = fields.Binary(string="Upload File", attachment=True)

    notes = fields.Text(string="Clinical Notes / Description")
    uploaded_by = fields.Many2one(
        'res.users',
        string="Uploaded By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    # Computed display helpers
    category_label = fields.Char(string="Category Label", compute="_compute_category_label")
    file_size_display = fields.Char(string="Size", compute="_compute_file_size_display")

    @api.depends('category')
    def _compute_category_label(self):
        cat_map = dict(DOCUMENT_CATEGORIES)
        for rec in self:
            rec.category_label = cat_map.get(rec.category, 'Other')

    @api.depends('file_size')
    def _compute_file_size_display(self):
        for rec in self:
            size = rec.file_size or 0
            if size >= 1_048_576:
                rec.file_size_display = f"{size / 1_048_576:.1f} MB"
            elif size >= 1024:
                rec.file_size_display = f"{size / 1024:.1f} KB"
            elif size > 0:
                rec.file_size_display = f"{size} B"
            else:
                rec.file_size_display = "—"

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-link ir.attachment when file_upload is provided."""
        records = super().create(vals_list)
        for rec in records:
            if rec.file_upload and not rec.attachment_id:
                attachment = self.env['ir.attachment'].create({
                    'name': rec.name,
                    'datas': rec.file_upload,
                    'res_model': self._name,
                    'res_id': rec.id,
                })
                rec.attachment_id = attachment
        return records

    def action_download(self):
        """Return a URL action to download the attached file."""
        self.ensure_one()
        if not self.attachment_id:
            return False
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.attachment_id.id}?download=true',
            'target': 'self',
        }
