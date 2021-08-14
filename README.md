# Intruder Detection

Python project for detecting intruders in live video with Firebase alert and auto-recording.

### Version

1.0.0

## Requirements

python 3.x

tensorflow 2.x

numpy

opencv

pyrebase (Optional)

## About the project

The project is a python-based intruder detection system that leverages an Object Detection model to detect the presence of individuals in a live video with auto-recording, Firebase connectivity and alert.

### Features

1. Uses the model [EfficientNet D1](https://arxiv.org/abs/1911.09070) of the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) trained on the [COCO 2017](https://cocodataset.org/) dataset for fast detection.
2. Multi-threaded process for not missing any key moment while the model is running.
3. Automatic recording when an intruder(s) has been detected. Recording stops when the intruder(s) moves out of the camera frame.
4. Code for connecting to a Firebase app wherein the user can set alert modes to start/stop the system. For example, when leaving home/reaching back.
5. Automatic app notification via Firebase incase an intruder has been detected when the system is in alert mode.

## Demo

To try the project locally,
1. Clone the repo
2. Set up the environment. Install requirements manually or use the .yml file. For Anaconda package manager ->
```bash
$ conda env create -f environment.yml

$ conda activate intruder-detection
```
4. Start the system through CLI ->
```bash
$ python intruder-detection.py
```

## Author

Yagaagowtham P ([github.com/yagaag](https://github.com/yagaag))
