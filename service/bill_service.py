import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import register_adapter, AsIs
from datetime import datetime
from typing import List, Optional, Union
from model import OutgoingRecipient, OutgoingBill, OutgoingRecipientCreate, OutgoingBillCreate, OutgoingRecipientUpdate, OutgoingBillUpdate
import os
from dotenv import load_dotenv
import uuid

# Register UUID adapter for psycopg2
register_adapter(uuid.UUID, lambda u: AsIs(f"'{u}'::uuid"))


class BillService:
    def __init__(self):
        load_dotenv()
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
    
    def get_recipients_by_modified(self, modified_after: Optional[datetime] = None) -> List[OutgoingRecipient]:
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if modified_after:
                    cur.execute("SELECT * FROM outgoing_recipient WHERE modified > %s ORDER BY modified", (modified_after,))
                else:
                    cur.execute("SELECT * FROM outgoing_recipient ORDER BY modified")
                
                rows = cur.fetchall()
                return [OutgoingRecipient.model_validate(dict(row)) for row in rows]
        finally:
            conn.close()
    
    def get_bills_by_modified(self, modified_after: Optional[datetime] = None) -> List[OutgoingBill]:
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if modified_after:
                    cur.execute("SELECT * FROM outgoing_bill WHERE modified > %s ORDER BY modified", (modified_after,))
                else:
                    cur.execute("SELECT * FROM outgoing_bill ORDER BY modified")
                
                rows = cur.fetchall()
                recipients = {}
                bills = []
                for row in rows:
                    bill_dict = dict(row)
                    bills.append(OutgoingBill.model_validate(bill_dict))
                return bills
        finally:
            conn.close()
    
    def save_recipients(self, recipients: List[Union[OutgoingRecipient, OutgoingRecipientCreate]]) -> List[OutgoingRecipient]:
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                saved_recipients = []
                for recipient in recipients:
                    if hasattr(recipient, 'id') and recipient.id is not None:
                        # Try to update existing
                        cur.execute(
                            "UPDATE outgoing_recipient SET name=%s, address=%s, postal_code=%s, city=%s, oib=%s, modified=%s WHERE id=%s RETURNING *",
                            (recipient.name, recipient.address, recipient.postal_code, recipient.city, recipient.oib, recipient.modified, recipient.id)
                        )
                        row = cur.fetchone()
                        if row is None:
                            # ID doesn't exist, insert with provided ID
                            cur.execute(
                                "INSERT INTO outgoing_recipient (id, name, address, postal_code, city, oib, modified) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                                (recipient.id, recipient.name, recipient.address, recipient.postal_code, recipient.city, recipient.oib, recipient.modified)
                            )
                            row = cur.fetchone()
                    else:
                        # Insert new
                        recipient_id = uuid.uuid4()
                        cur.execute(
                            "INSERT INTO outgoing_recipient (id, name, address, postal_code, city, oib, modified) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                            (recipient_id, recipient.name, recipient.address, recipient.postal_code, recipient.city, recipient.oib, recipient.modified)
                        )
                        row = cur.fetchone()
                    saved_recipients.append(OutgoingRecipient.model_validate(dict(row)))
                conn.commit()
                return saved_recipients
        finally:
            conn.close()
    
    def save_bills(self, bills: List[Union[OutgoingBill, OutgoingBillCreate]]) -> List[OutgoingBill]:
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                saved_bills = []
                for bill in bills:
                    if hasattr(bill, 'id') and bill.id is not None:
                        # Try to update existing
                        cur.execute(
                            "UPDATE outgoing_bill SET project_name=%s, project_description=%s, base_price=%s, pdv_price=%s, price=%s, price_text=%s, date_time=%s, recipient_id=%s, bill_number=%s, modified=%s WHERE id=%s RETURNING *",
                            (bill.project_name, bill.project_description, bill.base_price, bill.pdv_price, bill.price, bill.price_text, bill.date_time, bill.recipient_id, bill.bill_number, bill.modified, bill.id)
                        )
                        row = cur.fetchone()
                        if row is None:
                            # ID doesn't exist, insert with provided ID
                            cur.execute(
                                "INSERT INTO outgoing_bill (id, project_name, project_description, base_price, pdv_price, price, price_text, date_time, recipient_id, bill_number, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
                                (bill.id, bill.project_name, bill.project_description, bill.base_price, bill.pdv_price, bill.price, bill.price_text, bill.date_time, bill.recipient_id, bill.bill_number, bill.modified)
                            )
                            row = cur.fetchone()
                    else:
                        # Insert new
                        bill_id = uuid.uuid4()
                        cur.execute(
                            "INSERT INTO outgoing_bill (id, project_name, project_description, base_price, pdv_price, price, price_text, date_time, recipient_id, bill_number, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
                            (bill_id, bill.project_name, bill.project_description, bill.base_price, bill.pdv_price, bill.price, bill.price_text, bill.date_time, bill.recipient_id, bill.bill_number, bill.modified)
                        )
                        row = cur.fetchone()
                    row_dict = dict(row)
                    saved_bills.append(OutgoingBill.model_validate(row_dict))
                conn.commit()
                return saved_bills
        finally:
            conn.close()