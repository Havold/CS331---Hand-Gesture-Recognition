# CS331 - Hand Gesture Recognition
This is a Computer Vision projct about Hand Gesture Recognition
## Instruction
1. Install required libraries:
   ```bash
    pip install opencv-python==4.9.0.80
    pip install scikit-learn==1.4.1
    pip install mediapip==0.9.0.1
   ```
2. Run file collect_data.py to collect data:
   - Create the hand gesture you want to collect for training and press Q to start collecting.
   - There will be 3 labels in total, each label will contain 100 photos.
   - Please change the angle of the gesture and the distance of the hand gesture during the collection process to obtain the most comprehensive and complete data set.
4. Run file create_dataset.py to data processing.
5. Run file train_classifier.py to train model.
6. Run file inference_classifier.py to test model.
