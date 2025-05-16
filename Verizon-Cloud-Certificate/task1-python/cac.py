#!/usr/bin/env python
# encoding: utf-8

import time, random, caconstants

"""
  Helper Classes Section
"""

# Squid Proxy Vpn App Class.
class VpnWebApp:

  # Initialize variables.
  def __init__(self, scale):
    self.pods = []
    for i in range(scale):
      self.newPod()
      time.sleep(1)
    self.scale = int(scale)
    self.status = caconstants.RUNNING
    self.created = time.time()
    print(">>> Squid proxy VPN Server is UP")

  # Get the number of pods currently running.
  def getActivePods(self):
    active_cnt = 0
    for pod in self.pods:
      if pod.getStatus() == caconstants.RUNNING:
        active_cnt += 1
    return int(active_cnt)

  # Create a new pod with in the given state.
  def newPod(self, status=caconstants.RUNNING):
    unique_str = str(int(time.time()*1000.0))[-5:]
    self.pods.append(SquidPod('squid-proxy-' + unique_str, status))

  # Bring all the existing pods to Running state.
  def upAllPods(self):
    for pod in self.pods:
      pod.setStatus(caconstants.RUNNING)

  # Return the overall status of the current app.
  def getStatus(self):
    active_pods = int(self.getActivePods())
    if active_pods == int(self.scale) and active_pods != 0:
      return caconstants.RUNNING
    elif active_pods < int(self.scale):
      return caconstants.SCALING_UP
    elif active_pods > int(self.scale):
      return caconstants.SCALING_DOWN
    else:
      return caconstants.STOPPED

  # Prints to console the status of the app with all the pods.
  def stat(self):
    if self.getActivePods() == 0:
      self.status = caconstants.STOPPED

    self.status = self.getStatus()
    print(">>> Application is ***{status}*** with a total of {active}/{scale} running pods.".format(
      status=self.getStatus(),
      active=self.getActivePods(),
      scale=self.scale
    ))
    print(">>> POD_NAME\t\t\tSTATUS\t\t\tREADY\t\tAGE")
    for pod in self.pods:
      print(">>> {name}\t\t{status: <17}\t{status_val}/1\t\t{age}".format(
        name=pod.getName(),
        status=pod.getStatus(),
        status_val=pod.getStatusVal(),
        age=pod.getAge()
      ))
    self.webHTML()
    print("------------")

  # Prints out the status web HTML page.
  def webHTML(self):
    if int(self.getActivePods()) > 0:
      print(caconstants.WEB_200)
    else:
      print(caconstants.WEB_404)

  # Prints out user privilege testing results for given pod.
  def getUserPrivilege(self, name):
    found = False
    for pod in self.pods:
      if pod.getName() == name:
        found = True
        print("Connecting to pod {name}...".format(name=name))
        print("{name} $ id -u".format(name=name))
        print("1001")
        print("{name} $ whoami".format(name=name))
        print("root")

        #  Looks like {name} is running with the super admin user 'root'. This
        #  is a problem and should be reported to the developers.
        #
        #  To follow the principle of least privilege, the application should
        #  not be run using the root user, instead there should be a dedicated
        #  user (e.g. squid) that has just enought privilege to running the
        #  squid proxy application and nothing else!

    if not found:
      print("Pod {name} does not exist.".format(name=name))

    print("------------")

  # Terminate a pod given the name.
  def killPod(self, name):
    success = False
    pod_idx = None
    for idx, pod in enumerate(self.pods):
      if pod.getName() == name and pod.getStatus() == caconstants.RUNNING:
        pod.setStatus(caconstants.TERMINATING)
        self.stat()
        time.sleep(0.5)
        pod_idx = idx
        success = True

    if not success:
      print("pod '{name}' either does not exist or is not in Running status".format(
        name=name
      ))
      return
    else:
      del self.pods[pod_idx]
      self.newPod(caconstants.CREATING)

    self.stat()
    time.sleep(random.randint(3, 6))
    self.upAllPods()
    self.stat()

  # Scale app up/down to the given number of pods
  def scaleApp(self, cnt):
    if int(cnt) > 0:
      print("Scaling the application to {num} pods".format(num=cnt))
    else:
      cnt = 0
      print("Scaling the application to 0 pods")

    self.scale = cnt
    print("Current scale = {scale}, active pods = {active}".format(
      scale=self.scale,
      active=self.getActivePods()
    ))

    if self.getActivePods() < int(cnt):
      for i in range(len(self.pods), int(cnt)):
        self.newPod(caconstants.CREATING)
        time.sleep(0.5)
      self.stat()
      time.sleep(random.randint(1, 3))
      self.upAllPods()
      self.stat()

    elif self.getActivePods() > int(cnt):
      success = False
      pod_idx = None
      for idx, pod in enumerate(self.pods):
        if idx >= int(cnt):
          pod.setStatus(caconstants.TERMINATING)
      self.stat()
      time.sleep(0.5)

      to_del = len(self.pods) - int(cnt)
      self.pods = self.pods[:-to_del]
      self.stat()
      time.sleep(0.5)

    else:
      print("App already scaled to {scale}, no action performed".format(scale=cnt))

