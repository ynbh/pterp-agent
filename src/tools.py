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


# gemini 2.5 flash sucks with dates. maybe this helps?
@function_tool
def today():
    """
    Get the current date. 
    """
    return datetime.now().strftime("%Y-%m-%d")
    
