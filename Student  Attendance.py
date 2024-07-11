import os
import cv2
import numpy as np
from deepface import DeepFace
from matplotlib import pyplot as plt
import psycopg2
from psycopg2 import sql
def insert_attendance_record(date, subject, student_name, image_path):
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(
            dbname="College DB",
            user="postgres",
            password="Geetha@522",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Fetch subject_id from Subject table
        cur.execute("SELECT id FROM subject WHERE name=%s", (subject,))
        subject_id_result = cur.fetchone()
        if subject_id_result is None:
            # Insert the subject if it doesn't exist
            cur.execute("INSERT INTO subject (name) VALUES (%s) RETURNING id", (subject,))
            subject_id = cur.fetchone()[0]
        else:
            subject_id = subject_id_result[0]

        # Fetch student_id from Student table
        cur.execute("SELECT id FROM student WHERE name=%s", (student_name,))
        student_id_result = cur.fetchone()
        if student_id_result is None:
            # Insert the student if it doesn't exist
            cur.execute("INSERT INTO student (name) VALUES (%s) RETURNING id", (student_name,))
            student_id = cur.fetchone()[0]
        else:
            student_id = student_id_result[0]

        # Insert attendance record
        cur.execute('''
            INSERT INTO attendance (date, subject_id, student_id, image)
            VALUES (%s, %s, %s, %s)
        ''', (date, subject_id, student_id, image_path))

        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        print(f"Attendance record inserted for {student_name}")

    except Exception as e:
        print(f"Error inserting attendance record: {e}")
        print(f"Date: {date}, Subject: {subject}, Student: {student_name}, image_path: {image_path}")

# Function to recognize multifaced image 

def load_known_faces(training_dir):
    known_faces = {}
    for person_name in os.listdir(training_dir):
        person_dir = os.path.join(training_dir, person_name)
        if os.path.isdir(person_dir):
            known_faces[person_name] = [os.path.join(person_dir, img_name) for img_name in os.listdir(person_dir)]
    return known_faces

def extract_face_data(facial_area):
    if isinstance(facial_area, dict):
        return facial_area.get('x', 0), facial_area.get('y', 0), facial_area.get('w', 0), facial_area.get('h', 0)
    elif isinstance(facial_area, (list, tuple)) and len(facial_area) == 4:
        return facial_area
    else:
        print(f"Unexpected facial_area format: {facial_area}")
        return None

def recognize_faces(image_path, known_faces, model_name="VGG-Face", distance_metric="cosine"):
    faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    recognized_persons = []

    for face in faces:
        facial_area = extract_face_data(face['facial_area'])
        if facial_area is None:
            continue

        x, y, w, h = facial_area
        face_img = img[y:y+h, x:x+w]
        temp_face_path = "temp_face.jpg"
        cv2.imwrite(temp_face_path, face_img)

        try:
            result = DeepFace.find(img_path=temp_face_path,
                                   db_path=training_dir,
                                   model_name=model_name,
                                   distance_metric=distance_metric,
                                   enforce_detection=False)

            if result and len(result[0]) > 0:
                recognized_path = result[0]['identity'][0]
                recognized_name = os.path.basename(os.path.dirname(recognized_path))
                recognized_persons.append(recognized_name)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, recognized_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        except Exception as e:
            print(f"Error processing a face: {str(e)}")
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        finally:
            if os.path.exists(temp_face_path):
                os.remove(temp_face_path)

    return img, recognized_persons

# Set up paths
training_dir = r"/content/drive/MyDrive/Colab Notebooks/Image Dataset/Training Data"
test_image_path = r"/content/Group images/History 2024-06-22 10001100.jpeg"
known_faces = load_known_faces(training_dir)

# Extract subject and date from filename
image_name = os.path.basename(test_image_path)
parts = image_name.split('_')
if len(parts) >= 2:
    subject, date = parts[:2]
else:
    # Handle the error, for example:
    subject = "Maths"
    date = "2024-06-22"
subject = subject.split('.')[0]  # Remove file extension

# Recognize faces in the test image
result_img, recognized_persons = recognize_faces(test_image_path, known_faces)

# Display the result
plt.figure(figsize=(10, 4))
plt.imshow(result_img)
plt.axis('off')
plt.title(f"Recognized Faces - {subject} {date}")
plt.show()

# Print the attendance information
print(f"Students {', '.join(recognized_persons)} attended {subject} class on {date}")

# Connect to the database and insert attendance records
