from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models import *
from app.services.study_plan_service import generate_38_day_plan
from datetime import date
import os

def read_content_file(filepath):
    """Read content from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return f"# Content\n\nContent not available."

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    content_dir = os.path.join(os.path.dirname(__file__), 'content')

    if db.query(Topic).count() == 0:
        topics_data = [
            {"name": "SQL", "slug": "sql", "description": "SQL Fundamentals and Advanced Queries", "icon": "database", "category": "database", "order_index": 1},
            {"name": "Python", "slug": "python", "description": "Python Programming for Data Engineering", "icon": "code", "category": "programming", "order_index": 2},
            {"name": "Tableau", "slug": "tableau", "description": "Data Visualization with Tableau", "icon": "chart", "category": "visualization", "order_index": 3},
            {"name": "Informatica", "slug": "informatica", "description": "ETL and Data Integration with Informatica", "icon": "workflow", "category": "etl", "order_index": 4},
            {"name": "Data Engineering", "slug": "data-engineering", "description": "Core Data Engineering Concepts", "icon": "engineering", "category": "engineering", "order_index": 5},
        ]

        for t in topics_data:
            topic = Topic(**t)
            db.add(topic)
        db.commit()

        sql_topic = db.query(Topic).filter(Topic.slug == "sql").first()
        python_topic = db.query(Topic).filter(Topic.slug == "python").first()
        tableau_topic = db.query(Topic).filter(Topic.slug == "tableau").first()
        informatica_topic = db.query(Topic).filter(Topic.slug == "informatica").first()
        de_topic = db.query(Topic).filter(Topic.slug == "data-engineering").first()

        # Load lessons from content files
        lessons_data = [
            # SQL Lessons (from content files)
            {"topic_id": sql_topic.id, "title": "SQL Fundamentals", "slug": "sql-fundamentals", "content": read_content_file(os.path.join(content_dir, "sql", "sql_fundamentals.md")), "duration_minutes": 90, "order_index": 1},
            {"topic_id": sql_topic.id, "title": "SQL Advanced", "slug": "sql-advanced", "content": read_content_file(os.path.join(content_dir, "sql", "sql_advanced.md")), "duration_minutes": 90, "order_index": 2},
            {"topic_id": sql_topic.id, "title": "SQL Practice", "slug": "sql-practice", "content": read_content_file(os.path.join(content_dir, "sql", "sql_practice.md")), "duration_minutes": 60, "order_index": 3},
            # SQL Labs
            {"topic_id": sql_topic.id, "title": "Lab: Basic SELECT", "slug": "sql-lab-basic-select", "content": read_content_file(os.path.join(content_dir, "sql", "lab1_basic_select.md")), "duration_minutes": 45, "order_index": 4},
            {"topic_id": sql_topic.id, "title": "Lab: Aggregations", "slug": "sql-lab-aggregations", "content": read_content_file(os.path.join(content_dir, "sql", "lab2_aggregations.md")), "duration_minutes": 45, "order_index": 5},
            {"topic_id": sql_topic.id, "title": "Lab: JOINs and Subqueries", "slug": "sql-lab-joins-subqueries", "content": read_content_file(os.path.join(content_dir, "sql", "lab3_joins_subqueries.md")), "duration_minutes": 60, "order_index": 6},

            # Python Lessons
            {"topic_id": python_topic.id, "title": "Python Fundamentals", "slug": "python-fundamentals", "content": read_content_file(os.path.join(content_dir, "python", "python_fundamentals.md")), "duration_minutes": 90, "order_index": 1},
            {"topic_id": python_topic.id, "title": "Python Data Structures", "slug": "python-data-structures", "content": read_content_file(os.path.join(content_dir, "python", "python_data_structures.md")), "duration_minutes": 60, "order_index": 2},
            {"topic_id": python_topic.id, "title": "Python Pandas", "slug": "python-pandas", "content": read_content_file(os.path.join(content_dir, "python", "python_pandas.md")), "duration_minutes": 90, "order_index": 3},
            {"topic_id": python_topic.id, "title": "Python Practice", "slug": "python-practice", "content": read_content_file(os.path.join(content_dir, "python", "python_practice.md")), "duration_minutes": 60, "order_index": 4},
            # Python Labs
            {"topic_id": python_topic.id, "title": "Lab: Variables and Data Types", "slug": "python-lab-variables", "content": read_content_file(os.path.join(content_dir, "python", "lab1_variables_datatypes.md")), "duration_minutes": 45, "order_index": 5},
            {"topic_id": python_topic.id, "title": "Lab: Data Structures", "slug": "python-lab-data-structures", "content": read_content_file(os.path.join(content_dir, "python", "lab2_data_structures.md")), "duration_minutes": 45, "order_index": 6},
            {"topic_id": python_topic.id, "title": "Lab: Functions and Modules", "slug": "python-lab-functions", "content": read_content_file(os.path.join(content_dir, "python", "lab3_functions_modules.md")), "duration_minutes": 60, "order_index": 7},
            {"topic_id": python_topic.id, "title": "Lab: Pandas Data Analysis", "slug": "python-lab-pandas", "content": read_content_file(os.path.join(content_dir, "python", "lab4_pandas_data_analysis.md")), "duration_minutes": 90, "order_index": 8},

            # Tableau Lessons
            {"topic_id": tableau_topic.id, "title": "Tableau Fundamentals", "slug": "tableau-fundamentals", "content": read_content_file(os.path.join(content_dir, "tableau", "tableau_fundamentals.md")), "duration_minutes": 90, "order_index": 1},
            {"topic_id": tableau_topic.id, "title": "Tableau Advanced", "slug": "tableau-advanced", "content": read_content_file(os.path.join(content_dir, "tableau", "tableau_advanced.md")), "duration_minutes": 90, "order_index": 2},
            {"topic_id": tableau_topic.id, "title": "Tableau Practice", "slug": "tableau-practice", "content": read_content_file(os.path.join(content_dir, "tableau", "tableau_practice.md")), "duration_minutes": 60, "order_index": 3},
            # Tableau Labs
            {"topic_id": tableau_topic.id, "title": "Lab: Basic Visualizations", "slug": "tableau-lab-basics", "content": read_content_file(os.path.join(content_dir, "tableau", "lab1_basic_visualizations.md")), "duration_minutes": 45, "order_index": 4},
            {"topic_id": tableau_topic.id, "title": "Lab: Calculations and Filters", "slug": "tableau-lab-calculations", "content": read_content_file(os.path.join(content_dir, "tableau", "lab2_calculations_filters.md")), "duration_minutes": 60, "order_index": 5},
            {"topic_id": tableau_topic.id, "title": "Lab: LOD Expressions", "slug": "tableau-lab-lod", "content": read_content_file(os.path.join(content_dir, "tableau", "lab3_lod_advanced.md")), "duration_minutes": 90, "order_index": 6},

            # Informatica Lessons
            {"topic_id": informatica_topic.id, "title": "Informatica Fundamentals", "slug": "informatica-fundamentals", "content": read_content_file(os.path.join(content_dir, "informatica", "informatica_fundamentals.md")), "duration_minutes": 90, "order_index": 1},
            # Informatica Labs
            {"topic_id": informatica_topic.id, "title": "Lab: Basic Mapping", "slug": "informatica-lab-basic", "content": read_content_file(os.path.join(content_dir, "informatica", "lab1_basic_mapping.md")), "duration_minutes": 60, "order_index": 2},
            {"topic_id": informatica_topic.id, "title": "Lab: Aggregator and Filter", "slug": "informatica-lab-aggregator", "content": read_content_file(os.path.join(content_dir, "informatica", "lab2_aggregator_filter.md")), "duration_minutes": 75, "order_index": 3},

            # Data Engineering Lessons
            {"topic_id": de_topic.id, "title": "Data Engineering Concepts", "slug": "de-concepts", "content": read_content_file(os.path.join(content_dir, "data_engineering", "data_engineering_concepts.md")), "duration_minutes": 90, "order_index": 1},
            # Data Engineering Labs
            {"topic_id": de_topic.id, "title": "Lab: Data Pipeline Design", "slug": "de-lab-pipeline", "content": read_content_file(os.path.join(content_dir, "data_engineering", "lab1_data_pipeline.md")), "duration_minutes": 90, "order_index": 2},
        ]

        for lesson in lessons_data:
            db.add(Lesson(**lesson))
        db.commit()

        sql_topic = db.query(Topic).filter(Topic.slug == "sql").first()
        python_topic = db.query(Topic).filter(Topic.slug == "python").first()
        tableau_topic = db.query(Topic).filter(Topic.slug == "tableau").first()
        informatica_topic = db.query(Topic).filter(Topic.slug == "informatica").first()
        de_topic = db.query(Topic).filter(Topic.slug == "data-engineering").first()

        questions_data = [
            {"topic_id": sql_topic.id, "question_text": "Which SQL clause is used to filter records?", "option_a": "WHERE", "option_b": "FILTER", "option_c": "GROUP BY", "option_d": "ORDER BY", "correct_option": "A", "explanation": "WHERE clause is used to filter records based on conditions.", "difficulty": "easy"},
            {"topic_id": sql_topic.id, "question_text": "Which JOIN returns all rows from both tables with NULLs for non-matches?", "option_a": "INNER JOIN", "option_b": "LEFT JOIN", "option_c": "RIGHT JOIN", "option_d": "FULL OUTER JOIN", "correct_option": "D", "explanation": "FULL OUTER JOIN returns all rows when there's a match in either table.", "difficulty": "medium"},
            {"topic_id": sql_topic.id, "question_text": "What does COUNT(*) return?", "option_a": "Number of unique values", "option_b": "Number of non-NULL values", "option_c": "Total number of rows", "option_d": "Sum of values", "correct_option": "C", "explanation": "COUNT(*) counts all rows including duplicates and NULLs.", "difficulty": "easy"},
            {"topic_id": sql_topic.id, "question_text": "Which clause groups rows with the same values?", "option_a": "WHERE", "option_b": "GROUP BY", "option_c": "HAVING", "option_d": "ORDER BY", "correct_option": "B", "explanation": "GROUP BY groups rows with the same values into summary rows.", "difficulty": "easy"},
            {"topic_id": sql_topic.id, "question_text": "What is a primary key?", "option_a": "Any column", "option_b": "Unique identifier for a table", "option_c": "First column", "option_d": "Foreign reference", "correct_option": "B", "explanation": "Primary key uniquely identifies each row in a table.", "difficulty": "easy"},

            {"topic_id": python_topic.id, "question_text": "Which data type is immutable in Python?", "option_a": "List", "option_b": "Dictionary", "option_c": "Set", "option_d": "Tuple", "correct_option": "D", "explanation": "Tuples are immutable sequences in Python.", "difficulty": "medium"},
            {"topic_id": python_topic.id, "question_text": "What does pd.DataFrame() create?", "option_a": "A series", "option_b": "A two-dimensional data structure", "option_c": "A function", "option_d": "A database connection", "correct_option": "B", "explanation": "DataFrame is a two-dimensional labeled data structure in Pandas.", "difficulty": "easy"},
            {"topic_id": python_topic.id, "question_text": "How do you comment in Python?", "option_a": "// comment", "option_b": "/* comment */", "option_c": "# comment", "option_d": "-- comment", "correct_option": "C", "explanation": "Hash (#) is used for single-line comments in Python.", "difficulty": "easy"},
            {"topic_id": python_topic.id, "question_text": "Which method reads a CSV file in Pandas?", "option_a": "pd.read_file()", "option_b": "pd.load_csv()", "option_c": "pd.read_csv()", "option_d": "pd.import_csv()", "correct_option": "C", "explanation": "pd.read_csv() is the Pandas method to read CSV files.", "difficulty": "easy"},
            {"topic_id": python_topic.id, "question_text": "What is the output of len([1, 2, 3])?", "option_a": "1", "option_b": "2", "option_c": "3", "option_d": "4", "correct_option": "C", "explanation": "len() returns the number of elements in a list.", "difficulty": "easy"},

            {"topic_id": tableau_topic.id, "question_text": "In Tableau, what are Measures?", "option_a": "Qualitative data", "option_b": "Numerical data to be aggregated", "option_c": "Filters", "option_d": "Calculations only", "correct_option": "B", "explanation": "Measures are numeric quantitative data that can be aggregated.", "difficulty": "easy"},
            {"topic_id": tableau_topic.id, "question_text": "Which chart type is best for trends over time?", "option_a": "Pie Chart", "option_b": "Bar Chart", "option_c": "Line Chart", "option_d": "Scatter Plot", "correct_option": "C", "explanation": "Line charts are ideal for showing trends over continuous time periods.", "difficulty": "easy"},
            {"topic_id": tableau_topic.id, "question_text": "What do Dimensions represent in Tableau?", "option_a": "Numeric values", "option_b": "Aggregated data", "option_c": "Categorical descriptive data", "option_d": "Calculations", "correct_option": "C", "explanation": "Dimensions are categorical descriptive data that organize measures.", "difficulty": "easy"},
            {"topic_id": tableau_topic.id, "question_text": "Which is a FIXED LOD expression?", "option_a": "{FIXED [Region] : SUM([Sales])}", "option_b": "{INCLUDE [Customer] : AVG([Profit])}", "option_c": "{EXCLUDE [Category] : SUM([Sales])}", "option_d": "All of the above", "correct_option": "D", "explanation": "FIXED, INCLUDE, and EXCLUDE are all types of LOD expressions.", "difficulty": "hard"},
            {"topic_id": tableau_topic.id, "question_text": "What is a dashboard in Tableau?", "option_a": "A single visualization", "option_b": "A collection of views", "option_c": "A data source", "option_d": "A calculation", "correct_option": "B", "explanation": "A dashboard combines multiple visualizations into a single view.", "difficulty": "easy"},

            {"topic_id": informatica_topic.id, "question_text": "What does ETL stand for?", "option_a": "Extract, Transform, Load", "option_b": "Evaluate, Transfer, Load", "option_c": "Extract, Transfer, Load", "option_d": "Enter, Transform, Leave", "correct_option": "A", "explanation": "ETL stands for Extract, Transform, Load.", "difficulty": "easy"},
            {"topic_id": informatica_topic.id, "question_text": "Which is an active transformation?", "option_a": "Expression", "option_b": "Lookup", "option_c": "Filter", "option_d": "Sequence", "correct_option": "C", "explanation": "Filter is an active transformation as it can change the number of rows.", "difficulty": "medium"},
            {"topic_id": informatica_topic.id, "question_text": "What is a mapping in Informatica?", "option_a": "Data type conversion", "option_b": "Rules for data transformation from source to target", "option_c": "A database table", "option_d": "A workflow", "correct_option": "B", "explanation": "A mapping defines how data is extracted, transformed, and loaded.", "difficulty": "medium"},
            {"topic_id": informatica_topic.id, "question_text": "Which transformation performs calculations?", "option_a": "Filter", "option_b": "Router", "option_c": "Expression", "option_d": "Aggregator", "correct_option": "C", "explanation": "Expression transformation performs row-level calculations.", "difficulty": "medium"},
            {"topic_id": informatica_topic.id, "question_text": "What is a workflow in Informatica?", "option_a": "A single task", "option_b": "A sequence of tasks that execute based on conditions", "option_c": "A data mapping", "option_d": "A transformation", "correct_option": "B", "explanation": "Workflows orchestrate the execution of multiple tasks.", "difficulty": "medium"},

            {"topic_id": de_topic.id, "question_text": "What is a star schema?", "option_a": "Normalized database design", "option_b": "Fact table with dimension tables", "option_c": "No relationships", "option_d": "Type of NoSQL", "correct_option": "B", "explanation": "Star schema has a fact table surrounded by denormalized dimension tables.", "difficulty": "medium"},
            {"topic_id": de_topic.id, "question_text": "Which is a 'V' of Big Data?", "option_a": "Volume", "option_b": "Velocity", "option_c": "Variety", "option_d": "All of the above", "correct_option": "D", "explanation": "The 5 V's of Big Data are Volume, Velocity, Variety, Veracity, and Value.", "difficulty": "easy"},
            {"topic_id": de_topic.id, "question_text": "What is data lake?", "option_a": "Small database", "option_b": "Structured data only", "option_c": "Storage repository for raw data in various formats", "option_d": "Data visualization", "correct_option": "C", "explanation": "A data lake stores raw data in its original format.", "difficulty": "easy"},
            {"topic_id": de_topic.id, "question_text": "What is Apache Kafka used for?", "option_a": "Batch processing", "option_b": "Stream processing", "option_c": "Data storage", "option_d": "Visualization", "correct_option": "B", "explanation": "Kafka is a distributed streaming platform for real-time data streams.", "difficulty": "medium"},
            {"topic_id": de_topic.id, "question_text": "What is denormalization?", "option_a": "Creating more tables", "option_b": "Combining tables for faster queries", "option_c": "Deleting data", "option_d": "Encrypting data", "correct_option": "B", "explanation": "Denormalization combines tables to reduce joins and improve read performance.", "difficulty": "medium"},
        ]

        for q in questions_data:
            db.add(Question(**q))
        db.commit()

    if db.query(StudyPlanDay).count() == 0:
        plan = generate_38_day_plan()
        for day in plan:
            db.add(day)
        db.commit()

    if db.query(MockExam).count() == 0:
        mock_exam = MockExam(
            title="TCS Wings Full Mock Test",
            description="Complete mock exam covering SQL, Python, Tableau, Informatica, and Data Engineering",
            duration_minutes=120,
            total_questions=50,
            passing_marks=35
        )
        db.add(mock_exam)
        db.commit()

    db.close()
    print("Database seeded successfully with full content!")

if __name__ == "__main__":
    seed_database()
