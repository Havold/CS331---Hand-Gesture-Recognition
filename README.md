# CS331 - Hand Gesture Recognition
This is a Computer Vision projct about Hand Gesture Recognition
## Instruction
1. Install required libraries:
   ```bash
    pip install opencv-python==4.9.0.80
    pip install scikit-learn==1.4.1
    pip install mediapipe==0.9.0.1  //But you can use the latest version.
   ```
2. Run file collect_data.py to collect data:
   - Create the hand gesture you want to collect for training and press Q to start collecting.
   - There will be 3 labels in total, each label will contain 100 photos.
   - Please change the angle of the gesture and the distance of the hand gesture during the collection process to obtain the most comprehensive and complete data set.
   - NOTE: Please collect consistently. For example: If you want to train a model for 1 hand, then only collect 1 hand. If you collect both 1 hand and 2 hands, when you go to the training step the model will have an error because there are not the same number of landmarks to convert to numpy array
4. Run file create_dataset.py to data processing.
5. Run file train_classifier.py to train model.
7. Run file inference_classifier.py to test model.
## NOTE: Remember to change the argument in the row below to correspond to your laptop's webcam. Because my laptop doesn't have a webcam, I used the IP Webcam app on my phone so I could use my phone instead of my laptop's webcam.
```bash
   cap = cv2.VideoCapture('http://192.168.137.153:8080/video') # My IP webcam address
   cap = cv2.VideoCapure(0) # You can change like this if your laptop has a webcam
```
