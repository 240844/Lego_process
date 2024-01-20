import cv2

from app.camera import processing
from app.image_processing.image_processing import reduce, replace_color, get_darkest_color, square

class Blob:
    def __init__(self, x, y, w, h, brick=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.brick = brick
        self.confidence = 0
    def __str__(self):
        return f'Blob of brick{self.brick.name} at ({self.x}, {self.y})'

    def is_similar(self, blob):
        x1 = self.x
        y1 = self.y
        w1 = self.w
        h1 = self.h

        x2 = blob.x
        y2 = blob.y
        w2 = blob.w
        h2 = blob.h

        if (x2 <= x1 <= x2 + w2 or x1 <= x2 <= x1 + w1) and (y2 <= y1 <= y2 + h2 or y1 <= y2 <= y1 + h1):
            return True
        return False

def paste_blobs(image, blobs):
    image = image.copy()

    for blob in blobs:
        x = blob.x
        y = blob.y
        w = blob.w
        h = blob.h
        brick = blob.brick

        if brick is None:
            color = (255, 255, 255)
            name = "Not classified"
            confidence = ""
        else:
            color = brick.getColor()
            name = brick.name
            confidence = f"{blob.confidence:.2f}"

        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness=2)
        cv2.putText(image, str(name), (x+w+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=1 )
        cv2.putText(image, str(confidence), (x+w+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=1 )

    return image


def find_blobs(image, min_blob_size=100):
    blobs = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    _, thresholded = cv2.threshold(v, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h >= min_blob_size:
            new_blob = Blob(x, y, w, h, None)
            blobs.append(new_blob)

    return blobs

def detect_new_blobs(image):
    blurred_image = processing.gauss(image, size=8)
    blobs = find_blobs(blurred_image)
    image = paste_blobs(image, blobs)
    return image, blobs



def copy_identified_blobs(prev_blobs, new_blobs):
    for new_blob in new_blobs:
        for prev_blob in prev_blobs:
            if prev_blob.is_similar(new_blob):
                new_blob.brick = prev_blob.brick
                new_blob.confidence = prev_blob.confidence



def classify_blob(model, blob, frame):

    #blob.brick = get_random_brick()
    image = frame[blob.y:blob.y+blob.h, blob.x:blob.x+blob.w][..., ::-1]

    image = reduce(image, 2)
    image = replace_color(image, get_darkest_color(image), [0, 0, 0])
    image = square(image, 56)

    result = model.predict_brick(image)

    blob.brick = result[0][0]
    blob.confidence = result[0][1]
    print(f"Classified blob as {blob.brick.name} with confidence {blob.confidence*100/1}")
    return True



def find_unclassified_blob(blobs, frame_size):
    for blob in blobs:
        if blob.brick is None:
            if blob.w * blob.h > 500 and blob.x + blob.w < frame_size[0]:
                return blob
    return None

def count_unclassified(blobs):
    amount = 0
    for blob in blobs:
        if blob.brick is not None:
            amount += 1
    return amount
