activate_this = '/home/spotlight/spotlightVenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from main import app as application
