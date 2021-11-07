# vim:fileencoding=utf-8:noet
""" Verilog Auto Instantiation.
    Copyright (C) 2020 Yuliang Tao - All Rights Reserved.

    You may use, distribute and modify this code under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License, or any later
    version.

    You should have received a copy of the GNU General Public License along with this file.
    If not, see <http://www.gnu.org/licenses/>.

    This package requires the following packages:
    1. Python 3.7 or later
    2. Pyverilog 1.2 or later
"""

import argparse
import glob
import os
import pprint
import re
import sys
from functools import reduce
from pyverilog.utils.verror import DefinitionError
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.dataflow import DFIntConst, DFOperator
from pyverilog.vparser.parser import parse, ParseError
from pyverilog.vparser.ast import InstanceList, ParamArg, Instance, PortArg, Output
from pyverilog.vparser.ast import IntConst, Minus, Plus, Times, Divide, Srl, Sll
from vlogai.directive import directives

def parse_args(args):
    """Parse vim command argements.
    """

    parser = argparse.ArgumentParser(prog='VAI', description="Verilog Auto Instantiation",
                                     usage=('VAI [-i|--inst inst_name] [-r|--regexp m_pat s_pat]'
                                            '[--reset] [-d|--declare]'))
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-i', '--inst', type=str, help='Specify instantiation name')
    group1.add_argument('-d', '--declare', action='store_true',
                       help='Declare instport as wires and external port')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-r', '--regexp', nargs=2, type=str,
                        help='Change instport naming using python regexp')
    group2.add_argument('--reset', action='store_true',
                        help='Reset parameter value and instport name to default')
    group2.add_argument('--keep', action='store_true',
                        help=('Keep all old auto declarations if corresponding directives not '
                              'found. All old declarations are cleared by default. This option'
                              ' is valid only with -d/--declare option'))
    return parser.parse_args(args)


def grep_vim_buf(vim_buf, pattern):
    """Grep lines matching the specified pattern from vim buffer.
    """

    re_pat = re.compile(rf'{pattern}')
    matched_lines = []
    for line in vim_buf:
        if re_pat.search(line):
            matched_lines.append(line.rstrip())
    return matched_lines


def find_declares_ln(vim_buf):
    """Find the line number of auto-declarasion directives.
    """
    
    re_pat_prespace = re.compile(r'^(\s*)')
    re_pat_aws = re.compile(rf'^\s*/\*\s*{directives["AW"]}-begin\s*\*/')
    re_pat_awe = re.compile(rf'^\s*/\*\s*{directives["AW"]}-end\s*\*/')
    re_pat_aps = re.compile(rf'^\s*/\*\s*{directives["AP"]}-begin\s*\*/')
    re_pat_ape = re.compile(rf'^\s*/\*\s*{directives["AP"]}-end\s*\*/')
    ap_begin_ln, ap_end_ln, aw_begin_ln, aw_end_ln = (0, 0, 0, 0)
    ap_indent, aw_indent = (0, 0)
    for i, line in enumerate(vim_buf):
        if ap_begin_ln == 0 and re_pat_aps.search(line):
            ap_begin_ln = i + 1
            ap_indent = len(re_pat_prespace.search(line).group(1))
            continue
        if ap_end_ln == 0 and re_pat_ape.search(line):
            ap_end_ln = i + 1
            continue
        if aw_begin_ln == 0 and re_pat_aws.search(line):
            aw_indent = len(re_pat_prespace.search(line).group(1))
            aw_begin_ln = i + 1
            continue
        if aw_end_ln == 0 and re_pat_awe.search(line):
            aw_end_ln = i + 1
            continue
    return {'ap': (ap_begin_ln, ap_end_ln, ap_indent),
            'aw': (aw_begin_ln, aw_end_ln, aw_indent)}

def list_dedup_inorder(list_):
    return sorted(set(list_), key=lambda x: list_.index(x))

def validate_file(files, parent=''):
    valid_files = []
    for f in files:
        abs_path = os.path.abspath(f)
        if os.path.exists(abs_path):
            valid_files.append(abs_path)
            continue
        abs_path_full = os.path.abspath(os.path.join(parent, f))
        if os.path.exists(abs_path_full):
            valid_files.append(abs_path_full)
            continue
        print(f"{f} doesn't exist in both parent dir:{parent} and cwd:{os.getcwd()}")
    return valid_files

