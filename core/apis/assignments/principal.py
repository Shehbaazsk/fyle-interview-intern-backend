from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from core.libs.exceptions import FyleError
from .schema import AssignmentSchema,AssignmentGradeSchema
from core.apis.teachers.schema import TeacherSchema


principal_assignments_resources = Blueprint('principal_assignments_resources',__name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignment(p):
    """Returns list of assignments"""
    all_assignments = Assignment.get_assignments_by_principal()
    all_assignments_dumps = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=all_assignments_dumps)

@principal_assignments_resources.route('/teachers',methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """Returns list of teachers"""
    all_teachers = Teacher.list_all_teachers()
    all_teachers_dumps = TeacherSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=all_teachers_dumps)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """"Grade or re-grade assignment"""

    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)