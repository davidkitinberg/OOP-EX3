# notification_service.py

class Observer:
    """Abstract base class for observers."""
    def notify(self, message):
        raise NotImplementedError("Subclasses must implement this method")

class EmailNotifier(Observer):
    """Observer for email notifications."""
    def notify(self, message):
        print(f"Sending Email: {message}")

class SMSNotifier(Observer):
    """Observer for SMS notifications."""
    def notify(self, message):
        print(f"Sending SMS: {message}")

class NotificationService:
    """Manages observers and dispatches notifications."""
    def __init__(self):
        self.observers = [] # List of the Observers in the system

    def add_observer(self, observer):
        """Register an observer."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove a registered observer."""
        self.observers.remove(observer)

    def notify_all(self, message):
        """Notify all registered observers."""
        for observer in self.observers:
            observer.notify(message)
