#!/usr/bin/env python
import imp
import inspect
import launchd_plist
import mac_colors
import os
import plistlib
import public
import runcmd
import sys

LOGS = os.path.join(os.environ["HOME"], "Library/Logs/LaunchAgents")


def _files(path):
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)


@public.add
def scripts(path="~/Library/LaunchAgents"):
    """return list with `*.py` files"""
    if not path:
        path = "~/Library/LaunchAgents"
    path = os.path.expanduser(path)
    result = []
    for f in _files(path):
        if "/." not in path and os.path.splitext(f)[1] == ".py":
            result.append(f)
    return result


@public.add
def agents(path="~/Library/LaunchAgents"):
    """return list with launchd.plist files for .py scripts"""
    if not path:
        path = "~/Library/LaunchAgents"
    path = os.path.expanduser(path)
    result = []
    for f in _files(path):
        if "/." not in path and os.path.splitext(f)[1] == ".plist":
            result.append(f)
    return result


@public.add
def create(path):
    """create launchd.plist from python file and return path"""
    path = os.path.abspath(os.path.expanduser(path))
    cli = False
    for line in open(path).read().splitlines():
        if "__name__" in line and "__main__" in line and line == line.lstrip():
            cli = True
    if not cli:
        print('SKIP: if __name__ == "__name__" line NOT FOUND (%s)' % path)
        return
    module = imp.load_source(path, path)
    classes = []
    for k, v in module.__dict__.items():
        if inspect.isclass(v) and issubclass(v, Agent):
            classes.append(v)
    if not len(classes):
        print("SKIP: mac_agents.Agent subclass NOT FOUND (%s)" % path)
    if len(classes) != 1:
        print("SKIP: %s mac_agents.Agent subclasses %s (%s)" % (len(classes), classes, path))
    agent = classes[0](script=path)
    agent.create()
    return agent.path


class Job:
    """launchctl Job class. attrs: `pid`, `status`, `label`"""
    string = None
    pid = None
    status = None
    label = None

    def __init__(self, string):
        self.parse(string)

    def parse(self, string):
        self.string = string
        values = list(filter(None, string.split()))
        self.pid = (int(values[0]) if values[0] != "-" else None)
        self.status = (int(values[1]) if values[1] != "-" else None)
        self.label = values[2]

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()


@public.add
def jobs():
    """return list with launchctl jobs (`pid`, `status`, `label`)"""
    result = []
    out = os.popen("launchctl list").read()
    rows = out.splitlines()[1:]
    for row in rows:
        job = Job(row)
        if os.path.splitext(job.label)[1]==".py":
            result.append(job)
    return result


def _tree(path, top):
    while path != os.path.dirname(top):
        yield path
        path = os.path.dirname(path)


@public.add
def tag(path="~/Library/LaunchAgents"):
    """set Finder tags. `red` - status, `orange` - stderr, `gray` - unloaded"""
    if not path:
        path = "~/Library/LaunchAgents"
    path = os.path.expanduser(path)
    gray, orange, red = [], [], []
    files = agents(path)
    tree = []
    JOBS = jobs()
    for f in files:
        paths = list(_tree(f, path))
        tree += paths
        data = plistlib.readPlist(f)
        Label = data.get("Label", None)
        job = (list(filter(lambda j: j.label == Label, JOBS)) or [None])[0]
        gray += paths if not job else []
        red += paths if job and job.status != 0 else []
        err = data.get("StandardErrorPath", "")
        if err and os.path.exists(err) and os.path.getsize(err) > 0:
            orange += paths

    mac_colors.add(["gray"], gray)
    mac_colors.rm(["gray"], list(set(tree) - set(gray)))
    mac_colors.add(["orange"], orange)
    mac_colors.rm(["orange"], list(set(tree) - set(orange)))
    mac_colors.add(["red"], red)
    mac_colors.rm(["red"], list(set(tree) - set(red)))


"""
predefined keys:
label (Label)
args (ProgramArguments)
stdout (StandardOutPath)
stderr (StandardErrorPath)
"""


