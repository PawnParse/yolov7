import cv2

from onnx_detector import ONNX_Detector


# Example usage:
weights_path = "models/bbox-chess3-tiny.onnx"
image_path = 'data/datasets/bbox-chess3/images/test/84a8bde7-9183-4ab2-81f4-f1fa7a3066cd.jpeg'

# Load and preprocess image
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # images should be in RGB format and CxHxW

detector = ONNX_Detector(weights_path)
results = detector.infer(img)

print(results)  # Process the results as needed