# -------------------------------------------------
# generate_data.py  -  Synthetic Indian Customer Dataset Generator
# -------------------------------------------------
# Generates a LARGE, realistic synthetic dataset of Indian
# banking customers with behavioral financial signals for
# the Pre-Delinquency Intervention Engine.
#
# All data is Indian: names, cities, phone numbers, PAN,
# Aadhaar, IFSC codes, bank branches, INR currency.
#
# Produces 50,000 samples for robust model training.
# -------------------------------------------------

import os
import numpy as np
import pandas as pd

# Reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Number of synthetic customers  -  LARGE dataset for strong training
N_SAMPLES = 50_000

# Output path
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(DATA_DIR, "customer_signals.csv")

# ============================================================
# Indian Name, Location, and Banking Pools
# ============================================================

INDIAN_FIRST_NAMES_MALE = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh",
    "Ayaan", "Krishna", "Ishaan", "Shaurya", "Atharva", "Advik", "Pranav",
    "Advaith", "Aaryan", "Dhruv", "Kabir", "Ritvik", "Anay", "Rohan",
    "Harsh", "Arnav", "Sahil", "Kunal", "Rajesh", "Suresh", "Ramesh",
    "Vikram", "Deepak", "Amit", "Sumit", "Manish", "Rakesh", "Manoj",
    "Sanjay", "Nikhil", "Rohit", "Gaurav", "Ankur", "Vishal", "Karan",
    "Abhishek", "Pradeep", "Sunil", "Ajay", "Vijay", "Naveen", "Pankaj",
    "Ashish", "Mohit", "Tarun", "Varun", "Ravi", "Arun", "Hemant",
    "Yogesh", "Sachin", "Tushar", "Rahul", "Akash", "Devendra", "Prakash",
    "Dinesh", "Ganesh", "Mahesh", "Naresh", "Paresh", "Hitesh", "Jitesh",
    "Nilesh", "Rajat", "Sameer", "Tanmay", "Umesh", "Vinod", "Yash",
    "Zeeshan", "Farhan", "Irfan", "Junaid", "Kamran", "Nadeem", "Omar",
    "Shahid", "Tariq", "Wasim", "Aman", "Bharat", "Chetan", "Darshan",
    "Eshan", "Girish", "Harish", "Jayesh", "Kartik", "Lakshman",
    "Madhav", "Neeraj", "Omkar", "Parth", "Raghav", "Siddharth",
]

INDIAN_FIRST_NAMES_FEMALE = [
    "Aadhya", "Aanya", "Ananya", "Diya", "Myra", "Sara", "Ira",
    "Aisha", "Kiara", "Riya", "Prisha", "Anvi", "Amaira", "Navya",
    "Pari", "Saanvi", "Meera", "Nisha", "Pooja", "Neha", "Priya",
    "Sneha", "Divya", "Kavya", "Shruti", "Swati", "Megha", "Deepa",
    "Sunita", "Anita", "Geeta", "Seema", "Rekha", "Lata", "Shobha",
    "Usha", "Asha", "Kiran", "Jyoti", "Savita", "Suman", "Rani",
    "Parveen", "Shabana", "Nasreen", "Fatima", "Ayesha", "Zara",
    "Bhavna", "Chhaya", "Damini", "Ekta", "Gauri", "Hema", "Indira",
    "Janki", "Komal", "Leela", "Mala", "Nandini", "Padma", "Radha",
    "Sarita", "Tara", "Uma", "Varsha", "Yamini", "Archana", "Bindu",
    "Chitra", "Durga", "Esha", "Garima", "Heena", "Isha", "Juhi",
    "Kriti", "Lavanya", "Mansi", "Nikita", "Pallavi", "Rashmi",
    "Sakshi", "Tanvi", "Urmi", "Vidya", "Yashika", "Zoya",
    "Madhuri", "Namrata", "Poonam", "Ritu", "Shilpa", "Trupti",
]

