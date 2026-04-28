from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.study_plan import StudyPlanDay

def generate_38_day_plan(start_date: date = date(2026, 4, 25)) -> list:
    topics_schedule = [
        ("SQL Fundamentals", ["SELECT statements", "WHERE clause", "Basic filtering"], 1),
        ("SQL Advanced", ["JOINs", "Subqueries", "Window Functions"], 1),
        ("Python Basics", ["Variables", "Data Types", "Control Flow"], 2),
        ("Python Data Structures", ["Lists", "Dictionaries", "Sets"], 2),
        ("Python Libraries", ["Pandas", "NumPy", "Matplotlib"], 2),
        ("Tableau Fundamentals", ["Connect to Data", "Worksheets", "Basic Charts"], 3),
        ("Tableau Calculations", ["Calculated Fields", "LOD Expressions", "Table Calculations"], 3),
        ("Tableau Dashboards", ["Dashboard Design", "Actions", "Stories"], 3),
        ("Informatica Basics", ["PowerCenter", "Mappings", "Transformations"], 4),
        ("Informatica Workflows", ["Workflow Manager", "Tasks", "Session"], 4),
        ("Data Engineering Concepts", ["ETL/ELT", "Data Warehousing", "Big Data"], 5),
        ("Integration Projects", ["End-to-End Scenarios", "Best Practices"], 5),
        ("Mock Tests & Review", ["Full Length Tests", "Revision"], 5),
    ]

    plan = []
    current = start_date
    day_num = 1

    while current <= date(2026, 6, 1) and day_num <= 38:
        topic_idx = (day_num - 1) // 3 % len(topics_schedule)
        topic_name, objectives, topic_id = topics_schedule[topic_idx]

        hours = 4 if day_num <= 10 else 5 if day_num <= 22 else 6

        plan.append(StudyPlanDay(
            day_number=day_num,
            date=current.strftime("%Y-%m-%d"),
            day_topic=topic_name,
            topics=[topic_name],
            objectives=objectives,
            estimated_hours=hours,
            is_completed=False
        ))

        current += timedelta(days=1)
        day_num += 1

    return plan
