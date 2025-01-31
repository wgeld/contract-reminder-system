from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models.NotificationLogModel import NotificationLog
from database.db_connection import get_db_session

class NotificationLogService:
    def __init__(self, session: Session):
        self.session = session



    def get_unprocessed_notifications(self):
        unprocessed_notifications = self.session.query(NotificationLog).filter(NotificationLog.Processed == False).all()
        return unprocessed_notifications
    
    def mark_notification_as_processed(self, notification_id: int):
        notification = self.session.query(NotificationLog).get(notification_id)
        if notification:
            notification.Processed = True
            self.session.commit()
        else:
            raise ValueError(f"Notification with ID {notification_id} not found")
    
    
        

