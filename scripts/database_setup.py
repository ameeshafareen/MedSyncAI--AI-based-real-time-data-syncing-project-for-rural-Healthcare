
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ameesha'  # replace with your MySQL password
)
cursor = conn.cursor()

# Step 1: Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS MedSyncAI")
cursor.execute("USE MedSyncAI")

# Step 2: Create tables
# Patient Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient (
    PatientID INT PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(100)
)
""")

# Doctor Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Doctor (
    DoctorID INT PRIMARY KEY,
    DoctorName VARCHAR(100),
    Specialization VARCHAR(100),
    DoctorContact VARCHAR(20)
)
""")

# Appointment Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Appointment (
    AppointmentID INT PRIMARY KEY,
    Date DATE,
    Time TIME,
    PatientID INT,
    DoctorID INT,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
)
""")

# Medical Procedure Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS MedicalProcedure (
    ProcedureID INT PRIMARY KEY,
    ProcedureName VARCHAR(100),
    AppointmentID INT,
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
)
""")

# Billing Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Billing (
    InvoiceID INT PRIMARY KEY,
    PatientID INT,
    Items TEXT,
    Amount DECIMAL(10,2),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
)
""")

# Diagnosis Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Diagnosis (
    DiagnosisID INT PRIMARY KEY,
    AppointmentID INT,
    PatientID INT,
    DoctorID INT,
    Diagnosis TEXT,
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
)
""")

# Prescription Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Prescription (
    PrescriptionID INT PRIMARY KEY,
    AppointmentID INT,
    PatientID INT,
    DoctorID INT,
    Medicine VARCHAR(255),
    Dosage VARCHAR(100),
    FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
)
""")

# Done!
conn.commit()
cursor.close()
conn.close()

print("✅ Database and tables created successfully!")
