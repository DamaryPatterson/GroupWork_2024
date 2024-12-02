% GPA Calculation Predicates

% Grade point mapping
grade_point(4.0, 'A').
grade_point(3.67, 'A-').
grade_point(3.33, 'B+').
grade_point(3.0, 'B').
grade_point(2.67, 'B-').
grade_point(2.33, 'C+').
grade_point(2.0, 'C').
grade_point(1.67, 'C-').
grade_point(1.33, 'D+').
grade_point(1.0, 'D').
grade_point(0.0, 'F').

% Calculate grade points for a module
calculate_module_grade_points(GradePoints, Credits, ModuleGradePoints) :-
    ModuleGradePoints is GradePoints * Credits.

% Calculate semester GPA
calculate_semester_gpa(Modules, Semester, SemesterGPA) :-
    include(is_semester_module(Semester), Modules, SemesterModules),
    maplist(module_grade_points, SemesterModules, GradePointsList),
    sumlist(GradePointsList, TotalGradePoints),
    maplist(module_credits, SemesterModules, CreditsList),
    sumlist(CreditsList, TotalCredits),
    (TotalCredits > 0 -> 
        SemesterGPA is TotalGradePoints / TotalCredits
    ;   SemesterGPA = 0).

% Calculate cumulative GPA
calculate_cumulative_gpa(Modules, CumulativeGPA) :-
    maplist(module_grade_points, Modules, GradePointsList),
    sumlist(GradePointsList, TotalGradePoints),
    maplist(module_credits, Modules, CreditsList),
    sumlist(CreditsList, TotalCredits),
    (TotalCredits > 0 -> 
        CumulativeGPA is TotalGradePoints / TotalCredits
    ;   CumulativeGPA = 0).

% Check academic probation status
check_academic_probation(Modules, Threshold, OnProbation) :-
    calculate_cumulative_gpa(Modules, CumulativeGPA),
    (CumulativeGPA =< Threshold -> 
        OnProbation = true 
    ;   OnProbation = false).

% Helper predicates
is_semester_module(Semester, module(_, Semester, _, _)).
module_grade_points(module(_, _, GradePoints, Credits), ModuleGradePoints) :-
    calculate_module_grade_points(GradePoints, Credits, ModuleGradePoints).
module_credits(module(_, _, _, Credits), Credits).

% Main calculation predicate to be called from Python
calculate_gpa(Modules, Results) :-
    maplist(extract_semester, Modules, Semesters),
    list_to_set(Semesters, UniqueSemesters),
    calculate_semester_gpas(Modules, UniqueSemesters, SemesterGPAs),
    calculate_cumulative_gpa(Modules, CumulativeGPA),
    Results = [cumulative_gpa(CumulativeGPA) | SemesterGPAs].

% Calculate GPAs for each semester
calculate_semester_gpas(_, [], []).
calculate_semester_gpas(Modules, [Semester|RestSemesters], 
                        [semester_gpa(Semester, SemesterGPA)|RestResults]) :-
    calculate_semester_gpa(Modules, Semester, SemesterGPA),
    calculate_semester_gpas(Modules, RestSemesters, RestResults).

% Extract semester from module
extract_semester(module(_, Semester, _, _), Semester).

% Predicate to format results for Python
format_gpa_result(Results, FormattedResults) :-
    maplist(format_single_result, Results, FormattedResults).

format_single_result(cumulative_gpa(GPA), 
                     result(key='Cumulative GPA', value=GPA)).
format_single_result(semester_gpa(Semester, GPA), 
                     result(key=['Semester ', Semester, ' GPA'], value=GPA)).