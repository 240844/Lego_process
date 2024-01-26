## Libraries

- CV2
- PyQt5

## Requirements

- Python 3.9


## Installation

1. Download openCV library: `pip3 install opencv-python`
2. Install application in mobile device: **IP Webcam**

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
2. Create and run connector:
```python
import app.camera.connector as connector
camera = connector.Connector()
camera.run(process)
```