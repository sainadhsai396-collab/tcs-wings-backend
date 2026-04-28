from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter(prefix="/api/ai", tags=["ai"])

class ChatRequest(BaseModel):
    message: str

# Simple rule-based responses for common topics
topic_responses = {
    "sql": {
        "join": """**SQL JOINs Explained:**

• **INNER JOIN**: Returns rows that have matching values in BOTH tables
• **LEFT JOIN**: Returns ALL rows from left table + matching rows from right
• **RIGHT JOIN**: Returns ALL rows from right table + matching rows from left
• **FULL OUTER JOIN**: Returns all rows when there's a match in either table

**Example:**
```sql
SELECT e.name, d.department
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id
```

**Tip**: Use LEFT JOIN when you need to keep all records from the primary table!""",
        "window": """**SQL Window Functions:**

Window functions perform calculations across rows related to the current row.

**Common Functions:**
• `ROW_NUMBER()` - Assigns unique row numbers
• `RANK()` - Assigns rank with gaps
• `DENSE_RANK()` - Assigns rank without gaps
• `SUM() OVER()` - Running total
• `AVG() OVER()` - Moving average

**Example:**
```sql
SELECT name, salary,
  RANK() OVER (ORDER BY salary DESC) as rank,
  SUM(salary) OVER (PARTITION BY department) as dept_total
FROM employees
```

**Key Concept**: OVER() clause defines the window!""",
        "select": """**SELECT Statement Best Practices:**

1. **Specify columns** - Don't use SELECT * in production
2. **Use aliases** - Make output readable
```sql
SELECT first_name AS "First Name" FROM users
```
3. **Use DISTINCT** - Remove duplicates
4. **Filter with WHERE** - Reduce rows early
5. **Sort with ORDER BY** - Control output order

**Performance Tip**: Filter data early to reduce processing load!""",
        "default": """**SQL Fundamentals:**

• **SELECT**: Choose columns
• **FROM**: Specify table
• **WHERE**: Filter rows
• **GROUP BY**: Aggregate data
• **HAVING**: Filter groups
• **ORDER BY**: Sort results

Ask about: JOINs, Window Functions, Subqueries, Indexes, Optimization"""
    },
    "python": {
        "list": """**Python List Comprehension Tips:**

```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested
flat = [x for row in matrix for x in row]

# With multiple operations
names = [f"{n.upper()} - {len(n)} chars" for n in names]
```

**Benefits**: More concise, often faster than loops!""",
        "pandas": """**Pandas Tips for Data Engineering:**

```python
import pandas as pd

# Read data efficiently
df = pd.read_csv('data.csv', dtype={'col': 'str'})

# Select columns (faster)
df = df[['a', 'b', 'c']]

# Filter rows (faster)
df = df[df['status'] == 'active']

# Group and aggregate
summary = df.groupby('category').agg({'value': 'sum', 'count': 'size'})

# Merge dataframes
result = pd.merge(df1, df2, on='key', how='left')
```

**Tip**: Use `df.info()` to check memory usage!""",
        "dictionary": """**Python Dictionary Tips:**

```python
# Create from two lists
keys = ['a', 'b', 'c']
vals = [1, 2, 3]
d = dict(zip(keys, vals))

# Safe get
value = d.get('missing', 'default')

# Update
d.update({'new_key': 'new_value'})

# Comprehension
squares = {k: k**2 for k in range(5)}
```""",
        "default": """**Python for Data Engineering:**

Topics to explore:
• **Data Types**: Lists, Dictionaries, Sets, Tuples
• **Control Flow**: if/else, loops, comprehensions
• **Functions**: def, lambda, args, kwargs
• **Libraries**: Pandas, NumPy, Matplotlib

Ask about: specific Python concepts, Pandas operations, data structures"""
    },
    "tableau": {
        "calculated": """**Tableau Calculated Fields:**

1. **Go to**: Analysis > Create Calculated Field
2. **Syntax**: `[Field] OPERATOR value`

**Common Examples:**
```tableau
// Profit calculation
[Sales] - [Cost]

// Percentage
[Profit] / [Sales] * 100

// Conditional
IF [Sales] > 1000 THEN "High"
ELSEIF [Sales] > 500 THEN "Medium"
ELSE "Low" END
```

**Tips:**
• Use IIF() for simple conditionals
• ATTR() for aggregating dimensions
• ZN() to replace nulls with zero""",
        "lod": """**Tableau LOD Expressions (Level of Detail):**

**FIXED LOD:**
```tableau
{ FIXED [Region] : SUM([Sales]) }
```
Calculates sales per region regardless of visualization.

**INCLUDE LOD:**
```tableau
{ INCLUDE [Customer] : AVG([Order Size]) }
```
Calculates average per customer in current context.

**EXCLUDE LOD:**
```tableau
{ EXCLUDE [Month] : SUM([Sales]) }
```
Removes Month from calculation.

**When to use:**
• Per-customer metrics in region visualization
• Keeping dimension while adding aggregations
• Ignoring certain dimensions in calculation""",
        "chart": """**Tableau Chart Types & Best Practices:**

1. **Bar Charts** - Compare categories
2. **Line Charts** - Show trends over time
3. **Scatter Plots** - Show relationships
4. **Heat Maps** - Show density
5. **Tree Maps** - Show proportions

**Design Tips:**
• Use color purposefully
• Label axes clearly
• Add tooltips for context
• Sort bars for impact
• Avoid 3D effects""",
        "default": """**Tableau for Data Visualization:**

Key areas to master:
• **Connecting** data sources
• **Building** worksheets with charts
• **Calculated Fields** and logic
• **LOD Expressions** for complex calculations
• **Dashboards** combining multiple views
• **Actions** for interactivity

Ask about: Specific chart types, Calculated fields, LOD expressions, Dashboard design"""
    },
    "data engineering": {
        "etl": """**ETL vs ELT:**

**ETL (Extract, Transform, Load):**
1. Extract data from sources
2. Transform in staging area
3. Load to destination

**ELT (Extract, Load, Transform):**
1. Extract from sources
2. Load raw data to destination
3. Transform using destination power

**When to use:**
• ETL: Small data, strict transformation needs
• ELT: Large data, modern cloud data warehouses""",
        "warehouse": """**Data Warehouse Concepts:**

**Star Schema:**
• Fact table (transactions, measurements)
• Dimension tables (descriptive attributes)
• Simple joins, fast queries

**Snowflake Schema:**
• Normalized dimensions
• Less redundancy, more complex

**Facts vs Dimensions:**
• **Fact**: Measurable metrics (sales, quantity)
• **Dimension**: Context (who, what, where, when)

**Slowly Changing Dimensions (SCD):**
• Type 1: Overwrite
• Type 2: Add new row
• Type 3: Add new column""",
        "pipeline": """**Building Data Pipelines:**

**Best Practices:**
1. **Start with sources** - Understand data origins
2. **Add logging** - Track processing steps
3. **Handle errors** - Implement retries
4. **Monitor** - Track data quality
5. **Document** - Schema, lineage

**Common Tools:**
• **Batch**: Airflow, Luigi, Databricks
• **Streaming**: Kafka, Flink, Spark Streaming
• **Orchestration**: Airflow, Prefect, Dagster

**Testing**: Validate data at each step!""",
        "default": """**Data Engineering Fundamentals:**

Key concepts:
• **ETL/ELT** - Data integration patterns
• **Data Warehousing** - Schema design, star/snowflake
• **Data Lakes** - Raw storage for diverse data
• **Data Pipelines** - Automation and orchestration
• **Big Data** - Distributed processing

Ask about: specific concepts, architecture patterns, tools comparison"""
    }
}

