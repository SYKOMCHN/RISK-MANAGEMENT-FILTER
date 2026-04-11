import pandas as pd
import numpy as np

def generate_mock_database(num_records=10000):
    """
    Generates a synthetic HR dataset designed to test privacy-preserving algorithms.
    """
    print(f"Generating {num_records} synthetic employee records...")
    
    #same seed for now
    np.random.seed(11) 

    #--Direct Identifiers
    emp_ids = range(10000, 10000 + num_records)

    #--Quasi-Identifiers
    ages = np.random.randint(22, 75, num_records)
    zip_codes = np.random.choice(['44122', '44123', '44124', '44125', '44126'], num_records)

    #--Skew the Department Distribution
    #  engineering - huge (Safe) -- Executive/SpecialOps - tiny (Privacy Threat)
    departments = ['Engineering', 'Sales', 'Customer Support', 'HR', 'Executive', 'SpecialOps']
    
    dept_probs = [0.40, 0.30, 0.20, 0.095, 0.004, 0.001] 
    depts = np.random.choice(departments, num_records, p=dept_probs)

    #--Sensitive Attributes (Salary)
    #normal distribution centered at 70k with a 15k standard deviation
    salaries = np.random.normal(loc=70000, scale=15000, size=num_records)
    # Ensure no negative salaries and round to whole numbers
    salaries = np.clip(salaries, a_min=35000, a_max=None).astype(int)

    #--Pandas DataFrame
    df = pd.DataFrame({
        'EmployeeID': emp_ids,
        'Age': ages,
        'Department': depts,
        'ZipCode': zip_codes,
        'Salary': salaries
    })

    return df

if __name__ == "__main__":
    # generate 10,000 rows
    hr_database = generate_mock_database(10000)
    
    # Save as CSV 
    hr_database.to_csv('mock_hr_database.csv', index=False)
    print("Successfully generated and saved to 'mock_hr_database.csv'")
    
    # Print a quick distribution check to prove the skewed data worked
    print("\nDepartment Frequency Distribution:")
    print(hr_database['Department'].value_counts())