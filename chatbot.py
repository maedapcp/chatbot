import atexit
import chatwork
import configparser
import os
import re
import signal
import socket
import subprocess
import time
import traceback

config = configparser.ConfigParser()
config.read('chatbot.ini')

key = config['chatwork']['key']
room = config['chatwork'].getint('room')
repo = config['git']['repo']
pub_port = config['publishing'].getint('port')

cli = chatwork.auth(key)
me = cli.me().account_id

httpd = None


def publish():
  global httpd

  if httpd:
    httpd.kill()
    httpd.communicate()

  httpd = subprocess.Popen(
    ['python', '-m', 'http.server', str(pub_port)],
    cwd=repo)


@atexit.register
def exit_handler():
  global httpd

  if httpd:
    httpd.kill()
    httpd.communicate()


def term_handler(signal, frame):
  exit()


def build(rev):
  cmd = """cd {repo} && \\
git fetch origin && \\
git checkout {rev} && \\
chmod +x gradlew && \\
./gradlew clean assemble
""".format(
    repo=repo,
    rev=rev)

  proc = subprocess.Popen(
    cmd,
    shell=True,
    stderr=subprocess.PIPE,
    universal_newlines=True)

  cli.post('Now building...')

  outs, errs = proc.communicate()

  if proc.returncode == 0:
    publish()

    cli.post("""Build successful.
http://{addr}:{port}/app/build/outputs/apk
""".format(
      addr=socket.gethostbyname(socket.gethostname()),
      port=pub_port))

  elif errs:
    raise Exception(errs.strip())


def respond(msgs):
  for m in [m for m in tome if 'hello' in m.body.lower()]:
    cli.post("Hello! I'm {0}.".format(
      socket.gethostbyname(socket.gethostname())))

  tasks = [m for m in tome if 'build android' in m.body]

  if tasks:
    try:
      match = re.search(r'.*build +android *([^ ]+).*', tasks[-1].body)

      if match:
        rev = match.group(1)
      else:
        rev = 'origin/master'

      build(rev)
    except:
      cli.post("""Build has been canceled.
--
{err}
""".format(err=traceback.format_exc()))


signal.signal(signal.SIGINT, term_handler)
signal.signal(signal.SIGTERM, term_handler)

publish()

while True:
  try:
    tome = []

    for m in cli.visit(room).messages():
      if 'To:{0}'.format(me) in m.body or 'aid={0}'.format(me) in m.body:
        tome.append(m)

    if tome:
      respond(tome)
  except:
    print(traceback.format_exc())

  time.sleep(6)  # API呼び出しは5分あたり100回まで = 3秒に1回
