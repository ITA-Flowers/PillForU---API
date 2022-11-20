import bcrypt as bc
from flask import jsonify
from flask_mysqldb import MySQL

import api.models.user as mduser
import api.models.device as mddev
import api.models.dosage as mddos

# MySQL connection
def sql_connect(app):
    global mysql
    mysql = MySQL(app)

# -----------------------------------------------------------------------------
# DB Queries
# -- Users
#  * GET
def get_user_by_uuid(uuid : str):
    query = f'SELECT * FROM `users` WHERE uuid="{uuid}"'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchone()
    
    if not rv:
        return None
    
    _role = rv[3]
    if _role == 'caretaker':
        _role = mduser.ROLE.CARETAKER
    else:
        _role = mduser.ROLE.PUPIL
        
    user = mduser.User(uuid=rv[0], login=rv[1], password=rv[2], phone_number=rv[4], role=_role)
    return user.get_json(json_obj=False)

def get_user_by_login(login : str):
    query = f'SELECT * FROM `users` WHERE login="{login}"'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchone()
    
    if not rv:
        return None
    
    _role = rv[3]
    if _role == 'caretaker':
        _role = mduser.ROLE.CARETAKER
    else:
        _role = mduser.ROLE.PUPIL
        
    user = mduser.User(uuid=rv[0], login=rv[1], password=rv[2], phone_number=rv[4], role=_role)
    return user.get_json(json_obj=False)

def get_users():
    query = f'SELECT * FROM `users`'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None

    users = []
    for result in rv:
        _role = result[3]
        if _role == 'caretaker':
            _role = mduser.ROLE.CARETAKER
        else:
            _role = mduser.ROLE.PUPIL

        user = mduser.User(uuid=result[0], login=result[1], password=result[2], phone_number=result[4], role=_role)
        users.append(user.get_json(json_obj=False))
    
    return users

#  * POST
def add_user(user : mduser.User):
    # Query
    sql = "INSERT INTO `users` (`uuid`, `login`, `password`, `role`, `phone_number`) VALUES (UUID(), %s, %s, %s, %s)"
    val = (user.login, user.password, user.role, user.phone_number)
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(sql, val)
        mysql.connection.commit()
    
#  * PUT
def update_user(user : mduser.User):
    # Check if user exists
    existed_user = get_user_by_login(user.login)
    if existed_user is None:
        return False
    
    user.uuid = existed_user['uuid']
    
    # Query
    sql = "UPDATE `users` SET `password` = %s, `role` = %s, `phone_number` = %s WHERE `users`.`uuid` = %s"
    val = (user.password, user.role, user.phone_number, user.uuid)
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(sql, val)
        mysql.connection.commit()

    return True

#  * DELETE
def delete_user(uuid : str):
    # Query
    query = f'DELETE FROM `users` WHERE `users`.`uuid` = "{uuid}"'
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        mysql.connection.commit()

       
# -- Devices
#  * GET
def get_device_by_uid(uid : str):
    query = f'SELECT * FROM `devices` WHERE uid="{uid}"'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchone()
    
    if not rv:
        return None
        
    dev = mddev.Device(uid=rv[0])
    return dev.get_json(json_obj=False)

def get_devices():
    query = f'SELECT * FROM `devices`'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None

    devs = []
    for result in rv:
        dev = mddev.Device(uid=result[0])
        devs.append(dev.get_json(json_obj=False))
    
    return devs

#  * POST
def add_device(dev : mddev.Device):
    # Query
    sql = "INSERT INTO `devices` (`uid`) VALUES (%s)"
    val = (dev.uid)
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(sql, val)
        mysql.connection.commit()
        
#  * DELETE
def delete_device(uid : str):
    # Query
    query = f'DELETE FROM `devices` WHERE `devices`.`uid` = "{uid}"'
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        mysql.connection.commit()
    
    
# -- Dosages
#  * GET
def get_dosage_by_id(id : int):
    query = f'SELECT * FROM `dosage` WHERE id="{id}"'
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchone()
    
    if not rv:
        return None
        
    when_day = rv[6]
    
    dosage = mddos.Dosage(id=rv[0], 
                       caretaker_uuid=rv[1], 
                       pupil_uuid=rv[2], 
                       device_uid=rv[3], 
                       med_name=rv[4], 
                       pills_count=int(rv[5]), 
                       when_day=when_day, 
                       when_time=rv[7], 
                       until_date=rv[8])
    
    return dosage.get_json(json_obj=False)

