# bird_counter

Run via Docker:
docker run -v $(pwd)/videos:/app/videos \     
           -v $(pwd)/frames:/app/frames \
           -v $(pwd)/output_frames:/app/output \
           bird-detection-workflow
