
# models
class TooManyStudentError(Exception):
    """Exception raised for errors in the student exceed school capacity case.
    Attributes:
        school_name (str, optional: name of the school.
        max_student (int, optional): maximum number of student accepted by the school.
    """

            # raise Exception(f'{self.school.name} has already {school_max_student} students. No more is allowed.')
    def __init__(self, school_name=None, max_student=None, message='Student is exceed the school capacity.'):
        self.school_name = school_name
        self.max_student = max_student
        super().__init__(message)

    def __str__(self):
        if None in (self.school_name, self.max_student):
            return 'Student is exceed the school capacity.'
        else:
            return f'{self.school_name} has already {self.max_student} students. No more is allowed.'
