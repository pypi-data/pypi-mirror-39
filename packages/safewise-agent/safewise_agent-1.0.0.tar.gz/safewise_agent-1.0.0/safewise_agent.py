import safewiseagentlib.gpg
import safewiseagentlib.ssh
from safewiseagentlib.device.safewise import SafeWISE as DeviceType

ssh_agent = lambda: safewiseagentlib.ssh.main(DeviceType)
gpg_tool = lambda: safewiseagentlib.gpg.main(DeviceType)
gpg_agent = lambda: safewiseagentlib.gpg.run_agent(DeviceType)
