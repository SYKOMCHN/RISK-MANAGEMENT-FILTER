## System Architecture & Data Flow

The Adaptive Privacy Shield operates on a multi-tier architecture to ensure that neither the end-user nor the backend database administrator can compromise data privacy. 

# Step-by-Step Data Journey

The following outlines the exact lifecycle of a data query as it passes through the **Adaptive Privacy Shield** architecture. The system is designed to ensure that neither the end-user nor the backend database administrator can compromise data privacy.

### 1. User Input (The Request Initiator)
* **Action:** A data analyst interacting with the client interface submits a request for an aggregate metric of a specific demographic (e.g., the "Average Salary" of the "Executive" department).
* **Data State:** The user inputs the target demographic (`Department = 'Executive'`) and establishes the strictness of the defense mechanism by setting the K-Anonymity threshold (e.g., $k=10$) and the Differential Privacy budget (e.g., $\epsilon=1.0$).

### 2. Streamlit App (The Frontend Proxy)
* **Action:** The graphical user interface captures the user's request. It does **not** directly connect to the SQL database using a standard `SELECT` statement. Instead, it securely packages the parameters and hands them off to the backend Python middleware.

### 3. Oblivious Fetch Request (Access Pattern Protection)
* **Action:** To prevent a compromised database administrator from inferring what the user is analyzing, the middle layer masks the request. It randomly selects 2-3 "dummy" demographics (e.g., "HR" and "Sales"). 
* **Data State:** The proxy sends a bulk fetch request to the backend database for *all* employees in Executive, HR, and Sales. The database returns this massive, mixed block of data to the proxy's isolated secure memory. The backend database remains completely oblivious to the true target.

### 4. K-Anonymity Check (The Threat Assessor)
* **Action:** Inside the secure proxy, the dummy data blocks (HR and Sales) are immediately discarded. The system isolates the true target subset (Executives). Before performing any calculations, it evaluates the size of this subset ($S_{size}$).
* **Data State (The Fork):**
  * 🚫 **Path A (Threat Detected):** If there are only 12 Executives ($12 < k=50$), the system flags the query as a high re-identification risk. The data is wiped from memory, the flow is terminated, and a "Privacy Threat" error is returned to the user.
  * ✅ **Path B (Safe to Proceed):** If the target was "Engineering" and there are 20,000 records ($20,000 \ge k=50$), the system approves the subset and passes it to the next node.

### 5. DP Noise Injection (The Obfuscator)
* **Action:** Now that the subset is deemed large enough to hide individuals, the system calculates the *true* aggregate answer (e.g., True Average Salary = $75,400). It then determines the mathematical sensitivity ($\Delta f$) of the requested data. 
* **Data State:** The system utilizes the Laplace mechanism, combining the data sensitivity and the user's privacy budget ($\epsilon$) to generate a random noise value (e.g., +$632). It adds this noise to the true value. The true underlying data is then permanently deleted from proxy memory.

### 6. Output to User (The Delivery)
* **Action:** The sanitized, differentially private aggregate (e.g., $76,032) is sent back to the Streamlit frontend. 
* **Data State:** The user receives a highly accurate, yet perfectly anonymous aggregate data point on their dashboard. The privacy of the individuals in the backend database remains entirely mathematically uncompromised.