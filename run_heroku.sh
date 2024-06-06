heroku ps:scale web=0 -a yom-ml-ap
heroku apps:destroy -a yom-ml-app
heroku create yom-ml-app
# https://yom-ml-app-0855a800bcc2.herokuapp.com/
# https://git.heroku.com/yom-ml-app.git
heroku container:login
docker buildx build --platform linux/amd64 -t registry.heroku.com/yom-ml-app/web --push .
heroku container:release web -a yom-ml-app
heroku logs --tail -a yom-ml-app