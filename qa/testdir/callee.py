import pexpect
pexpect.run("bash -c \"echo '===%s=== curlRate: %s KBps  |  dataRate: %sKBps' >> BW_record\"")
