from flaskext.wtf import Form as BaseForm
from flask import flash

class Form(BaseForm):
  
  def validate_on_submit(self):
    value = super(Form, self).validate_on_submit()
    if not value:
      for field, errors in self.errors.items():
        for error in errors:
          flash(u"Erreur sur le champ %s - %s" % (
            getattr(self, field).label.text, error))
    return value
