:- dynamic default_gpa/1.

% Default GPA threshold
default_gpa(2.0).

% Update the default GPA threshold
update_default_gpa(NewGPA) :-
    retractall(default_gpa(_)),
    assertz(default_gpa(NewGPA)).

% Calculate GPA
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

% Check if a student is on probation
is_on_probation(StudentID) :-
    default_gpa(DefaultGPA),
    student_gpa(StudentID, GPA),
    GPA =< DefaultGPA.