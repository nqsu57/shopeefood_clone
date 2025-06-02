# FROM python:3.11-slim
# WORKDIR /app 
# # COPY ./backend/app /app
# # COPY ./backend/requirements.txt .
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# # RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY ./app ./app

RUN pwd

RUN ls

# Expose the port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
