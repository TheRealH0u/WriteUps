# Use the official PHP CLI image
FROM php:8.2-cli

# Create a low-privilege user
RUN useradd -m -s /bin/bash lowprivuser

# Set the working directory
WORKDIR /var/www/html

# Copy the application code
COPY --chown=lowprivuser:lowprivuser ./app /var/www/html
COPY --chown=lowprivuser:lowprivuser ./assets /var/www/html/assets

# Switch to the low-privilege user
USER lowprivuser