def find_files_from_dirs(dir_list, glob_pats=('*'), parent=''):
    """Mimic find command in linux to find files with glob patterns from specific dirs, e.g,
    // vai-incdirs: ./submod, ./interface
    """

    all_matcheds = [glob.glob(os.path.join(d, rf'{pat}')) for d in dir_list for pat in glob_pats]
    # use set to remove duplication
    all_files = [y for x in all_matcheds for y in x]
    return validate_file(list_dedup_inorder(all_files), parent)

def find_files_from_lines(text_lines, parent=''):
    """Find files in a text line, e.g.,
    // vai-incfiles: ./macros.v, ./led.v
    """

    all_files = [f for l in text_lines for f in l.split(':')[-1].replace(' ', '').split(',')]
    return validate_file(list_dedup_inorder(all_files), parent)

def find_files_from_flist(flist_fnames, grep_pats=('.',), parent=''):
    """Find files in filelists.
    """

    all_files = []
    for flist in flist_fnames:
        if not os.path.exists(flist):
            print(f"flist {flist} doesn't exist in {os.getcwd()}")
            continue
        with open(flist) as fl:
            all_files += [mat for pat in grep_pats for mat in grep_vim_buf(fl, rf'{pat}')]
    return validate_file(list_dedup_inorder(all_files), parent)

def get_vai_files(vim_buf, parent=''):
    """Get vai design file list from vim buffer.
    """

    # design files
    vai_file_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCFILE"]}\s*:')
    vai_dir_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCDIR"]}\s*:')
    vai_flist_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCFLIST"]}\s*:')
    # get all *.v/*.sv files, including files in incdirs and flist
    vai_vlog_files = find_files_from_lines(vai_file_lines, parent)
    all_dirs = find_files_from_lines(vai_dir_lines, parent)
    vai_vlog_files += find_files_from_dirs(dir_list=all_dirs, glob_pats=('*.v', '*.sv'), parent=parent)
    all_flists = find_files_from_lines(vai_flist_lines, parent)
    vai_vlog_files += find_files_from_flist(flist_fnames=all_flists, grep_pats=('\.v$', '\.sv$'), parent=parent)

    return tuple(vai_vlog_files)

def get_vai_if_files(vim_buf, parent=''):
    """Get vai interface file list from vim buffer.
    """

    # interface files
    vai_intf_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCIF"]}\s*:')
    vai_intfdir_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCIFDIR"]}\s*:')
    vai_intflist_lines = grep_vim_buf(vim_buf, rf'^\s*//\s*{directives["INCIFFLIST"]}\s*:')
    # get all *.if.sv files, including files in incifdirs and flist
    vai_intf_files = find_files_from_lines(vai_intf_lines, parent)
    all_dirs = find_files_from_lines(vai_intfdir_lines, parent)
    vai_intf_files += find_files_from_dirs(dir_list=all_dirs, glob_pats=('*.if.sv', ), parent=parent)
    all_flists = find_files_from_lines(vai_intflist_lines, parent)
    vai_intf_files += find_files_from_flist(flist_fnames=all_flists, grep_pats=('\.if\.sv$', ), parent=parent)

    return tuple(vai_intf_files)

