#!/usr/bin/python3
import unittest

from lib.ConnectionUtilities import create_connection_from_config
from lib.CredentialUtilities import create_user
from lib.DatabaseUtilities import \
    create_db_connection,\
    get_network_name,\
    add_instance_to_user,\
    remove_instance_from_user,\
    create_image_document,\
    add_root_password_to_user,\
    remove_root_password_from_user,\
    get_images,\
    get_user_info
from lib.StatusUtilites import get_instance_status
    

conn = create_connection_from_config()
client = create_db_connection()
db = client["t2ee"]

class test_database(unittest.TestCase):
    def test_get_network_name(self):
        self.assertEqual(get_network_name(), "provider1")
    
    def test_add_instance_to_user(self):
        add_instance_to_user("test_user1", "test_instance", "whatever")
        user_col = db["user"]
        result = user_col.find_one({"name": "test_user1", "instance": {"$elemMatch":{"instance_name":"test_instance"}}})
        self.assertIsNotNone(result)

    def test_remove_instance_from_user(self):
        add_instance_to_user("test_user1", "test_instance", "whatever")
        user_col = db["user"]
        result = user_col.find_one({"name": "test_user1", "instance": {"$elemMatch":{"instance_name":"test_instance"}}})
        self.assertIsNotNone(result)
        remove_instance_from_user("test_user1", "test_instance")
        result = user_col.find_one({"name": "test_user1", "instance": {"$elemMatch":{"instance_name":"test_instance"}}})
        self.assertIsNone(result)

    def test_create_image_document(self):
        create_image_document("test_user1", "test_image", "docker", "whatever")
        image_col = db["image"]
        result = image_col.find_one({"image_name": "test_image", "username": "test_user1"})
        self.assertIsNotNone(result)
    
    def test_add_root_password_to_user(self):
        add_root_password_to_user("test_user1", "whatever")
        user_col = db["user"]
        result = user_col.find_one(
            {"name" : "test_user1",
             "root_password": "whatever"}
        )
        self.assertIsNotNone(result)

    def test_get_images(self):
        result = get_images()
        print(result)

    def test_get_user_info(self):
        print(get_instance_status(conn, "test_creation"))
        result = get_user_info("test_user1")
        for instance in result['instance']:
            print(instance)
            instance['status'] = get_instance_status(conn, instance["instance_name"])
        print(result)
if __name__ == '__main__':
    unittest.main()