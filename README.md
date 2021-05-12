# The Autism DRIVE

Version 1.11.4

Please see the individual readme files in Frontend and Backend for details.

# Deploy to Staging

To deploy for staging:

1. Have sartography ssh credentials set up. 

2. Add remote to sartography staging server in star-drive (*NOT star-drive-dist*)


```bash 
git remote add staging sartography:star.git
```


2. Be on the staging branch & merge in changes
3. Push to the remote staging server with

```bash
git push staging
```


*Note: if this hangs during push, reload instance on AWS.*
