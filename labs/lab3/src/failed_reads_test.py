import logs_reader as lr
import logs_utilities as utils

log = lr.read_log()

merged = False
failed_reads = utils.get_failed_reads(log, merged)
print(f"Failed reads as {'merged' if merged else 'split'}")
if merged:
    utils.print_entries(failed_reads)
else:
    utils.print_entries(failed_reads[0])
    print()
    utils.print_entries(failed_reads[1])