def get_instances(flist, vim_buf, inst_name=None, search_dir=''):
    """Get instance information from files in filelist.

    Args:
    :param tuple flist: verilog file list.
    :param list vim_buf: vim buffer
    :param str inst_name: instance name.

    Returns: instance dict with parameters and ports.
    """

    # parse verilog files
    try:
        ast, __ = parse(flist)
        print(ast.show())
    except ParseError as pe:
        print(pe)
        return None

    # precimpiled regexp patterns
    re_pat_cmt = re.compile(r'^\s*//')
    re_pat_prespace = re.compile(r'^(\s*)')
    re_pat_semicolon = re.compile(r';')
    re_pat_port_type = re.compile(r'//([WP]?)([IO]+)')

    # Find the max and min line number for module port list
    port_line_nums = [int(p.lineno) for p in ast.children()[0].children()[0].portlist.ports]
    max_modport_ln = max(port_line_nums) if port_line_nums else 0
    min_modport_ln = min(port_line_nums) if port_line_nums else 0

    # get ports of current top module
    # top_mod = ast.children()[0].children()[0].name
    # print(top_mod)
    # flist = flist + get_vai_files(vim_buf, parent=search_dir)
    # inst = VlogAutoInst(flist, top_mod)
    # pprint.pprint(inst.port_dict)
    # pprint.pprint(inst.param_dict)

    # out_port_dict = {}
    # max_modport_ln, min_modport_ln = (0, 99999999)
    # print(ast.children()[0].children()[0].portlist.ports)
    # for p in ast.children()[0].children()[0].portlist.ports:
    #     max_modport_ln = p.lineno if p.lineno > max_modport_ln else max_modport_ln
    #     min_modport_ln = p.lineno if p.lineno < min_modport_ln else min_modport_ln
    #     print(f'attr_names={p.attr_names}, first={p.first}, second={p.second}, childen={p.children()}')
    #     for c in p.children():
    #         print(f'attr_names={c.attr_names}, dimensions={c.dimensions}, name={c.name}, width={c.width}, signed={c.signed}, childen={c.children()}')
    #         if c.width is not None:
    #             print(f'attr_names={c.width.attr_names}, msb={c.width.msb}, lsb={c.width.lsb}, childen={c.width.children()}')
    #             print(dir(c.width.msb))
    #             print(type(c.width.msb))
    #             # print(f'attr_names={c.width.msb.attr_names}, left={c.width.msb.left}, right={c.width.msb.right}, childen={c.width.msb.children()}')
    #             print(f'attr_names={c.width.msb.attr_names}, childen={c.width.msb.children()}')

    # Iterate all instances
    # Source->Description->ModuleDef->InstanceList->Instance
    inst_dict = {}
    for mod_def in ast.children()[0].children()[0].children():
        if not isinstance(mod_def, InstanceList):
            continue
        # instances = [x for x in mod_def.children() if isinstance(x, Instance)]
        for i in mod_def.instances:
            # params = [x for x in i.children() if isinstance(x, ParamArg)]
            # ports = [x for x in i.children() if isinstance(x, PortArg)]
            # get parameter list
            param_dict = {p.paramname: str(p.argname) for p in i.parameterlist}
            #  get port list
            port_dict = {}
            for p in i.portlist:
                childen = tuple(map(str, p.argname.children()))
                instp_name = childen[0] if childen else str(p.argname)
                slice_expr = f"[{':'.join(childen[1:])}]" if childen else ''
                line_num = int(p.lineno)
                # get port type: WI/O, PI/O, or I/O
                mat = re_pat_port_type.search(vim_buf[line_num-1])
                port_type = mat.group(1) if mat else ''
                direction = mat.group(2) if mat else ''
                port_dict.update({str(p.portname): dict(instp=instp_name, slice=slice_expr,
                                                        type=port_type, dir=direction)})
            port_ln = [int(p.lineno) for p in i.portlist]
            max_port_ln = max(port_ln) if port_ln else (i.lineno + 1)
            min_port_ln = min(port_ln) if port_ln else (i.lineno + 1)
            # print(f'max={max_port_ln}, min={min_port_ln}')
            # validate vai-autoinst directive.
            # vai-autoinst directive should be between the start line and the min port line
            valid_vai_inst = False
            re_pat_inst = re.compile(rf'{i.name}\s*\(\s*/\*\s*{directives["AI"]}\s*\*/')
            # minus 1 because vim buffer index starts from 1
            for line in vim_buf[(i.lineno-1):(min_port_ln-1)]:
                if re_pat_cmt.search(line):
                    continue
                if re_pat_inst.search(line):
                    valid_vai_inst = True
            # stop if current instance doesn't have vai-autoinst directive
            if not valid_vai_inst:
                continue

            # find the end line number.
            end_ln = max_port_ln
            # minus 1 because vim buffer index starts from 1
            for idx, line in enumerate(vim_buf[(max_port_ln-1):]):
                if re_pat_cmt.search(line):
                    continue
                if re_pat_semicolon.search(line):
                    end_ln += idx
                    break
            
            # get the indent
            mat = re_pat_prespace.search(vim_buf[i.lineno - 1])
            indent = len(mat.group(1)) if mat else 0

            inst_dict.update({i.name: {
                                        'parent_port_ln': (min_modport_ln, max_modport_ln),
                                        'mod': i.module,
                                        'begin_ln': i.lineno, 
                                        'end_ln': end_ln,
                                        'indent': indent,
                                        'param': param_dict,
                                        'port': port_dict }})
    return inst_dict if inst_name is None else inst_dict.get(inst_name, None)

