from datetime import datetime
from typing import List

from faker import Faker
from faker.providers import internet

fake = Faker(locale="pt-BR")
fake.add_provider(internet)

from database.models.user import UserModel


def fake_populated_user(n:int = 10)->List[UserModel]:
    fake_list = []
    for _ in range(10):
        fake_list.append(
            {
                "id":_+5, "username": fake.name(),
                "email": f"{fake.ascii_company_email()}", "password": "testpassword",
                "first_name": fake.name(), "last_name":fake.name(),
                "is_deleted": False, "is_active": True, "created_at": datetime.now(),
                "updated_at": datetime.now()
            } for _ in range(100)
        )
    return [
        {
            "id":4, "username": "olduserr",
            "password": "testpassword", "email": f"{fake.ascii_company_email()}",
            "first_name": "old", "last_name":"name",
            "is_deleted": False, "is_active": True, "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        *fake_list
    ]
