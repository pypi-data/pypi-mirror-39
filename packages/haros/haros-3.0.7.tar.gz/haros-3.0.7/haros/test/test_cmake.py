import os

from .. import cmake_parser

PATH = os.path.dirname(os.path.realpath(__file__))

SRCDIR = PATH
BINDIR = PATH

CMAKELISTS = os.path.join(PATH, "cmake", "CMakeLists.txt")

parser = cmake_parser.RosCMakeParser(SRCDIR, BINDIR)
parser.parse(CMAKELISTS)

"""
line = ('CHECK_CXX_SOURCE_COMPILES("\n'
'    #include <string>\n'
'    #include <map>\n'
'    #include <vector.hpp>\n'
'\n'
'    class TreeElement;\n'
'    typedef std::map<std::string, TreeElement> SegmentMap;\n'
'\n'
'    class TreeElement\n'
'    {\n'
'        TreeElement(const std::string& name): number(0) {}\n'
'\n'
'    public:\n'
'        int number;\n'
'        SegmentMap::const_iterator parent;\n'
'        std::vector<SegmentMap::const_iterator> children;\n'
'\n'
'        static TreeElement Root(std::string& name)\n'
'        {\n'
'            return TreeElement(name);\n'
'        }\n'
'    };\n'
'\n'
'    int main()\n'
'    {\n'
'        return 0;\n'
'    }\n'
'    "\n'
'    HAVE_STL_CONTAINER_INCOMPLETE_TYPES)')

FuncName, Args, Comment = cmake_parser.CMakeGrammar.parse_line(line)

Args = cmake_parser.CMakeGrammar.split_args(Args)

print "\n\n".join(repr(a) for a in Args)
"""