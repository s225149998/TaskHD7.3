# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "hangman_1.1.py", "--server.port=8501", "--server.address=0.0.0.0"]
