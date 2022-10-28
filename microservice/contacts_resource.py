import pymysql
import os


class ContactsResource:

    def __init__(self):
        self.conn = ContactsResource._get_connection()

    @staticmethod
    def _get_connection():

        # usr = os.environ.get("DBUSER") # "okcloud"
        # pw = os.environ.get("DBPW") # "okcloudokcloud"
        # h = os.environ.get("DBHOST") # "okcloud-requests-database.cw2ylftvdgpn.us-east-1.rds.amazonaws.com"

        usr = "okcloud"
        pw = "okcloudokcloud"
        h = "okcloud-requests-database.cw2ylftvdgpn.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def close_connection(self):
        self.conn.close()

    def fetch_all_contacts():
        conn = ContactsResource._get_connection()
        cur = conn.cursor()
        sql = """
            select u.*, a.address, p.phone, e.email
            from ride_share_contact_database.users u
            left join ride_share_contact_database.addresses a
            on u.user_id = a.user_id
            left join ride_share_contact_database.phones p
            on u.user_id = p.user_id
            left join ride_share_contact_database.emails e
            on u.user_id = e.user_id;
            """
        cur.execute(sql)
        result = cur.fetchall()
        return result


    def get_by_userid(userid):

        sql = """
                select u.*, a.address, p.phone, e.email from
                (select *
                from ride_share_contact_database.users
                where user_id=%s) u
                left join ride_share_contact_database.addresses a
                on u.user_id = a.user_id
                left join ride_share_contact_database.phones p
                on u.user_id = p.user_id
                left join ride_share_contact_database.emails e
                on u.user_id = e.user_id;
                """
        conn = ContactsResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=userid)
        result = cur.fetchone()

        return result

    def create_contacts(userid, info):
        sql1 = """
                insert into ride_share_contact_database.users 
                (user_id, last_name, first_name) 
                values (%s, %s, %s);
                """

        sql2 = """
                insert into ride_share_contact_database.addresses
                (user_id, address) 
                values (%s, %s);
                """

        sql3 = """
                insert into ride_share_contact_database.phones
                (user_id, phone) 
                values (%s, %s);
                """

        sql4 = """
                insert into ride_share_contact_database.emails
                (user_id, email) 
                values (%s, %s);
                """
        conn = ContactsResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql1, [userid, info[0], info[1]]) # last name, first name
        cur.execute(sql2, [userid, info[2]]) # address
        cur.execute(sql3, [userid, info[3]]) # phone
        cur.execute(sql4, [userid, info[4]]) # email

    def update_contact(userid, info):
        sql1 = """
                update ride_share_contact_database.users 
                set last_name=%s, first_name=%s
                where user_id=%s;
                """

        sql2 = """
                update ride_share_contact_database.addresses 
                set address=%s
                where user_id=%s;
                """

        sql3 = """
                update ride_share_contact_database.phones 
                set phone=%s
                where user_id=%s;
                """

        sql4 = """
                update ride_share_contact_database.emails 
                set email=%s
                where user_id=%s;
                """
        conn = ContactsResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql1, [info[0], info[1], userid])  # last name, first name
        cur.execute(sql2, [info[2], userid])  # address
        cur.execute(sql3, [info[3], userid])  # phone
        cur.execute(sql4, [info[4], userid])  # email

    def delete_contact(userid):
        sql1 = """delete from ride_share_contact_database.users where user_id=%s"""
        sql2 = """delete from ride_share_contact_database.addresses where user_id=%s"""
        sql3 = """delete from ride_share_contact_database.phones where user_id=%s"""
        sql4 = """delete from ride_share_contact_database.emails where user_id=%s"""

        conn = ContactsResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql1, args=userid)
        cur.execute(sql2, args=userid)
        cur.execute(sql3, args=userid)
        cur.execute(sql4, args=userid)