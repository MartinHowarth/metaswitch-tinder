from typing import List

from metaswitch_tinder.database import User, get_user, Request, get_request_by_id
from metaswitch_tinder.app import db


class Base:

    def test_setup(self):
        db.create_all()

    def test_teardown(self):
        db.drop_all()

    def create_user_directly(self, name: str) -> User:
        user = User(name, '{}@email.com'.format(name))
        user.add()
        return user

    def delete_user(self, name: str):
        user = get_user(name)
        # TODO

    def set_user_tags(self, user: User, tags: List[str]):
        user.tags = tags

    def get_user_tags(self, user: User) -> List[str]:
        return user.tags

    def create_request_directly(self, maker: User, tags: List[str]) -> Request:
        request = Request(maker.name, tags)
        request.add()
        return request
