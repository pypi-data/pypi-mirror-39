import pytest
from xontrib_rerun import Rerun, RerunView, subcommand_router

# def random_cmds_generator():
#     import random
#     import string

#     def random_string():
#         string_length = random.randint(0, 30)
#         string_chars = string.ascii_letters + string.digits
#         string_res = ''.join(random.choice(string_chars) for _ in range(string_length))
#         return string_res

#     str1 = random_string()
#     str2 = random_string()
#     int1 = random.randint(0, 100)
#     rerun = 'rerun' if not random.randint(0, 30) else ''
#     and_rerun = f"and {rerun}" if rerun else ''
#     rerun_and = f"{rerun} and" if rerun else ''

#     cmds = [
#         f"mkdir {str1} and cd {str1}"
#          "touch {str2} {and_rerun} \ "
#          "and cd .. and rm -rf {str1}",
#         f"ls -l {rerun}",
#         f"{rerun} and echo {str1}",
#         f"curl google.fr {and_rerun}",
#         f"{rerun} and locale",
#         f"env {and_rerun}",
#         f"{rerun}",
#         f"history {int1} {and_rerun}",
#         f"touch {str1} {and_rerun} and cat {str1} and rm {str1}"
#     ]

#     return random.choice(cmds)


# def test_subcommand_router():
# return None

SELF = Rerun()


class TestRerun:
    empty_arguments = {
        "--startswith": False,
        "--contain": [],
        "--eq": False,
        "LEN": None,
        "OFFSET": None,
        "INDEX": None,
        "--edit": 'sh',
    }
    # def test__get_xonsh_history(self):
    # return None

    def test__eval_string(self):
        assert SELF._eval_string("test") == "test"
        assert SELF._eval_string("'test'") == "test"
        assert SELF._eval_string('"test"') == "test"
        assert SELF._eval_string('"""test"""') == "test"
        assert SELF._eval_string("'tes't'") == "tes't"
        assert SELF._eval_string('"tes"t"') == 'tes"t'

    def test_cmds_filter(self):
        SELF.reversed_history = SELF._get_xonsh_history()

        assert SELF.cmds_filter(self.empty_arguments) == (0, -1)
        assert SELF.cmds_filter(self.empty_arguments, _from=1, to=10) == (1, 10)
        arguments = {
            "--startswith": "test",
            "--contain": ["con", "tain"],
            "--eq": True,
            "LEN": None,
        }
        assert SELF.cmds_filter(arguments) == False
        assert SELF.cmds_filter(arguments, 1, -1) == False

    def test_cmds_modify(self):
        assert SELF.cmds_modify({"--edit": 'truc'}) == False
        assert SELF.cmds_modify({"--replace": ['wrongentry']}) == False

#     def test_cmds_run(self):
#         return None

#     def test_rerun(self):
#         return None

#     def test_rerun_ls(self):
#         return None

#     def test_rerun_list(self):
#         return None

#     def test_rerun_rerun(self):
#         return None

#     def test_rerun_rerun_ls(self):
#         return None

#     def test_rerun_rerun_list(self):
#         return None


# class TestRerunView:
#     def test_pluralize(self):
#         return None

#     def test_print(self):
#         return None

#     def test_confirm(self):
#         return None

#     def test_cancel(self):
#         return None

#     def test_error(self):
#         return None

#     def test_edit(self):
#         return None

#     def test_summarize(self):
#         return None
