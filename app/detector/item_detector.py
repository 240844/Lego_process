import cv2

from app.camera import processing
from app.image_processing.image_processing import reduce, replace_color, get_darkest_color, square
from app.utils.config import options


class Blob:
    """
    Class representing an object found in the image.
    """
    def __init__(self, x, y, w, h, brick=None):

        self.x = x # x coordinate of top left corner of blob
        self.y = y # y coordinate of top left corner of blob

        self.w = w # width of blob
        self.h = h # height of blob

        self.brick = brick # classification result
        self.confidence = 0 # confidence of classification result

        self.unwanted = False # turns on alarm if blob is unwanted
    def __str__(self):
        return f'Blob of brick {self.brick.name} at ({self.x}, {self.y})'

    def getSize(self):
        return self.w * self.h

    """
    Check if blob is too big or too small to be one of the bricks.
    """
    def is_wrong_size(self):
        if self.getSize() < options.min_object_size or self.getSize() > options.max_object_size:
            return True
        return False

    """
    Check if blob is already classified / marked as unwanted.
    """
    def is_classified(self):
        if self.brick is not None:
            return True
        if self.unwanted is True:
            return True
        return False

    """
    Check if two blobs are similar enough to be considered the same object.
    """
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

    def mark_as_unwanted(self):
        if self.unwanted is True:
            pass
        self.unwanted = True
        self.brick = None
        self.confidence = 0

    #check if blobs are touching
    def touching(self, blob):
        return ((self.x <= blob.x <= self.x + self.w or blob.x <= self.x <= blob.x + blob.w)
                and (self.y <= blob.y <= self.y + self.h or blob.y <= self.y <= blob.y + blob.h))

    """
    Check if blob is touching the edge of the frame.
    """
    def is_touching_edge(self, frame_size):
        if self.x + self.w >= frame_size[0] or self.y + self.h >= frame_size[1]:
            return True
        if self.x == 0 or self.y == 0:
            return True
        return False

    """
    Check if blob is unwanted based on confidence.
    """
    def is_confidence_too_low(self):
        if self.is_classified() and self.confidence < options.alarm_threshold:
            print(f"Found unwanted object of confidence {self.confidence * 100:.1f}, size {self.getSize()}")
            return True
        return False

    """
    Classify blob using model.
    """
    def classify(self, model, frame):

        # blob.brick = get_random_brick()
        image = frame[self.y:self.y + self.h, self.x:self.x + self.w][..., ::-1]

        image = reduce(image, 2)
        image = replace_color(image, get_darkest_color(image), [0, 0, 0])
        image = square(image, 56)

        result = model.predict_brick(image)

        self.brick = result[0][0]
        self.confidence = result[0][1]

        # print result
        # for brick, confidence in result:
        #    print(f"Predicted class: {brick.name}, confidence: {confidence * 100:.1f}%")

        print(f"Classified blob as {self.brick.name} with confidence {self.confidence * 100 / 1}")
        # cv2.imshow(blob.brick.name + str(blob.confidence), cv2.resize(image[..., ::-1], (112, 112)))



"""
Find objects in image.
"""
def find_blobs(image, min_blob_size=100) -> list[Blob]:
    image = processing.gauss(image, size=3)
    blobs = []
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    _, thresholded = cv2.threshold(v, options.threshold*255, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h >= min_blob_size:
            new_blob = Blob(x, y, w, h, None)
            blobs.append(new_blob)

    return blobs

"""
Carry over classification results from previous frame to current frame.
"""
def copy_identified_blobs(prev_blobs, new_blobs):
    for new_blob in new_blobs:
        for prev_blob in prev_blobs:

            if prev_blob.is_similar(new_blob):
                new_blob.unwanted = prev_blob.unwanted

                if prev_blob.is_classified():
                    new_blob.brick = prev_blob.brick
                    new_blob.confidence = prev_blob.confidence


"""
Find the first unclassified blob that is not touching the edge of the frame, in order to classify it.
"""
def find_unclassified_blob(blobs, frame_size):

    for blob in blobs:

        if blob.is_touching_edge(frame_size):
            continue

        if blob.is_classified() is False:
            print(f"Found unclassified object of size {blob.getSize()}")
            return blob

    return None

"""
Count the number of unclassified blobs.
"""
def count_unclassified(blobs):
    amount = 0
    for blob in blobs:
        if blob.brick is not None:
            amount += 1
    return amount
