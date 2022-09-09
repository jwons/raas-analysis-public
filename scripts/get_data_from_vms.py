import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--all', action='store_true')
parser.add_argument('--dbs', action='store_true')
parser.add_argument('--touts', action='store_true')
parser.add_argument('--dirs', action='store_true')
parser.add_argument('--vms', nargs='+')

args = parser.parse_args()


vms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

if(args.vms):
    vms = args.vms

dbs = False
touts = False
dirs = False

if args.dbs: dbs = True 
if args.touts: touts = True 
if args.dirs: dirs = True

if args.all:
    dbs = True 
    touts = True 
    dirs = True



ip_temp_list = os.environ.get("IP_LIST").split(";")
ip_list = []
for vm in vms:
    ip_list.append(ip_temp_list[int(vm)])

print(ip_list)

copy_db_command = "scp -i ~/.ssh/id_rsa ubuntu@HOST:/home/ubuntu/raas/db/app.db ../data/raas_dbs/NUMBER-app-redo.db"
copy_timeouts_command = "scp -i ~/.ssh/id_rsa ubuntu@HOST:/home/ubuntu/raas/eval/raas_timeout_dois.txt ../data/raas_timeouts/NUMBER-timeout-dois-redo.txt"
copy_prov_dirs_command = "scp -i ~/.ssh/id_rsa ubuntu@HOST:/home/ubuntu/raas/eval/prov_dirs.tar ../data/prov_dirs/NUMBER-prov_dirs_redo.tar"

counter = 0
for ip_addr in ip_list:
    ip_db_command = copy_db_command.replace("HOST", ip_addr).replace("NUMBER", str(vms[counter]))
    ip_timeout_command = copy_timeouts_command.replace("HOST", ip_addr).replace("NUMBER", str(vms[counter]))
    ip_dirs_command = copy_prov_dirs_command.replace("HOST", ip_addr).replace("NUMBER", str(vms[counter]))

    counter += 1
    if dbs: os.system(ip_db_command)
    if touts: os.system(ip_timeout_command)
    if dirs: os.system(ip_dirs_command)
