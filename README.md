# bird_counter

## Running via Docker

To run the `bird_counter` application using Docker, follow these steps:

```bash
docker run -v $(pwd)/videos:/app/videos \
           -v $(pwd)/frames:/app/frames \
           -v $(pwd)/output_frames:/app/output \
           bird-detection-workflow
```

## Running Python script directly in venv

To run the `bird_counter` application by executing Python scripts directly, follow these steps:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python extract_frames_from_video.py && python detect_birds_in_frames.py && python csv_to_sqlite.py && python plot_bird_detections.py
```
