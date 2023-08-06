"""
Tab indentation style checker for flake8
"""

__version__ = "1.0.0"

import collections
import re
import tokenize

import flake8.checker
import flake8.processor
from flake8.processor import NEWLINE, count_parentheses


# List of keywords in Python as of Python 3.7.2rc1
# See: https://docs.python.org/3/reference/lexical_analysis.html#keywords (update as needed)
KEYWORDS = frozenset({
	'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 'raise',
	'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 'lambda', 'try',
	'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 'global', 'not', 'with',
	'async', 'elif', 'if', 'or', 'yield'
})

# List of keywords that start a new definition (function or class)
KEYWORDS_DEFINITION = frozenset({'async', 'def', 'class'})

NEWLINE_CLOSE = NEWLINE | {tokenize.OP}


class Indent(collections.namedtuple("Indent", ("tabs", "spaces"))):
	"""
	Convience class representing the combined indentation of tabs and spaces with vector-style math
	"""
	def __pos__(self):
		return self
	
	def __neg__(self):
		return Indent(-self.tabs, -self.spaces)
	
	def __add__(self, other):
		return Indent(self.tabs + other[0], self.spaces + other[1])
	
	def __sub__(self, other):
		return Indent(self.tabs - other[0], self.spaces - other[1])
	
	def __mul__(self, other):
		return Indent(self.tabs * other[0], self.spaces * other[1])
	
	def __div__(self, other):
		return Indent(self.tabs / other[0], self.spaces / other[1])

Indent.null = Indent(0, 0)


class FileChecker(flake8.checker.FileChecker):
	"""
	Blacklist some `pycodestyle` checks that our plugin will implement instead
	"""
	
	BLACKLIST = frozenset({
		# E101 indentation contains mixed spaces and tabs
		#  – Incorrectly reports cases of using tabs for indentation but spaces for alignment
		#    (We have our own checks for cases where the two are mixed, which is still an error.)
		"pycodestyle.tabs_or_spaces",
		
		# E121 continuation line under-indented for hanging indent
		# E122 continuation line missing indentation or outdented
		# E123 closing bracket does not match indentation of opening bracket’s line
		# E126 continuation line over-indented for hanging indent
		# E127 continuation line over-indented for visual indent
		# E128 continuation line under-indented for visual indent
		#  – We handle these ourselves: That's what this checker is about after all
		# E124 closing bracket does not match visual indentation
		# E125 continuation line with same indent as next logical line
		# E129 visually indented line with same indent as next logical line
		# E131 continuation line unaligned for hanging indent
		# E133 closing bracket is missing indentation
		#  – These aren't handled yet but cannot be disabled separately
		"pycodestyle.continued_indentation",
		
		# W191 indentation contains tabs
		#  – Not applicable since we love tabs 🙂️
		"pycodestyle.tabs_obsolete",
		
		# W291 trailing whitespace
		# W293 blank line contains whitespace
		#  – Implemented by `BlankLinesChecker` with more options and saner defaults
		"pycodestyle.trailing_whitespace",
	})
	
	def __init__(self, filename, checks, options):
		for checks_type in checks:
			checks[checks_type] = list(filter(
				lambda c: c["name"] not in self.BLACKLIST,
				checks[checks_type]
			))
		super().__init__(filename, checks, options)

def expand_indent(line):
	r"""Return the amount of indentation (patched function for `flake8`)
	
	Tabs are expanded to the next multiple of the current tab size.
	
	>>> expand_indent('    ')
	4
	>>> expand_indent('\t')
	8
	>>> expand_indent('       \t')
	8
	>>> expand_indent('        \t')
	16
	"""
	if "\t" not in line:
		return len(line) - len(line.lstrip())
	result = 0
	for char in line:
		if char == "\t":
			result  = result // IndentationChecker.TAB_WIDTH * IndentationChecker.TAB_WIDTH
			result += IndentationChecker.TAB_WIDTH
		elif char == " ":
			result += 1
		else:
			break
	return result


def patch_flake8():
	flake8.checker.FileChecker = FileChecker
	flake8.processor.expand_indent = expand_indent


