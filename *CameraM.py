import depthai as dai
import cv2
import numpy as np

global frame

class OakDCamera:
    def __init__(self, preview_size=(240, 180), fps=15):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define sources and outputs
        self.cam_rgb = self.pipeline.create(dai.node.ColorCamera)
        self.cam_rgb.setPreviewSize(preview_size[0], preview_size[1])
        self.cam_rgb.setFps(fps)
        self.xout_rgb = self.pipeline.create(dai.node.XLinkOut)

        # Set output stream name
        self.xout_rgb.setStreamName("rgb")

        # Configure camera properties
        self.cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        self.cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.cam_rgb.setFps(30)

        # Link nodes
        self.cam_rgb.video.link(self.xout_rgb.input)

        # Initialize device and output queue
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        # Placeholder for last captured frame
        self.last_frame = None

    def get_video(self):
        """
        This function returns a generator that yields frames from the video stream.
        """
        in_rgb = self.q_rgb.get()
        frame = in_rgb.getCvFrame()

        return frame

    def video_displayed(self):
        """
        This function displays the video stream until the 'q' key is pressed.
        """
        print("Press 'q' to exit the video display...")
        for frame in self.get_video():
            # Display the frame
            cv2.imshow("Video Stream", frame)

            # End display when 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                print("Exiting video display...")
                break

        cv2.destroyAllWindows()

    def get_image(self):
        """
        This function returns the last captured image from the video stream.
        """
        if frame is None:
            print("No frame captured yet.")
            return None
        else:
            last_frame = frame
            return last_frame


# Example usage
if __name__ == "__main__":
    oakd_camera = OakDCamera()

    # Display the video until 'q' is pressed
    oakd_camera.video_displayed()

    # Get the last captured image and save it (optional)
    image = oakd_camera.get_image()
    if image is not None:
        cv2.imwrite("last_captured_image.jpg", image)
        print("Last image captured and saved as 'last_captured_image.jpg'.")