INDIAN_LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah",
    "Mehta", "Joshi", "Mishra", "Pandey", "Tiwari", "Dubey", "Shukla",
    "Srivastava", "Yadav", "Chauhan", "Thakur", "Rajput", "Jain",
    "Agarwal", "Bansal", "Goyal", "Mittal", "Arora", "Kapoor", "Malhotra",
    "Chopra", "Bhatia", "Khanna", "Sethi", "Tandon", "Saxena", "Mathur",
    "Trivedi", "Bhatt", "Dave", "Desai", "Nair", "Menon", "Pillai",
    "Iyer", "Iyengar", "Reddy", "Rao", "Naidu", "Raju", "Murthy",
    "Hegde", "Kulkarni", "Patil", "Deshpande", "Jog", "Pawar", "Shinde",
    "Jadhav", "More", "Gaikwad", "Bhosale", "Chavan", "Deshmukh",
    "Mukherjee", "Chatterjee", "Banerjee", "Ghosh", "Das", "Bose",
    "Sen", "Roy", "Dutta", "Sarkar", "Majumdar", "Chakraborty",
    "Hussain", "Ahmed", "Khan", "Ansari", "Sheikh", "Siddiqui",
    "Choudhury", "Rahman", "Malik", "Gill", "Dhillon", "Brar",
    "Sandhu", "Kaur", "Bajwa", "Grewal", "Mann", "Saini", "Khatri",
    "Mahajan", "Kashyap", "Chandra", "Rathore", "Solanki", "Parmar",
]

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai",
    "Kolkata", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore",
    "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad",
    "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot",
    "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar",
    "Navi Mumbai", "Prayagraj", "Howrah", "Ranchi", "Gwalior", "Jabalpur",
    "Coimbatore", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota",
    "Chandigarh", "Guwahati", "Solapur", "Hubli", "Tiruchirappalli",
    "Bareilly", "Mysuru", "Tiruppur", "Gurugram", "Noida", "Dehradun",
    "Shimla", "Bhubaneswar", "Thiruvananthapuram", "Kochi", "Mangaluru",
]

INDIAN_STATES = {
    "Mumbai": "Maharashtra", "Delhi": "Delhi", "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana", "Ahmedabad": "Gujarat", "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal", "Pune": "Maharashtra", "Jaipur": "Rajasthan",
    "Lucknow": "Uttar Pradesh", "Kanpur": "Uttar Pradesh", "Nagpur": "Maharashtra",
    "Indore": "Madhya Pradesh", "Thane": "Maharashtra", "Bhopal": "Madhya Pradesh",
    "Visakhapatnam": "Andhra Pradesh", "Patna": "Bihar", "Vadodara": "Gujarat",
    "Ghaziabad": "Uttar Pradesh", "Ludhiana": "Punjab", "Agra": "Uttar Pradesh",
    "Nashik": "Maharashtra", "Faridabad": "Haryana", "Meerut": "Uttar Pradesh",
    "Rajkot": "Gujarat", "Varanasi": "Uttar Pradesh", "Srinagar": "Jammu & Kashmir",
    "Aurangabad": "Maharashtra", "Dhanbad": "Jharkhand", "Amritsar": "Punjab",
    "Navi Mumbai": "Maharashtra", "Prayagraj": "Uttar Pradesh", "Howrah": "West Bengal",
    "Ranchi": "Jharkhand", "Gwalior": "Madhya Pradesh", "Jabalpur": "Madhya Pradesh",
    "Coimbatore": "Tamil Nadu", "Vijayawada": "Andhra Pradesh", "Jodhpur": "Rajasthan",
    "Madurai": "Tamil Nadu", "Raipur": "Chhattisgarh", "Kota": "Rajasthan",
    "Chandigarh": "Chandigarh", "Guwahati": "Assam", "Solapur": "Maharashtra",
    "Hubli": "Karnataka", "Tiruchirappalli": "Tamil Nadu", "Bareilly": "Uttar Pradesh",
    "Mysuru": "Karnataka", "Tiruppur": "Tamil Nadu", "Gurugram": "Haryana",
    "Noida": "Uttar Pradesh", "Dehradun": "Uttarakhand", "Shimla": "Himachal Pradesh",
    "Bhubaneswar": "Odisha", "Thiruvananthapuram": "Kerala", "Kochi": "Kerala",
    "Mangaluru": "Karnataka",
}

BANK_BRANCHES = [
    "SBI Main Branch", "HDFC Bank", "ICICI Bank", "Axis Bank", "Bank of Baroda",
    "Punjab National Bank", "Canara Bank", "Union Bank of India", "Bank of India",
    "Indian Bank", "Central Bank of India", "Indian Overseas Bank", "UCO Bank",
    "Kotak Mahindra Bank", "Yes Bank", "IDBI Bank", "Federal Bank",
    "South Indian Bank", "Karur Vysya Bank", "City Union Bank",
    "Bandhan Bank", "RBL Bank", "IDFC First Bank", "IndusInd Bank",
]

LOAN_TYPES = [
    "Home Loan", "Personal Loan", "Car Loan", "Education Loan",
    "Business Loan", "Gold Loan", "Two Wheeler Loan", "Consumer Durable Loan",
    "Credit Card EMI", "Loan Against Property",
]