def generate_declares(instances, windent=0, pindent=0, precomma=True):
    """Generate wire and external port declaration for inst ports.

    Args: 
    :param dict instances: instance dict
    :param int windent: indent for autowire declaration
    :param int pindent: indent for autoport declaration
    :param bool precomma: whether adding prefix comma for autoport declaration.
    """

    # Find out the max length of wire/port signals
    max_instp_len, max_slice_len = (0, 0)
    for inst in instances.values():
        if not inst['port']:
            continue
        len_list = [(len(v["instp"]), len(v["slice"])) for v in inst['port'].values()]
        instp_len, slice_len = tuple(map(max, list(zip(*len_list))))
        max_instp_len = instp_len if max_instp_len < instp_len else max_instp_len
        max_slice_len = slice_len if max_slice_len < slice_len else max_slice_len
    
    # Get all instports for wire and port declarations. Dict is used to remove duplicated name.
    wire_dict, port_dict = ({}, {})
    for inst in instances.values():
        # wire declarations
        wires = {v['instp']: (f'wire {v["slice"]:{max_slice_len}} {v["instp"]:{max_instp_len}};',
                              0 if v['slice'] == '' else reduce(lambda x0, x1: x0 - x1, tuple(map(int, v['slice'][1:-1].split(':'))))
                             )
                 for v in inst['port'].values() if v['type'] == 'W'}
        # add new signal or update the duplicate signal using the one with wider bits
        for k, v in wires.items():
            if k not in wire_dict or (wire_dict[k][1] < v[1]):
                wire_dict[k] = v

        # port declarations 
        ports = {v['instp']: ((f'{"input " if v["dir"] == "I" else ("output" if v["dir"] == "O" else "inout ")} '
                               f'{v["slice"]:{max_slice_len}} {v["instp"]}'),
                              0 if v['slice'] == '' else reduce(lambda x0, x1: x0 - x1, tuple(map(int, v['slice'][1:-1].split(':'))))
                             )
                 for v in inst['port'].values() if v['type'] == 'P'}
        # add new signal or update the duplicate signal using the one with wider bits
        for k, v in ports.items():
            if k not in port_dict or (port_dict[k][1] < v[1]):
                port_dict[k] = v

    # wire declarations
    wire_declare_code = None
    if wire_dict:
        wire_indent = ' ' * windent
        wire_declare_code = f'{wire_indent}/* {directives["AW"]}-begin */\n'
        wire_declare_code += f'{wire_indent}'
        wire_declare_code += f'\n{wire_indent}'.join([x[0] for x in wire_dict.values()])
        wire_declare_code += f'\n{wire_indent}/* {directives["AW"]}-end */'

    # port declarations 
    port_declare_code = None
    if port_dict:
        port_indent = ' ' * pindent
        port_declare_code = f'{port_indent}/* {directives["AP"]}-begin */\n{port_indent}'
        port_declare_code += ',' if precomma else ''
        port_declare_code += f'\n{port_indent},'.join([x[0] for x in port_dict.values()])
        port_declare_code += '' if precomma else f'\n{port_indent},'
        port_declare_code += f'\n{port_indent}/* {directives["AP"]}-end */'

    return (port_declare_code, len(port_dict), wire_declare_code, len(wire_dict))


def get_intf_portlist(text):
    """Get port list of a module interface definition.
    """
    port_dec_list = text.replace(r'\n', '').split(',')
    re_pat_port_dec = re.compile(r'([\w\.]+)\s+(?:\[([^\]]+)\])?\s*(\w+)')
    port_list = []
    for p in port_dec_list:
        mat = re_pat_port_dec.search(p)
        if mat:
            port_list.append([mat.group(3), mat.group(2), mat.group(1)])
    return port_list

def parse_sv_modport(modport_list):
    modports = {}
    for name, ports in modport_list:
        modports.update({name: get_modport_portlist(ports)})
    return modports

def parse_sv_interface(flist):
    re_pat_intf_def = r'\s*interface\s+(\w+)\s*\((.*?)\).*?endinterface'
    re_pat_comment = re.compile(r'/[/\*].*$')

    intf_defs = {}
    for fname in flist:
        with open(fname) as intf_file:
            all_lines = ''
            for line in intf_file:
                # remove blanks at head and tail, and comment
                line = re_pat_comment.sub(r'', line)
                text = line.rstrip(' ').lstrip(' ')
                if text != '':
                    all_lines += ' ' + text
            # interface definition
            intf_def_list = re.findall(re_pat_intf_def, all_lines, re.S)
            for intf_name, ports_text in intf_def_list:
                # find all variables in interface
                intf_port_list = get_intf_portlist(ports_text)
                intf_defs.update({intf_name: intf_port_list})
    return intf_defs

