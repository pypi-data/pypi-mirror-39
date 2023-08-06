# -*- coding: utf-8 -*-


import collections
import inspect
import sys
import os

# Licence: GPLv3
#  (full text: http://www.gnu.org/licenses/gpl-3.0-standalone.html)
# Origin: a coobook example extended by Carsten Knoll for personal needs
# Please send bug reports via Email
# "Carsten.+".replace('+', 'Knoll@') + "tu-dresden.de"


"""
Module which quickly offers IPythons embedding functions.

In principle this module could be reduced to

from IPython import embed as IPS

but there are some additional features in this module


typical usage:

from ipHelp import ip_syshook, IPS, TracerFactory, dirsearch



IPS() # starts the ipython embedded shell
(with the ability to prevent further invocations with `_ips_exit = True`)
#!! this currently does not work. (but not very important anyway)

ST = TracerFactory()
...
ST() # starts the debugger prompt ("Start Trace"); type 'help' to get started
in contrast to the IPython Shell the debugger allows to go stepwise through
the following code.


ip_syshook(1) # starts debugger on exceptions and adds some infos
to tracebacks (like the values of calling args)

dirsearch # has nothing to do with ipython but may help to explore
the namespace. Example: import os; dirsearch('path', os)


known bugs:
- - - - - -

if used from within a PyQt app: annoying meassages

  "QCoreApplication::exec: The event loop is already running"

solution:
QtCore.pyqtRemoveInputHook() # to be called in __init__ of main-dialog-class


------------

the way colors are represented in a "normal" shell conflicts with embedded
shells in eclipse, pyscripter or spyder; result: ugly control characters

workarround: start your script from an externall shell

-----------

The embedded IPython-Shell seems to conflict with output suppressing in
the module py.test (for unittesting).

To avoid this, disable the output suppressing via:
py.test -s <testfiles>

-----------

There have been problems with pyparallel


-----------
-----------


If IPython is not installed, dummy objects are created.
This makes it possible to run code which import the ipHelp module on machines
where IPython is not available (useful for modules which are still under
development, but already are deployd on different machines/ platforms)

"""


class DummyMod(object):
    """A dummy module used for IPython's interactive module when
    a name space must be assigned to the module's __dict__."""
    pass


def format_frameinfo(fi):
    """
    Takes a frameinfo object (from the inspect module)

    returns a properly formated string
    """
    s1 = "{0}:{1}".format(fi.filename, fi.lineno)
    s2 = "function:{0},    code_context:".format(fi.function)
    if fi.code_context:
        s3 = fi.code_context[0]
    else:
        s3 = "<no code context available>"

    return "\n".join([s1, s2, s3])


def get_frame_list():
    """
    Create the list of frames
    """

    # TODO: use this function in IPS below (less code duplication)

    frame_info_list = []
    frame_list = []
    frame = inspect.currentframe()
    while not frame == None:
        frame_list.append(frame)
        info = inspect.getframeinfo(frame)
        frame_info_list.append(info)
        frame = frame.f_back

    frame_info_list.reverse()
    frame_list.reverse()
    frame_info_str_list = [format_frameinfo(fi) for fi in frame_info_list]

    return frame_list, frame_info_list, frame_info_str_list

