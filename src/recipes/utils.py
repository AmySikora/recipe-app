from recipes.models import Recipe   #you need to connect parameters from books model

#define a function that takes the ID
def get_recipename_from_id(val):
   #this ID is used to retrieve the name from the record
   recipename=Recipe.objects.get(id=val)
   #and the name is returned back
   return recipename