class EntityClass:
	employee_id=''
	first_name=''
	last_name=''
	email=''
	phone_number=''
	job_id=''
	salary=''
	commission_pct=''
	manager_id=''
	department_id=''
	hiredate=''
	def __str__(self):
		return  '%s        %s        %s        %s        %s        %s        %s        %s        %s        %s        %s        ' %(self.employee_id,self.first_name,self.last_name,self.email,self.phone_number,self.job_id,self.salary,self.commission_pct,self.manager_id,self.department_id,self.hiredate)