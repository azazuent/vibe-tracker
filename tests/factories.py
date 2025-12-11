import uuid

import factory
from factory import Faker

from app.db.models.comment import Comment
from app.db.models.ticket import Priority, Status, Ticket


class TicketFactory(factory.Factory):
    class Meta:
        model = Ticket

    id = factory.LazyFunction(uuid.uuid4)
    title = Faker("sentence", nb_words=4)
    description = Faker("text", max_nb_chars=200)
    assignee = Faker("name")
    priority = Priority.MEDIUM
    status = Status.TODO
    due_date = Faker("date_object")
    created_at = Faker("date_time")
    closed_at = None


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    id = factory.LazyFunction(uuid.uuid4)
    author = Faker("name")
    content = Faker("text", max_nb_chars=100)
    created_at = Faker("date_time")
