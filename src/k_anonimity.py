
import pandas as pd

def evaluate_k_anonymity(subset_df, k_threshold):
    """
    Evaluates if a queried subset meets the minimum k-anonymity threshold
    
    
    -subset_df (DataFrame): The isolated data the user wants to query
    -k_threshold (int): The minimum allowable group size to prevent re-identification
        
    Returns:
        is_safe (bool): True if safe (size >= k), False if a threat (size < k)
        subset_size (int): The exact number of records found
    """
    #num rows
    subset_size = len(subset_df)
    
    # threshold check
    if subset_size < k_threshold:
        return False, subset_size  # Threat detect
    
    return True, subset_size       # Safe set


#local test
if __name__ == "__main__":
    print("Testing K-Anonymity Evaluator...")
    
    
    mock_executive_data = pd.DataFrame({
        'Department': ['Executive', 'Executive', 'Executive'],
        'Salary': [150000, 160000, 145000]
    })
    
    #Test 1: High k-threshold - should Fail
    strict_k = 50
    print(f"\nTest 1: Strict Threshold (k={strict_k})")
    safe, size = evaluate_k_anonymity(mock_executive_data, strict_k)
    if not safe:
        print(f"Threat successfully blocked! Only found {size} records.")
    
    #Test 2: Low k-threshold - should Pass
    loose_k = 2
    print(f"\nTest 2: Loose Threshold (k={loose_k})")
    safe, size = evaluate_k_anonymity(mock_executive_data, loose_k)
    if safe:
        print(f"Data approved for processing. Found {size} records.")