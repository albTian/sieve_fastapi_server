from typing import List, Dict
import torch
import cv2
from sort import Sort
import numpy as np
import uuid

# load model and set the confidence level
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = .7

# sieve_sort and sieve_format_results from https://github.com/sieve-community/examples/tree/main/yolo_object_tracking
def sieve_sort(it: List) -> Dict:
    l = []
    for i in it:
        if len(i) > 0:
            l.append(i)
    sorted_by_frame_number = sorted(l, key=lambda k: k[0]['frame_number'])
    separated_by_class = {}
    for i in sorted_by_frame_number:
        entities = i
        frame_number = i[0]['frame_number']
        for entity in entities:
            if entity['class_name'] not in separated_by_class:
                separated_by_class[entity['class_name']] = {}
            
            if separated_by_class[entity['class_name']].get(frame_number) is None:
                separated_by_class[entity['class_name']][frame_number] = []
            separated_by_class[entity['class_name']][frame_number].append(entity)

    # object id key and object value where object is a list of boxes
    objects = {}
    for i in separated_by_class:
        number_to_uuid = {}
        boxes = []
        mot_tracker = Sort()
        for frame_number in sorted(separated_by_class[i].keys()):
            for box in separated_by_class[i][frame_number]:
                boxes.append([box['box'][0], box['box'][1], box['box'][2], box['box'][3], box['score']])
            if len(boxes) == 0:
                boxes = np.empty((0, 5))
            else:
                boxes = np.array(boxes)
            trackers = mot_tracker.update(boxes)
            for d in trackers:
                if d[4] not in number_to_uuid:
                    number_to_uuid[d[4]] = str(uuid.uuid4())
                if number_to_uuid[d[4]] not in objects:
                    objects[number_to_uuid[d[4]]] = []
                objects[number_to_uuid[d[4]]].append({
                    "frame_number": frame_number,
                    "box": [d[0], d[1], d[2], d[3]],
                    "class": i
                })
            boxes = []

    return objects

# from sieve-examples
def sieve_format_results(results, frame_number):
    outputs = []
    for pred in reversed(results.pred):
        for *box, conf, cls in reversed(pred):
            cls_name = results.names[int(cls)]
            box = [float(i) for i in box]
            score = float(conf)
            outputs.append({
                "box": box,
                "class_name": cls_name,
                "score": score,
                "frame_number": frame_number
            })
    return outputs

def ml_process_video(source_url):
    print("running ml processing...")
    cap = cv2.VideoCapture(source_url)

    yolo_results = []
    frame_number = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is None:
            print("Finished processing video")
            break
        
        # rely on AutoShape to fit our frame, format result to our desired shape
        results = model(frame)
        outputs = sieve_format_results(results, frame_number)
        yolo_results.append(outputs)
        frame_number += 1

    sort_results = sieve_sort(yolo_results)
    cap.release()
    cv2.destroyAllWindows()
    print("finished ml processing.")
    return sort_results
