'''from datetime import datetime

my_date = datetime(1, 1, 1)
print(my_date.now())'''
argue = ['True', 'True', 'True', 'nm']
        
ddddd = {
    0: (" branch_id = "),
    1: (" employee_id = "),
    2: (" table = "),
    3: (" action = ")
        
    
}
emp = 'True'
if not emp == "True":
    emp, _ = map(str.strip, emp.split('-'))
    argue[1] = emp
    emp_condition = f"id = '{emp}'"
for tt, arr in zip(ddddd.items(),argue):
    i, val = tt
    if not arr == "True":
        argue[i] = f"{val} '{arr}'"
    else:
        argue[i] = f"True"

search_condition = " and ".join(argue)
print("====",search_condition)