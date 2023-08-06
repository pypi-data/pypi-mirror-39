import utils

@utils.checkshellcommand('git')
def hello():
    print('this sohuld work')

@utils.checkshellcommand('helloooaa')
def nope():
    print('this sohuld not')

hello()
nope()
