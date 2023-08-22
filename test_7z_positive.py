from sshcheckers import ssh_checkout, upload_files
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)


def test_step0():
    res = []
    upload_files(f"{data['host']}", f"{data['remote_user']}", "11", f"{data['local_path']}/p7zip-full.deb",
                 f"{data['remote_path']}/p7zip-full.deb")
    res.append(ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                            f"echo '11' | sudo -S dpkg -i {data['remote_path']}/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                            "echo '11' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    assert all(res)


def test_step1(make_folders, clear_folders, make_files):
    res1 = ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                        "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                        "ls {}".format(data['folder_out']), "arx1.7z"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    res = []
    res.append(
        ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                     "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                     "Everything is Ok"))
    res.append(ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                            "cd {}; 7z e arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                            "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                                "ls {}".format(data['folder_ext']), item))
    assert all(res)


def test_step3():
    assert ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                        "cd {}; 7z t {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test1 Fail"


def test_step4():
    assert ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                        "cd {}; 7z u {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test1 Fail"


def test_step5(clear_folders, make_files):
    res = []
    res.append(
        ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                     "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                     "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                                "cd {}; 7z l arx1.7z".format(data['folder_out']), item))
    assert all(res)


def test_step7():
    assert ssh_checkout(f"{data['host']}", f"{data['remote_user']}", "11",
                        "7z d {}/arx1.7z".format(data['folder_out']), "Everything is Ok"), "Test1 Fail"