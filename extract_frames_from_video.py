import cv2
import os

def init():
    """
    Initialize input and output directories
    """
    video_dir = 'videos'
    frames_dir = 'frames'

    # Create frames directory if it doesn't exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    return video_dir, frames_dir

def main():
    video_dir, frames_dir = init()

    video_path = os.path.join(video_dir, 'input_video.mp4')
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    frame_count = 0

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break  # Break the loop if no frame is returned (end of video)

        frame_filename = os.path.join(frames_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames to {frames_dir}")

if __name__ == "__main__":
    main()