def get_dosages_by_devuid(device_uid : str):
    query = f'SELECT * FROM `dosage` WHERE device_uid="{device_uid}"'
    
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None
        
    dosages = []
    for r in rv:
        when_day = r[6]
        
        dosage = mddos.Dosage(id=r[0], 
                           caretaker_uuid=r[1], 
                           pupil_uuid=r[2], 
                           device_uid=r[3], 
                           med_name=r[4], 
                           pills_count=int(r[5]), 
                           when_day=when_day, 
                           when_time=r[7], 
                           until_date=r[8])
        
        dosages.append(dosage.get_json(json_obj=False))
    
    return dosages

def get_dosages_by_caretaker_uuid(caretaker_uuid : str):
    query = f'SELECT * FROM `dosage` WHERE caretaker_uuid="{caretaker_uuid}"'
    
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None
        
    dosages = []
    for r in rv:
        when_day = r[6]
        
        dosage = mddos.Dosage(id=r[0], 
                           caretaker_uuid=r[1], 
                           pupil_uuid=r[2], 
                           device_uid=r[3], 
                           med_name=r[4], 
                           pills_count=int(r[5]), 
                           when_day=when_day, 
                           when_time=r[7], 
                           until_date=r[8])
        
        dosages.append(dosage.get_json(json_obj=False))
        
    return dosages

def get_dosages_by_pupil_uuid(pupil_uuid : str):
    query = f'SELECT * FROM `dosage` WHERE pupil_uuid="{pupil_uuid}"'
    
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None
        
    dosages = []
    for r in rv:
        when_day = r[6]
        
        dosage = mddos.Dosage(id=r[0], 
                           caretaker_uuid=r[1], 
                           pupil_uuid=r[2], 
                           device_uid=r[3], 
                           med_name=r[4], 
                           pills_count=int(r[5]), 
                           when_day=when_day, 
                           when_time=r[7], 
                           until_date=r[8])
        
        dosages.append(dosage.get_json(json_obj=False))
    
    return dosages

def get_dosages():
    query = f'SELECT * FROM `dosage`'
    
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        rv = curr.fetchall()
    
    if not rv:
        return None
        
    dosages = []
    for r in rv:
        when_day = r[6]
        
        dosage = mddos.Dosage(id=r[0], 
                   caretaker_uuid=r[1], 
                   pupil_uuid=r[2], 
                   device_uid=r[3], 
                   med_name=r[4], 
                   pills_count=int(r[5]), 
                   when_day=when_day, 
                   when_time=r[7], 
                   until_date=r[8])
        
        dosages.append(dosage.get_json(json_obj=False))
    
    return dosages

#  * POST
def add_dosage(dosage : mddos.Dosage):
    # Query
    sql = "INSERT INTO `dosage` (`caretaker_uuid`, `pupil_uuid`, `device_uid`, `med_name`, `pills_count`, `when_day`, `when_time`, `until_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (dosage.caretaker_uuid, dosage.pupil_uuid, dosage.device_uid, dosage.med_name, str(dosage.pills_count), dosage.when_day.value, dosage.when_time, dosage.until_date)
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(sql, val)
        mysql.connection.commit()

#  * PUT
def update_dosage(dosage : mddos.Dosage):
    # Check if user exists
    existed_dosage = get_dosage_by_id(dosage.id)
    if existed_dosage is None:
        return False
    
    dosage.id = existed_dosage.json[0].get('id')
    
    # Query
    sql = "UPDATE `dosage` SET `caretaker_uuid` = %s, `pupil_uuid` = %s, `device_uid` = %s, `med_name` = %s, `pills_count` = %s, `when_day` = %s, `when_time` = %s, `until_date` = %s WHERE `dosage`.`id` = %s"
    val = (dosage.caretaker_uuid, dosage.pupil_uuid, dosage.device_uid, dosage.med_name, str(dosage.pills_count), dosage.when_day.value, dosage.when_time, dosage.until_date, str(dosage.id))
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(sql, val)
        mysql.connection.commit()

    return True

#  * DELETE
def delete_dosage(id : int):
    # Query
    query = f'DELETE FROM `dosage` WHERE `dosage`.`id` = "{id}"'
    
    # Execute query
    with mysql.connection.cursor() as curr:
        curr.execute(query)
        mysql.connection.commit()

'''
INSERT INTO `dosage` (`id`, `caretaker_uuid`, `pupil_uuid`, `device_uid`, `med_name`, `pills_count`, `when_day`, `when_time`, `until_date`) VALUES ('1', '1da38e8d-650b-11ed-8cfc-d20ab87e4f10', '99c63c69-650b-11ed-8cfc-d20ab87e4f10', '100039308789940224', 'Polopiryna', '3', 'saturday', '21:00:00', '2022-12-31');
'''