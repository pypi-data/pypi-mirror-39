# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['slackperson']
install_requires = \
['attrs>=18.2,<19.0', 'nameparser>=1.0,<2.0']

setup_kwargs = {
    'name': 'slackperson',
    'version': '0.5.1',
    'description': 'Simple class to store slack profile information',
    'long_description': "slackperson\n===========\n.. image:: https://travis-ci.org/rickh94/slackperson.svg?branch=master\n    :target: https://travis-ci.org/rickh94/slackperson\n\n.. image:: https://codecov.io/gh/rickh94/slackperson/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/rickh94/slackperson\n\n\nA simple class \\(``SlackPerson``\\) for retrieving and storing information about a\nperson in your slack channel from the slack api.\n\nInstallation\n============\n``$ pip install slackperson``\n\nYou will also need the `slackclient\n<https://github.com/slackapi/python-slackclient>`_ package.\n\nUsage\n=====\nThe ``SlackPerson`` class can be initialized with the from_userlist method\nthat allows you to supply a username or userid and the output of the\nusers.list method to get data about a user.\n\nAfter initialization, an instance of ``SlackPerson`` will have these\nattributes:\n\n* username: the username supplied at instantiation (if username was supplied\n  with preceeding '@', it will be stripped off.)\n\n* userid: the internal id of the user (this is useful for tagging in api\n  generated messages.\n\n* email: the user's account email address in slack\n\n* fname: the user's first name\n\n* lname: the user's last name\n\n* team: the user's team id\n\n\nImport and use the ``SlackPerson`` class:\n\n.. code::\n\n  from slackperson import SlackPerson\n  from slackclient import SlackClient\n\n  sc = SlackClient(os.environ['SLACK_API_TOKEN'])\n  userlist = sc.api_call('users.list')\n  me = SlackPerson.from_userlist('myusername', userlist)\n\nIf ``myusername`` is a member of your channel (i.e. on the userlist), the\nobject ``me`` will now have all of the SlackPerson attributes. If not, it\nwill raise ``SlackDataError``. It will also raise ``SlackDataError`` if the\nuserlist is malformed in any way.\n\n\nTests\n=====\nThere is a test case for a successful creation of a SlackPerson object and\nfor the cases where exceptions should be raised. They are unittests so they\ncan be run with unittest discovery or ``pytest``.\n\n",
    'author': 'Rick Henry',
    'author_email': 'fredericmhenry@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
