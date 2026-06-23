FROM odoo:19.0

# Switch to root to copy files and install python dependencies
USER root

# Install external python dependencies
RUN pip3 install --break-system-packages openpyxl ofxparse qifparse

# Create the extra-addons directory (just in case)
RUN mkdir -p /mnt/extra-addons

# Copy the entire workspace into the image's addons directory
COPY . /mnt/extra-addons

# Ensure the odoo user owns all copied files
RUN chown -R odoo:odoo /mnt/extra-addons

# Switch back to the default odoo user
USER odoo