# Squid Pod Class.
class SquidPod:

  # Initialize variables.
  def __init__(self, name, status=caconstants.RUNNING):
    self.name = name
    self.status = status
    self.created = int(time.time())

  # Return the name of the pod.
  def getName(self):
    return self.name

  # Return the age of the pod.
  def getAge(self):
    return str(int(time.time()) - self.created) + 's'

  # Return the status of the pod.
  def getStatus(self):
    return self.status

  # Return the status value of the pod.
  def getStatusVal(self):
    return 1 if self.getStatus() == caconstants.RUNNING else 0

  # Set the status of the pod.
  def setStatus(self, new_status):
    self.status = new_status



"""
  Helper Function Section
"""

# Initialize application objects.
def initWebApp():
  # Create the VpnWebApp object with 4 pods
  app = VpnWebApp(4)
  app.stat()
  return app

# Prints the list of accepted commands and usage for this simulation.
def printCommandList(init=False):
  if init == True:
    print("""
    ‖ ======================================================================== ‖
    ‖ Welcome to the application simulation, in this exercise we will use this ‖
    ‖ python program to simulate testing whether our Squid app has the desired ‖
    ‖ cloud-native traits. Refer to the README.md file for more information    ‖
    ‖ ======================================================================== ‖
    """)

  commands = """
  A list of all the accepted commands for this simulation:
  help                    # Prints out the list of supported commands
  status                  # Prints the status of the application
  web                     # Simulate application's status web page HTML
  kill [POD_NAME]         # Simulate killing off pod with given [POD_NAME]
  scale [NUMBER]          # Simulate autoscaling the application to run the
                              application with [NUMBER] pods
  get-user [POD_NAME]     # Simulate checking the privilege of the user
                              account running on the target Squid Server pod
  quit                    # Terminate program
  """
  print(commands)

# Parses user input and execute them.
def parseUserInput(input, app):
  tokens = input.split()

  if len(tokens) == 0:
    print("Unrecognized command.")
    printCommandList()
    return

  elif len(tokens) == 1:
    cmd = tokens[0]
    if cmd == "status":
      print("Reading status...")
      app.stat()
    elif cmd == "web":
      print("Loading Status Web Page...")
      app.webHTML()
    elif cmd == "help":
      printCommandList()
    elif cmd == "quit":
      print("Terminating...")
      quit()
    else:
      print("Unrecognized command.")
      printCommandList()
      return

  elif len(tokens) == 2:
    cmd = tokens[0]
    arg = tokens[1]

    if arg.isdigit():
      if cmd == "scale":
        app.scaleApp(arg)

      else:
        print("Unrecognized command.")
        printCommandList()
        return

    elif isinstance(arg, str):
      if cmd == "kill":
        app.killPod(arg)
      if cmd == "get-user":
        app.getUserPrivilege(arg)

    else:
      print("Unrecognized command.")
      printCommandList()
      return

  else:
    print("Unrecognized command.")
    printCommandList()
    return

  return input