def expand_inst_ports(inst, intf_defs, port_defs):
    if inst['mod'] not in intf_defs:
        return

    used_def_intfs = {x[0]: x[2] for x in intf_defs[inst['mod']]}
    expanded_intf_ports = recursive_expand_intf(intf_defs, inst['mod'])
    new_inst_ports = {}
    for k, v in inst['port'].items():
        # an interface port, expand it
        if k not in port_defs and k in used_def_intfs.keys():
            for port in expanded_intf_ports:
                if port.startswith(k) and port in port_defs:
                    new_inst_ports[port] = {'dir': port_defs[port]['dir'], 
                        'instp': f"{v['instp']}_{port.lstrip(k)}",
                        'slice': port_defs[port]['slice'],
                        'type': v['type']}
    # update
    inst['port'].update(new_inst_ports)
 

def recursive_expand_intf(intf_defs, mod):
    if mod not in intf_defs:
        return []

    intf_port_list = []
    for instp, _, intf in intf_defs[mod]:
        if intf not in ('input', 'output'):
            intf_port_list += [f'{instp}_{x}' for x in recursive_expand_intf(intf_defs, intf)]
        else:
            intf_port_list.append(instp)
    return intf_port_list



class VlogAutoInst:
    """Verilog Auto Instantiation.

    Args:
    :param tuple flist: verilog file list. If macros defined, put macro files prior to design file.
    :param str top_mod: top module.
    """

    def __init__(self, flist, top_mod):
        self.mod = top_mod 
        self.flist = flist
        self.param_dict = None
        self.port_dict = None
        self.analyzer = VerilogDataflowAnalyzer(flist, top_mod)
        # print(dir(self.analyzer))
        self.error = 0
        try:
            self.analyzer.generate()
        except DefinitionError as de:
            print(de)
            self.error = 1
        except ParseError as pe:
            print(pe)
            self.error = 2

        # get params and ports
        if self.error == 0:
            self.param_dict = self._get_params()
            self.port_dict = self._get_ports()

    def _get_param_value(self, param_list):
        param_dict = {}
        for k, v in self.analyzer.getBinddict().items():
            if k in param_list:
                if isinstance(v[0].tree, DFIntConst):
                    param_dict.update({str(k): v[0].tree})
                else:
                    print('Error: paramater tree is not a constant')
        return param_dict

    def _get_xsb_value(self, node):
        """Get the msb and lsb value of an terms.
        """

        node_val = None
        if isinstance(node, DFIntConst):
            node_val = node.eval()
        elif isinstance(node, DFOperator):
            node_val = int(eval(self._expr_map(node.tocode())))
        else:
            print(f'Invalid node format: {type(node)}:{node.tostr()}')
        return node_val

    def _expr_map(self, expr):
        """Replace parameters in expression with values.
        """

        new_expr = expr
        for k, v in self.param_dict.items():
            # change . to _
            name = str(k).replace('.', '_')
            new_expr = str(new_expr).replace(name, f'{v.eval()}')
        # print(f'expr={expr}, new_expr={new_expr}')
        return new_expr

    def _get_params(self):
        param_list = []
        for k, v in self.analyzer.getTerms().items():
            # getTerms() returns all hierarchical elements. however we only need the ones in the 
            #first-level scope. So filter all elements with hierarchical level greater than 2
            term_full_hier = str(k).split('.')
            if len(term_full_hier) > 2:
                continue
            # Filter parameters
            if 'Parameter' in v.termtype:
                param_list.append(v.name)
        return self._get_param_value(param_list)

    def _get_ports(self):
        port_dict = {}
        for k, v in self.analyzer.getTerms().items():
            # getTerms() returns all hierarchical elements. however we only need the ones in the 
            #first-level scope. So filter all elements with hierarchical level greater than 2
            term_full_hier = str(k).split('.')
            if len(term_full_hier) > 2:
                continue
            # Filter ports
            port_dir = list({'Input', 'Output', 'Inout'} & v.termtype)
            if port_dir:
                msb_v, lsb_v = (None, None)
                direction = 'I' if port_dir[0] == 'Input' else \
                            ('O' if port_dir[0] == 'Output' else 'IO')
                msb_v = self._get_xsb_value(v.msb)
                lsb_v = self._get_xsb_value(v.lsb)
                port_dict.update({str(k).split('.')[-1]: {'dir': direction,
                                      'slice': f'[{msb_v}:{lsb_v}]' if msb_v != lsb_v else '',
                                      'instp': str(k).split('.')[-1],
                                      'type': 'W'
                                     }})
        return port_dict

    def reset(self, flist=None):
        """Re-instantiate the whole design.

        Args:
        :param tuple flist: new file list for parse. If set to None, use the old flist.
        """

        new_flist = self.flist if flist is None else flist
        self.analyzer = VerilogDataflowAnalyzer(new_flist, self.mod)
        self.analyzer.generate()
        # get params
        self.param_dict = self._get_params()
        # get port_dict
        self.port_dict = self._get_ports()

    def update(self, param_dict=None, port_dict=None, port_regexp=None):
        """Update parameter value and port based on custom changes.

        Args:
        :param dict param_dict: parameter dict {param: 'value'}
        :param dict port_dict: port dict {port_name: instport_name}
        :param tuple port_regexp: regexp for changing instport name, (pattern, sub_pattern)
        """

        # Update parameters' value
        if param_dict:
            # Convert str to DFIntConst first
            new_param_dict = {f'{self.mod}.{k}':DFIntConst(v) for k, v in param_dict.items()}
            self.param_dict.update(new_param_dict)
            # update port width
            self.port_dict = self._get_ports()

        # update instport name according to regexp and user's manual changes.
        if port_dict:
            for k, v in self.port_dict.items():
                if k in port_dict:
                    # only need to update instp and type
                    self.port_dict[k]['type'] = port_dict[k]['type']
                    self.port_dict[k]['instp'] = port_dict[k]['instp']
        if port_regexp:
            # apply regexp on instp
            re_pat = re.compile(rf'{port_regexp[0]}')
            for k, v in self.port_dict.items():
                self.port_dict[k]['instp'] = re_pat.sub(rf'{port_regexp[1]}', v['instp'])

    def generate_code(self, inst_name, indent=0):
        """Generate instantiation code.
        """

        indent_lvl0 = ' ' * indent
        indent_lvl1 = f'{indent_lvl0}    '

        code = f'{indent_lvl0}{self.mod} '
        if self.param_dict:
            code += f'#(\n{indent_lvl1} .'
            # find the max length of parameter length
            max_k_len = max([len(str(k).split(".")[-1]) for k in self.param_dict.keys()])
            max_v_len = max([len(v.value) for v in self.param_dict.values()])
            param_list = [f'{str(k).split(".")[-1]:{max_k_len}} ({v.value:{max_v_len}})'
                          for k, v in self.param_dict.items()]
            code += f'\n{indent_lvl1},.'.join(param_list)
            code += f'\n{indent_lvl0}) '

        code += f'{inst_name} ( /* {directives["AI"]} */\n{indent_lvl1} .'
        # find the max length of port length
        len_list = [(len(k), len(f'{v["instp"]}{v["slice"]}')) for k, v in self.port_dict.items()]
        max_k_len, max_v_len = tuple(map(max, list(zip(*len_list))))
        # print(f'max_k={max_k_len}, max_v={max_v_len}')
        ports = [f'{k:{max_k_len}} ({v["instp"]+v["slice"]:{max_v_len}}) //{v["type"]}{v["dir"]}'
                 for k, v in self.port_dict.items()]
        code += f'\n{indent_lvl1},.'.join(ports)
        code += f'\n{indent_lvl0}); // end of {inst_name}'

        return code

    def generate_wire_declare(self, indent=0):
        """Generate wire declaration.
        """

        indent_lvl0 = ' ' * indent
        code = f'{indent_lvl0}'

        # find the max length of port width slice
        len_list = [(len(v["instp"]), len(v["slice"])) for v in self.port_dict.values()]
        max_instp_len, max_slice_len = tuple(map(max, list(zip(*len_list))))
        ports = [f'wire {v["slice"]:{max_slice_len}} {v["instp"]:{max_instp_len}};'
                 for v in self.port_dict.values() if v['type'] == 'W']
        code += f'\n{indent_lvl0}'.join(ports)
        return code


    def generate_port_declare(self, indent=0):
        """Generate external port declaration.
        """

        indent_lvl0 = ' ' * indent
        code = f'{indent_lvl0}'

        # find the max length of port width slice
        max_slice_len = max([len(v["slice"]) for v in self.port_dict.values()])
        ports = [(f'{"input" if v["dir"] == "I" else ("output" if v["dir"] == "O" else "inout")} '
                 f'{v["slice"]:{max_slice_len}} {v["instp"]}')
                 for v in self.port_dict.values() if v['type'] == 'P']
        code += f'\n{indent_lvl0},'.join(ports)
        return code
