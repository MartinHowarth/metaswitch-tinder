from . import matches, completed_matches, mentee, mentor, settings, mentor_skills
from ..pages import mentee_request

tabs = {
    'mentee': mentee.layout,
    'mentee_matches': matches.layout,
    'mentee_request': mentee_request.layout,
    'mentor': mentor.layout,
    'mentor_matches': matches.layout,
    'mentor_skills': mentor_skills.layout,
    'completed_matches': completed_matches.layout,
    'settings': settings.layout,
}