try:

    from IPython import embed
    from IPython.terminal.ipapp import load_default_config
    from IPython.terminal.embed import InteractiveShellEmbed
    from IPython.core import ultratb

    class InteractiveShellEmbedWithoutBanner(InteractiveShellEmbed):
        display_banner = False

    def IPS(copy_namespaces=True, overwrite_globals=False):
        """Starts IPython embedded shell. This is similar to IPython.embed() but with some
        additional features:

        1. Print a list of the calling frames before entering the prompt
        2. (optionally) copy local name space to global one to prevent certain IPython bug.
        3. while doing so optinally overwrite names in the global namespace

        """

        # let the user know, where this shell is 'waking up'
        # construct frame list
        # this will be printed in the header
        frame_info_list = []
        frame_list = []
        frame = inspect.currentframe()
        while not frame == None:
            frame_list.append(frame)
            info = inspect.getframeinfo(frame)
            frame_info_list.append(info)
            frame = frame.f_back

        frame_info_list.reverse()
        frame_list.reverse()
        frame_info_str_list = [format_frameinfo(fi) for fi in frame_info_list]

        custom_header1 = "----- frame list -----\n\n"
        frame_info_str = "\n--\n".join(frame_info_str_list[:-1])
        custom_header2 = "\n----- end of frame list -----\n"

        custom_header = "{0}{1}{2}".format(custom_header1, frame_info_str, custom_header2)

        # prevent IPython shell to be launched in IP-Notebook
        test_str = str(frame_info_list[0]) + str(frame_info_list[1])
        #print test_str
        if 'IPython' in test_str and 'zmq' in test_str:
            print("\n- Not entering IPython embedded shell  -\n")
            return

        # copied (and modified) from IPython/terminal/embed.py
        config = load_default_config()

        config.InteractiveShellEmbed = config.TerminalInteractiveShell


        # these two lines prevent problems related to the initialization
        # of ultratb.FormattedTB below
        InteractiveShellEmbed.clear_instance()
        InteractiveShellEmbed._instance = None

        shell = InteractiveShellEmbed.instance()

        # achieve that custom macros are loade in interactive shell
        shell.magic('load_ext storemagic')
        if config.StoreMagics.autorestore == True:
            shell.magic('store -r')
            ar_keys = [k.split("/")[-1] for k in shell.db.keys() if k.startswith("autorestore/")]
        else:
            ar_keys = []


        # adapt the namespaces to prevent missing names inside the shell
        # see: https://github.com/ipython/ipython/issues/62
        # https://github.com/ipython/ipython/issues/10695
        if copy_namespaces and len(frame_list) >= 2:
            # callers_frame to IPS()
            # note that frame_list and frame_info_list were reversed above
            f1 = frame_list[-2]
            lns = f1.f_locals
            gns = f1.f_globals

            l_keys = set(lns)
            g_keys = set(gns)
            u_keys = shell.user_ns.keys()

            # those keys which are in local ns but not in global
            safe_keys = l_keys - g_keys
            unsafe_keys = l_keys.intersection(g_keys)

            assert safe_keys.union(unsafe_keys) == l_keys

            gns.update({k:lns[k] for k in safe_keys})

            if unsafe_keys and not overwrite_globals:
                custom_header += "following local keys have " \
                                 "not been copied:\n{}\n".format(unsafe_keys)

            if unsafe_keys and overwrite_globals:
                gns.update({k:lns[k] for k in unsafe_keys})
                custom_header += "following global keys have " \
                                 "been overwritten:\n{}\n".format(unsafe_keys)

            # now update the gns with stuff from the user_ns (if it will not overwrite anything)
            # this could be implemented cleaner
            for k in ar_keys:
                if k not in gns:
                    gns[k] = shell.user_ns[k]
                else:
                    print("omitting key from user_namespace:", k)

            dummy_module = DummyMod()
            dummy_module.__dict__ = gns

        else:
            # unexpected few frames or no copying desired:
            lns = None
            dummy_module = None


        # now execute the shell
        shell(header=custom_header, stack_depth=2, local_ns=lns, module=dummy_module)

        custom_excepthook = getattr(sys, 'custom_excepthook', None)
        if custom_excepthook is not None:
            assert callable(custom_excepthook)
            sys.excepthook = custom_excepthook


    # TODO: remove code duplication
    def ip_shell_after_exception(frame):
        """
        Launches an IPython embedded shell in the namespace where an exception occured

        :param frame:
        :return:
        """

        # let the user know, where this shell is 'waking up'
        # construct frame list
        # this will be printed in the header
        frame_info_list = []
        frame_list = []
        frame = frame or inspect.currentframe()

        local_ns = frame.f_locals
        # global_ns = frame.f_globals  # this is deprecated by IPython
        dummy_module = DummyMod()
        dummy_module.__dict__ = frame.f_globals

        while not frame == None:
            frame_list.append(frame)
            info = inspect.getframeinfo(frame)
            frame_info_list.append(info)
            frame = frame.f_back

        frame_info_list.reverse()
        frame_list.reverse()
        frame_info_str_list = [format_frameinfo(fi) for fi in frame_info_list]

        custom_header1 = "----- frame list -----\n\n"
        frame_info_str = "\n--\n".join(frame_info_str_list[:-1])
        custom_header2 = "\n----- end of frame list -----\n"
        custom_header2 = "\n----- ERROR -----\n"

        custom_header = "{0}{1}{2}".format(custom_header1, frame_info_str, custom_header2)

        # prevent IPython shell to be launched in IP-Notebook
        if len(frame_info_list) >= 2:
            test_str = str(frame_info_list[0]) + str(frame_info_list[1])
            #print test_str
            if 'IPython' in test_str and 'zmq' in test_str:
                print("\n- Not entering IPython embedded shell  -\n")
                return

        # copied (and modified) from IPython/terminal/embed.py
        config = load_default_config()
        config.InteractiveShellEmbed = config.TerminalInteractiveShell

        # these two lines prevent problems in related to the initialization
        # of ultratb.FormattedTB below
        InteractiveShellEmbedWithoutBanner.clear_instance()
        InteractiveShellEmbedWithoutBanner._instance = None

        shell = InteractiveShellEmbedWithoutBanner.instance()

        shell(header=custom_header, stack_depth=2, local_ns=local_ns, module=dummy_module)


    def ips_excepthook(excType, excValue, traceback):

        # first: print the traceback:
        tb_print_func  = ultratb.FormattedTB(mode="Context", color_scheme='Linux', call_pdb=False)
        tb_print_func(excType, excValue, traceback)

        # go down the stack
        tb = traceback
        while tb.tb_next is not None:
            tb = tb.tb_next

        critical_frame = tb.tb_frame
        # IPS()
        ip_shell_after_exception(frame=critical_frame)

    def activate_ips_on_exception():
        # set the hook
        sys.excepthook = ips_excepthook

        # save the hook (because it might be overridden from extern)
        sys.custom_excepthook = ips_excepthook


    def color_exepthook(pdb=0, mode=2):
        """
        Make tracebacks after exceptions colored, verbose, and/or call pdb
        (python cmd line debugger) at the place where the exception occurs
        """

        modus = ['Plain', 'Context', 'Verbose'][mode] # select the mode

        sys.excepthook = ultratb.FormattedTB(mode=modus,
                                        color_scheme='Linux', call_pdb=pdb)

    # for backward compatibiliy
    ip_syshook = color_exepthook

    # now, we immediately  apply this new excepthook.
    # consequence: often its sufficient jsut to import this module
    color_exepthook()


    def ip_extra_syshook(fnc, pdb=0, filename=None):
        """
        Extended system hook for exceptions.

        supports logging of tracebacks to a file

        lets fnc() be executed imediately before the IPython
        Verbose Traceback is started

        this can be used to pop up a QTMessageBox: "An exception occured"
        """

        assert isinstance(fnc, collections.Callable)
        from IPython.core import ultratb
        import time

        if not filename == None:
            assert isinstance(filename, str)
            pdb = 0

        ip_excepthook = ultratb.FormattedTB(mode='Verbose',
                                        color_scheme='Linux', call_pdb=pdb)

        fileTraceback = ultratb.FormattedTB(mode='Verbose',
                                        color_scheme='NoColor', call_pdb=0)


        # define the new excepthook
        def theexecpthook (type, value, traceback):
            fnc()
            ip_excepthook(type, value, traceback)
            # write this to a File without Colors
            if not filename == None:
                outFile = open(filename, "a")
                outFile.write("--" + time.ctime()+" --\n")
                outFile.write(fileTraceback.text(type, value, traceback))
                outFile.write("\n-- --\n")
                outFile.close()

        # assign it
        sys.excepthook = theexecpthook