def get_topic_key(message):
    msg = message.lower()
    if 'sql' in msg:
        if any(w in msg for w in ['join', 'inner', 'left', 'right', 'outer']): return 'sql.join'
        if any(w in msg for w in ['window', 'rank', 'row_number', 'over', 'partition']): return 'sql.window'
        if any(w in msg for w in ['select', 'query', 'where', 'basic']): return 'sql.select'
        return 'sql.default'
    if any(w in msg for w in ['python', 'pandas', 'list', 'dict', 'data structure']):
        if 'list' in msg: return 'python.list'
        if any(w in msg for w in ['pandas', 'dataframe', 'df']): return 'python.pandas'
        if any(w in msg for w in ['dict', 'dictionary']): return 'python.dictionary'
        return 'python.default'
    if any(w in msg for w in ['tableau', 'visualization', 'chart', 'dashboard']):
        if any(w in msg for w in ['calculat', 'field', 'formula']): return 'tableau.calculated'
        if any(w in msg for w in ['lod', 'level of detail', 'fixed', 'include', 'exclude']): return 'tableau.lod'
        if any(w in msg for w in ['chart', 'visual', 'bar', 'line']): return 'tableau.chart'
        return 'tableau.default'
    if any(w in msg for w in ['data engineer', 'etl', 'elt', 'pipeline', 'warehouse', 'data lake']):
        if 'etl' in msg or 'elt' in msg: return 'data engineering.etl'
        if any(w in msg for w in ['warehouse', 'star', 'snowflake', 'dimension']): return 'data engineering.warehouse'
        if any(w in msg for w in ['pipeline', 'orchestrat', 'airflow']): return 'data engineering.pipeline'
        return 'data engineering.default'
    return None

