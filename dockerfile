# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1-mesa-glx \
        && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the extraction, detection, and plotting scripts
CMD ["bash", "-c", "python extract_frames_from_video.py && python detect_birds_in_frames.py && python csv_to_sqlite.py && python plot_bird_detections.py"]
