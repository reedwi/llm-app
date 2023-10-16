# Document Processor

## Server Commands
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/gh_id_ed25519
git pull (inside repo)
./service_restart.sh
sudo sed -i 'd' /var/log/doc_training_celery/logs.log 
sudo sed -i 'd' /var/log/doc_training/logs.log 
```