class BlankLinesChecker:
	"""
	Checks indentation in blank lines to match the next line if there happens to be any
	"""
	name    = "flake8-tabs"
	version = __version__
	
	
	REGEXP = re.compile(r"([ \t\v]*).*?([ \t\v]*)([\r\x0C]*\n?)$")
	
	DEFAULT_MODE = "maybe"
	MODE = DEFAULT_MODE
	
	
	@classmethod
	def add_options(cls, option_manager):
		pass
		# Indentation style options
		MODE_CHOICES = ("maybe", "always", "never")
		option_manager.add_option(
			"--blank-lines-indent", type="choice", choices=MODE_CHOICES, metavar="MODE",
			default=cls.DEFAULT_MODE, parse_from_config=True,
			help=("Whether there should be, properly aligned, indentation in blank lines; "
				"\"always\" forces this, \"never\" disallows this (Default: %default)")
		)
	
	@classmethod
	def parse_options(cls, option_manager, options, extra_args):
		cls.MODE = options.blank_lines_indent
	
	def __new__(cls, physical_line, lines, line_number):
		indent, trailing, crlf = cls.REGEXP.match(physical_line).groups()
		if len(physical_line) - len(crlf) < 1:  # Totally blank line
			if cls.MODE != "always":
				return  # Otherwise check whether the next non-blank line is also unindented
		elif len(indent) + len(crlf) == len(physical_line):
			if cls.MODE == "never":  # Cannot have indented blank line in this mode
				return (0, "W293 (flake8-tabs) blank line contains whitespace")
		else:
			# Not a blank line with whitespace
			if len(trailing) > 0:
				return (
					len(physical_line) - len(trailing) - len(crlf),
					"W291 (flake8-tabs) trailing whitespace"
				)
			return
		
		# Scan for next non-blank line
		expected_indent = ""
		for idx in range(line_number, len(lines)):
			line_indent, _, line_crlf = cls.REGEXP.match(lines[idx]).groups()
			if len(line_indent) + len(line_crlf) != len(lines[idx]):
				expected_indent = line_indent
				break
		
		# Compare the two indents
		if indent != expected_indent:
			return (0, "W293 (flake8-tabs) blank line contains unaligned whitespace")
	
	def __init__(self, physical_line, lines, line_number):
		pass



