:- dynamic default_gpa/1.

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

% Default GPA threshold
default_gpa(2.0).

update_default_gpa(NewGPA) :-
    retractall(default_gpa(_)),
    assertz(default_gpa(NewGPA)).

calculate_gpa(GradePoints, Credits, GPA) :-
    sum_product(GradePoints, Credits, TotalGradePoints),
    sum(Credits, TotalCredits),
    GPA is TotalGradePoints / TotalCredits.

sum_product([], [], 0).
sum_product([G|Gs], [C|Cs], Total) :-
    sum_product(Gs, Cs, SubTotal),
    Total is SubTotal + G * C.

sum([], 0).
sum([X|Xs], Total) :-
    sum(Xs, SubTotal),
    Total is SubTotal + X.