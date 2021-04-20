import os

# for a in ['test_src', 'prmp_lib', 'src', 'old_src', 'other_srcs']:
#     os.system(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Test_GUI\android\adb32\adb.exe push C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\%s /sdcard/time_table'%a)


a = r'C:\Users\Administrator\Documents\My\Compulsory\Python\Gui'
os.system(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Test_GUI\android\adb32\adb.exe pull /sdcard/time_table "%s"'%a)