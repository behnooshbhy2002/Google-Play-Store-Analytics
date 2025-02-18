SELECT count(app_name)  
FROM apps a  
INNER JOIN categories c ON a.category_id = c.id  
WHERE c.category_name = 'productivity' and a.rating<=3.0 and a.price=0
