# COMMANDS #

### Start project/app ###

(python manage.py) django start(project/app) name

### Make migration ###

After we change models.py we need to make migration to our database. 
First we need to process our changes into new migrations file.

    python manage.py makemigrations

Then we can "migrate" this data to our database:

    python manage.py migrate


### Create virtual environment ###

python -m venv venv
venv/Scripts/activate

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODELS #

### How we set up data in db ###
![img_1.png](img_1.png)

In models.py we create our model with some data (category, name, etc.). Then it is translated 
to migration files and then sent to our db. Database then can deal with new data of that type.

### How to create model ###

In models.py wy create class which take over models.Model. We give our model some fields and __str__ method.
This method defines how we are going to see each of those models in admin panel.

### What if we want to have models as a parameter for another model? ###

In this case we want to tell model that this field is a defined model from above. we do it like this:

```
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
```
That way we create ForeignKey for our model/class and set delete method.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GENERAL NOTES #

### .env files ###
We use .env files to store critical data.

to load .env file to settings.py:
  - load_dotenv()

to access some data:
  - SECRET_KEY = os.getenv("SECRET_KEY")

### Static and media urls ###
Static files are used to store icons, logo and more "static data". In media we store links to photos 
or another content that we want to shw on our website (there is no reason to store all that files in project).




