
import numpy as np

def calculate_sensitivity(query_type, subset_size, max_possible_value=200000):
    """
    Establishes the mathematical sensitivity (Δf) of the query
    Sensitivity is the maximum impact one individual's data can have on the final result
    

    - query_type (str): type of SQL aggregate ('AVERAGE', 'COUNT')
    - subset_size (int): num rows
    - max_possible_value (int): The assumed upper bound of a single record (e.g., max salary)
        
    
    - sensitivity (float): The calculated Δf
    """
    if query_type == 'COUNT':

        return 1.0 
    
    elif query_type == 'AVERAGE':
    
        # Δf = Max Value / Number of People
        return max_possible_value / subset_size
    
    else:
        raise ValueError(f"Unsupported query type: {query_type}")


def apply_laplace_noise(true_value, sensitivity, epsilon):
    """
    Injects noise drawn from a Laplace distribution.
    Formula: f'(D) = f(D) + Lap(Δf / ε)
    
    
    - true_value (float): The exact, insecure aggregate result
    - sensitivity (float): Δf 
    - epsilon (float): "privacy budget" - ε. Lower ε = more noise -> more privacy
        
    
    - noisy_value (float): The safe, differentially private aggregate
    """
    # If epsilon is 0 or negative, privacy is absolute (infinite noise)
    if epsilon <= 0:
        raise ValueError("Epsilon (ε) must be strictly greater than 0.0")
        
        
        
    # find  scale of Laplace distribution
    scale = sensitivity / epsilon
    
    
    # draw random noise from the Laplace distribution centered at 0
    noise = np.random.laplace(loc=0.0, scale=scale)
    
    # Add the noise to the true value
    noisy_value = true_value + noise
    
    return noisy_value

#local test
if __name__ == "__main__":
    print("Testing Differential Privacy Functions ...")
    
    # Mock data for an "Average Salary" query of 500 Engineers
    true_average_salary = 75000
    subset_size = 500
    privacy_budget = 1  # standard epsilon / the smaller the epsilon the bigger the noise
    
    print(f"\n--- Scenario: Calculating Average Salary for {subset_size} employees ---")
    print(f"True (Vulnerable) Value: ${true_average_salary:,.2f}")
    
    # calculate sensetivity
    sens = calculate_sensitivity('AVERAGE', subset_size)
    print(f"Calculated Sensitivity (Δf): {sens}")
    
    # add noise
    safe_value = apply_laplace_noise(true_average_salary, sens, privacy_budget)
    
    print(f"Protected (Noisy) Value: ${safe_value:,.2f}")
    print(f"Noise Added: ${(safe_value - true_average_salary):,.2f}")
    print("\n Data is now mathematically guaranteed to be ε-differentially private.")