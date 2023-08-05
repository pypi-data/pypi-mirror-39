import os
import pickle
import re
import subprocess
from collections import deque
from functools import wraps
from itertools import product
from tempfile import NamedTemporaryFile

from docopt import docopt, DocoptExit
from schema import Regex, Schema, SchemaError
from path import Path


__all__ = ()
__version__ = "0.11"


def subcommand_router(*subcommands):
    def decorator(func):

        @wraps(func)
        def wrapper(self, argv):
            # Check if argv contain subcommand
            try:
                if argv[0] in subcommands:
                    subcommand = getattr(self, f"{func.__name__}_{argv[0]}")
                    return subcommand(argv[1:])
            except IndexError:
                pass
            
            # Else parse argv and call function
            try:
                if func.__name__ == 'rerun':
                    arguments = docopt(self.__doc__, argv)
                else:
                    arguments = docopt(func.__doc__, argv)
                return func(self, arguments)
            except DocoptExit as e:
                print(e)
        return wrapper
    
    return decorator 


class Rerun:
    """Rerun previous commands.
    
    Usage:
        rerun [--edit <editor>] [--startswith <sw>] [--contain <ct>]...
              [--replace <old=new>]... [--confirm]
        rerun LEN [OFFSET] [options] [-C <ct>]... [-R <old=new>]... [-c | --confirm-each]
        rerun (-h | --help)
    
    Commands:
        list                     View current history.
        ls                       Alias for ``list``.
        rerun                    Re-execute commands that have already been executed.

    Arguments:
        FROM:TO                  Rerun commands under specified index.
        LEN                      Number of commands to re-execute.
        OFFSET                   Re-execute commands before n last commands.
        INDEX                    Index of commands in ``rerun rerun list``.
    
    Options:
        -h, --help               Do we really need to explain?
        -c, --confirm            View commands and confirm their execution.
        --confirm-each           Confirm the execution of each command.
        -e, --edit <editor>      Edit commands. 
        -C, --contain <ct>       Rerun from last command containing <ct>.
        -S, --startswith <sw>    Rerun from last command starting with <sw>.
        -R, --replace <old=new>  Replace all substring in selected commands.
        --eq                     Rerun only if len of selected commands == LEN.

    Description:
        Let's assume that our history looks like this:
            >>> git init myproject && cd myproject
            >>> touch Dockerfile \\
            ...   && echo 'FROM nginx' >> Dockerfile \\
            ...   && echo 'WORKDIR /usr/share/nginx/html/' >> Dockerfile \\
            ...   && echo 'RUN echo "<h1>Foo</h1>" > index.html' >> Dockerfile
            >>> docker build . -t last_build
            >>> docker run --rm -it -p 8080:80 last_build

        We created a Dockerfile, we built a docker image with it. Then we runned a 
        container that uses this image.
        
        |  Note:
        |      All these commands work, you can launch them on your shell and then see 
        |      the result from your browser at http://localhost:8080.
        
        If we decide to stop the container with Ctrl+C and recreate the same container, 
        many shells offer to find and re-execute the last command by press 'Up Arrow' 
        then 'Enter'. Otherwise, you can do the same thing by simply typing:
            >>> rerun

        We stop our container with Ctrl+C, we run the commands below to check that 
        our container is no longer running:
            >>> docker ps
        Let's add the Dockerfile to our project and then make our first commit:
            >>> git add Dockerfile
            >>> git commit -am "create Dockerfile"

        Now let's suppose that we need to modify the Dockerfile:
            >>> echo 'RUN echo "<h1>Bar</h1>" >> index.html' >> Dockerfile
        
        If we run ``rerun list`` or ``rerun ls``, We can see our history look like this:
            10: rerun ls
            09: git init myproject && cd myproject
            08: touch Dockerfile \\
                  && echo 'FROM nginx' >> Dockerfile \\
                  && echo 'WORKDIR /usr/share/nginx/html/' >> Dockerfile \\
                  && echo 'RUN echo "<h1>Foo</h1>" > index.html' >> Dockerfile
            07: docker build . -t last_build
            06: docker run --rm -it -p 8080:80 last_build
            05: rerun
            04: docker ps
            03: git add Dockerfile
            02: git commit -am "create Dockerfile"
            01: echo 'RUN echo "<h1>Bar</h1>" >> index.html' >> Dockerfile
        
        To see the result in our browser, we need to re-execute commands below:
            >>> docker build . -t last_build
            >>> docker run --rm -it -p 8080:80 last_build 
        
        To do this, we just have to run:
            >>> rerun 2 5
        It means:
            "Restarts the two commands before the last five commands that have been 
             executed."
        If we want to see selected commands before and confirm their execution, we only 
        need to add '--confirm' option:
            >>> rerun 2 5 --confirm
        If we want to see and confirm execution of each command, we can do this:
            >>> rerun 2 5 --confirm-each

        Let's update our Dockerfile in our git branch, make another commit, then view 
        and confirm results commands:
            >>> rerun 2 -S 'git add' --replace create=update -c
        It means:
            "Restart the two commands from the first latest command starting with 
            'git add', replace all 'create' substrings by 'update' then show me the 
            result and let me confirm execution"
        The commands to be executed should now look like this:
            >>> git add Dockerfile
            >>> git commit -am "update Dockerfile"
        
        If instead we wanted to change the name of the Dockerfile by Mydockerfile, make 
        a commit, then view and confirm commands, do:
            >>> rerun 2 -c -S 'git add' \\
            ...            -R create=rename \\
            ...            -R 'add Dockerfile'='mv Dockerfile Mydockerfile'
        
        |  Note:
        |      You can use single/double quotes and even none with ``--replace`` 
        |      arguments. Just remember to escape quotes from your sub-chains.
        |      See examples below:
        |     
        |      >>> rerun --replace old="new"
        |      >>> rerun --replace "For what it's worth"='Buffalo Springfield'
        |      >>> rerun --replace TVSeries='That\\'s 70 Show'

        As you can see, you can replace as many substrings as you want. 
        But, you can quickly find it tiring to make all these changes with the command 
        line. You can use an editor with --edit instead of --replace:
        
        To use it, simply add the option --edit (or -e):
            >>> rerun 2 -c -S 'git add' --edit

        Modify your text and quit the editor. 
        
        |  Warning:
        |      All comments are deleted when you exit the text editor.
        
        If you have not specified one, rerun use $RERUN_EDITOR as default editor. And 
        $RERUN_EDITOR points directly to $EDITOR if you have not assigned a value to it.
        For example, if you want to use nano as default editor for rerun, add 
        ``$RERUN_EDITOR = nano`` to your .xonshrc.

        Now let's imagine that we need to re-execute commands that have already been 
        re-executed. Let's start by listing the commands:
            >>> rerun rerun list
            4: docker run --rm -it -p 8080:80 last_build
            3: docker build . -t last_build
               docker run --rm -it -p 8080:80 last_build
            2: git add Dockerfile
               git commit -am "update Dockerfile"
            1: git mv Dockerfile Mydockerfile
               git commit -am "rename Dockerfile"
        
        If you need to re-execute the last re-executed commands, just run:
            >>> rerun rerun
        Else, just specified index of commands:
            >>> rerun rerun 3
        Like the rerun command, you can use modifiers and confirm arguments like 
        ``--replace``, ``--edit``, ``--confirm`` or ``--confirm-each``:
            >>> rerun rerun 3 -e nano -c
    """
    # TODO  -C, --contain <substring>     Rerun from command containing <substring>.
    # TODO  --eq                          Rerun only if sum commands is equal to LEN.

    def __init__(self):
        self.rerunned = Rerunned()
        self.view = RerunView()
        self.cmds_to_rerun = ()

    def __call__(self, arguments, stdin=None):
        self._set_default_editor(arguments)
        self.reversed_history = self._get_history()
        # ReRun
        self.rerun(arguments)
    
    def _set_default_editor(self, argv):
        # Set Default Environment Variables Editor
        if not "RERUN_EDITOR" in os.environ:
            if not "EDITOR" in os.environ:
                os.environ["EDITOR"] = 'vi'
            os.environ["RERUN_EDITOR"] = os.environ["EDITOR"]

        if "-e" or "--edit" in argv:
            try:
                option_index = argv.index("--edit")
            except ValueError:
                option_index = argv.index("-e")
            argv.insert(option_index+1, os.environ["RERUN_EDITOR"])
    
    def _get_history(self):
        """Retrieve xonsh history.

        History order: Reverse chronology.
        """
        # Get history and reverse it
        reversed_history = self._strip_cmds([*__xonsh__.history.inps][::-1])

        return tuple(reversed_history)
    
    def _strip_cmds(self, cmds):
        stripped_cmds = []
        for cmd in cmds:
            stripped_cmds.append(''.join([line.strip() for line in cmd.splitlines()]))

        return tuple(stripped_cmds)
    
    def _eval_string(self, string):
        """Check if string is quoted and returned unquoted string.
        """

        quotes = ["'", '"""', '"']
        for q in quotes:
            if string.startswith(q) and string.endswith(q):
                unquoted_string = string[len(q):-len(q)]
                fixed_quoted_string = q + unquoted_string.replace(q, f'\\{q}') + q
                return eval(fixed_quoted_string)
        return string

    def cmds_filter(self, arguments, _from=0, to=-1):
        """Filter commands and return specifieds commands.
        
        Get the index of the first command starting with and/or contain specified
        <substring>. Except if --not-lt is enabled and total of commands is inferior
        to LEN.
        
        Returns:
            Boolean   -- Return True if commands has been found, else return False.
        """
        filters = ('--startswith', '--contain')
        constraints = ('--eq')
        
        if not arguments["LEN"]:
            arguments["LEN"] = 1

        if not any(bool(arguments[f]) for f in filters):
            self.cmds_to_rerun = self.reversed_history[_from:arguments["LEN"]]
            return True
        
        for index, cmd in enumerate(self.reversed_history[_from:to], 1):
            # --startswith
            if arguments["--startswith"]:
                if not cmd.startswith(arguments["--startswith"]):
                    continue
            # --contain
            if not all(substring in cmd for substring in arguments["--contain"]):
                continue
            # --eq
            if arguments["--eq"] and index >= arguments["LEN"]:
                continue
            else:
                _from = index - arguments["LEN"]
                to = index
                self.cmds_to_rerun = self.reversed_history[_from:to]
                return True

        error_msg = "No commands were found with options specified below:\n"
        if arguments["--startswith"]:
            error_msg += f"      --startswith: {arguments['--startswith']}\n"
        if arguments["--contain"]:
            error_msg += f"      --contain: {arguments['--contain']}\n"
        if arguments["--eq"]:
            error_msg += f"      --eq: {arguments['LEN']}\n"
        self.view.error(error_msg)

        return False

    def cmds_modify(self, arguments):
        """Modify commands.
        
        Replace all specifieds words and launch an editor if user requests it.
        
        Returns:
            Boolean -- Returns True if the operation went well, returns False if not.
        """

        # Replace regex
        regex = r"^(\"[^\"]+\"|'[^']+'|.+)=(\".*\"|'.*'|[^'\"]*)$"
        
        # Validate Arguments
        try:
            if isinstance(arguments['--edit'], str):
                if not subprocess.run(['xonsh', '-c', f"{arguments['--edit']} --help"],
                                      capture_output=True).stdout:
                    raise ValueError
        except ValueError:
            self.view.error(f"Editor not found: {arguments['--edit']}")
            return False
        try:
            if arguments['--replace']:
                for pattern in arguments['--replace']:
                    invalid_pattern = pattern
                    Regex(regex).validate(pattern)
        except SchemaError as e:
            self.view.error(
                f"Replace <old>=<new> does not match with {invalid_pattern}")
            return False
        modifiers = ('--edit', '--replace')
        
        if not any(m in arguments for m in modifiers):
            return None
        
        # --replace
        for cmd, substrings in product(self.cmds_to_rerun, arguments['--replace']):
            try:
                old_substring, new_substring = re.findall(regex, substrings)
                old_substring = self._eval_string(old_substring)
                new_substring = self._eval_string(new_substring)
            except Exception as e:
                print(e)
            cmd = cmd.replace(old_substring, new_substring)

        # --edit
        if arguments["--edit"]:
            # Set Default Editor
            if not isinstance(arguments["--edit"], str):
                arguments["--edit"] = os.environ["RERUN_EDITOR"]
            # Cmds to Text
            original_text = ""
            header_msg = ("# Warnings:\n"
                          "#   - All comments are deleted when you exit the text editor.\n"
                          "#   - Rerun use '# [Command Index]:' pattern to split commands after edition.\n"
                          "#     You can add/split/modify or delete commands, but don't forget to keep a\n"
                          "#     valid order so that Rerun separates them correctly.\n"
                          "#   - All 'rerun' commands are ignored to avoid infinite loop.\n")
            for counter, cmd in enumerate(self.cmds_to_rerun, 1):
                original_text += f"# {counter}:\n" + cmd 
            # Edit
            modified_text = self.view.edit(original_text, arguments["--edit"], header_msg)
            # Text to Cmds
            edited_cmds_to_rerun, cmd, counter, copy = [], "", 1, False
            for line in modified_text.splitlines():
                if line.startswith(f"# {counter}:"):
                    copy = True
                elif line.startswith(f"# {counter+1}:"):
                    edited_cmds_to_rerun.append(cmd)
                    counter += 1
                    cmd = ''
                else:
                    if copy and not line.startswith("#"):
                        cmd += line + '\n'
            if cmd:
                edited_cmds_to_rerun.append(cmd)
            self.cmds_to_rerun = tuple(edited_cmds_to_rerun)

            # Remove rerun commands
            self.cmds_to_rerun = tuple([cmd for cmd in self.cmds_to_rerun if not cmd.startswith("rerun")])
            # Strip commands
            self.cmds_to_rerun = self._strip_cmds(self.cmds_to_rerun)
        return True

    def cmds_run(self, arguments, reversed_index=False):
        """Run commands contained in self.reversed_history[_from:to]. Checks whether validation 
           by user are required.
        
        Returns:
            Boolean -- Returns True if the operation went well, returns False if not.
        """
        
        if not self.cmds_to_rerun:
            self.view.error("No commands have been runned for now.")
            return False
        
        if arguments["--confirm"] or arguments["--confirm-each"]:
            self.view.summarize(self.cmds_to_rerun, reversed_index)
            if arguments["--confirm"]:
                if not self.view.confirm():
                    self.view.cancel()
                    return False
        for counter, cmd in enumerate(self.cmds_to_rerun):
            if arguments["--confirm-each"]:
                self.view.summarize(cmd, reversed_index)
                if not self.view.confirm():
                    self.view.cancel()
                    return False
            if not cmd.startswith("rerun"):
                subprocess.run(["xonsh", "-c", cmd])
                
        self.rerunned += self.cmds_to_rerun
        return True

    @subcommand_router('rerun', 'list', 'ls')
    def rerun(self, arguments):
        """Rerun the commands specified by user.
        
        Usage:
        rerun [--edit <editor>] [--startswith <sw>] [--contain <ct>]...
              [--replace <old=new>]... [--confirm]
        rerun LEN [OFFSET] [options] [-C <ct>]... [-R <old=new>]... [-c | --confirm-each]
        rerun (-h | --help)
    
        Arguments:
            LEN                      Number of commands to re-execute.
            OFFSET                   Re-execute commands before n last commands.

        Options:
            -h, --help               Do we really need to explain?
            -c, --confirm            View commands and confirm their execution.
            --confirm-each           Confirm the execution of each command.
            -e, --edit <editor>      Edit commands.
            -C, --contain <ct>       Rerun from last command containing <ct>.
            -S, --startswith <sw>    Rerun from last command starting with <sw>.
            -R, --replace <old=new>  Replace all substring in selected commands.
            --eq                     Rerun only if len of selected commands == LEN.
        """

        # Check History
        if not self.reversed_history:
            self.view.error("History is empty.")
            return False
        # Validate Arguments
        try:
            if arguments["LEN"]:
                try:
                    arguments['LEN'] = int(arguments['LEN'])
                except ValueError:
                    self.view.error("LEN must be an integer.")
                    return False
                Schema(lambda n: n >= 1).validate(arguments["LEN"])
        except SchemaError:
            self.view.error("LEN cannot be less than 1.")
            return False
        try:
            if arguments["OFFSET"]:
                try:
                    arguments['OFFSET'] = int(arguments['OFFSET'])
                except ValueError:
                    self.view.error("OFFSET must be an integer.")
                    return False
                Schema(lambda n: n >= 1).validate(arguments["OFFSET"])
        except SchemaError:
            self.view.error("OFFSET cannot be less than 1.")
            return False
        # PreFilter
        _from = arguments["OFFSET"] - 1 if arguments["OFFSET"] else 0
        to = _from + (arguments["LEN"] if arguments["LEN"] else -1)
        # Filter
        if not self.cmds_filter(arguments, _from, to):
            return False
        # Modify
        if not self.cmds_modify(arguments):
            return False
        # Run
        if not self.cmds_run(arguments):
            return False
        
        return True
    
    def rerun_ls(self, arguments): return self.rerun_list(arguments)

    def rerun_list(self, arguments):
        """View current history.

        Usage:
            rerun ls [-h | --help]
            rerun list [-h | --help]
        """
        self.view.summarize(
            self.reversed_history[::-1], summarize_msg="Current History", reversed_index=True
        )
        return True
    
    @subcommand_router('list', 'ls')
    def rerun_rerun(self, arguments):
        """Re-execute commands that have already been executed by ReRun.

        Usage:
            rerun rerun [--edit <editor>] [-R <old=new>]... [-c | --confirm-each]
            rerun rerun INDEX [options] [-R <old=new>]... [-c | --confirm-each]
            rerun rerun (ls | list)
            rerun rerun (-h | --help)

        Commands:
            list                     List commands that have already been executed.
            ls                       Alias for ``list``.

        Arguments:
            INDEX                    Index of commands in ``rerun rerun list``.

        Options:
            -h, --help               Do we really need to explain?
            -c, --confirm            View commands and confirm their execution.
            --confirm-each           Confirm the execution of each command.
            -e, --edit <editor>      Edit commands.
            -C, --contain <ct>       Rerun from last command containing <ct>.
            -S, --startswith <sw>    Rerun from last command starting with <sw>.
            -R, --replace <old=new>  Replace all substring in selected commands.
        """
        # Validate Arguments
        try:
            if arguments["INDEX"]:
                try:
                    arguments['INDEX'] = int(arguments['INDEX'])
                except ValueError:
                    self.view.error("INDEX must be an integer.")
                    return False
                Schema(lambda n: n > 1).validate(arguments["INDEX"])
        except SchemaError:
            self.view.error("INDEX cannot be less than 1.")
        
        if not self.rerunned:
            self.view.error("No commands have been re-executed for now.")
            return False
        
        # Set commands to re-execute
        index = (arguments["INDEX"] or 1) - 1
        self.cmds_to_rerun = self.rerunned[index]
        # Modify
        if not self.cmds_modify(arguments):
            return False
        # Run
        if not self.cmds_run(arguments):
            return False
        
        return True

    def rerun_rerun_ls(self, arguments): return self.rerun_rerun_list(arguments)

    def rerun_rerun_list(self, arguments):
        """List commands that have already been executed.

        Usage:
            rerun rerun ls [-h | --help]
            rerun rerun list [-h | --help]
        """
        self.view.summarize(
            self.rerunned, summarize_msg="Rerun List", reversed_index=True
        )
        return True


