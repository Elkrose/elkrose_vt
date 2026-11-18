# Enrollment queries only: no saved state, random draws, or grade mutation.
init python:
    def vt_grade_offer_target(actor, allow_daughter=False):
        """Return the enrolled recipient; relationship/grade fields alone are insufficient."""
        if actor is None:
            return None
        daughter = getattr(actor, "daughter", None)
        if daughter is not None:
            if not allow_daughter:
                return None
            target = daughter
        else:
            target = actor
        if getattr(target, "alumni", False) or not hasattr(target, "grades"):
            return None
        # Identity prevents a detached/stale same-ID object from receiving a write.
        if any(student is target for student in academy.girl_manager.get_students()):
            return target
        return None
