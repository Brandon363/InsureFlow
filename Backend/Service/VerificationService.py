from sqlalchemy.orm import Session
from rapidfuzz import fuzz
from Repository import VerificationRepository
from Model.VerificationModel import VerifiedUserDTO, VerificationResponse


def get_all_active_verified_users(db_session: Session, id_number: str, first_name: str = None,
        last_name: str = None, email: str = None, phone_number: str = None) -> VerificationResponse:

    matched_users = {}
    message = "No users found."
    has_exact_match = False

    exact_match = VerificationRepository.find_active_user_by_id_number(db_session, id_number)
    if exact_match:
        has_exact_match = True
        matched_users[exact_match.id] = ("exact_id", exact_match)

    potential_id_matches = VerificationRepository.find_users_by_id_number_partial(db_session, id_number)
    for user in potential_id_matches:
        similarity = fuzz.ratio(id_number, user.id_number)
        if similarity >= 70:  # threshold for "close enough" match
            if user.id not in matched_users:
                match_type = "fuzzy_id" if similarity < 100 else "partial_id"
                matched_users[user.id] = (match_type, user)

    if first_name or last_name:
        name_matches = VerificationRepository.find_users_by_name_partial(db_session, first_name or "", last_name or "")
        for user in name_matches:
            name_similarity = max(fuzz.partial_ratio(first_name.lower(), user.first_name.lower()) if first_name else 0,
                fuzz.partial_ratio(last_name.lower(), user.last_name.lower()) if last_name else 0)
            if name_similarity >= 70:  # catch 'Andrew' vs 'Andrews' or 'Pato' vs 'Paton'
                if user.id not in matched_users:
                    matched_users[user.id] = ("fuzzy_name", user)

    if email:
        email_matches = VerificationRepository.find_users_by_email_partial(db_session, email)
        for user in email_matches:
            if user.id not in matched_users:
                matched_users[user.id] = ("email", user)

    if phone_number:
        phone_matches = VerificationRepository.find_users_by_phone_partial(db_session, phone_number)
        for user in phone_matches:
            if user.id not in matched_users:
                matched_users[user.id] = ("phone", user)

    matches = [VerifiedUserDTO(id=user.id, id_number=user.id_number, first_name=user.first_name, last_name=user.last_name,
        other_names=user.other_names, email=user.email, phone_number=user.phone_number, verification_status=user.verification_status)
        for _, (match_type, user) in matched_users.items()]

    total_matches = len(matches)

    if total_matches > 0:
        message = "Matching users found successfully."

    return VerificationResponse(status_code=200, success=True, message=message, query_id_number=id_number,
          total_matches=total_matches, has_exact_match=has_exact_match, matches=matches)
