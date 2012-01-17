from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.contribu.auth.models import User
from vizwall.accounts.models import UserProfile
import datetime

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
    make_option('--username', action='store_true', dest='use_username',
         default=False, help='--username <some.user some.user2...>')
    make_option('--id', action='store_true', dest='use_id',
         default=False, help='--id <1 23 3...>')
    make_option('--email', action='store_true', dest='use_email',
         default=False, help='--email <someone@d.com noone@a.com...>')
    )
  args = '<1 3 23...> by user id'
  help = 'Deletes users. Default expects user ID numbers ( same as --id )'

  def handle(self, *args, **options):
    if options.get('use_username', False):
      # username option
      for uname in args:
        try:
          user = User.objects.get(username=uname)
        except User.DoesNotExist:
          raise CommandError('User "%s" does not exist' % (uname))
        user.profile.delete()
        user.delete()
        sys.stdout.write('Successfully deleted User "%s"\n' % (uname))
    elif options.get('use_email', False):
      # email option
      for uemail in args:
        try:
          user = User.objets.get(email=uemail)
        except User.DoesNotExist:
          raise CommandError('User "%s" does not exist' % (uemail))
        user.profile.delete()
        user.delete()
        sys.stdout.write('Successfully deleted User "%s"\n' % (uemail))
    else:
      # user id
      for uid in args:
        try:
          user = User.objects.get(pk=uid)
        except User.DoesNotExist:
          raise CommandError('User "%s" does not exist' % (uid))
        user.profile.delete()
        user.delete()
        sys.stdout.write('Successfully deleted User "%s"\n' % (uid))

