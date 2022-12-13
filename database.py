import json
import psycopg2
from psycopg2 import OperationalError
import datetime


def create_db(database, user, password):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
                Drop table humans, list;
                CREATE TABLE humans (
                    vkid int4 PRIMARY KEY,
                    name varchar NOT NULL,
                    surname varchar NOT NULL,
                    birthday date NOT NULL,
                    city varchar NOT NULL,
                    gender bool NOT NULL,
                    photo JSON
                );
                CREATE TABLE list (
                    owner_id int4 REFERENCES humans(vkid),
                    vkid int4 REFERENCES humans(vkid),
                    sel_ign bool NOT NULL,
                    CONSTRAINT list_pk PRIMARY KEY (owner_id, vkid)
                );
                """)
            conn.commit()
            print('БД VKinder создана успешно')
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()


def insert_client(database, user, password,
                  owner_id: int, name: str, surname: str, birthday: datetime, city: str, gender: bool, photo: json):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """INSERT
                    INTO
                    humans (VKid,
                    name,
                    surname,
                    birthday,
                    city,
                    gender, 
                    photo)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s);""", (owner_id, name, surname, birthday, city, gender, photo))
            conn.commit()
            print(f'Клиент {name} {surname} успешно добавлен')
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()


def insert_selected(database, user, password, owner_id: int, vk_id: int, sel_ign: bool,
                    name, surname, birthday, city, gender, photo):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                INSERT
                    INTO humans (
                        VKid,
                        name,
                        surname,
                        birthday,
                        city,
                        gender, 
                        photo)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s);
                INSERT 
                    INTO list (
                        owner_id,
                        VKid,
                        sel_ign)
                VALUES
                    (%s, %s, %s)        
                """, (vk_id, name, surname, birthday, city, gender, photo, owner_id, vk_id, sel_ign))
            conn.commit()
            print(f'Выбранная запись {name} {surname} успешно добавлена')
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()


def update_client(database, user, password,
                  owner_id: int, name: str, surname: str, birthday: datetime, city: str, gender: bool, photo: json):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                UPDATE humans SET
                    name=%s, 
                    surname=%s, 
                    birthday=%s, 
                    city=%s, 
                    gender=%s, 
                    photo=%s::json
                WHERE vkid=%s;
                """, (name, surname, birthday, city, gender, photo, owner_id))
            conn.commit()
            print(f'Клиент {name} {surname} успешно обновлен')
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()


def delete_from_list(database, user, password, owner_id: int, vk_id: int):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """                  
                    DELETE FROM list
                    WHERE owner_id=%s AND vkid=%s;
                    DELETE FROM humans
                    WHERE (SELECT count(vkid) FROM list WHERE vkid=%s) = 0 AND vkid=%s               
                """, (owner_id, vk_id, vk_id, vk_id))
            conn.commit()
            print(f'Выбранная запись {owner_id} {vk_id} успешно удалена')
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()


def favorites_list(database, user, password, owner_id):
    conn = psycopg2.connect(database=database, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """                  
                    SELECT name, surname, birthday, city, photo FROM humans as h, list as l
                    WHERE owner_id=%s AND h.vkid = l.vkid             
                """, (owner_id,))
            conn.commit()
            return cur.fetchall()
        except OperationalError as e:
            print(f"Произошла ошибка '{e}'")
    conn.close()
    