OCCUPATIONS = [
    "Software Engineer", "Teacher", "Doctor", "Business Owner", "Government Employee",
    "Bank Employee", "CA/Accountant", "Shopkeeper", "Farmer", "Driver",
    "Construction Worker", "Factory Worker", "Sales Executive", "Marketing Manager",
    "HR Professional", "Lawyer", "Pharmacist", "Nurse", "Electrician", "Plumber",
    "Auto Rickshaw Driver", "Delivery Executive", "Security Guard", "Chef/Cook",
    "Real Estate Agent", "Insurance Agent", "Freelancer", "Daily Wage Worker",
    "Retired", "Homemaker",
]


def _generate_indian_phone():
    """Generate a valid-looking Indian mobile number (+91-9XXXXXXXXX)."""
    first = np.random.choice([6, 7, 8, 9])
    rest = ''.join([str(np.random.randint(0, 10)) for _ in range(9)])
    return f"+91-{first}{rest}"


def _generate_account_number():
    """Generate a realistic Indian bank account number (12-16 digits)."""
    prefix = np.random.choice(["1001", "2004", "3056", "5001", "6234", "9100", "0412"])
    rest = ''.join([str(np.random.randint(0, 10)) for _ in range(8)])
    return f"{prefix}{rest}"


def _generate_pan():
    """Generate a realistic-looking Indian PAN number (ABCDE1234F)."""
    letters1 = ''.join(np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 5))
    digits = ''.join([str(np.random.randint(0, 10)) for _ in range(4)])
    letter2 = np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return f"{letters1}{digits}{letter2}"


def _generate_aadhaar():
    """Generate a masked Aadhaar number (XXXX-XXXX-1234)."""
    last4 = ''.join([str(np.random.randint(0, 10)) for _ in range(4)])
    return f"XXXX-XXXX-{last4}"


def _generate_ifsc():
    """Generate a realistic IFSC code (e.g. SBIN0012345)."""
    bank_codes = [
        "SBIN0", "HDFC0", "ICIC0", "UTIB0", "BARB0", "PUNB0", "CNRB0",
        "UBIN0", "BKID0", "IDIB0", "KKBK0", "YESB0", "IDFB0", "INDB0",
    ]
    code = np.random.choice(bank_codes)
    branch = ''.join([str(np.random.randint(0, 10)) for _ in range(6)])
    return f"{code}{branch}"