def set_unique():
    def decorator(func):

        @wraps(func)
        def wrapper(self, element):
            return func(self, element)
        
        return wrapper
    
    return decorator


class Rerunned():

    FILE_PATH = os.path.expanduser("~") + "/.local/share/rerun/"
    FILE = FILE_PATH + 'rerunned.pickle'

    def __init__(self):
        if not os.path.exists(self.FILE_PATH):
            os.makedirs(self.FILE_PATH)
    
    def __repr__(self):
        return f"<Rerunned Object: {self.data}>"
    
    def __str__(self):
        return str(self.data)
    
    def __getattr__(self, name):
        if name == "data":
            self._load_data()
            return self.data

    def __getitem__(self, index):
        return self.data[index]

    def __iter__(self):
        self._load_data()

        for cmds in self.data:
            yield cmds
    
    def __len__(self):
        return len(self.data)
    
    def __add__(self, element):
        if element in self.data:
            self.data.remove(element)
            self.data.insert(0, element)
        else:
            self.data.insert(0, element)
        self._save_data()
        return self.data
    
    def __iadd__(self, element): return self.__add__(element)

    def _load_data(self):
        try:
            with open(self.FILE, 'rb') as f:
                try:
                    self.data = pickle.load(f)
                except Exception as e:
                    print(e)
                    return False
        except FileNotFoundError:
            self.data = []
        return True
    
    def _save_data(self):
        with open(self.FILE, 'wb+') as f:
            try:
                pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print(e)
                return False
        return True


