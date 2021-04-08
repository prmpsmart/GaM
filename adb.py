import os

# for a in ['test_src', 'prmp_lib', 'src', 'old_src', 'other_srcs']:
#     os.system(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Test_GUI\android\adb32\adb.exe push C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\%s /sdcard/time_table'%a)


for a in ['PRMP_Encrypt-setup_V1.5.exe', 'PRMP_Photoviewer-setup_v1.exe']:
    os.system(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Test_GUI\android\adb32\adb.exe push "C:\Users\Administrator\Documents\My\PRMP Smart exes\%s" /sdcard/time_table'%a)