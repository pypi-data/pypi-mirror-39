```
#!/usr/bin/env python3.7

from shell_scripting import run, shell, shell_list

run("date | sed s/2018/2019/ > test.out")

print(shell("env | grep USER").stdout.split("\n"))

print(shell("cat /root/file"))

r = shell("cat /root/file")
print(
    f"""\
    args: {r.args}
    returncode: {r.returncode}
    stdout: {r.stdout}
    stderr: {r.stderr}\
""",
    end="",
)

for x in shell_list("env"):
    print(x)
```
