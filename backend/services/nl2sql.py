import os
from groq import Groq

# ==========================================
# GROQ CLIENT (Lazy Loaded)
# ==========================================

_client = None

def get_groq_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables")
        _client = Groq(api_key=api_key)
    return _client


# ==========================================
# DATABASE SCHEMA
# ==========================================

SCHEMA = """
Tables:
Customer(CustomerID, Name, Email, Phone, Address)
Product(ProductID, Name, Description, Price)
"Order"(OrderID, CustomerID, OrderDate, TotalAmount)
OrderDetail(OrderDetailID, OrderID, ProductID, Quantity, UnitPrice)
Employee(EmployeeID, Name, Email, Phone, Position)
Activity(ActivityID, EmployeeID, Type, Description, ActivityDate, ActivityTime)
Campaign(CampaignID, Name, StartDate, EndDate, Budget)

Relationships:
"Order".CustomerID → Customer.CustomerID
OrderDetail.OrderID → "Order".OrderID
OrderDetail.ProductID → Product.ProductID
Activity.EmployeeID → Employee.EmployeeID
"""

RESERVED_TABLES = ["Order"]


# ==========================================
# SANITIZE RESERVED TABLES
# ==========================================

def sanitize_sql(sql: str) -> str:
    for table in RESERVED_TABLES:
        sql = sql.replace(f"FROM {table}", f'FROM "{table}"')
        sql = sql.replace(f"JOIN {table}", f'JOIN "{table}"')
        sql = sql.replace('"Order"Detail', 'OrderDetail')
    return sql


# ==========================================
# VALIDATION LAYER
# ==========================================

def validate_sql(sql: str):
    lower_sql = sql.lower()

    # Must start with SELECT
    if not lower_sql.startswith("select"):
        raise ValueError("Only SELECT statements allowed")

    # Block dangerous keywords
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    for word in forbidden:
        if word in lower_sql:
            raise ValueError("Dangerous SQL detected")

    # Prevent SELECT *
    if "select *" in lower_sql:
        raise ValueError("SELECT * is not allowed")

    # Prevent invalid-question execution
    if "invalid question" in lower_sql:
        raise ValueError("Question cannot be answered from schema")


# ==========================================
# MAIN SQL GENERATION
# ==========================================

def generate_sql(question: str) -> str:
    client = get_groq_client()

    prompt = f"""
You are a deterministic SQL compiler.

You MUST strictly follow the schema.
You are NOT allowed to invent tables, columns, or relationships.

========================
DATABASE SCHEMA
========================
{SCHEMA}

========================
STRICT RULES
========================
1. ONLY generate one SELECT statement.
2. NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER.
3. NEVER use tables not in schema.
4. NEVER use columns not in schema.
5. NEVER guess relationships.
6. ONLY JOIN tables if required.
7. DO NOT use SELECT *.
8. Return only necessary columns.
9. For sales → compute:
   OrderDetail.Quantity * OrderDetail.UnitPrice
10. Always include LIMIT 100.
11. Quote reserved table exactly as "Order".
12. If question cannot be answered, return:
   SELECT 'INVALID QUESTION' AS error LIMIT 1;
13. Use PostgreSQL date functions only.
    - Use EXTRACT(YEAR FROM column)
    - Use EXTRACT(MONTH FROM column)
    - Use DATE_TRUNC('month', column)
    - NEVER use YEAR() or MONTH() functions.

========================
OUTPUT RULES
========================
- Return SQL only.
- No explanation.
- No markdown.
- No comments.

========================
USER QUESTION
========================
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Remove markdown blocks if model adds them
    if sql.startswith("```"):
        sql = "\n".join(sql.split("\n")[1:-1])

    # Keep only first statement
    sql = sql.split(";")[0].strip() + ";"

    # Ensure LIMIT exists
    if "limit" not in sql.lower():
        sql = sql.rstrip(";") + " LIMIT 100;"

    # Sanitize reserved table usage
    sql = sanitize_sql(sql)

    # Validate before execution
    validate_sql(sql)

    return sql