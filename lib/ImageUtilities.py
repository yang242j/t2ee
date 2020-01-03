import openstack
from lib.DatabaseUtilities import create_db_connection

'''
Function: create_image_from_instance
Date: 2020/01/03
Purpose: Create image from instance
Parameters: 
    conn: OpenStack connection
    instance_name: The name of instance
    image_name: The name of the image needs to be created
Return value: 
    None
'''
def create_image_from_instance(conn, instance_name, image_name, description):
    instance = conn.compute.find_server(instance_name)
    image = conn.compute.create_server_image(instance, image_name)
    print(image)
    client = create_db_connection()
    db = client["t2ee"]
    image_col = db["image"]
    image_data = {
        'name' : image_name,
        'id' : image.id,
        'description' : description
    }
    image_col.insert_one(image_data)

'''
Function: delete image
Date: 2020/01/03
Purpose: Create image from instance
Parameters: 
    conn: OpenStack connection
    instance_name: The name of instance
    image_name: The name of the image needs to be created
Return value: 
    None
'''
def delete_image(conn, image_name):
    image = conn.compute.find_image(image_name)
    
    #Delete database record first
    client = create_db_connection()
    db = client["t2ee"]
    image_col = db["image"]
    
    query = {'id' : image.id}
    image_col.delete_one(query)

    #Delete image from OpenStack
    conn.compute.delete_image(image)