class IndentationChecker:
	"""
	Checks indentation within braces with a “tabs for indentation, spaces for alignment” kind of
	mindset
	"""
	name    = "flake8-tabs"
	version = __version__
	
	# Tab width: Used when requiring further indentation after we already have alignment
	DEFAULT_TAB_WIDTH = 4
	TAB_WIDTH = DEFAULT_TAB_WIDTH
	
	# Indentation style: Can be used to restrict indentation to only alignment or indents for
	#                    function calls or function/class definitions
	DEFAULT_INDENT_STYLE_CALL = "auto"  # "auto" (PEP-8) / "indent" / "align"
	DEFAULT_INDENT_STYLE_DEF  = "auto"  # "auto" (PEP-8) / "indent" / "align"
	INDENT_STYLE_CALL = DEFAULT_INDENT_STYLE_CALL
	INDENT_STYLE_DEF  = DEFAULT_INDENT_STYLE_DEF
	
	# Indentation tabs: The number of tabs, when indenting, to require for the first level of
	#                   indentation of functions calls, function/class definitions and other
	#                   expressions
	DEFAULT_INDENT_TABS_CALL = 1
	DEFAULT_INDENT_TABS_DEF  = 2  # PEP-8 requires indentation to be destingishable
	DEFAULT_INDENT_TABS_EXPR = 1
	INDENT_TABS_CALL = DEFAULT_INDENT_TABS_CALL
	INDENT_TABS_DEF  = DEFAULT_INDENT_TABS_DEF
	INDENT_TABS_EXPR = DEFAULT_INDENT_TABS_EXPR
	
	
	@classmethod
	def add_options(cls, option_manager):
		patch_flake8()
		
		# Indentation style options
		INDENT_STYLE_CHOICES = ("auto", "indent", "align")
		option_manager.add_option(
			"--indent-style-call", type="choice", choices=INDENT_STYLE_CHOICES, metavar="STYLE",
			default=cls.DEFAULT_INDENT_STYLE_CALL, parse_from_config=True,
			help=("Indentation style to force for function/method calls; setting this to "
				"\"auto\" will auto-chose based on first line (Default: %default)")
		)
		option_manager.add_option(
			"--indent-style-def", type="choice", choices=INDENT_STYLE_CHOICES, metavar="STYLE",
			default=cls.DEFAULT_INDENT_STYLE_DEF, parse_from_config=True,
			help=("Indentation style to force for class/function defintions; setting this to "
				"\"auto\" will auto-chose based on first line (Default: %default)")
		)
		
		# First-indentation tabs options
		option_manager.add_option(
			"--indent-tabs-call", type="int", metavar="TABS",
			default=cls.DEFAULT_INDENT_TABS_CALL, parse_from_config=True,
			help=("Number of tabs to indent on the first level of indentation within a function/"
				"method call (Default: %default)")
		)
		option_manager.add_option(
			"--indent-tabs-def", type="int", metavar="TABS",
			default=cls.DEFAULT_INDENT_TABS_DEF, parse_from_config=True,
			help=("Number of tabs to indent on the first level of indentation within a class/"
				"function definition (Default: %default)")
		)
		option_manager.add_option(
			"--indent-tabs-expr", type="int", metavar="TABS",
			default=cls.DEFAULT_INDENT_TABS_EXPR, parse_from_config=True,
			help=("Number of tabs to indent on the first level of indentation within an "
				"expression (Default: %default)")
		)
		
		# Prevent conflict with other plugins registering `--tab-width` as well
		for option in option_manager.options:
			if option.dest == "tab_width":
				return
		
		option_manager.add_option(
			"--tab-width", type="int", metavar="n",
			default=cls.DEFAULT_TAB_WIDTH, parse_from_config=True,
			help="Number of spaces per tab character for line length checking (Default: %default)",
		)
		iter({
			"a": int("6",
			         10)
		})
		
		return (
			("bla"
		))
	
	@classmethod
	def parse_options(cls, option_manager, options, extra_args):
		cls.INDENT_STYLE_CALL = options.indent_style_call
		cls.INDENT_STYLE_DEF  = options.indent_style_def
		
		cls.INDENT_TABS_CALL = options.indent_tabs_call
		cls.INDENT_TABS_DEF  = options.indent_tabs_def
		cls.INDENT_TABS_EXPR = options.indent_tabs_expr
		
		cls.TAB_WIDTH = options.tab_width
	
	
	@classmethod
	def _parse_line_indent(cls, line):
		"""
		Count number of tabs at start of line followed by number of spaces at start of line
		"""
		tabs   = 0
		spaces = 0
		expect_tab = True
		for char in line:
			if expect_tab and char == '\t':
				tabs += 1
			elif expect_tab and char == ' ':
				spaces += 1
				expect_tab = False
			elif not expect_tab and char == ' ':
				spaces += 1
			elif not expect_tab and char == '\t':
				raise ValueError("Mixed tabs and spaces in indentation")
			else:
				break
		return Indent(tabs, spaces)
	
	@classmethod
	def _group_tokens_by_physical_line(cls, tokens):
		idx_last = len(tokens) - 1
		current  = []
		for idx, token in enumerate(tokens):
			current.append(token)
			if idx >= idx_last or token.end[0] < tokens[idx + 1].start[0]:
				yield tuple(current)
				current.clear()
	
	def __init__(self, logical_line, indent_char, line_number, noqa, tokens):
		self.messages = []
		
		# We only care about tab indented lines
		# (However there should only be minimal change required for supporting space
		#  indents as well!)
		if indent_char != '\t' or len(tokens) < 1 or noqa:
			return
		
		# Detect which general category the given set of tokens belongs to
		tokens = list(tokens)
		
		# Assume first line to be correctly indented
		try:
			first_indent = current_indent = self._parse_line_indent(tokens[0].line)
		except ValueError:  # mixed tabs and spaces – report error and abort this logical line
			self.messages.append((
				tokens[0].start,
				"E101 (flake8-tabs) indentation contains mixed spaces and tabs"
			))
			return
		
		# Category stack: Keeps track which indentation style we should expect at this level
		category_stack = ["expression"]
		next_category = "expression"
		
		# Identation stack: Keeps track of the indentation `(tabs, spaces)` caused by each brace
		indent_stack = [current_indent]
		
		prev_parentheses_count = 0
		for token_set in self._group_tokens_by_physical_line(tokens):
			assert len(token_set) >= 1
			
			try:
				line_indent = self._parse_line_indent(token_set[0].line)
			except ValueError:  # mixed tabs and spaces – report error and abort this logical line
				self.messages.append((
					tokens[0].start,
					"E101 (flake8-tabs) indentation contains mixed spaces and tabs"
				))
				return
			
			# Count parantheses and detect the category (definition, function call or expression)
			# that we're currently in
			parentheses_count = prev_parentheses_count
			parenthese_offset = 0
			parenthese_at_end = False
			parentheses_closed_indent = Indent.null
			for token in token_set:
				if token.type in NEWLINE:
					continue
				
				parenthese_at_end = False
				
				if token.type == tokenize.OP:
					last_parentheses_count = parentheses_count
					parentheses_count = count_parentheses(parentheses_count, token.string)
					if last_parentheses_count < parentheses_count:
						# Opening parathese: Push latest expected category on stack
						category_stack.append(next_category)
						
						# Since this parenthesis has not caused any indent yet, push dummy value
						indent_stack.append(Indent.null)
						
						# Only offset of the last brace will survive, telling us how many spaces
						# to add should we chose alignment
						parenthese_offset = token.end[1] - line_indent.tabs - line_indent.spaces
						
						# This will be overwritten if the last token in the line wasn't an
						# opening parenthese
						parenthese_at_end = True
					elif last_parentheses_count > parentheses_count:
						# Closing parathese: Remove last category from stack
						category_stack.pop()
						
						# Add up all the removed indentation thanks to closing parenthesis
						# (Remember that most will be `(0, 0)`.)
						parentheses_closed_indent += indent_stack.pop()
				elif token.type == tokenize.NAME:
					if token.string in KEYWORDS_DEFINITION:
						# Definition keyword for class or function
						# (If it's not a definition it'd have be a syntax error.)
						next_category = "definition"
						continue
					elif token.string not in KEYWORDS and next_category != "definition":
						# Non-keyword name not preceeded by definition: Probably a function call
						next_category = "call"
						continue
					elif token.string not in KEYWORDS:
						continue
				
				# Catch-all for cases other than the two above
				next_category = "expression"
			assert parentheses_count == len(category_stack) - 1
			category = category_stack[-1]
			
			# Choose expected indentation style for the following lines based on the innermost
			# active category
			indent_style = "indent"
			indent_tabs  = self.INDENT_TABS_EXPR
			if category == "call":
				indent_style = self.INDENT_STYLE_CALL
				indent_tabs  = self.INDENT_TABS_CALL
			elif category == "definition":
				indent_style = self.INDENT_STYLE_DEF
				indent_tabs  = self.INDENT_TABS_DEF
			if indent_style not in ("indent", "align"):
				# Auto-choose style based on what next line uses (PEP-8)
				indent_style = "align" if not parenthese_at_end else "indent"
			
			# Calculate new expected indentation (both for this and the following lines)
			current_indent_delta = Indent.null
			if parentheses_count > prev_parentheses_count:
				if indent_style == "indent":
					# Expect one extra level of indentation for each line that left some braces
					# open in the following lines, except for the first level which has a
					# configurable increase per type
					tabs = indent_tabs if prev_parentheses_count == 0 else 1
					
					# Do not increase number of tabs after having added spaces for any reason
					if current_indent.spaces - parentheses_closed_indent.spaces > 0:
						current_indent_delta += (0, tabs * self.TAB_WIDTH)
					else:
						current_indent_delta += (tabs, 0)
				else:  # indent_style == "align"
					current_indent_delta += (0, parenthese_offset)
			
			# Update indent stack entry to attach the diff from above to the last opened brace
			indent_stack[-1] = indent_stack[-1] + current_indent_delta
			
			# Apply indentation changes caused by closed braces
			current_indent_delta -= parentheses_closed_indent
			
			
			# Expect the closing braces to be on the new level already if there is
			# no other content on this line
			if parentheses_count < prev_parentheses_count \
			and all(map(lambda t: t.type in NEWLINE_CLOSE, token_set)):
				current_indent      += current_indent_delta
				current_indent_delta = Indent.null
			
			# Compare settings on current line
			if line_indent != current_indent:
				# Find error code similar to `pycodestyle`
				code = 112
				if line_indent == first_indent:
					code = 122
				elif current_indent.spaces == line_indent.spaces == 0:
					if line_indent.tabs < current_indent.tabs:
						code = 121
					else:
						code = 126
				else:
					if line_indent.spaces > current_indent.spaces:
						code = 127
					else:
						code = 128
				code_text = "E{0} (flake8-tabs)".format(code)
				
				# Generate and store error message
				if current_indent.spaces == line_indent.spaces:
					self.messages.append((
						token_set[0].start,
						"{0} unexpected number of tabs within {1} "
						"(expected {2.tabs}, got {3.tabs})".format(
							code_text, category, current_indent, line_indent
						)
					))
				elif current_indent.tabs == line_indent.tabs:
					self.messages.append((
						token_set[0].start,
						"{0} unexpected number of spaces within {1} "
						"(expected {2.spaces}, got {3.spaces})".format(
							code_text, category, current_indent, line_indent
						)
					))
				else:
					self.messages.append((
						token_set[0].start,
						"{0} unexpected number of tabs and spaces within {1} "
						"(expected {2.tabs} tabs and {2.spaces} spaces, "
						"got {3.tabs} tabs and {3.spaces} spaces)".format(
							code_text, category, current_indent, line_indent,
						)
					))
			
			# Apply deltas
			current_indent += current_indent_delta
			assert sum(indent_stack, Indent.null) == current_indent
			
			# Remember stuff for next iteration
			prev_parentheses_count = parentheses_count
		
		# All parentheses that were opened must have been closed again
		assert prev_parentheses_count == 0
	
	def __iter__(self):
		return iter(self.messages)
