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
from pathlib import Path
# The following line can be removed after vlogai is installed.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vlogai.vai as vai

def main():
    vlog_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'vlogcode'
    top_file = vlog_dir / 'top.v'
    print(top_file)

    vim_buf = None
    with open(top_file, 'r') as f:
        vim_buf = f.readlines()
    
    instances = vai.get_instances((top_file, ), vim_buf)
    pprint.pprint(instances)

    vlog_files = [vlog_dir / f for f in vai.get_vai_files(vim_buf, parent=vlog_dir)]
    # vlog_files = vai.get_vai_files(vim_buf)
    print(f"flist: {vlog_files}")

    # inst = vai.VlogAutoInst((vlog_dir / 'macros.v', vlog_dir / 'led.v'), 'led')
    inst = vai.VlogAutoInst(vlog_files, 'led')
    print(inst.generate_code('u_led', 2))
    # # update params
    # new_params = {'STEP': '4', 'LEN': "8'hf", 'WIDTH': "4'hc"}
    # new_ports = {'din': 'led_din', 'addr1': 'led_addr1'}
    regexp = (r'^', r'u_LED_')
    inst.update(instances['u_my_led']['param'], instances['u_my_led']['port'], regexp)
    print(inst.generate_code('u_led', 2))

    inst.reset()
    inst.update(None, None, regexp)
    print(inst.generate_code('u_led', 2))



if __name__ == '__main__':
    main()