#    from IPython.Debugger import Tracer
#    ST=Tracer() # "ST" = "start trace"

    from IPython.core.debugger import Tracer

    def TracerFactory():
        """
        Returns a callable `Tracer` object.
        When this object is called it starts the ipython commandline debugger
        in that place.
        """
        return Tracer(colors='Linux')

    # this has legacy reasons:
    def ST():
        a = " "*3
        print("\n"*5, a, "ST is dreprecated due to namespace problems.")
        print(a, "use: ST = TracerFactory() or")
        print(a, "from IPython.core.debugger import Tracer")
        print(a, "ST=Tracer(colors='Linux')")
        print(a, "\n"*2)
        print(a , "<ENTER>")
        print(a, "\n"*5)
        try:
            input()
        except:
            pass


except ImportError as E:
    # IPython seems not to be installed
    # create dummy functions

    print("ipython Import Error: ", E)

    def IPS():
        print("(EE): IPython is not available")
        pass
    def ip_syshook(*args, **kwargs):
        pass

    def ip_extra_syshook(*args, **kwargs):
        pass

    def ST():
        pass


#################################
# Code below is jupyter notebook specific



def get_notebook_name():
    """
    Return the full path of the jupyter notebook.
    """
    # taken from https://github.com/jupyter/notebook/issues/1000#issuecomment-359875246

    from requests.compat import urljoin
    import ipykernel
    import requests
    import json
    import re
    from notebook.notebookapp import list_running_servers

    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)