def generate_response(message):
    topic_key = get_topic_key(message)
    if topic_key:
        topic, subtopic = topic_key.split('.')
        return topic_responses.get(topic, {}).get(subtopic, topic_responses.get(topic, {}).get('default'))

    # Greeting handling
    msg_lower = message.lower()
    if any(g in msg_lower for g in ['hello', 'hi', 'hey', 'help']):
        return "Hello! I'm your AI study assistant for TCS Wings. I can help you with:\n\n• **SQL** - Queries, JOINs, Window Functions\n• **Python** - Data structures, Pandas, best practices\n• **Tableau** - Charts, calculations, LOD expressions\n• **Data Engineering** - ETL, warehousing, pipelines\n\nWhat would you like to learn about today?"

    # Study tips
    if any(t in msg_lower for t in ['tip', 'trick', 'advice', 'how to study']):
        return """**📚 Study Tips & Tricks:**

1. **Practice Daily** - Code every day, even 30 minutes helps
2. **SQL by Doing** - Write queries, don't just read
3. **Real Data** - Work with actual datasets, not just examples
4. **Teach Others** - Explaining reinforces learning
5. **Build Projects** - Apply concepts in end-to-end projects

**For Interviews:**
• Practice SQL on LeetCode/Hackerrank
• Build a Tableau portfolio
• Explain your projects confidently
• Know the difference between Data Lake and Warehouse

Would you like to dive into any specific topic?"""

    # Default
    return """I'm here to help with your TCS Wings preparation! I specialize in:

🔹 **SQL** - Fundamentals, JOINs, Window Functions, Optimization
🔹 **Python** - Basics, Data Structures, Pandas, Best Practices
🔹 **Tableau** - Charts, Calculations, LOD Expressions, Dashboards
🔹 **Data Engineering** - ETL/ELT, Data Warehousing, Pipelines

Try asking:
- "Explain SQL JOINs with examples"
- "Python list comprehension tips"
- "Tableau calculated fields tutorial"
- "Data Engineering interview questions"
- "Study tips for TCS preparation"

What would you like to explore?"""

@router.post("/chat")
async def chat(request: ChatRequest):
    response = generate_response(request.message)
    return {"response": response}