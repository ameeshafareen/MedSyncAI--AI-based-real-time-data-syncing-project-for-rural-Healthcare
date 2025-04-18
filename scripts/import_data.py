import mysql.connector
import csv
import os

# Set up the connection to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # change if needed
    password="ameesha",  # change if needed
    database="medsyncai"  # your actual DB name
)
cursor = conn.cursor()

# Folder where CSVs are located
data_folder = "./data"  # adjust path if needed

# Function to import CSV data
def import_csv(filename, table_name, columns):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        for row in reader:
            values = [row[col] for col in columns]
            cursor.execute(query, values)
    conn.commit()
    print(f"{table_name}: Data import completed.")

# ----------------------
# Import for each table
# ----------------------

# Patient
import_csv(os.path.join(data_folder, "patient.csv"), "Patient", ["PatientID", "firstname", "lastname", "email"])

# Doctor
import_csv(os.path.join(data_folder, "doctor.csv"), "Doctor", ["DoctorID", "DoctorName", "Specialization", "DoctorContact"])

# Appointment
import_csv(os.path.join(data_folder, "appointment.csv"), "Appointment", ["AppointmentID", "Date", "Time", "PatientID", "DoctorID"])

# MedicalProcedure
import_csv(os.path.join(data_folder, "Medical Procedure.csv"), "MedicalProcedure", ["ProcedureID", "ProcedureName", "AppointmentID"])

# Billing
import_csv(os.path.join(data_folder, "billing.csv"), "Billing", ["InvoiceID", "PatientID", "Items", "Amount"])

# Utility: Check if value exists in table

# Generate Diagnosis CSV
cursor.execute("""
SELECT Appointment.AppointmentID, Patient.PatientID, Doctor.DoctorID
FROM Appointment
INNER JOIN Patient ON Appointment.PatientID = Patient.PatientID
INNER JOIN Doctor ON Appointment.DoctorID = Doctor.DoctorID
""")
diagnosis_data = cursor.fetchall()

with open("diagnosis.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["DiagnosisID", "AppointmentID", "PatientID", "DoctorID", "Diagnosis"])
    for i, row in enumerate(diagnosis_data):
        writer.writerow([f"D{i+1}", row[0], row[1], row[2], "Sample Diagnosis"])  # Add realistic values

print("diagnosis.csv generated successfully!")

# Generate Prescription CSV
cursor.execute("""
SELECT Appointment.AppointmentID, Patient.PatientID, Doctor.DoctorID
FROM Appointment
INNER JOIN Patient ON Appointment.PatientID = Patient.PatientID
INNER JOIN Doctor ON Appointment.DoctorID = Doctor.DoctorID
""")
prescription_data = cursor.fetchall()

with open("prescription.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["PrescriptionID", "AppointmentID", "PatientID", "DoctorID", "Medicine", "Dosage"])
    for i, row in enumerate(prescription_data):
        writer.writerow([f"P{i+1}", row[0], row[1], row[2], "Medicine A", "Once Daily"])

print("prescription.csv generated successfully!")

# Close connection
conn.commit()  # 🔒 This is critical!
cursor.close()
conn.close()
print("✅ All data successfully imported.")
