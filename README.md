# mlops-deploymenta

### Create Heroku project

```bash
heroku login
heroku create your-app-name
heroku git:remote your-app-name
heroku stack:set container
git push heroku main
```

# TEST