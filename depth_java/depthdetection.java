// import org.bytedeco.opencv.opencv_core.*;
// import org.bytedeco.opencv.opencv_imgproc.*;
// import org.bytedeco.opencv.opencv_videoio.*;
// import org.bytedeco.opencv.global.opencv_core.*;
// import org.bytedeco.opencv.global.opencv_imgproc.*;
// import org.bytedeco.opencv.global.opencv_videoio.*;
// import org.bytedeco.opencv.global.opencv_highgui.*;
// import org.bytedeco.opencv.global.opencv_imgcodecs.*;

// public class ObjectDetection {
//     public static void main(String[] args) {
//         System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

//         System.out.println("Opening video");

//         int lowerHueNear = -10;
//         int upperHueNear = 9;
//         int lowerSaturationNear = 150;
//         int upperSaturationNear = 255;

//         int lowerHueClose = -10;
//         int upperHueClose = 4;
//         int lowerSaturationClose = 150;
//         int upperSaturationClose = 255;

//         VideoCapture cap = new VideoCapture("depthlab_videos/pole_and_stuff.mp4");
//         int count = 0;
//         int numFramesNear = 0;
//         int numFramesClose = 0;
//         boolean objectDetected = false;
//         boolean closeObjectDetected = false;
//         int scale = 2;

//         int leftDetected = 0;
//         int centerDetected = 0;
//         int rightDetected = 0;

//         int[] detection = { leftDetected, centerDetected, rightDetected };

//         Mat frame = new Mat();

//         while (cap.isOpened()) {
//             cap.read(frame);

//             if (frame.empty()) {
//                 break;
//             }

//             Size frameSize = frame.size();
//             int width = (int) frameSize.width();
//             int height = (int) frameSize.height();

//             int displayHeight = height / scale;
//             int displayWidth = width / scale;

//             Mat displayFrame = new Mat();
//             Imgproc.resize(frame, displayFrame, new Size(displayWidth, displayHeight));

//             int sectionWidth = width / 3;
//             int leftSection = sectionWidth;
//             int center = 2 * sectionWidth;
//             int rightSection = width;

//             Mat hsvFrame = new Mat();
//             Imgproc.cvtColor(frame, hsvFrame, Imgproc.COLOR_BGR2HSV);

//             // Near objects
//             Scalar lowerColorNear = new Scalar(lowerHueNear, lowerSaturationNear, 0, 0);
//             Scalar upperColorNear = new Scalar(upperHueNear, upperSaturationNear, 255, 0);

//             Mat mask = new Mat();
//             Core.inRange(hsvFrame, lowerColorNear, upperColorNear, mask);

//             Mat result = new Mat();
//             Core.bitwise_and(frame, frame, result, mask);

//             Mat displayResult = new Mat();
//             Imgproc.resize(result, displayResult, new Size(displayWidth, displayHeight));

//             MatOfPoint coordinates = new MatOfPoint();
//             Core.findNonZero(mask, coordinates);

//             if (coordinates.toArray().length > 0) {
//                 Moments moments = Imgproc.moments(coordinates, false);
//                 double centerX = moments.get_m10() / moments.get_m00();
//                 double centerY = moments.get_m01() / moments.get_m00();

//                 if (objectDetected && centerX < leftSection && !closeObjectDetected) {
//                     System.out.println("Left Near");
//                     // Update detection accordingly
//                     detection = new int[] { 1, 0, 0 };
//                 } else if (objectDetected && centerX < center && !closeObjectDetected) {
//                     System.out.println("Center Near");
//                     // Update detection accordingly
//                     detection = new int[] { 0, 1, 0 };
//                 } else if (objectDetected && !closeObjectDetected) {
//                     System.out.println("Right Near");
//                     // Update detection accordingly
//                     detection = new int[] { 0, 0, 1 };
//                 }
//             }

//             if (numFramesNear == 25) {
//                 objectDetected = true;
//                 System.out.println("Near object detected");
//             }

//             // Close objects
//             Scalar lowerColorClose = new Scalar(lowerHueClose, lowerSaturationClose, 0, 0);
//             Scalar upperColorClose = new Scalar(upperHueClose, upperSaturationClose, 255, 0);

//             Mat mask2 = new Mat();
//             Core.inRange(hsvFrame, lowerColorClose, upperColorClose, mask2);

//             Mat result2 = new Mat();
//             Core.bitwise_and(frame, frame, result2, mask2);

//             Mat displayResult2 = new Mat();
//             Imgproc.resize(result2, displayResult2, new Size(displayWidth, displayHeight));

//             if (objectDetected) {
//                 if (coordinates.toArray().length > 0.05 * displayWidth * displayHeight) {
//                     if (centerX < leftSection) {
//                         System.out.println("Left Close");
//                         // Update detection accordingly
//                         detection = new int[] { 2, 0, 0 };
//                     } else if (centerX < center) {
//                         System.out.println("Center Close");
//                         // Update detection accordingly
//                         detection = new int[] { 0, 2, 0 };
//                     } else {
//                         System.out.println("Right Close");
//                         // Update detection accordingly
//                         detection = new int[] { 0, 0, 2 };
//                     }
//                 }
//             }

//             if (numFramesClose == 15) {
//                 closeObjectDetected = true;
//                 System.out.println("Close object detected");
//             }

//             if (coordinates.toArray().length > 0) {
//                 if (coordinates.toArray().length > 0.05 * displayWidth * displayHeight) {
//                     numFramesNear++;
//                     Imgproc.circle(displayResult, new Point(centerX / scale, centerY / scale), 5, new Scalar(255, 0, 0), -1);
//                     Imgproc.putText(displayResult, "Text", new Point(centerX / scale - 70, centerY / scale + 40), Imgproc.FONT_HERSHEY_SIMPLEX, 1, new Scalar(255, 0, 0), 1);
//                 }
//             }

//             HighGui.imshow("Near object", displayResult);
//             HighGui.imshow("Window Name", displayFrame);

//             count++;
//             char key = (char) HighGui.waitKey(10);
//             if (key == 'q') {
//                 break;
//             }

//             detection = new int[] { 0, 0, 0 };
//         }

//         cap.release();
//         HighGui.destroyAllWindows();
//         System.out.println("Video finished");
//     }
// }
