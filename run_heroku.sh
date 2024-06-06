# heroku login
# heroku ps:scale web=0 -a yom-ml-ap
# heroku apps:destroy -a yom-ml-app
# heroku create yom-ml-app
# https://yom-ml-app-0bb04ecda93c.herokuapp.com/
# https://git.heroku.com/yom-ml-app.git
# git remote add heroku https://git.heroku.com/yom-ml-app.git
# git remote -v
git checkout main
git pull
git push heroku main
heroku logs --tail -a yom-ml-app