def marks_to_grade_points(marks: int) -> float:
    """
    Converts marks to grade points.
    Use this tool to convert a student's raw course marks or score (e.g., 78) into GPA grade points.
    """
    if marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"

    if marks >= 85:
        return 4.00
    elif marks >= 80:
        return 3.70
    elif marks >= 75:
        return 3.30
    elif marks >= 70:
        return 3.00
    elif marks >= 65:
        return 2.70
    elif marks >= 61:
        return 2.30
    elif marks >= 58:
        return 2.00
    elif marks >= 55:
        return 1.70
    elif marks >= 50:
        return 1.00
    else:
        return 0.00




def calculate_semester_gpa(grade_points: list[float], credit_hours: list[float]) -> float:
    """
    Calculates the GPA for a single semester.
    Use this tool when you need to compute a student's semester GPA using a list of their grade points and a list of their corresponding credit hours for that specific semester. Do not use this for projected or cumulative GPA (CGPA).
    """
    if len(grade_points) != len(credit_hours):
        return "Error: The number of grade points and credit hours must match."
    
    if not grade_points or not credit_hours:
        return "Error: Lists cannot be empty."
        
    total_credits = sum(credit_hours)
    if total_credits == 0:
        return "Error: Total credit hours cannot be zero."
        
    total_points = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    return total_points / total_credits




def calculate_new_cgpa(current_cgpa: float, completed_credit_hours: float, semester_gpa: float, semester_credit_hours: float) -> float:
    """
    Calculates the new cumulative GPA (CGPA) after completing a new semester.
    Use this tool to update a student's CGPA by taking a weighted average of their previously completed credit hours and their most recent semester.
    """
    if semester_credit_hours <= 0:
        return "Error: Semester credit hours must be greater than zero."
        
    if completed_credit_hours < 0:
        return "Error: Completed credit hours cannot be negative."
        
    if not (0.0 <= current_cgpa <= 4.0) or not (0.0 <= semester_gpa <= 4.0):
        return "Error: GPAs must be within the 0.0 to 4.0 scale."
        
    new_cgpa = (current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours) / (completed_credit_hours + semester_credit_hours)
    
    return new_cgpa




def required_gpa_for_target(target_cgpa: float, current_cgpa: float, completed_credit_hours: float, remaining_credit_hours: float) -> float:
    """
    Calculates the GPA required over remaining credit hours to achieve a target CGPA.
    Use this tool to determine the average GPA a student needs in their future courses to hit their goal.
    """
    if remaining_credit_hours <= 0:
        return "Error: Remaining credit hours must be greater than zero to avoid division by zero."
        
    if completed_credit_hours < 0:
        return "Error: Completed credit hours cannot be negative."
        
    if not (0.0 <= current_cgpa <= 4.0):
        return "Error: Current CGPA must be within the 0.0 to 4.0 scale."
        
    required_gpa = (target_cgpa * (completed_credit_hours + remaining_credit_hours) - current_cgpa * completed_credit_hours) / remaining_credit_hours
    
    return required_gpa




COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0)],


    2: [("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5)],


    3: [("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("GE-201", "Pakistan Studies", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],


    4: [("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5)],


    5: [("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5)],


    6: [("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5)],


    7: [("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5)],


    8: [("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5)],
}




def get_semester_courses(semester: int) -> str:
    """
    Retrieves and formats the list of courses for a given semester.
    Use this tool to look up the required courses, their codes, and credit hours for semesters 1 through 8.
    """
    if semester < 1 or semester > 8:
        return "Error: semester must be between 1 and 8"
        
    courses = COURSES.get(semester, [])
    formatted_courses = []
    
    for code, name, credits in courses:
        formatted_courses.append(f"{code}: {name} ({credits} Cr. Hrs.)")
        
    return "\n".join(formatted_courses)




def get_remaining_credit_hours(start_semester: int, end_semester: int) -> float:
    """
    Calculates the total credit hours from start_semester through end_semester (inclusive).
    Use this tool to determine the exact credit load for specific horizons (e.g., just semester 5, or semesters 5 through 7).
    """
    if start_semester < 1 or start_semester > 8 or end_semester < 1 or end_semester > 8:
        return "Error: semesters must be between 1 and 8"
        
    if start_semester > end_semester:
        return "Error: start_semester cannot be greater than end_semester"
        
    total_credits = sum(
        course[2] 
        for semester in range(start_semester, end_semester + 1) 
        for course in COURSES.get(semester, [])
    )
    
    return float(total_credits)




def save_report(filename: str, content: str) -> str:
    """
    Saves the provided content to a file in the current directory.
    Use this tool to generate the final output document once calculations are complete.
    """
    if not filename.endswith('.txt') and not '.' in filename:
        filename += '.txt'
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Report successfully saved to {filename}"
    except Exception as e:
        return f"Error: Failed to save report to {filename}. Details: {str(e)}"
