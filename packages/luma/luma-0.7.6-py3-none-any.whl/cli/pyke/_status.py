from collections import Counter
import json
import uuid

USE_HTTP = None

class Status():
  @staticmethod
  def new():
    status = Status()
    return status

  def __init__(self):
    self.summary = None
    self.id = str(uuid.uuid4())[:8]
    self.properties = {}
    self.percent = 0
    self.overall_percent = 0
    self.error_message = None

  def to_json(self):
    return {
      'percent': self.percent,
      'properties': self.properties,
      'errorMessage': self.error_message
    }

  def add_progress(self, percent):
    self.percent += percent
    if self.percent > 100:
      self.percent = 100

  def set_progress(self, new_percent):
    self.percent = new_percent

  def set_property(self, name, value):
    self.properties[name] = value

  def set_error(self, error, message=None, is_complete=True):
    error_text = None
    if error is not None:
      error_text = str(error)

    if message is not None:
      self.error_message = message
      if error_text:
        self.error_message += ': {}'.format(error_text)
    elif error_text is not None:
      self.error_message = error_text

    if is_complete:
      self.set_progress(100)