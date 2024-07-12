import cv2
import os
import csv
from datetime import timedelta
from ultralytics import YOLO

def init():
    """
    Initialize input and output directories and return video file path
    """
    frames_dir = 'frames'
    output_dir = 'output'

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    video_file_path = 'videos/input_video.mp4'
    return frames_dir, output_dir, video_file_path

def frame_to_timestamp(frame_count, fps):
    """
    Convert frame count to a timestamp string
    """
    seconds = frame_count / fps
    return str(timedelta(seconds=seconds))

def detect_birds_in_frame(model, frame, frame_count, output_dir, writer, fps):
    """
    Apply YOLOv8 object detection on the frame and save the output
    """
    results = model(frame)
    
    for result in results:
        # Render the detection results onto the frame
        annotated_frame = result.plot()

        # Get the detection details
        for box in result.boxes.data.tolist():
            x0, y0, x1, y1, confidence, cls = box
            class_name = model.names[int(cls)]
            timestamp = frame_to_timestamp(frame_count, fps)
            writer.writerow([class_name, timestamp, frame_count, x0, y0, x1, y1, confidence])

        output_filename = os.path.join(output_dir, f"detected_frame_{frame_count:04d}.jpg")
        cv2.imwrite(output_filename, annotated_frame)
        print(f"Processed and saved {output_filename}")

def main():
    frames_dir, output_dir, video_file_path = init()

    # Load YOLOv8 model pre-trained on COCO dataset
    model = YOLO('yolov8n.pt')

    # Capture video to extract fps
    video_capture = cv2.VideoCapture(video_file_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_file_path}")
        return

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f"Inferred fps from video: {fps}")

    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])

    # Prepare CSV file
    csv_filename = os.path.join(output_dir, "detection_results.csv")
    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Class", "Timestamp", "Frame", "BoundingBox_Coord0", "BoundingBox_Coord1", "BoundingBox_Coord2", "BoundingBox_Coord3", "Confidence"])

        for frame_count, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)

            if frame is None:
                print(f"Error: Could not read frame {frame_path}")
                continue

            detect_birds_in_frame(model, frame, frame_count, output_dir, writer, fps)

    video_capture.release()

if __name__ == "__main__":
    main()
