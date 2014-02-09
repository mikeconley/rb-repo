import subprocess


class GitCommitIterator(object):
    """A class for iterating Git commits up their ancestry chain."""
    previous = None
    current = None

    def __init__(self, start):
        if not rev_is_valid(start):
            raise Exception('No commit exists with ID %s' % start)
        self.current = start

    def __iter__(self):
        return self

    def next(self):
        """Takes one step up the ancestry chain."""
        parents = get_parents(self.current)
        # We're not doing a good job of dealing with merge commits,
        # so right now we just choose the first parent. We'll definitely
        # need to do something about this in the future.
        if len(parents) == 0:
            self.current = None
            raise StopIteration
        else:
            self.current = parents[0]
        return self.current


def get_parents(rev):
    """Returns a list of the parents of the commit with ID rev."""
    git_command = ('git log -n 1 --pretty=%%P %s' % rev)
    stdout = execute(git_command)
    return [x for x in stdout.split(' ') if x]


def rev_is_valid(rev):
    git_command = ('git rev-list -n 1 %s' % rev)
    stdout = execute(git_command)
    return stdout == rev


def execute(command):
    """Executes the specified command and returns the return code
       and stdout output.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return process.communicate()[0].strip()