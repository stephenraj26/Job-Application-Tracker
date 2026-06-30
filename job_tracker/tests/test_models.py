import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import models
from models import (
    init_db, create_user, get_user_by_username,
    create_application, get_applications, get_stats,
    update_application, delete_application
)

TEST_DB = "test_applications.db"

def setup_function():
    models.DB_PATH = TEST_DB
    init_db()

def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_create_and_get_user():
    models.DB_PATH = TEST_DB
    create_user("jobuser", "job@gmail.com", "hashed_password")
    user = get_user_by_username("jobuser")
    assert user is not None
    assert user["email"] == "job@gmail.com"

def test_create_and_filter_applications():
    models.DB_PATH = TEST_DB
    create_user("filteruser", "filter@gmail.com", "hashed_password")
    user = get_user_by_username("filteruser")
    create_application(user["id"], "TCS", "Associate Engineer", "applied", "2026-06-01", "", "")
    create_application(user["id"], "Infosys", "Python Developer", "interview", "2026-06-05", "", "")

    all_apps = get_applications(user["id"], "all")
    assert len(all_apps) == 2

    interview_apps = get_applications(user["id"], "interview")
    assert len(interview_apps) == 1
    assert interview_apps[0]["company_name"] == "Infosys"

def test_stats():
    models.DB_PATH = TEST_DB
    create_user("statsuser", "stats@gmail.com", "hashed_password")
    user = get_user_by_username("statsuser")
    create_application(user["id"], "Wipro", "Junior Dev", "applied", "2026-06-01", "", "")
    create_application(user["id"], "HCL", "QA Engineer", "offer", "2026-06-02", "", "")

    stats = get_stats(user["id"])
    assert stats["total"] == 2
    assert stats["applied"] == 1
    assert stats["offer"] == 1

def test_delete_application():
    models.DB_PATH = TEST_DB
    create_user("deluser", "del@gmail.com", "hashed_password")
    user = get_user_by_username("deluser")
    create_application(user["id"], "Capgemini", "Trainee", "applied", "2026-06-01", "", "")
    apps = get_applications(user["id"])
    delete_application(apps[0]["id"])
    remaining = get_applications(user["id"])
    assert len(remaining) == 0
