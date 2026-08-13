import csv
import random
from datetime import date

# Set fixed seed for repeatable mock data
random.seed(42)

DEPARTMENTS = ["Engineering", "HR", "Sales", "Finance", "Product"]
TITLES = {
    "Engineering": ["Software Engineer", "Senior Developer", "QA Engineer"],
    "HR": ["HR Specialist", "HR Director"],
    "Sales": ["Account Executive", "Sales Director"],
    "Finance": ["Financial Analyst", "Finance Manager"],
    "Product": ["Product Manager", "UI/UX Designer"]
}

INDIAN_NAMES = [
    "Aarav Sharma", "Rohan Verma", "Priya Nair", "Ananya Iyer", "Vikram Malhotra",
    "Siddharth Patel", "Kavita Reddy", "Neha Gupta", "Rahul Kapoor", "Aditi Joshi",
    "Arjun Singh", "Meera Deshmukh", "Karan Mehta", "Pooja Kumar", "Sanjay Rao"
]

def generate_base_dataset(file_path, num_records=15):
    records = []
    for emp_id in range(101, 101 + num_records):
        dept = random.choice(DEPARTMENTS)
        title = random.choice(TITLES[dept])
        name = INDIAN_NAMES[(emp_id - 101) % len(INDIAN_NAMES)]
        salary = random.choice([600000, 850000, 1200000, 1800000, 2500000])
        
        records.append({
            "emp_id": emp_id,
            "full_name": name,
            "department": dept,
            "job_title": title,
            "salary": salary,
            "hire_date": "2021-01-15",
            "status": "Active",
            "updated_at": "2026-08-09"
        })
    
    write_csv(file_path, records)
    print(f"[SUCCESS] Day 1 dataset created: {file_path}")
    return records

def generate_day2_updates(file_path, base_records):
    day2_records = []
    
    for record in base_records:
        rec = record.copy()
        rec["updated_at"] = "2026-08-10"
        
        # Simulate changes
        if rec["emp_id"] == 103:
            rec["status"] = "Resigned"  # Attrition event
        elif rec["emp_id"] == 105:
            rec["salary"] = rec["salary"] + 300000  # Salary raise
        elif rec["emp_id"] == 107:
            rec["department"] = "Engineering"  # Department change
            rec["job_title"] = "QA Engineer"
            
        day2_records.append(rec)
        
    write_csv(file_path, day2_records)
    print(f"[SUCCESS] Day 2 dataset created with updates: {file_path}")

def write_csv(file_path, records):
    fieldnames = ["emp_id", "full_name", "department", "job_title", "salary", "hire_date", "status", "updated_at"]
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    day1_data = generate_base_dataset("employees_day1.csv")
    generate_day2_updates("employees_day2.csv", day1_data)
