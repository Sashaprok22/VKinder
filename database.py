import json
import psycopg2
from psycopg2 import OperationalError
import datetime


class VKinderDB:
    def __init__(self, database='VKinder', user='postgres', password=''):
        self.connect = psycopg2.connect(database=database, user=user, password=password)
        with self.connect.cursor() as cur:
            try:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS humans (
                        vkid int4 PRIMARY KEY,
                        name varchar NOT NULL,
                        surname varchar NOT NULL,
                        birthday date NOT NULL,
                        city varchar NOT NULL,
                        gender bool NOT NULL,
                        photo JSON
                    );
                    CREATE TABLE IF NOT EXISTS list (
                        owner_id int4 REFERENCES humans(vkid),
                        vkid int4 REFERENCES humans(vkid),
                        sel_ign bool NOT NULL,
                        CONSTRAINT list_pk PRIMARY KEY (owner_id, vkid)
                    );
                    """)
                self.connect.commit()
                print('БД VKinder создана успешно', database)
            except OperationalError as e:
                print(f"Произошла ошибка '{e}'")

    def insert_client(self,
                      owner_id: int, name: str, surname: str, birthday: datetime, city: str, gender: bool, photo: json):
        with self.connect.cursor() as cur:
            try:
                cur.execute(
                    """INSERT
                        INTO
                        humans (vkid,
                        name,
                        surname,
                        birthday,
                        city,
                        gender, 
                        photo)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT ON CONSTRAINT humans_pkey DO 
                    UPDATE SET
                        name=%s, 
                        surname=%s, 
                        birthday=%s, 
                        city=%s, 
                        gender=%s, 
                        photo=%s::json
                    WHERE humans.vkid=%s;""", (owner_id, name, surname, birthday, city, gender, photo,
                                               name, surname, birthday, city, gender, photo, owner_id))
                self.connect.commit()
                print(f'Клиент {name} {surname} успешно добавлен')
            except OperationalError as e:
                print(f"Произошла ошибка '{e}'")

    def insert_selected(self, owner_id: int, vk_id: int, sel_ign: bool,
                        name, surname, birthday, city, gender, photo):
        with self.connect.cursor() as cur:
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
                        (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT humans_pkey DO 
                    UPDATE SET
                        name=%s, 
                        surname=%s, 
                        birthday=%s, 
                        city=%s, 
                        gender=%s, 
                        photo=%s::json
                    WHERE humans.vkid=%s;
                    INSERT 
                        INTO list (
                            owner_id,
                            VKid,
                            sel_ign)
                    VALUES
                        (%s, %s, %s)
                    ON CONFLICT ON CONSTRAINT list_pk DO NOTHING     
                    """, (vk_id, name, surname, birthday, city, gender, photo,
                          name, surname, birthday, city, gender, photo, vk_id, owner_id, vk_id, sel_ign))
                self.connect.commit()
                print(f'Выбранная запись {name} {surname} успешно добавлена')
            except OperationalError as e:
                print(f"Произошла ошибка '{e}'")

    def delete_from_list(self, owner_id: int, vk_id: int):
        with self.connect.cursor() as cur:
            try:
                cur.execute(
                    """                  
                        DELETE FROM list
                        WHERE owner_id=%s AND vkid=%s;
                        DELETE FROM humans
                        WHERE (SELECT count(vkid) FROM list WHERE vkid=%s) = 0 AND vkid=%s               
                    """, (owner_id, vk_id, vk_id, vk_id))
                self.connect.commit()
                print(f'Выбранная запись {owner_id} {vk_id} успешно удалена')
            except OperationalError as e:
                print(f"Произошла ошибка '{e}'")

    def favorites_list(self, owner_id, black_or_white):
        with self.connect.cursor() as cur:
            try:
                cur.execute(
                    """                  
                        SELECT name, surname, birthday, city, photo FROM humans as h, list as l
                        WHERE owner_id=%s AND sel_ign = %s AND h.vkid=l.vkid             
                    """, (owner_id, black_or_white))
                self.connect.commit()
                return cur.fetchall()
            except OperationalError as e:
                print(f"Произошла ошибка '{e}'")

    def close_connect(self):
        self.connect.close()