def generate_dataset(n: int = N_SAMPLES) -> pd.DataFrame:
    """
    Generate a large synthetic dataset of Indian banking customers.

    Returns DataFrame with:
      - Indian identity fields (name, city, phone, PAN, Aadhaar, bank, INR amounts)
      - 10 financial stress signal features
      - Binary target: default (0/1)
    """
    print(f"  Generating {n:,} synthetic Indian customer records...")

    # ---- Indian identity fields ----
    genders = np.random.choice(["Male", "Female"], n, p=[0.55, 0.45])
    first_names = []
    for g in genders:
        if g == "Male":
            first_names.append(np.random.choice(INDIAN_FIRST_NAMES_MALE))
        else:
            first_names.append(np.random.choice(INDIAN_FIRST_NAMES_FEMALE))

    last_names = np.random.choice(INDIAN_LAST_NAMES, n)
    names = [f"{fn} {ln}" for fn, ln in zip(first_names, last_names)]

    ages = np.random.normal(35, 10, n).clip(21, 65).astype(int)
    cities = np.random.choice(INDIAN_CITIES, n)
    states = [INDIAN_STATES.get(c, "Unknown") for c in cities]
    phones = [_generate_indian_phone() for _ in range(n)]
    pan_numbers = [_generate_pan() for _ in range(n)]
    aadhaar_masked = [_generate_aadhaar() for _ in range(n)]
    account_numbers = [_generate_account_number() for _ in range(n)]
    ifsc_codes = [_generate_ifsc() for _ in range(n)]
    branches = np.random.choice(BANK_BRANCHES, n)
    occupations = np.random.choice(OCCUPATIONS, n)

    # Monthly income in INR (INR 10,000 to INR 5,00,000 range)
    monthly_income = np.random.lognormal(10.5, 0.7, n).clip(10000, 500000).astype(int)

    loan_types = np.random.choice(LOAN_TYPES, n)
    loan_amounts = (monthly_income * np.random.uniform(6, 60, n)).clip(50000, 10000000).astype(int)
    tenures = np.random.choice([12, 24, 36, 48, 60, 84, 120, 180, 240], n)
    emi_amounts = (loan_amounts / tenures).astype(int)
    active_loans = np.random.poisson(1.5, n).clip(1, 8)
    emi_to_income_ratio = ((emi_amounts / monthly_income) * 100).clip(0, 100).round(2)
    upi_txn_count = np.random.poisson(45, n).clip(0, 300)

    # ---- Financial stress signal features (core ML inputs) ----
    print("  Generating financial stress signals...")

    salary_delay_days = np.random.exponential(3, n).clip(0, 30).round(1)
    balance_trend = np.random.normal(-5, 15, n).clip(-50, 20).round(2)
    bill_payment_delay = np.random.exponential(4, n).clip(0, 30).round(1)
    transaction_anomaly = np.abs(np.random.normal(1, 1.2, n)).clip(0, 5).round(2)
    discretionary_drop_pct = (np.random.beta(2, 5, n) * 100).round(2)
    atm_withdrawal_spike = np.random.lognormal(0.2, 0.5, n).clip(0.5, 5).round(2)
    failed_auto_debits = np.random.poisson(0.8, n).clip(0, 5)
    lending_app_txns = np.random.poisson(2, n).clip(0, 20)
    savings_drawdown_pct = (np.random.beta(2, 5, n) * 100).round(2)
    credit_utilization = (np.random.beta(2, 3, n) * 100).round(2)

    # ---- Target variable via logistic model ----
    print("  Computing default probabilities...")
    logit = (
        0.20 * salary_delay_days
        - 0.06 * balance_trend
        + 0.15 * bill_payment_delay
        + 0.40 * transaction_anomaly
        + 0.025 * discretionary_drop_pct
        + 0.35 * (atm_withdrawal_spike - 1)
        + 0.60 * failed_auto_debits
        + 0.12 * lending_app_txns
        + 0.03 * savings_drawdown_pct
        + 0.02 * credit_utilization
        + 0.02 * emi_to_income_ratio
        + 0.10 * (active_loans - 1)
        - 8.2  # intercept calibrated for ~25% default rate
    )
    prob = 1 / (1 + np.exp(-logit))
    default = (np.random.rand(n) < prob).astype(int)

    # ---- Assemble DataFrame ----
    print("  Assembling DataFrame...")
    df = pd.DataFrame({
        "customer_id": [f"CUST-{i+1:06d}" for i in range(n)],
        "name": names,
        "gender": genders,
        "age": ages,
        "phone": phones,
        "city": cities,
        "state": states,
        "pan_number": pan_numbers,
        "aadhaar_masked": aadhaar_masked,
        "account_number": account_numbers,
        "ifsc_code": ifsc_codes,
        "bank_branch": branches,
        "occupation": occupations,
        "monthly_income_inr": monthly_income,
        "loan_type": loan_types,
        "loan_amount_inr": loan_amounts,
        "emi_amount_inr": emi_amounts,
        "loan_tenure_months": tenures,
        "active_loans": active_loans,
        "emi_to_income_ratio": emi_to_income_ratio,
        "upi_txn_count": upi_txn_count,
        # Core 10 ML features
        "salary_delay_days": salary_delay_days,
        "balance_trend": balance_trend,
        "bill_payment_delay": bill_payment_delay,
        "transaction_anomaly": transaction_anomaly,
        "discretionary_drop_pct": discretionary_drop_pct,
        "atm_withdrawal_spike": atm_withdrawal_spike,
        "failed_auto_debits": failed_auto_debits,
        "lending_app_txns": lending_app_txns,
        "savings_drawdown_pct": savings_drawdown_pct,
        "credit_utilization": credit_utilization,
        # Target
        "default": default,
    })

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("  Generating Indian Customer Financial Signals Dataset")
    print("=" * 60)

    df = generate_dataset()
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n  Dataset saved to {OUTPUT_PATH}")
    print(f"  Shape: {df.shape}")
    print(f"  Default rate: {df['default'].mean():.2%}")
    print(f"  Total records: {len(df):,}")
    print(f"\n  Income: INR {df['monthly_income_inr'].min():,}  -  INR {df['monthly_income_inr'].max():,}")
    print(f"  Avg income: INR {df['monthly_income_inr'].mean():,.0f}/month")
    print(f"  Avg loan: INR {df['loan_amount_inr'].mean():,.0f}")
    print(f"  Avg EMI: INR {df['emi_amount_inr'].mean():,.0f}/month")

    print(f"\n  Top 10 cities:")
    print(df['city'].value_counts().head(10).to_string())

    print(f"\n  Gender split: {dict(df['gender'].value_counts())}")

    print(f"\n  Sample records:")
    cols = ['customer_id', 'name', 'city', 'monthly_income_inr',
            'loan_amount_inr', 'salary_delay_days', 'failed_auto_debits', 'default']
    print(df[cols].head(10).to_string())

    print("\n" + "=" * 60)
