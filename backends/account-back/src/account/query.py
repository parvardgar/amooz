from dataclasses import dataclass
from typing import List, Optional

from shared.cqrs.base import Query, BaseQueryHandler
from account import repository as acc_repo

@dataclass
class GetUserByIdQuery(Query):
    user_id: int

@dataclass
class GetUserByMobileQuery(Query):
    mobile: str

@dataclass
class SearchUsersQuery(Query):
    search_term: str

class UserQueryHandler(BaseQueryHandler):
    def __init__(self):
        self.repository = acc_repo.UserRepository()
    
    def handle(self, query: Query):
        if isinstance(query, GetUserByIdQuery):
            return self.repository.get_by_id(query.user_id)
        elif isinstance(query, GetUserByMobileQuery):
            return self.repository.get_by_mobile(query.mobile)
        elif isinstance(query, SearchUsersQuery):
            return self.repository.search_users(query.search_term)
        raise ValueError("Invalid query type")
    

@dataclass
class GetStudentProfileByUserMobileQuery(Query):
    user_mobile: str

@dataclass
class GetStudentProfileByIDQuery(Query):
    id: int


class StudentProfileQueryHandler(BaseQueryHandler):
    def __init__(self):
        self.repository = acc_repo.StudentProfileRepository()

    def handle(self, query: Query):
        if isinstance(query, GetStudentProfileByUserMobileQuery):
            return self.repository.get_by_user_mobile(query.user_mobile)
        elif isinstance(query, GetStudentProfileByIDQuery):
            return self.repository.get_by_id(query.id)
        elif isinstance(query, SearchUsersQuery):
            return self.repository.search_users(query.search_term)
        raise ValueError("Invalid query type")