# HackGTX
Scout empowers visually impaired individuals through an AI-based mobile app, delivering haptic feedback for seamless journeying from place to place.


## Inspiration
Our team was shocked at the lack of solutions for visually impaired individuals to effectively navigate crowded public spaces.  Aids, such as a seeing-eye dog, are highly useful but they can be restrictive and costly, and are thereby inaccessible to nearly 95 percent of the visually impaired population.

Thus, our team wanted to develop a solution that could provide visually impaired people with a similar level of autonomy, safety, and information when navigating public spaces and going about their daily lives, leading to the creation of Scout.  We wanted to help empower these individuals, one step at a time

## What it does
Scout is a mobile app designed to help visually impaired individuals navigate through crowded environments, effectively avoiding obstacles in real time.  As the user walks and points their phone camera in front of them, Scout utilizes two artificial intelligence models used to identify objects and to determine the object’s distance from the camera, a task not possible with a normal two-dimensional image.

Scout’s computer vision algorithm then processes the output of these two artificial intelligence models to determine the closest object to the user and translates this information into intuitive haptic (tactile) feedback signals the user feels holding their mobile phone.  Once the user comes close to walking into an object in the camera’s field of view, they are notified of the object’s location and proximity by the frequency and strength of vibration signals.  The user will also be audibly alerted of the type of object blocking their path.


## How we built it

Our team trained Scout with two Python artificial intelligence models: the YOLO8 algorithm for real-time object detection and the MiDaS algorithm to create a depth map for distance estimation.  These models were trained over the course of the weekend using Google Cloud and Google Colab.  Our team also developed a computer vision algorithm using OpenCV in Python to determine the closest object to the user.

The mobile interface, haptic feedback, and audio signals were developed in Android Studio. 
Real-time video streaming and processing was developed using OpenCV and IP Webcam. 

Finally, results were synchronized and connected back to the mobile interface via FastAPI. 

## Challenges we ran into

Our team faced many challenges over the course of the 36-hour hackathon.  From thinking we had to rewrite everything in Java 12 hours until submission, training a second artificial intelligence model with less than 8 hours to go, and finally connecting the mobile app and the artificial intelligence models with less than one hour– we are proud of our abilities to face challenges head-on and adapt to challenges.

Before HackGT, no team member had any previous experience with mobile development and with Android Studio.  A lot of time was spent learning through building our project, which proved to be both a challenging and rewarding experience.  Additionally, the project had a lot of moving parts–it involved connecting  OpenCV (a Python-based platform), Android Studio (a Java-based platform), numerous APIs, and multiple AI models. Managing conversions between languages and platforms as well as dependencies of various libraries and packages were a major challenge we dealt with throughout the development process. 


Finally, integrating and linking various features in one cohesive user experience and journey was challenging.  We had to think outside of the box– designing Scout to be both accessible and intuitive for visually impaired individuals.


## Accomplishments that we're proud of

Our team is extremely proud of our two real-time artificial intelligence models, working to accurately detect and categorize objects and a depth-to-distance calculation algorithm that is reliable and precise.

We are also proud of our unique yet intuitive user experience.  Scout provides haptic feedback outputs to users in a simple yet descriptive manner.  It specifies the direction, proximity, and identity of the obstacle via placement and intensity of the vibrations emitted when the user taps their phone in the region associated with where the obstacle is found. 

Most of all, our team is proud of filling a niche for the visually impaired community’s needs and building a tool with the potential to promote greater freedom in their daily lives.


## What we learned

Our team learned how to use Android Studio and new applications of OpenCV, both building further on our prior knowledge and challenging ourselves to integrate a dynamic and responsive front-end with a robust, interconnected backend.  Our team also learned to implement a fully functioning API.

Additionally, we learned how to use Depth API and augmented reality, as opposed to traditional image processing techniques to analyze and gain metrics from image and video data in a resource-efficient manner.

## What's next for Scout
Our team hopes Scout can be expanded to new hardware implementations as well, perhaps through developing an attachment for glasses to serve as an aid particularly to visually impaired/partially seeing individuals. We would also like to make Scout accessible to Apple users as well. Finally, our team would like to pursue building Scout into a fully functional and widespread app– one that is the gold standard for visually impaired users to navigate and live independently and safely. 
