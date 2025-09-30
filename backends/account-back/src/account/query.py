from dataclasses import dataclass
from typing import List, Optional

from shared.cqrs.base import Query, BaseQueryHandler
from account.repository import UserRepository

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
        self.repository = UserRepository()
    
    def handle(self, query: Query):
        if isinstance(query, GetUserByIdQuery):
            return self.repository.get_by_id(query.user_id)
        elif isinstance(query, GetUserByMobileQuery):
            return self.repository.get_by_mobile(query.mobile)
        elif isinstance(query, SearchUsersQuery):
            return self.repository.search_users(query.search_term)
        raise ValueError("Invalid query type")