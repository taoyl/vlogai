# vim:fileencoding=utf-8:noet
""" Demo for Verilog Auto Instantiation.
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

import os
import sys
import pprint
# The following line can be removed after vlogai is installed.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlogai.vai as vai
from pathlib import Path

def main():
    vlog_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'vlogcode'
    top_file = vlog_dir / 'top2.v'

    vim_buf = None
    with open(top_file, 'r') as f:
        vim_buf = f.readlines()
    
    instances = vai.get_instances((top_file, ), vim_buf)
    pprint.pprint(instances)

    vlog_files = [vlog_dir / f for f in vai.get_vai_files(vim_buf, parent=vlog_dir)]
    print(f"vlog: {vlog_files}")
    intf_files = [vlog_dir / f for f in vai.get_vai_if_files(vim_buf, parent=vlog_dir)]
    print(f"intf: {intf_files}")

    inst = vai.VlogAutoInst(vlog_files, 'example_mod')
    print(inst.generate_code('u_example_mod', 2))
    # pprint.pprint(inst.port_dict)

    intf_defs = vai.parse_sv_interface(intf_files)
    # pprint.pprint(intf_defs)

    # expand interface ports
    vai.expand_inst_ports(instances['u_example_mod'], intf_defs, inst.port_dict)
    # pprint.pprint(instances)
    

    inst.update(instances['u_example_mod']['param'], instances['u_example_mod']['port'])
    print(inst.generate_code('u_example_mod', 2))

    inst.reset()
    print(inst.generate_code('u_example_mod', 2))

    regexp = (r'^', r'MY_PREFIX_')
    inst.update(None, None, regexp)
    print(inst.generate_code('u_example_mod', 2))


if __name__ == '__main__':
    main()
