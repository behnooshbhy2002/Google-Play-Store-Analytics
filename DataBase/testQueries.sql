select count(a.app_name)
from apps as a
group by a.app_name
having count(a.app_name)>1

SELECT * FROM apps WHERE released IS NULL;


select *
from apps
where apps.id=1