class RerunView:
    def __init__(self):
        self.data = None

    @staticmethod
    def pluralize(self):
        return "s" if len(self.data) > 1 else ""

    def confirm(self, confirm_msg="Continue?", default="yes"):
        """Ask a yes/no question via input() and return True for yes and False for no.
        """
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("> Invalid default answer: '%s'  \n" % default)

        while True:
            print(confirm_msg + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                print("> Please respond with 'yes' or 'no' (or 'y' or 'n').  \n")

    def cancel(self, cancel_msg="Execution aborted."):
        print(
            "-" * (len(cancel_msg) + 6) + "\n"
         +  "> Cancel:  \n"
         + f">     {cancel_msg}"
        )
    
    def error(self, error_msg="Error"):
        print(
            "-" * (len(error_msg) + 6) + "\n"
         +  "> Error:  \n"
         + f">     {error_msg}"
        )

    def edit(self, text, editor, header_msg=''):
        """Open a text editor.
        
        Create temporary file, inject text inner, and open file with specified editor.
        Then retrieve modified tet and return it.
        """

        small_sep = f"#{'-' * 79}\n"
        large_sep = f"#{'=' * 79}\n"
        header = large_sep + "#\n# ReRun Command Editor\n#\n" + large_sep + header_msg + small_sep
        text = header + text
        try:
            with NamedTemporaryFile(prefix="rerun-", suffix=".tmp", dir="/tmp") as tf:
                tf.write(bytes(text, 'utf8'))
                tf.flush()
                subprocess.run([editor, tf.name])

                tf.seek(0)
                modified_text = tf.read().decode('utf8')
        except Exception as e:
            print(e)
        else:
            return modified_text

    def summarize(self, data, summarize_msg, reversed_index=False):
        """List specified commands with specified type of index.
        """

        if not summarize_msg:
            summarize_msg = f"Command{self.pluralize} that will be executed"
        self.data = data
        index = range(1, len(self.data) + 1)
        if reversed_index:
            index = reversed(index)

        rule = "-" * len(summarize_msg) + "\n"
        header = rule + f"{summarize_msg}\n" + rule
        body = ""
        for i, element in zip(index, self.data):
            try:
                first_line = True
                for line in element:
                    if first_line:
                        first_line = False
                        body += f"{i}: {line}\n"
                    else:
                        body += f"{(len(str(len(element))) + 2) * ' '}{line}\n"
            except TypeError:
                body += f"{i}: {element}\n"
            #   "```           \n"  Issue to rendering code block with mdv.
            #  f"{cmd}         \n"  Get '<' character instead of code. More Infos:
            #   "```           \n") https://github.com/axiros/terminal_markdown_viewer/issues/66
        print(header + body)


aliases["rerun"] = Rerun()