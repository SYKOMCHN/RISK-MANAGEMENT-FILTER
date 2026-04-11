
import pandas as pd
import numpy as np

#(The middle layer)

def basic_fetch(df, target_department):
    """Standard database fetch (Vulnerable to Access Pattern tracking)."""
    target_data = df[df['Department'] == target_department]
    return target_data

def oblivious_fetch(df, target_department, num_dummies=2):
    """Secure Oblivious RAM (ORAM) style fetch."""
    all_departments = df['Department'].unique()
    available_dummies = [d for d in all_departments if d != target_department]
    
    chosen_dummies = np.random.choice(available_dummies, size=num_dummies, replace=False)
    fetch_list = [target_department] + list(chosen_dummies)
    
    # Simulate backend fetch
    fetched_block = df[df['Department'].isin(fetch_list)]
    
    # Isolate target in proxy memory
    target_data = fetched_block[fetched_block['Department'] == target_department]
    
    return target_data, list(chosen_dummies)


# LOCAL TEST
# 

if __name__ == "__main__":
    print("Testing Oblivious Fetch Logic...")
    # Create a tiny mock dataframe just to test if the code compiles
    test_df = pd.DataFrame({
        'Department': ['HR', 'Engineering', 'Sales', 'Executive'],
        'Salary': [50000, 80000, 60000, 100000]
    })
    
    data, dummies = oblivious_fetch(test_df, 'Executive', 2)
    print(f"Target Acquired. Dummies used: {dummies}")
    data, dummies = oblivious_fetch(test_df, 'Executive', 2)
    print(f"Target Acquired. Dummies used: {dummies}")
    data, dummies = oblivious_fetch(test_df, 'Executive', 2)
    print(f"Target Acquired. Dummies used: {dummies}")
    
    data, dummies = oblivious_fetch(test_df, 'Executive', 3)
    print(f"Target Acquired. Dummies used: {dummies}")
    data, dummies = oblivious_fetch(test_df, 'Executive', 3)
    print(f"Target Acquired. Dummies used: {dummies}")
    data, dummies = oblivious_fetch(test_df, 'Executive', 3)
    print(f"Target Acquired. Dummies used: {dummies}")