## Libraries

- CV2
- PyQt5
- TensorFlow 2.15

## Requirements

- Python 3.9


## Installation

1. Download openCV library: `pip3 install opencv-python`
2. Download TensorFlow library `pip3 install tensorflow=2.15`
3. Install application in mobile device: **IP Webcam**

## Execution
1. Create processing pipeline:
```python
import app.camera.processing as processing
import numpy as np

def process(frame: np.ndarray):
    v = frame.copy()
    v = processing.grey_scale(v)
    v = processing.gauss(v, 4)
    v = processing.canny(v, 100, 200)
    return v

```
2. Create connector:
```python
import app.camera.connector as connector
camera = connector.Connector(
    port=8080,
    width=640,
    height=480,
    fps_max=30
)
```
3. Load learned model:
```python
from app.classifier.lego_model import LegoBrickModel
model = LegoBrickModel('lego_classifier_model_adam_[e=1,bs=600]' + '.keras')
```
4. Create and run interface:
```python
import sys
import camera.interface as interface
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
```