@public.add
class Agent(launchd_plist.Plist):
    """launchd.plist generator"""
    __readme__ = ["create", "rm", "read", "write", "update", "load","unload"] + ["script", "path", "Label", "ProgramArguments", "StandardOutPath", "StandardErrorPath", "WorkingDirectory"]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v:
                setattr(self, k, v)

    def create(self):
        """create launchd.plist file and `StandardOutPath`, `StandardErrorPath` logs"""
        launchd_plist.Plist.create(self, self.path)
        return self

    def read(self):
        """return a dictionary with plist file data"""
        return plistlib.readPlist(self.path)

    def write(self, data):
        """write a dictionary to a plist file"""
        return plistlib.writePlist(data, self.path)

    def update(self, **kwargs):
        """update plist file data"""
        data = self.read()
        data.update(kwargs)
        self.write(data)
        return self

    def disable(self):
        """set `Disabled` to true"""
        self.update(Disabled=True)

    def enable(self):
        """set `Disabled` to false"""
        self.update(Disabled=False)

    def load(self):
        """`launchctl load` plist file"""
        runcmd.run(["launchctl","load",self.path])
        return self

    def unload(self):
        """`launchctl unload` plist file"""
        runcmd.run(["launchctl","unload",self.path])
        return self

    def rm(self):
        """remove plist file (if exist)"""
        path = self.path
        if os.path.exists(path):
            os.unlink(path)
        return self

    @property
    def Label(self):
        """path.to.file.py"""
        if hasattr(self, "_label"):
            return getattr(self, "_label")
        path = self.script
        if os.getcwd() in self.script:
            path = os.path.relpath(self.script, os.getcwd())
        return ".".join(filter(None, path.split("/")))

    @Label.setter
    def Label(self, label):
        self._Label = label

    @property
    def StartInterval(self):
        return getattr(self, "interval", None)

    @StartInterval.setter
    def StartInterval(self, interval):
        self.interval = interval

    @property
    def StartCalendarInterval(self):
        return getattr(self, "calendar", None)

    @StartCalendarInterval.setter
    def StartCalendarInterval(self, data):
        self.calendar = dict(data)

    @property
    def WorkingDirectory(self):
        """script file dirname"""
        if getattr(self, "_WorkingDirectory", None):
            return getattr(self, "_WorkingDirectory")
        return os.path.dirname(self.script)

    @WorkingDirectory.setter
    def WorkingDirectory(self, path):
        self._WorkingDirectory = str(path)

    @property
    def ProgramArguments(self):
        """['bash','-l','-c','python $script $plist']"""
        if hasattr(self, "_ProgramArguments"):
            return self._ProgramArguments
        """
`bash -l` load environment variables
        """
        script = self.script if " " not in self.script else '"%s"' % self.script
        plist = self.path if " " not in self.path else '"%s"' % self.path
        return ["bash", "-l", "-c", 'python %s %s' % (script, plist)]

    @ProgramArguments.setter
    def ProgramArguments(self, args):
        self.args = list(args)

    @property
    def StandardOutPath(self):
        """`~/Library/Logs/LaunchAgents/$Label/out.log`"""
        if getattr(self, "_StandardOutPath", None):
            return self._StandardOutPath
        return os.path.join(LOGS, self.label, "out.log")

    @StandardOutPath.setter
    def StandardOutPath(self, path):
        self.stdout = str(path)

    @property
    def StandardErrorPath(self):
        """`~/Library/Logs/LaunchAgents/$Label/err.log`"""
        if getattr(self, "_StandardErrorPath", None):
            return self._StandardErrorPath
        return os.path.join(LOGS, self.label, "err.log")

    @StandardErrorPath.setter
    def StandardErrorPath(self, path):
        self.stderr = str(path)

    @property
    def path(self):
        """plist path - `file.py.plist`"""
        if hasattr(self, "_path"):
            return self._path
        return "%s.plist" % self.script

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def script(self):
        """script path - class module file"""
        if getattr(self, "_script", None):
            return getattr(self, "_script")
        return sys.modules[self.__class__.__module__].__file__

    @script.setter
    def script(self, path):
        if os.path.splitext(path)[1] != ".py":
            raise ValueError("not a python script - %s" % path)
        self._script = path

    def __str__(self):
        return "<Agent %s>" % str(self.data)

    def __repr__(self):
        return "<Agent %s>" % str(self.Label)
