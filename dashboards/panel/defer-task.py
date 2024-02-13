import time
import panel as pn

pn.extension(defer_load=True, loading_indicator=True, template="bootstrap")

def long_running_task():
    time.sleep(3)
    return "# I'm deferred and shown after load"

pn.Column("# I'm shown on load", long_running_task).servable()