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
    
    def set_reminder(self,  reminder_date: datetime, notification_id: int):   
        try:
            # Raw SQL query to update the ReminderDate
            self.session.execute(
                "UPDATE NotificationLog SET ReminderDate = :reminder_date, IsReminderSent = 0, Processed = 1 WHERE NotificationId = :notification_id",
                {"reminder_date": reminder_date, "notification_id": notification_id}
            )
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Failed to update reminder date for notification with ID {notification_id}: {str(e)}")
        
    def get_unprocessed_emails(self):
        unprocessed_emails = self.session.query(NotificationLog).filter(NotificationLog.IsReminderSent == 0).all()
        return unprocessed_emails
