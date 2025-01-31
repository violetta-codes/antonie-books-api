# CITB548_delivery_system
- [Requirements file](https://e-edu.nbu.bg/pluginfile.php/1500965/mod_resource/content/4/CITB548_Kostadinova_Logistic_Company.pdf)

### Important information
- Do not commit code directly to the `main` branch. **Create a PR before merging!**
- If possible please adhere to the [conventional commits convention](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.conventionalcommits.org%2Fen%2Fv1.0.0%2F%3Ffbclid%3DIwZXh0bgNhZW0CMTAAAR3UIxLOEKFjpPNF3w5FJQDi8b20g6lm9mmYqswIVPw1zlz0Ie2cw9BIHXQ_aem_TsnuxWY9VABbo9Blp5XdTA%23summary&h=AT0mkR5-dEhZK5N_PvbQR3YwFFK1zAXozhBzHfqA47rtRz0XPXbjCGffGzpqTpkSkMLZ01Lbax83EkH6atq3eCT4dDFpvqkaDu_pyrDbESUv5nE4sHktT0PFKBt0mpwMLVKnJ7P17Cs) to make our commits more clear and readable
- The project is running with a SQLite database which you can find in the repo. The superuser's credentials are both `admin`. **Please create a separate sqlite file and use that while you are developing.**

### How to set up your development environment
1. Clone the repository
2. Create a virtual environment and activate it
3. Run `pip install -r requirements.txt` **inside of your virtual environment** in order to install all dependencies
4. `cd` inside `~/delivery_system`
5. Create and apply migrations using `python manage.py makemigrations` and `python manage.py migrate`
6. Create a superuser using `python manage.py createsuperuser`
7. Run `python manage.py runserver` and the server will start
