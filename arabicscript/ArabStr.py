from .ArabChar import ArabChar
from .Joining import JoiningForm, JoiningType, JoiningGroup


class ArabStr(object):
    """Class that represents strings containing Arabic text in Unicode"""

    def __init__(self, string=""):
        """Initialize ArabicStr from a regular string or another ArabicStr object"""
        if isinstance(string, str):
            self._str = [ArabChar(s) for s in string]
        elif isinstance(string, ArabStr):
            self._str = string._str
        elif isinstance(string, ArabChar):
            self._str = [string]
        else:
            raise ValueError()

    def base_form(self):
        """Convert all characters to their dotless forms"""
        result = ArabStr()
        result._str = [c.base_form() for c in self._str ]
        return result

    def joining_form(self, index):
        """Return contextual combining form of Arabic letter: isolated, initial, medial, final
        Works correctly only for unmarked strings with no combining marks attached to letters"""
        if index < 0 or index >= len(self._str):
            raise IndexError()

        letter = self._str[index]
        joining_type = letter.joining_type()
        joining_group = letter.joining_group()

        if letter == 0x0621:  # HAMZA is always in Isolated form
            return JoiningForm.Isolated

        if joining_type not in [JoiningType.Dual_Joining, JoiningType.Right_Joining]:
            return JoiningForm.No_Joining_Form

        if joining_group is JoiningGroup.Rohingya_Yeh:  # Rohingya Yeh does not have Isolated form
            return JoiningForm.Final

        prev_letter = self._str[index - 1] if index > 0 else None
        next_letter = self._str[index + 1] if index < (len(self._str) - 1) else None

        if joining_type is JoiningType.Right_Joining:
            if not prev_letter:
                return JoiningForm.Isolated
            elif prev_letter.joining_type() is JoiningType.Dual_Joining:
                return JoiningForm.Final
            else:
                return JoiningForm.Isolated

        if joining_type is JoiningType.Dual_Joining:
            if not prev_letter or prev_letter.joining_type() is not JoiningType.Dual_Joining:  # Initial or Isolated
                if not next_letter:
                    return JoiningForm.Isolated
                elif next_letter.joining_type() in [JoiningType.Dual_Joining, JoiningType.Right_Joining]:
                    return JoiningForm.Initial
            elif prev_letter.joining_type() is JoiningType.Dual_Joining:  # Medial or Final
                if not next_letter:
                    return JoiningForm.Final
                elif next_letter.joining_type() in [JoiningType.Dual_Joining, JoiningType.Right_Joining]:
                    return JoiningForm.Medial
                elif next_letter.joining_type() is JoiningType.Non_Joining:
                    return JoiningForm.Final
        return JoiningForm.No_Joining_Form

    def __str__(self):
        """Convert to string and return"""
        result = [str(c) for c in self._str]
        return ''.join(result)

    def __repr__(self):
        result = [str(c) for c in self._str]
        return ''.join(result)

    def __len__(self):
        return len(self._str)

    def __bool__(self):
        return len(self._str) != 0

    def __contains__(self, item):
        return item in self._str

    def __eq__(self, other):
        if isinstance(other, ArabStr):
            return self._str == other._str

        if isinstance(other, str):
            return str(self) == other

    def __lt__(self, other):
        if isinstance(other, ArabStr):
            return self._str < other._str

        if isinstance(other, str):
            return str(self) < other
