import logs_reader as lr
import logs_utilities as utils
import labs.lab2.src.lab_2 as lab2

r'''
cd PycharmProjects/ScriptLanguages/labs
type nasa_data\NASA | python lab2\src\lab_2.py 500 | python lab3\src\main.py
'''

# lab2.read_lines()

log = lr.read_log()


print("Entries from standard input")
utils.print_entries(log)

sorted_log = utils.sort_log(log, lr.BYTES_INDEX)
print("Entries sorted by bytes")
utils.print_entries(sorted_log)

hostname = "unicomp6.unicomp.net"
filtered_log = utils.get_entries_by_addr(hostname, log)
print(f"Entries for hostname = {hostname}")
utils.print_entries(filtered_log)


code = 302
successful_reads = utils.get_entries_by_code(code, log)
print(f"Entries for code = {code}")
utils.print_entries(successful_reads)

merged = True
failed_reads = utils.get_failed_reads(log, merged)
print(f"Failed reads as {'merged' if merged else 'split'}")
if merged:
    utils.print_entries(failed_reads)
else:
    utils.print_entries(failed_reads[0])
    utils.print_entries(failed_reads[1])


extension = 'html'
filtered_log = utils.get_entries_by_extension(log, extension)
print(f"Requests for resources of type .{extension}")
utils.print_entries(filtered_log)


dict_log = lr.log_to_dict(log)
print("Log in dictionary form")
utils.print_dict_entry_dates(dict_log)


addresses = utils.get_addrs(dict_log)
print(f"Entries for hostname = {hostname}")
print(addresses)




