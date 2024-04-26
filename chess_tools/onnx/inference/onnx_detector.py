import cv2
import numpy as np
import onnxruntime as ort
import torch


"""
ONNX YOLOV7 Inference
"""
class ONNX_Detector:
    def __init__(self, weights_path):
        cuda = torch.cuda.is_available()

        # Initialize ONNX runtime session
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
        self.session = ort.InferenceSession(weights_path, providers=providers)
        
        # Get input and output names from the session
        self.input_name = [i.name for i in self.session.get_inputs()][0]
        self.output_name = [i.name for i in self.session.get_outputs()][0]

    def __letterbox__(self, im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, r, (dw, dh)

    """
    assumes single RGB images C x H x W
    """
    def infer(self, image, target_shape=(1280, 1280), auto_letterbox=False):
        # image = img.copy()

        # scale image the same as in training
        image, ratio, dwdh = self.__letterbox__(image, new_shape=target_shape, auto=auto_letterbox)

        image = image.transpose((2, 0, 1))
        image = np.expand_dims(image, 0)
        image = np.ascontiguousarray(image)
        image = image.astype(np.float32) / 255.0

        # Prepare inputs and run inference
        ort_inputs = {self.input_name: image}
        result = self.session.run([self.output_name], ort_inputs)[0]

        boxes = []
        # postprocess result, that is scale back
        for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(result):
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()

            boxes.append(box)

            # possible future features
            # cls_id = int(cls_id)
            # score = round(float(score),3)
            # name = 'move'

        return boxes