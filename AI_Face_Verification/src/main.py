import cv2
from ultralytics import YOLO
import numpy as np
from insightface.app import FaceAnalysis
import pytesseract

class IdentityVerification:
    def __init__(self, yolo_model_path, face_analysis_model_name='buffalo_s'):
        self.yolo_model = YOLO(yolo_model_path)
        self.face_analysis = FaceAnalysis(name=face_analysis_model_name, providers=['CPUExecutionProvider'])
        self.face_analysis.prepare(ctx_id=0, det_size=(640, 640))

    def enhance_image(self, img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return enhanced_img

    def remove_noise(self, img):
        return cv2.GaussianBlur(img, (5, 5), 0)

    def process_card(self, image_path):
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.yolo_model(rgb_image)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                card_image = image[y1:y2, x1:x2]
                enhanced_card_image = self.enhance_image(card_image)
                cleaned_card_image = self.remove_noise(enhanced_card_image)
                cv2.imwrite('cleaned_card_image.jpg', cleaned_card_image)
                return cleaned_card_image
        return None

    def extract_text(self, image_path):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        boxes = pytesseract.image_to_data(image_rgb, lang='fas', output_type=pytesseract.Output.DICT)
        text = ""
        for i in range(len(boxes['text'])):
            if int(boxes['conf'][i]) > 60:  # فقط متن با اعتماد بالا
                x, y, w, h = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
                text += boxes['text'][i] + " "
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite('text_with_boxes.jpg', image)  
        return text.strip()

    def detect_person(self, cleaned_card_image):
        person_results = self.yolo_model(cleaned_card_image)
        for person_result in person_results:
            for box in person_result.boxes:
                if box.cls[0] == 0:  
                    x1_person, y1_person, x2_person, y2_person = map(int, box.xyxy[0])
                    person_image = cleaned_card_image[y1_person:y2_person, x1_person:x2_person]
                    cv2.imwrite('/content/person_image.jpg', person_image)
                    return person_image
        return None

    def compare_faces(self, image_1, image_2):
        result_1 = self.face_analysis.get(image_1)
        embedding_1 = result_1[0]["embedding"] if result_1 else None

        result_2 = self.face_analysis.get(image_2)
        embedding_2 = result_2[0]["embedding"] if result_2 else None

        if embedding_1 is not None and embedding_2 is not None:
            distance = np.linalg.norm(embedding_1 - embedding_2)
            return distance < 25  
        return None

if __name__ == "__main__":
    verifier = IdentityVerification(yolo_model_path='yolov8l.pt')
    cleaned_card_image = verifier.process_card('/content/2.png')
    if cleaned_card_image is not None:
        text = verifier.extract_text("/content/2.png")
        print(text)
        
        person_image = verifier.detect_person(cleaned_card_image)
        if person_image is not None:
            imag_1 = cv2.imread("/content/person_image.jpg")
            imag_2 = cv2.imread("images2.jpg")
            if verifier.compare_faces(imag_1, imag_2):
                print("Same Person ✅")
            else:
                print("Different Persons 📛")
        else:
            print("No person detected in the card image.")
    else:
        print("No card detected.")
