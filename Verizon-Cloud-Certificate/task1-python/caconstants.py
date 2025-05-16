#!/usr/bin/env python
# encoding: utf-8

RUNNING = "Running"
STOPPED = "Stopped"
CREATING = "ContainerCreating"
TERMINATING = "Terminating"
SCALING_UP = "Scaling Up"
SCALING_DOWN = "Scaling Down"

WEB_200 = """
<!DOCTYPE html>
<html>
  <body>

    <center>
      <h1>Squid VPN Server</h1>
      <p>Server is up and running and serving traffic!</p>
    </center>

  </body>
</html>
"""

WEB_404 = """
<!DOCTYPE html>
<html>

<head>
  <title>404 Page Not Found</title>
</head>

<body>
  <center>
    <h1>404 Page Not Found</h1>
  </center>
</body>

</html>
"""
