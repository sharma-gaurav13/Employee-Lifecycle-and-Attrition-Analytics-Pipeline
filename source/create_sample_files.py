import pandas as pd

# Day 1 Initial Snapshot
day1_data = {
    "emp_id": [101, 102, 103],
    "full_name": ["Aarav Sharma", "Priya Patel", "Rohan Gupta"],
    "department": ["Engineering", "Marketing", "Engineering"],
    "job_title": ["Software Engineer", "Marketing Specialist", "DevOps Engineer"],
    "salary": [85000.0, 60000.0, 92000.0],
    "hire_date": ["2024-01-15", "2023-06-10", "2022-11-01"],
    "status": ["Active", "Active", "Active"],
    "updated_at": ["2026-08-09", "2026-08-09", "2026-08-09"]
}
pd.DataFrame(day1_data).to_csv("employees_day1.csv", index=False)

# Day 2 Updates (Priya gets a salary bump, Rohan changes department, a new employee is hired)
day2_data = {
    "emp_id": [101, 102, 103, 104],
    "full_name": ["Aarav Sharma", "Priya Patel", "Rohan Gupta", "Neha Verma"],
    "department": ["Engineering", "Marketing", "Data Science", "HR"],
    "job_title": ["Software Engineer", "Senior Marketing Specialist", "Data Scientist", "HR Manager"],
    "salary": [85000.0, 70000.0, 95000.0, 75000.0],
    "hire_date": ["2024-01-15", "2023-06-10", "2022-11-01", "2026-08-10"],
    "status": ["Active", "Active", "Active", "Active"],
    "updated_at": ["2026-08-10", "2026-08-10", "2026-08-10", "2026-08-10"]
}   
pd.DataFrame(day2_data).to_csv("employees_day2.csv", index=False)

print("Sample CSV files with Indian names generated successfully!")
