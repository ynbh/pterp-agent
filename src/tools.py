from datetime import datetime
from planet_terp import PlanetTerp
from agents import function_tool

client = PlanetTerp()

@function_tool
def get_professor(name: str, reviews: bool = False):
    """
    Get information about a professor from PlanetTerp.
    :param name: The name of the professor.
    :param reviews: Whether to include reviews. 
    """
    return client.professor(name, reviews)

@function_tool
def get_course(name: str, reviews: bool = False):
    """
    Get information about a course from PlanetTerp.
    :param name: The name of the course. E.g. CMSC330 
    :param reviews: Whether to include reviews.
    """
    return client.course(name, reviews)

@function_tool
def search_planet_terp(query: str, limit: int, offset: int):
    """
    Search PlanetTerp for information.
    :param query: The search query.
    :param limit: Maximum number of records to return.
    :param offset: Number of records to skip for pagination.
    """
    return client.search(query, limit, offset)

@function_tool
def get_grades(
    course: str = None, 
    professor: str = None, 
    semester: str = None, 
    section: str = None
):
    """
    Get grades for a course from PlanetTerp.
    
    :param course: Show only grades for the given course. Example: MATH140
    :param professor: Show only grades for the given professor. Example: Jon Snow
    :param semester: Show only grades for the given semester. Semester should be provided as the year followed by the semester code. 01 means Spring and 08 means Fall. For example, 202001 means Spring 2020. Default: all semesters
    :param section: Show only grades for the given section. Default: all sections
    """
    return client.grades(course, professor, semester, section)


@function_tool
def get_grades_report(
    course: str = None, 
    professor: str = None, 
    semester: str = None, 
    section: str = None
):
    """
    Get an aggregated grade report for a course/professor. 
    This tool calculates total counts and percentages accurately.
    
    :param course: Filter by course. Example: MATH140
    :param professor: Filter by professor. Example: Jon Snow
    :param semester: Filter by semester (e.g., 202001 for Spring 2020).
    :param section: Filter by section.
    """
    res = client.grades(course, professor, semester, section)
    if not res:
        return "No grade data found for the given filters."
    
    # Initialize totals
    totals = {
        "A+": 0, "A": 0, "A-": 0,
        "B+": 0, "B": 0, "B-": 0,
        "C+": 0, "C": 0, "C-": 0,
        "D+": 0, "D": 0, "D-": 0,
        "F": 0, "W": 0, "Other": 0
    }
    
    for g in res:
        totals["A+"] += g.A_plus
        totals["A"] += g.A
        totals["A-"] += g.A_minus
        totals["B+"] += g.B_plus
        totals["B"] += g.B
        totals["B-"] += g.B_minus
        totals["C+"] += g.C_plus
        totals["C"] += g.C
        totals["C-"] += g.C_minus
        totals["D+"] += g.D_plus
        totals["D"] += g.D
        totals["D-"] += g.D_minus
        totals["F"] += g.F
        totals["W"] += g.W
        totals["Other"] += g.Other

    total_graded = sum(totals.values())
    if total_graded == 0:
        return "Total student count is 0."

    percentages = {k: f"{(v/total_graded*100):.2f}%" for k, v in totals.items()}
    
    summary = {
        "Total Students": total_graded,
        "Grade Counts": totals,
        "Grade Percentages": percentages,
        "A-range (A+/A/A-)": f"{((totals['A+']+totals['A']+totals['A-'])/total_graded*100):.2f}%",
        "Pass Rate (>= C-)": f"{((total_graded - totals['D+'] - totals['D'] - totals['D-'] - totals['F'] - totals['W'] - totals['Other'])/total_graded*100):.2f}%"
    }
    
    return summary

@function_tool
def today():
    """
    Get the current date. 
    """
    return datetime.now().strftime("%Y-%m-%d")
    