def in_ipynb():
    """
    Test whether this functions is called from within an ipython notebook on jupyter
    """

    test_str = "\n".join(get_frame_list()[2])
    # this should be made more reliable
    if "ipykernel_launcher" in test_str and \
       "ipykernel/kernelapp.py" in test_str and \
       "zmq/eventloop" in test_str:
        return True
    else:
        return False


def save_current_nb_as_html(info=False):
    """
    Save the current notebook as html file in the same directory
    """
    assert in_ipynb()

    full_path = get_notebook_name()
    path, filename = os.path.split(full_path)

    wd_save = os.getcwd()
    os.chdir(path)
    cmd = 'jupyter nbconvert --to html "{}"'.format(filename)
    os.system(cmd)
    os.chdir(wd_save)

    if info:
        print("target dir: ", path)
        print("cmd: ", cmd)
        print("working dir: ", wd_save)


#################################

# The function below is just for convenience part of this module
# formally it would belong to an own module

###############################

def dirsearch(word, obj, only_keys = True, deep = 0):
    """
        search a string in dir(<some object>)
        if object is a dict, then search in keys

        optional arg only_keys: if False, returns also a str-version of
        the attribute (or dict-value) instead only the key

        this function is not case sensitive
    """
    word = word.lower()

    if isinstance(obj, dict):
        # only consider keys which are basestrings
        items = [(key, val) for key, val in list(obj.items()) \
                                                if isinstance(key, str)]
    else:
        #d = dir(obj)

        items = []
        for key in dir(obj):
            try:
                items.append( (key, getattr(obj, key)) )
            except AttributeError:
                continue
            except NotImplementedError:
                continue

    def maxlen(s, n):
        s = s.replace("\n", " ")
        if len(s) > n:
            s = s[:n-2]+'..'
        return s


    def match(word, key, value):
        if only_keys:
            return word in key.lower()
        else:
            # search also in value (if it is of type basestring)
            if not isinstance(value, str):
                value = "" # only local change

            return (word in key.lower()) or (word in value.lower())

    res = [(k, maxlen(str(v), 20)) for k,v in items if match(word, k, v)]
    # res is a list of (key,value)-pairs

    if deep >0:

        def interesting(obj):
            module = type(sys)
            deep_types  = (module, type, dict)
            res = isinstance(type(obj), deep_types)
            #res = res and not (obj is type)
            return res

        deeper_items = [(name, obj) for name, obj in items \
                                    if interesting(obj)]

        for name, obj in deeper_items:
            deep_res = dirsearch(word, obj, only_keys=False, deep = deep-1)
            deep_res = [("%s.%s" %(name, d_name), d_obj)
                                        for d_name, d_obj in deep_res]
            res.extend(deep_res)


    if only_keys and len(res) >0:
        res = list(zip(*res))[0]
        # now res only contains the keys
    return res


