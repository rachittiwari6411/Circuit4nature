import cv2
from ultralytics import YOLO
import time

# Configuration
CAMERA_INDEX = 0  # Change this to match your USB camera (0, 1, etc.)
MODEL_NAME = "yolo11n.pt"  # Using YOLOv11 Nano - fastest model for Raspberry Pi
CONFIDENCE_THRESHOLD = 0.25  # Detection confidence threshold
WINDOW_NAME = "YOLO Real-Time Detection"

def main():
    print("Initializing YOLO model...")
    
    # Load YOLO model (will download automatically on first run)
    model = YOLO(MODEL_NAME)
    print(f"Model loaded: {MODEL_NAME}")
    
    # Initialize USB camera
    print(f"Opening camera at index {CAMERA_INDEX}...")
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L)  # V4L backend for Raspberry Pi
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print(f"ERROR: Could not open camera at index {CAMERA_INDEX}")
        print("Try changing CAMERA_INDEX to 1 or run 'ls /dev/video*' to find your camera")
        return
    
    # Optional: Set camera resolution (lower = faster processing)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Camera opened successfully!")
    print("Press 'q' to quit")
    print("=" * 50)
    
    # Create named window
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    
    # FPS calculation variables
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    try:
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            
            if not ret:
                print("ERROR: Failed to grab frame")
                break
            
            # Run YOLO detection on the frame
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            
            # Get annotated frame with bounding boxes and labels
            annotated_frame = results[0].plot()
            
            # Calculate FPS
            fps_frame_count += 1
            if fps_frame_count >= 30:
                fps_end_time = time.time()
                fps = fps_frame_count / (fps_end_time - fps_start_time)
                fps_start_time = time.time()
                fps_frame_count = 0
            
            # Display FPS on frame
            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.1f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Display detected objects count
            num_detections = len(results[0].boxes)
            cv2.putText(
                annotated_frame,
                f"Objects: {num_detections}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Show the frame in window
            cv2.imshow(WINDOW_NAME, annotated_frame)
            
            # Print detection info (optional)
            if num_detections > 0:
                for box in results[0].boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = model.names[class_id]
                    print(f"Detected: {class_name} (confidence: {confidence:.2f})")
            
            # Check for 'q' key to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\nExiting...")
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed")

if __name__ == "__main__":
    main()
