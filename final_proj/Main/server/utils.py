import csv
import face_recognition
import cv2

def initialize_csv(attendant_file ,csv_file, attendants):
    with open(attendant_file, "r") as file:
        attendants = [line.strip() for line in file.readlines()]
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Attenandance"])
        for attendant in attendants:
            writer.writerow([attendant, "No"])
    print(f"CSV file {csv_file} initialized")

def attendant_signin(name, csv_file, csv_lock, late=False):
    global attendants
    with csv_lock:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Attendance"])
            for row in rows[1:]:
                if row[0] == name:
                    row[1] = "arrived late" if late else "arrive"
                writer.writerow(row)
    print(f"Attendant '{name}' signed in!")


def attendant_vote(name, value, csv_lock, csv_file, current_issue):
    with csv_lock:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Find the row corresponding to the name
        for row in rows[1:]:
            if row[0] == name:
                # Find the column corresponding to the issue
                for i, header in enumerate(rows[0]):
                    if header == current_issue:
                        # Update the value in the row
                        row[i] = value
                        break
                break

        # Write the updated content back to the CSV file
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f"Issue '{current_issue}' updated for {name}")

def verify(name, image):

    verifier_path = f"data/{name}.jpg"

    verifier = cv2.imread(verifier_path)
    # Encode faces from image1
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_encode = face_recognition.face_encodings(image)[0]

    # Encode faces from image2
    verifier = cv2.cvtColor(verifier, cv2.COLOR_BGR2RGB)
    verifier_encode = face_recognition.face_encodings(verifier)[0]

    # Compare the two face encodings
    distance = face_recognition.face_distance([image_encode], verifier_encode)[0]

    # Determine if the faces match within a certain tolerance
    tolerance = 0.5
    is_match = True if distance < tolerance else False

    # Prepare output
    return is_match