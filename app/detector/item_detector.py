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

    def getSize(self):
        return self.w * self.h

    #check if blob in last frame is similar to blob in current frame
    def is_similar(self, blob):

        if not self.touching(blob):
            return False

        blob1_ratio = self.w / self.h
        blob2_ratio = blob.w / blob.h
        ratio = blob1_ratio / blob2_ratio
        if ratio < 0.7 or ratio > 1.3:
            return False

        size_ratio = self.getSize() / blob.getSize()
        if size_ratio < 0.7 or size_ratio > 1.3:
            return False

        return True

    #check if blobs are touching
    def touching(self, blob):
        return (self.x <= blob.x <= self.x + self.w or blob.x <= self.x <= blob.x + blob.w) and (self.y <= blob.y <= self.y + self.h or blob.y <= self.y <= blob.y + blob.h)


def paste_blobs(image, blobs):
    image = image.copy()

    for blob in blobs:
        brick = blob.brick

        if brick is None:
            color = (255, 255, 255)
            name = "Not classified"
            confidence = ""
        else:
            color = brick.getColor()
            name = brick.name
            confidence = f"{blob.confidence:.2f}"

        cv2.rectangle(image, (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), color, thickness=2)
        cv2.putText(image, str(name), (blob.x + blob.w+10, blob.y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=1 )
        cv2.putText(image, str(confidence), (blob.x + blob.w+10, blob.y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=1 )

    return image


def find_blobs(image, min_blob_size=100):
    image = processing.gauss(image, size=3)
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
            if prev_blob.brick is not None and prev_blob.is_similar(new_blob):
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

    # print result
    for brick, confidence in result:
        print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")

    print(f"Classified blob as {blob.brick.name} with confidence {blob.confidence*100/1}")
    #cv2.imshow(blob.brick.name + str(blob.confidence), cv2.resize(image[..., ::-1], (112, 112)))
    return True


def touching_edge(blob, frame_size):
    if blob.x + blob.w >= frame_size[0] or blob.y + blob.h >= frame_size[1]:
        return True
    if blob.x == 0 or blob.y == 0:
        return True


def find_unclassified_blob(blobs, frame_size):
    for blob in blobs:
        if blob.brick is None and (300 < blob.getSize() < 9000) and not touching_edge(blob, frame_size):
            return blob
    return None

def count_unclassified(blobs):
    amount = 0
    for blob in blobs:
        if blob.brick is not None:
            amount += 1
    return amount
