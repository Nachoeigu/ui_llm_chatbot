# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV GOOGLE_API_KEY=
ENV ANTHROPIC_API_KEY=
ENV LANGCHAIN_DEBUG_LOGGING=
ENV ELEVEN_API_KEY=
ENV OPENAI_API_KEY=
ENV OPENAI_API_KEY=
ENV PINECONE_API_KEY=
ENV WORKDIR=/app

# Run the FastAPI application
CMD ["streamlit", "run", "src/front/streamlit_app.py","--server.port=8501", "--server.address=0.0.0.0"]