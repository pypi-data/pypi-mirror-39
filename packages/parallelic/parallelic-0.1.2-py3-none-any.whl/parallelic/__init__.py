__version__ = "0.1.2"

def main(dryRun=True, skipDiscovery=False, execMode="manager", **kwargs):
    if dryRun:
        # Force skipDiscovery and execMode to a dry-runnable state
        skipDiscovery = True
    kwargs["skipDiscovery"] = skipDiscovery
    kwargs["dryRun"] = dryRun
    if execMode == "manager":
        from parallelic.manager import run
    if execMode == "runner":
        from parallelic.runner import run
    return run(**kwargs)
