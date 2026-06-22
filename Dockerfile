FROM odoo:19.0

# Switch to root to copy files and change ownership
USER root

# Create the extra-addons directory (just in case)
RUN mkdir -p /mnt/extra-addons

# Copy the entire workspace into the image's addons directory
COPY . /mnt/extra-addons

# Ensure the odoo user owns all copied files
RUN chown -R odoo:odoo /mnt/extra-addons

# Switch back to the default odoo user
USER odoo
